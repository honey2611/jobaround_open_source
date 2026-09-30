const form = document.getElementById("resumeForm");
const statusBox = document.getElementById("status");
const result = document.getElementById("result");
const preview = document.getElementById("preview");
const pdfLink = document.getElementById("pdfLink");
const docxLink = document.getElementById("docxLink");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  statusBox.textContent = "Processing your resume… This can take a little while on a local model.";
  statusBox.className = "status loading";
  result.classList.add("hidden");

  try {
    const response = await fetch("/api/tailor", {
      method: "POST",
      body: new FormData(form)
    });

    const data = await response.json();

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
