(() => {
  // Footer year
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  class ServiceUI {
    constructor(prefix, endpoint) {
      this.prefix = prefix;
      this.endpoint = endpoint;
      this.selectedFile = null;
      this.selectedMode = "balanced";

      // Elements
      this.dropzone = document.getElementById(`${prefix}-dropzone`);
      this.fileInput = document.getElementById(`${prefix}-fileInput`);
      this.actionBtn = document.getElementById(`${prefix}-btn`);
      this.resetBtn = document.getElementById(`${prefix}-resetBtn`);
      this.statusPill = document.getElementById(`${prefix}-statusPill`);

      this.origImg = document.getElementById(`${prefix}-origImg`);
      this.outputImg = document.getElementById(`${prefix}-outputImg`);
      this.origEmpty = document.getElementById(`${prefix}-origEmpty`);
      this.outputEmpty = document.getElementById(`${prefix}-outputEmpty`);
      this.loader = document.getElementById(`${prefix}-loader`);
      this.downloadBtn = document.getElementById(`${prefix}-downloadBtn`);
      this.origMeta = document.getElementById(`${prefix}-origMeta`);
      this.outputMeta = document.getElementById(`${prefix}-outputMeta`);

      this.strengthInput = document.getElementById(`${prefix}-strength`);
      this.strengthVal = document.getElementById(`${prefix}-strengthVal`);

      if (!this.dropzone || !this.fileInput) {
        console.warn(`[ServiceUI] Could not find essential elements for ${prefix}`);
        return;
      }

      this.init();
      console.log(`[ServiceUI] Initialized ${prefix} service`);
    }

    init() {
      // Mode toggle
      const section = document.getElementById(`service-${this.prefix}`);
      if (section) {
        section.querySelectorAll(".seg__btn").forEach((btn) => {
          btn.addEventListener("click", () => {
            if (btn.disabled) return;
            section.querySelectorAll(".seg__btn").forEach(b => b.classList.remove("is-on"));
            btn.classList.add("is-on");
            this.selectedMode = btn.dataset.mode || "balanced";
            this.setStatus(`Mode: ${this.capitalize(this.selectedMode)}`);
          });
        });
      }

      if (this.strengthInput) {
        this.strengthInput.addEventListener("input", () => {
          if (this.strengthVal) this.strengthVal.textContent = `${this.strengthInput.value}%`;
        });
      }

      // Open file dialog
      this.dropzone.addEventListener("click", (e) => {
        // Prevent recursive clicks if clicked element is inside
        e.stopPropagation();
        this.fileInput.click();
      });

      this.dropzone.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          this.fileInput.click();
        }
      });

      // Drag/drop
      ["dragenter", "dragover"].forEach(evt => {
        this.dropzone.addEventListener(evt, (e) => {
          e.preventDefault();
          this.dropzone.classList.add("uploader--drag");
        });
      });
      ["dragleave", "drop"].forEach(evt => {
        this.dropzone.addEventListener(evt, (e) => {
          e.preventDefault();
          this.dropzone.classList.remove("uploader--drag");
        });
      });
      this.dropzone.addEventListener("drop", (e) => {
        const f = e.dataTransfer.files?.[0];
        if (f) this.handleFile(f);
      });

      this.fileInput.addEventListener("change", () => {
        const f = this.fileInput.files?.[0];
        if (f) this.handleFile(f);
      });

      if (this.resetBtn) {
        this.resetBtn.addEventListener("click", () => this.resetAll());
      }

      if (this.actionBtn) {
        this.actionBtn.addEventListener("click", () => this.process());
      }

      this.setStatus("Idle");
    }

    handleFile(file) {
      if (!file.type.startsWith("image/")) {
        alert("Please upload an image file.");
        return;
      }

      this.selectedFile = file;

      const url = URL.createObjectURL(file);
      this.origImg.src = url;
      this.origImg.style.display = "block";
      this.origEmpty.style.display = "none";

      // Reset output
      this.outputImg.src = "";
      this.outputImg.style.display = "none";
      this.outputEmpty.style.display = "block";
      this.downloadBtn.href = "#";
      this.downloadBtn.style.display = "none";

      this.origMeta.textContent = `${file.name} • ${this.prettyBytes(file.size)}`;
      this.outputMeta.textContent = "—";

      if (this.actionBtn) this.actionBtn.disabled = false;
      if (this.resetBtn) this.resetBtn.disabled = false;
      this.setStatus("Ready");
    }

    async process() {
      if (!this.selectedFile) return;

      this.setStatus("Processing…");
      this.loader.style.display = "grid";
      this.actionBtn.disabled = true;
      this.resetBtn.disabled = true;

      try {
        const formData = new FormData();
        formData.append("file", this.selectedFile);

        if (this.strengthInput) {
          formData.append("strength", this.strengthInput.value);
        }
        formData.append("mode", this.selectedMode);

        const response = await fetch(this.endpoint, {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          let message = "Processing failed.";
          try {
            const data = await response.json();
            if (data?.detail) message = data.detail;
          } catch (_) { }
          throw new Error(message);
        }

        const blob = await response.blob();
        const resultUrl = URL.createObjectURL(blob);

        this.outputImg.src = resultUrl;
        this.outputImg.style.display = "block";
        this.outputEmpty.style.display = "none";

        this.downloadBtn.href = resultUrl;
        this.downloadBtn.download = `${this.prefix}-${this.selectedFile.name}`;
        this.downloadBtn.style.display = "inline-flex";

        let meta = this.selectedMode;
        if (this.strengthInput) meta = `strength ${this.strengthInput.value}% • ${meta}`;
        this.outputMeta.textContent = meta;

        this.setStatus("Done");
      } catch (err) {
        console.error(`[ServiceUI] Error in ${this.prefix} process:`, err);
        this.setStatus("Failed");
        this.outputMeta.textContent = err.message || "—";
        alert(err.message || "Processing failed.");
      } finally {
        this.loader.style.display = "none";
        this.actionBtn.disabled = false;
        this.resetBtn.disabled = false;
      }
    }

    resetAll() {
      this.selectedFile = null;
      this.fileInput.value = "";

      this.origImg.src = "";
      this.origImg.style.display = "none";
      this.origEmpty.style.display = "block";

      this.outputImg.src = "";
      this.outputImg.style.display = "none";
      this.outputEmpty.style.display = "block";
      this.downloadBtn.href = "#";
      this.downloadBtn.style.display = "none";

      this.origMeta.textContent = "—";
      this.outputMeta.textContent = "—";

      if (this.actionBtn) this.actionBtn.disabled = true;
      if (this.resetBtn) this.resetBtn.disabled = true;
      this.setStatus("Idle");
    }

    setStatus(text) {
      if (this.statusPill) this.statusPill.textContent = text;
    }

    capitalize(s) {
      return s ? s.charAt(0).toUpperCase() + s.slice(1) : s;
    }

    prettyBytes(bytes) {
      const units = ["B", "KB", "MB", "GB"];
      let n = bytes;
      let i = 0;
      while (n >= 1024 && i < units.length - 1) {
        n /= 1024;
        i++;
      }
      return `${n.toFixed(i === 0 ? 0 : 1)} ${units[i]}`;
    }
  }

  // Initialize Services - Wrapped in DOMContentLoaded to be safe
  document.addEventListener('DOMContentLoaded', () => {
    new ServiceUI('cleaner', '/api/image-cleaner/clean');
    new ServiceUI('art', '/api/image-to-art');
  });

})();