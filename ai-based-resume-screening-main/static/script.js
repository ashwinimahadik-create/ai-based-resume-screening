const fileInput = document.getElementById("resumes");
const dropZone = document.getElementById("dropZone");
const fileList = document.getElementById("fileList");
const form = document.getElementById("screeningForm");
const analyzeBtn = document.getElementById("analyzeBtn");

function renderFiles(files) {
    fileList.innerHTML = "";

    if (!files || files.length === 0) {
        return;
    }

    const heading = document.createElement("div");
    heading.className = "file-count";
    heading.textContent = `${files.length} resume(s) selected`;
    fileList.appendChild(heading);

    Array.from(files).forEach((file, index) => {
        const item = document.createElement("div");
        item.className = "file-item";
        item.innerHTML = `
            <span>${index + 1}. ${file.name}</span>
            <small>${(file.size / 1024).toFixed(1)} KB</small>
        `;
        fileList.appendChild(item);
    });
}

fileInput.addEventListener("change", () => {
    renderFiles(fileInput.files);
});

dropZone.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropZone.classList.add("dragging");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragging");
});

dropZone.addEventListener("drop", (event) => {
    event.preventDefault();
    dropZone.classList.remove("dragging");

    const droppedFiles = Array.from(event.dataTransfer.files)
        .filter(file => file.name.toLowerCase().endsWith(".pdf"));

    const dataTransfer = new DataTransfer();
    droppedFiles.forEach(file => dataTransfer.items.add(file));
    fileInput.files = dataTransfer.files;

    renderFiles(fileInput.files);
});

form.addEventListener("submit", () => {
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing candidates...";
});
