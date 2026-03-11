(() => {
  // Footer year
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("fileInput");
  const cleanBtn = document.getElementById("cleanBtn");
  const resetBtn = document.getElementById("resetBtn");
  const statusPill = document.getElementById("statusPill");

  const origImg = document.getElementById("origImg");
  const cleanImg = document.getElementById("cleanImg");
  const origEmpty = document.getElementById("origEmpty");
  const cleanEmpty = document.getElementById("cleanEmpty");
  const loader = document.getElementById("loader");
  const downloadCleanBtn = document.getElementById("downloadCleanBtn");
  const origMeta = document.getElementById("origMeta");
  const cleanMeta = document.getElementById("cleanMeta");

  const strength = document.getElementById("strength");
  const strengthVal = document.getElementById("strengthVal");

  let selectedFile = null;
  let selectedMode = "balanced";

  // mode toggle
  document.querySelectorAll(".seg__btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".seg__btn").forEach(b => b.classList.remove("is-on"));
      btn.classList.add("is-on");
      selectedMode = btn.dataset.mode || "balanced";
      statusPill.textContent = `Mode: ${capitalize(selectedMode)}`;
    });
  });

  strength.addEventListener("input", () => {
    strengthVal.textContent = `${strength.value}%`;
  });

  // open file dialog
  dropzone.addEventListener("click", () => fileInput.click());
  dropzone.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") fileInput.click();
  });

  // drag/drop
  ["dragenter", "dragover"].forEach(evt => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.add("uploader--drag");
    });
  });
  ["dragleave", "drop"].forEach(evt => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.remove("uploader--drag");
    });
  });
  dropzone.addEventListener("drop", (e) => {
    const f = e.dataTransfer.files?.[0];
    if (f) handleFile(f);
  });

  fileInput.addEventListener("change", () => {
    const f = fileInput.files?.[0];
    if (f) handleFile(f);
  });

  resetBtn.addEventListener("click", () => resetAll());

  cleanBtn.addEventListener("click", async () => {
    if (!selectedFile) return;

    setStatus("Processing…");
    loader.style.display = "grid";
    cleanBtn.disabled = true;
    resetBtn.disabled = true;

    try {
      const cleanedUrl = await requestCleanedImage(selectedFile, {
        strength: parseInt(strength.value, 10),
        mode: selectedMode,
      });

      cleanImg.src = cleanedUrl;
      cleanImg.style.display = "block";
      cleanEmpty.style.display = "none";

      downloadCleanBtn.href = cleanedUrl;
      downloadCleanBtn.download = `cleaned-${selectedFile?.name || "image.png"}`;
      downloadCleanBtn.style.display = "inline-flex";

      cleanMeta.textContent = `strength ${strength.value}% • ${selectedMode}`;
      setStatus("Done");
    } catch (err) {
      console.error(err);
      setStatus("Failed");
      cleanMeta.textContent = err.message || "—";
      alert(err.message || "Image cleaning failed.");
    } finally {
      loader.style.display = "none";
      cleanBtn.disabled = false;
      resetBtn.disabled = false;
    }
  });

  function handleFile(file) {
    if (!file.type.startsWith("image/")) return;

    selectedFile = file;

    const url = URL.createObjectURL(file);
    origImg.src = url;
    origImg.style.display = "block";
    origEmpty.style.display = "none";

    // reset output
    cleanImg.src = "";
    cleanImg.style.display = "none";
    cleanEmpty.style.display = "block";
    downloadCleanBtn.href = "#";
    downloadCleanBtn.style.display = "none";

    origMeta.textContent = `${file.name} • ${prettyBytes(file.size)}`;
    cleanMeta.textContent = "—";

    cleanBtn.disabled = false;
    resetBtn.disabled = false;
    setStatus("Ready");
  }

  function resetAll() {
    selectedFile = null;
    fileInput.value = "";

    origImg.src = "";
    origImg.style.display = "none";
    origEmpty.style.display = "block";

    cleanImg.src = "";
    cleanImg.style.display = "none";
    cleanEmpty.style.display = "block";
    downloadCleanBtn.href = "#";
    downloadCleanBtn.style.display = "none";

    origMeta.textContent = "—";
    cleanMeta.textContent = "—";

    cleanBtn.disabled = true;
    resetBtn.disabled = true;
    setStatus("Idle");
  }

  function setStatus(text) {
    statusPill.textContent = text;
  }

  function capitalize(s) {
    return s ? s.charAt(0).toUpperCase() + s.slice(1) : s;
  }

  function prettyBytes(bytes) {
    const units = ["B", "KB", "MB", "GB"];
    let n = bytes;
    let i = 0;
    while (n >= 1024 && i < units.length - 1) {
      n /= 1024;
      i++;
    }
    return `${n.toFixed(i === 0 ? 0 : 1)} ${units[i]}`;
  }

  async function requestCleanedImage(file, opts) {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("strength", String(opts.strength ?? 60));
    formData.append("mode", opts.mode || "balanced");

    const response = await fetch("/api/image-cleaner/clean", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      let message = "Image cleaning failed.";
      try {
        const data = await response.json();
        if (data?.detail) message = data.detail;
      } catch (_) { }
      throw new Error(message);
    }

    const blob = await response.blob();
    return URL.createObjectURL(blob);
  }

  function fileToImage(file) {
    return new Promise((resolve, reject) => {
      const url = URL.createObjectURL(file);
      const img = new Image();
      img.onload = () => {
        URL.revokeObjectURL(url);
        resolve(img);
      };
      img.onerror = reject;
      img.src = url;
    });
  }

  // initialize
  setStatus("Idle");
})();