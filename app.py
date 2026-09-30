import os
import re
import json
import requests
from pathlib import Path
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
from docx import Document
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

ALLOWED = {"pdf", "docx", "txt"}

COUNTRY_GUIDANCE = {
    "United States": "Use concise achievement-focused language, strong action verbs, measurable impact, ATS-friendly formatting, and normally omit photo, date of birth, marital status and full street address.",
    "Canada": "Use a clear achievement-focused resume, Canadian spelling where appropriate, concise sections, and normally omit photo, age, marital status and other personal details.",
    "United Kingdom": "Use a concise CV style, achievement-oriented bullets, UK spelling where appropriate, and normally omit photo, date of birth, marital status and nationality unless specifically relevant.",
    "Germany": "Use a structured CV with clear chronology, qualifications and professional detail. Keep formatting conservative. A photo can be culturally common but should not be required.",
    "France": "Use a structured CV with clear professional summary, skills, education and experience. Keep language formal and concise.",
    "Netherlands": "Use a concise, direct CV emphasizing relevant achievements, skills and experience. Avoid unnecessary personal information.",
    "Sweden": "Use a clean, concise and achievement-oriented CV with clear skills and experience. Keep personal information limited.",
    "Switzerland": "Use a structured, detailed and professional CV, with clear dates, qualifications and language skills where relevant.",
    "Australia": "Use an achievement-focused resume with Australian spelling where appropriate. Normally omit photo, age, marital status and other unnecessary personal details.",
    "UAE": "Use a clear professional CV emphasizing experience, qualifications, skills and relevant international experience. Personal details should only be included when genuinely useful for the role.",
    "Singapore": "Use a concise, structured resume emphasizing relevant achievements, skills and qualifications. Keep personal information limited.",
    "Japan": "Use a clear, formal and highly structured resume. Japanese applications may use standardized formats, but for international/English roles a concise English resume is appropriate.",
    "India": "Use a concise, ATS-friendly resume with measurable achievements, relevant skills, education and professional experience.",
}

def extract_text(path):
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        reader = PdfReader(path)
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    if ext == ".docx":
        doc = Document(path)
        parts = [p.text for p in doc.paragraphs]
        for table in doc.tables:
            for row in table.rows:
                parts.append(" | ".join(cell.text for cell in row.cells))
        return "\n".join(parts)
    if ext == ".txt":
        return Path(path).read_text(encoding="utf-8", errors="ignore")
    raise ValueError("Unsupported file type")

def clean_text(text):
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def fallback_tailor(resume, country, job_title, job_description):
    """Useful fallback when Ollama is not reachable. It does not invent experience."""
    lines = [x.strip() for x in resume.splitlines() if x.strip()]
    keywords = []
    source = (job_title + " " + job_description).lower()
    for word in re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{2,}", source):
        if word not in keywords:
            keywords.append(word)
    matched = []
    resume_lower = resume.lower()
    for word in keywords:
        if word in resume_lower and word not in matched:
            matched.append(word)
    summary = f"Professional with experience relevant to {job_title or 'the target role'}, tailored for the {country} job market."
    if matched:
        summary += " Relevant keywords already present in the resume include: " + ", ".join(matched[:12]) + "."
    return (
        f"TARGET ROLE\n{job_title or 'Not specified'}\n\n"
        f"TARGET COUNTRY\n{country}\n\n"
        f"PROFESSIONAL SUMMARY\n{summary}\n\n"
        f"ORIGINAL RESUME CONTENT\n{resume}\n\n"
        f"TAILORING NOTE\nThe automatic local-model service was not available, so the original facts were preserved and no new qualifications or experience were invented."
    )

def tailor_with_ollama(resume, country, job_title, job_description):
    guidance = COUNTRY_GUIDANCE.get(country, "Use the country's common professional resume conventions while avoiding unsupported assumptions.")
    prompt = f"""
You are Jobaround, a professional resume localization assistant.

TASK:
Rewrite the user's resume for a job application in {country}.
Target job title: {job_title or "Not specified"}.
Job description:
{job_description or "Not provided"}.

COUNTRY GUIDANCE:
{guidance}

STRICT RULES:
1. Never invent employers, dates, degrees, certifications, technologies, achievements, metrics, job titles or responsibilities.
2. Only rewrite, reorder, shorten or clarify information that is actually present in the source resume.
3. If a job description contains a keyword that is not supported by the resume, do not claim the user has that skill.
4. Make the result ATS-friendly using standard headings and plain text.
5. Use strong action verbs where supported by the original content.
6. Prioritize measurable achievements already present in the source.
7. Return a complete resume, not commentary about the resume.
8. Do not use tables, columns, emojis or decorative symbols.
9. Keep personal information appropriate for the target country.
10. Do not add a photo requirement.
11. Preserve the person's real identity and contact information if present.

SOURCE RESUME:
---BEGIN RESUME---
{resume}
---END RESUME---

Return the tailored resume with these sections where the source supports them:
NAME / CONTACT
PROFESSIONAL SUMMARY
CORE SKILLS
PROFESSIONAL EXPERIENCE
PROJECTS
EDUCATION
CERTIFICATIONS
ADDITIONAL INFORMATION
"""
    r = requests.post(
        f"{OLLAMA_URL.rstrip('/')}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2}
        },
        timeout=180
    )
    r.raise_for_status()
    data = r.json()
    result = data.get("response", "").strip()
    if not result:
        raise RuntimeError("Ollama returned an empty response")
    return result

