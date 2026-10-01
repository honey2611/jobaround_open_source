import re

def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

# photo: "omit" | "optional" | "common"
_RAW = [
    ("United States", "🇺🇸", "omit", "One page, achievement bullets, and no photo, age, or full street address."),
    ("United Kingdom", "🇬🇧", "omit", "A concise CV with UK spelling. Leave off photo, date of birth, and marital status."),
    ("Germany", "🇩🇪", "common", "A structured Lebenslauf with clear dates. A photo is common, never required by this tool."),
    ("Japan", "🇯🇵", "optional", "International English resumes stay concise. Domestic applications often use a rirekisho."),
    ("Canada", "🇨🇦", "omit", "Achievement-focused, Canadian spelling, and no photo, age, or marital status."),
    ("Australia", "🇦🇺", "omit", "A two-to-three page resume is normal. Skip photo, age, and marital status."),
    ("UAE", "🇦🇪", "optional", "A clear CV with qualifications and relevant international experience."),
    ("Singapore", "🇸🇬", "omit", "Short, structured, and specific. Keep personal details limited."),
    ("France", "🇫🇷", "optional", "A formal CV with a short profile, skills, and a clean chronology."),
    ("Netherlands", "🇳🇱", "omit", "Direct language, relevant results, and little personal information."),
    ("Sweden", "🇸🇪", "omit", "Clean, modest, and skill-led. Avoid personal details that are not needed."),
    ("Switzerland", "🇨🇭", "optional", "Detailed dates, qualifications, and language levels where the source includes them."),
    ("India", "🇮🇳", "omit", "ATS-friendly sections, measurable achievements, and a compact skills list."),
    ("Ireland", "🇮🇪", "omit", "A UK-style CV with plain headings and no photo or date of birth."),
    ("New Zealand", "🇳🇿", "omit", "A clear, achievement-led resume. Skip photo, age, and marital status."),
    ("Spain", "🇪🇸", "optional", "A structured CV. A photo is sometimes used; this tool does not require one."),
    ("Italy", "🇮🇹", "optional", "A chronological CV with education and experience easy to scan."),
    ("Portugal", "🇵🇹", "optional", "A concise European-style CV with clear dates and qualifications."),
    ("Belgium", "🇧🇪", "optional", "Language skills matter when they are already in the source resume. Keep the layout conservative."),
    ("Austria", "🇦🇹", "common", "A structured CV similar to a German Lebenslauf, with a photo only if the source already has one."),
    ("Norway", "🇳🇴", "omit", "Short, factual, and modest. Do not add personal details."),
    ("Denmark", "🇩🇰", "omit", "Informal but precise. Focus on results and leave off a photo."),
    ("Finland", "🇫🇮", "omit", "A compact CV. Highlight skills and keep personal information limited."),
    ("Poland", "🇵🇱", "optional", "A clear chronology. A photo is sometimes expected; do not invent one."),
    ("Czech Republic", "🇨🇿", "optional", "A structured CV with education and experience in reverse chronological order."),
    ("South Korea", "🇰🇷", "optional", "For English roles, use a concise international resume rather than a full domestic form."),
    ("China", "🇨🇳", "optional", "International roles usually want a concise English resume. Do not add a photo unless it is already present."),
    ("Hong Kong", "🇭🇰", "omit", "A concise, achievement-led resume closer to UK or international style."),
    ("Taiwan", "🇹🇼", "optional", "A clear English resume for international roles, with dates and education easy to find."),
    ("Malaysia", "🇲🇾", "optional", "A straightforward CV. Include only personal details that are already in the source."),
    ("Thailand", "🇹🇭", "optional", "A polite, structured CV. Do not add a photo or age if they are not in the source."),
    ("Indonesia", "🇮🇩", "optional", "A chronological CV with education and experience clearly separated."),
    ("Philippines", "🇵🇭", "optional", "A detailed but scannable resume. Keep claims limited to the source text."),
    ("Vietnam", "🇻🇳", "optional", "A simple chronological CV for international applications."),
    ("South Africa", "🇿🇦", "omit", "A skills-and-achievement resume. Omit photo, age, and marital status."),
    ("Nigeria", "🇳🇬", "omit", "A clear, achievement-led CV with standard headings and no unnecessary personal data."),
    ("Kenya", "🇰🇪", "omit", "A concise CV focused on results, tools, and education already in the source."),
    ("Brazil", "🇧🇷", "optional", "A objective-led CV is common. Do not invent an objective that the source does not support."),
    ("Mexico", "🇲🇽", "optional", "A chronological CV. A photo is sometimes used; this tool will not require one."),
    ("Argentina", "🇦🇷", "optional", "A structured CV with education and experience. Keep personal details limited."),
    ("Chile", "🇨🇱", "optional", "A clean chronological CV with a short profile drawn only from the source."),
    ("Colombia", "🇨🇴", "optional", "A clear CV with dates, education, and relevant skills already listed by the user."),
    ("Saudi Arabia", "🇸🇦", "optional", "A professional CV emphasizing qualifications and experience. Add personal details only when they are already present."),
    ("Qatar", "🇶🇦", "optional", "A structured CV similar to other Gulf applications, without invented personal data."),
    ("Israel", "🇮🇱", "omit", "A concise, direct resume. One to two pages is typical for most roles."),
    ("Turkey", "🇹🇷", "optional", "A chronological CV. A photo is sometimes included; do not create one."),
    ("Greece", "🇬🇷", "optional", "A structured CV with education and experience easy to follow."),
    ("Romania", "🇷🇴", "optional", "A Europass-like structure is common, but a clean international CV is appropriate."),
    ("Hungary", "🇭🇺", "optional", "A conservative CV with clear dates, education, and experience."),
    ("Luxembourg", "🇱🇺", "optional", "Language ability matters when the source lists it. Keep the layout formal."),
]

