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

document.querySelectorAll("[data-toggle-password]").forEach((button) => {
  button.addEventListener("click", () => {
    const input = document.getElementById(button.getAttribute("data-toggle-password"));
    if (!input) return;
    const show = input.type === "password";
    input.type = show ? "text" : "password";
    button.setAttribute("aria-label", show ? "Hide password" : "Show password");
  });
});

const flagBank = [...document.querySelectorAll(".flag-bank svg")];
const flagTiles = [...document.querySelectorAll(".flag-tile")];
if (flagBank.length && flagTiles.length) {
  const cursor = flagTiles.map((_, index) => index);
  const showFlag = (tile, index) => {
    tile.replaceChildren(flagBank[index].cloneNode(true));
  };
  flagTiles.forEach((tile, index) => showFlag(tile, cursor[index]));
  let turn = 0;
  window.setInterval(() => {
    const slot = turn % flagTiles.length;
    const tile = flagTiles[slot];
    cursor[slot] = (cursor[slot] + flagTiles.length) % flagBank.length;
    tile.classList.add("swap");
    window.setTimeout(() => {
      showFlag(tile, cursor[slot]);
      tile.classList.remove("swap");
    }, 320);
    turn += 1;
  }, 1600);
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
