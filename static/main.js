const nav = document.getElementById("nav");
const menu = document.querySelector(".menu");
const links = document.getElementById("links");

window.addEventListener("scroll", () => {
  nav.classList.toggle("scrolled", window.scrollY > 8);
}, { passive: true });

if (menu && links) {
  menu.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    menu.setAttribute("aria-expanded", open ? "true" : "false");
  });
  links.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => links.classList.remove("open"));
  });
}

const revealNodes = document.querySelectorAll(".reveal");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
if (reduceMotion) {
  revealNodes.forEach((node) => node.classList.add("in"));
} else if (revealNodes.length) {
  const watcher = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("in");
        watcher.unobserve(entry.target);
      }
    });
  }, { threshold: 0.01 });
  revealNodes.forEach((node) => watcher.observe(node));
}

const file = document.getElementById("resume");
const fileLabel = document.getElementById("fileLabel");
const dropzone = document.getElementById("dropzone");
if (file && fileLabel) {
  file.addEventListener("change", () => {
    fileLabel.textContent = file.files[0] ? file.files[0].name : "Drop a PDF, DOCX, or TXT — or click to browse";
    dropzone.classList.toggle("hot", Boolean(file.files[0]));
  });
}