def make_docx(text, path):
    doc = Document()
    for block in text.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        first = lines[0].strip()
        if first.upper() in {
            "PROFESSIONAL SUMMARY", "CORE SKILLS", "PROFESSIONAL EXPERIENCE",
            "PROJECTS", "EDUCATION", "CERTIFICATIONS", "ADDITIONAL INFORMATION",
            "TARGET ROLE", "TARGET COUNTRY", "NAME / CONTACT"
        }:
            p = doc.add_paragraph()
            run = p.add_run(first)
            run.bold = True
            for line in lines[1:]:
                doc.add_paragraph(line)
        else:
            for line in lines:
                doc.add_paragraph(line)
    doc.save(path)

def make_pdf(text, path):
    styles = getSampleStyleSheet()
    body = styles["BodyText"]
    body.fontName = "Helvetica"
    body.fontSize = 9.5
    body.leading = 13
    doc = SimpleDocTemplate(path, pagesize=A4, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42)
    story = []
    for block in text.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        first = lines[0].strip()
        if first.upper() in {
            "PROFESSIONAL SUMMARY", "CORE SKILLS", "PROFESSIONAL EXPERIENCE",
            "PROJECTS", "EDUCATION", "CERTIFICATIONS", "ADDITIONAL INFORMATION",
            "TARGET ROLE", "TARGET COUNTRY", "NAME / CONTACT"
        }:
            story.append(Paragraph(f"<b>{first}</b>", body))
            story.append(Spacer(1, 5))
            content = "<br/>".join(escape_html(x) for x in lines[1:])
        else:
            content = "<br/>".join(escape_html(x) for x in lines)
        if content:
            story.append(Paragraph(content, body))
            story.append(Spacer(1, 8))
    doc.build(story)

def escape_html(s):
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
    )

@app.errorhandler(RequestEntityTooLarge)
def file_too_large(_error):
    return jsonify({"error": "File is too large. Maximum size is 8 MB."}), 413

@app.route("/")
def index():
    return render_template("index.html", countries=sorted(COUNTRY_GUIDANCE))

@app.post("/api/tailor")
def tailor():
    uploaded = request.files.get("resume")
    country = request.form.get("country", "").strip()
    job_title = request.form.get("job_title", "").strip()
    job_description = request.form.get("job_description", "").strip()

    if not uploaded or not uploaded.filename:
        return jsonify({"error": "Please upload a resume."}), 400
    if country not in COUNTRY_GUIDANCE:
        return jsonify({"error": "Please select a supported country."}), 400

    ext = Path(uploaded.filename).suffix.lower().lstrip(".")
    if ext not in ALLOWED:
        return jsonify({"error": "Upload PDF, DOCX or TXT only."}), 400

    safe = secure_filename(uploaded.filename)
    input_path = os.path.join(UPLOAD_DIR, safe)
    uploaded.save(input_path)

    try:
        resume = clean_text(extract_text(input_path))
        if len(resume) < 50:
            return jsonify({"error": "Could not extract enough text from the resume. Try a text-based PDF or DOCX."}), 400

        used_ai = True
        try:
            tailored = tailor_with_ollama(resume, country, job_title, job_description)
        except Exception:
            used_ai = False
            tailored = fallback_tailor(resume, country, job_title, job_description)

        stem = Path(safe).stem
        docx_path = os.path.join(OUTPUT_DIR, f"{stem}_jobaround.docx")
        pdf_path = os.path.join(OUTPUT_DIR, f"{stem}_jobaround.pdf")
        make_docx(tailored, docx_path)
        make_pdf(tailored, pdf_path)

        return jsonify({
            "success": True,
            "ai_used": used_ai,
            "message": "Resume tailored successfully." if used_ai else "Resume processed using fallback mode because the local AI service was unavailable.",
            "preview": tailored,
            "docx": f"/download/docx/{Path(docx_path).name}",
            "pdf": f"/download/pdf/{Path(pdf_path).name}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            os.remove(input_path)
        except OSError:
            pass

@app.get("/download/<kind>/<filename>")
def download(kind, filename):
    if kind not in {"docx", "pdf"}:
        return "Invalid file type", 400
    safe = secure_filename(filename)
    path = os.path.join(OUTPUT_DIR, safe)
    if not os.path.exists(path):
        return "File not found", 404
    return send_file(path, as_attachment=True)

@app.get("/health")
def health():
    return jsonify({"status": "ok", "ollama_url": OLLAMA_URL, "ollama_model": OLLAMA_MODEL})

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