COUNTRIES = []
COUNTRY_GUIDANCE = {}
for name, flag, photo, note in _RAW:
    item = {
        "name": name,
        "flag": flag,
        "photo": photo,
        "note": note,
        "slug": slugify(name),
        "guidance": note,
    }
    COUNTRIES.append(item)
    COUNTRY_GUIDANCE[name] = note

FEATURED = [
    "United States", "United Kingdom", "Germany", "Japan", "Canada", "Australia",
    "UAE", "Singapore", "France", "Netherlands", "Sweden", "Switzerland",
]
BY_SLUG = {c["slug"]: c for c in COUNTRIES}
BY_NAME = {c["name"]: c for c in COUNTRIES}

BLOG_POSTS = [
    {
        "slug": "adapt-a-resume-for-a-new-country",
        "title": "How to adapt a resume for a new country",
        "date": "March 12, 2026",
        "excerpt": "Hiring norms change at the border. Here is what to check before you send the same file everywhere.",
        "paragraphs": [
            "A resume that reads well in one market can look unfinished in another. The usual differences are length, photo, date of birth, spelling, and how strongly you are expected to sell your results.",
            "Start with the facts you already have. Reorder them so the most relevant role is easy to see, and use the spelling of the country you are applying in. Do not add a degree, a tool, or a metric that is not in your history.",
            "Jobaround applies those country notes to the text it can actually read from your file. If a detail is missing from the upload, it stays missing.",
        ],
    },
    {
        "slug": "what-ats-software-reads",
        "title": "What applicant tracking systems actually read",
        "date": "February 2, 2026",
        "excerpt": "Most tracking systems want plain headings and text, not columns, text boxes, or icons.",
        "paragraphs": [
            "An applicant tracking system stores the text it can extract. Tables, sidebars, and graphics often come through out of order or not at all.",
            "Use standard headings such as Experience, Education, and Skills. Put dates on the same line as the role, and write bullets as sentences a person can read aloud.",
            "Jobaround exports a simple PDF and DOCX for that reason. The preview you see is the same text that goes into the file.",
        ],
    },
    {
        "slug": "details-to-leave-off",
        "title": "Details to leave off an international application",
        "date": "January 18, 2026",
        "excerpt": "Photo, age, marital status, and a full home address are often unnecessary, and sometimes unwelcome.",
        "paragraphs": [
            "In the United States, Canada, the United Kingdom, and Australia, recruiters usually do not want a photo, date of birth, or marital status on a resume.",
            "Some European and Gulf markets still see a photo on CVs. That does not mean you should add one if your file does not already include it, and it does not mean a photo is a requirement.",
            "When you are unsure, keep the document to contact details, work, education, and skills. Jobaround follows that rule unless the country note says a photo is culturally common.",
        ],
    },
    {
        "slug": "bullets-that-travel",
        "title": "Write achievement bullets that still make sense abroad",
        "date": "December 9, 2025",
        "excerpt": "A result is easier to trust than a job title. Keep the number only if you can point to it in the original resume.",
        "paragraphs": [
            "Strong bullets name the work and the outcome: what changed, for whom, and by how much. If the original resume has no number, do not invent one for the new country.",
            "Action verbs help when they match the work. 'Led' is not a synonym for 'helped with'. The rewrite should stay inside the original responsibility.",
            "Paste the job description when you have it. Jobaround can emphasize overlapping skills, and it is instructed not to claim a keyword you never used.",
        ],
    },
]

POSTS_BY_SLUG = {p["slug"]: p for p in BLOG_POSTS}

FAQS = [
    ("Which files can I upload?", "PDF, DOCX, and TXT, up to 8 MB. Scanned image-only PDFs often have no extractable text."),
    ("Do I need an account?", "No. You can tailor a resume without signing in. An account only saves the preview and download links on this server."),
    ("Does this use a paid AI key?", "No OpenAI key is required. The app calls a local Ollama model when OLLAMA_URL is reachable, and otherwise rewrites nothing: it keeps your original text and adds a short targeting note."),
    ("Will it invent experience?", "It is instructed not to. The fallback path never adds employers, dates, or skills that were not in the upload."),
    ("How many countries are supported?", "Fifty. Each one has its own formatting note, and you can read the guide before you generate a file."),
    ("Where do my files go?", "The upload is deleted after text is extracted. The generated PDF and DOCX stay in the app's output folder so the download links work."),
]
