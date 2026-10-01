const form = document.getElementById("resumeForm");
const statusBox = document.getElementById("status");
const result = document.getElementById("result");
const preview = document.getElementById("preview");
const pdfLink = document.getElementById("pdfLink");
const docxLink = document.getElementById("docxLink");

if (form) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    statusBox.textContent = "Tailoring your resume…";
    statusBox.className = "status loading";
    result.classList.add("hidden");

    try {
      const response = await fetch("/api/tailor", {
        method: "POST",
        body: new FormData(form)
      });
      const raw = await response.text();
      let data;
      try {
        data = JSON.parse(raw);
      } catch {
        throw new Error("The server could not process the upload. Try a text-based PDF, DOCX, or TXT under 8 MB.");
      }
      if (!response.ok) throw new Error(data.error || "Something went wrong.");
      statusBox.textContent = data.message;
      statusBox.className = data.ai_used ? "status success" : "status warning";
      preview.textContent = data.preview;
      pdfLink.href = data.pdf;
      docxLink.href = data.docx;
      result.classList.remove("hidden");
    } catch (err) {
      statusBox.textContent = err.message;
      statusBox.className = "status error";
    }
  });
}
