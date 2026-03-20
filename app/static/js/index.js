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
      this.outputBox = document.getElementById(`${prefix}-outputBox`) || this.outputImg?.parentElement;


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
        showModal("Invalid File", "Please upload a valid image file (PNG, JPG, etc.).", "📂");
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
      this.loader.style.display = "flex";
      if (this.outputBox) this.outputBox.classList.add("preview__box--scanning");
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

          // Special case for insufficient credits: show modal then redirect on click
          if (response.status === 402) {
            this.setStatus("Credit limit reached");
            showModal("Insufficient Credits", message, "⚡", "/pricing");
            return;
          }

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
        showModal("Processing Error", err.message || "Something went wrong.", "⚠️");
      } finally {
        this.loader.style.display = "none";
        if (this.outputBox) this.outputBox.classList.remove("preview__box--scanning");
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

  class BackgroundMotion {
    constructor() {
      this.canvas = document.getElementById('bg-canvas');
      if (!this.canvas) return;
      this.ctx = this.canvas.getContext('2d');
      this.bubbles = [];
      this.count = 45;

      window.addEventListener('resize', () => this.resize());

      this.resize();
      this.init();
      this.animate();
    }

    resize() {
      this.canvas.width = window.innerWidth;
      this.canvas.height = window.innerHeight;
    }

    init() {
      for (let i = 0; i < this.count; i++) {
        this.bubbles.push({
          x: (Math.random() - 0.5) * 3000,
          y: (Math.random() - 0.5) * 3000,
          z: Math.random() * 2000,
          size: 15 + Math.random() * 30,
          speed: 0.5 + Math.random() * 2.0
        });
      }
    }

    animate() {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

      const centerX = this.canvas.width / 2;
      const centerY = this.canvas.height / 2;

      // Sort bubbles by depth to draw furthest first
      this.bubbles.sort((a, b) => b.z - a.z);

      for (let i = 0; i < this.bubbles.length; i++) {
        const p = this.bubbles[i];

        // Move float naturally upwards
        p.y -= p.speed;
        if (p.y < -1500) p.y = 1500;

        // Perspective projection
        // Offset z to be in front of camera
        const zOffset = p.z + 1000;
        if (zOffset < 1) continue;

        const scale = 800 / zOffset;
        const px = p.x * scale + centerX;
        const py = p.y * scale + centerY;
        const ps = p.size * scale;

        // Draw 3D Bubble
        this.ctx.beginPath();
        this.ctx.arc(px, py, ps, 0, Math.PI * 2);

        // Radial gradient for 3D bubble effect
        const gradient = this.ctx.createRadialGradient(
          px - ps * 0.3, py - ps * 0.3, ps * 0.1,
          px, py, ps
        );
        gradient.addColorStop(0, `rgba(255, 255, 255, ${Math.min(1, scale * 0.7)})`);
        gradient.addColorStop(0.3, `rgba(142, 117, 255, ${Math.min(1, scale * 0.4)})`);
        gradient.addColorStop(0.8, `rgba(80, 50, 200, ${Math.min(1, scale * 0.1)})`);
        gradient.addColorStop(1, `rgba(108, 71, 255, ${Math.min(1, scale * 0.5)})`);

        this.ctx.fillStyle = gradient;
        this.ctx.fill();

        // Bubble outline
        this.ctx.lineWidth = Math.max(0.5, scale * 1.5);
        this.ctx.strokeStyle = `rgba(255, 255, 255, ${Math.min(1, scale * 0.6)})`;
        this.ctx.stroke();
      }

      requestAnimationFrame(() => this.animate());
    }
  }

  // Initialize Services - Wrapped in DOMContentLoaded to be safe
  document.addEventListener('DOMContentLoaded', () => {
    new ServiceUI('cleaner', '/api/image-cleaner/clean');
    new ServiceUI('art', '/api/image-to-art');
    new BackgroundMotion();

    // Profile dropdown toggle
    const avatar = document.getElementById('user-avatar');
    const dropdown = document.getElementById('profile-dropdown');
    const sidebarAvatar = document.getElementById('sidebar-avatar-btn');
    const sidebarDropdown = document.getElementById('sidebar-profile-dropdown');

    if (avatar && dropdown) {
      avatar.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdown.classList.toggle('is-active');
        if (sidebarDropdown) sidebarDropdown.classList.remove('is-active');
      });
    }

    if (sidebarAvatar && sidebarDropdown) {
      sidebarAvatar.addEventListener('click', (e) => {
        e.stopPropagation();
        sidebarDropdown.classList.toggle('is-active');
        if (dropdown) dropdown.classList.remove('is-active');
      });
    }

    document.addEventListener('click', () => {
      if (dropdown) dropdown.classList.remove('is-active');
      if (sidebarDropdown) sidebarDropdown.classList.remove('is-active');
    });

    // Explicit logout handler to ensure navigation happens
    const logoutBtns = document.querySelectorAll('.menu-item.logout');
    logoutBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation(); // Stop dropdown from toggling before navigation
        // Force navigation to ensure the server receives the logout request
        window.location.href = btn.href;
      });
    });

    // Demo Slider Logic
    const demoWrappers = document.querySelectorAll('.demo-slider-wrapper');
    demoWrappers.forEach(wrapper => {
      const afterImage = wrapper.querySelector('.demo-image-after');
      const handle = wrapper.querySelector('.demo-slider-handle');

      let isSliding = false;
      let isHovering = false;
      let autoPosition = 50;
      let autoDirection = 0.15; // Speed and direction

      const updateSlider = (percent) => {
        afterImage.style.width = `${percent}%`;
        handle.style.left = `${percent}%`;
      };

      const slide = (e) => {
        if (!isSliding) return;
        let x = e.clientX;
        if (e.touches && e.touches.length > 0) {
          x = e.touches[0].clientX;
        }

        let rect = wrapper.getBoundingClientRect();
        let position = ((x - rect.left) / rect.width) * 100;
        if (position < 0) position = 0;
        if (position > 100) position = 100;

        autoPosition = position; // Sync auto position
        updateSlider(position);
      };

      wrapper.addEventListener('mousedown', () => isSliding = true);
      wrapper.addEventListener('mouseup', () => isSliding = false);
      wrapper.addEventListener('mouseleave', () => {
        isSliding = false;
        isHovering = false;
      });
      wrapper.addEventListener('mouseenter', () => isHovering = true);
      wrapper.addEventListener('mousemove', (e) => {
        if (isSliding) slide(e);
      });

      wrapper.addEventListener('touchstart', () => {
        isSliding = true;
        isHovering = true;
      });
      wrapper.addEventListener('touchend', () => {
        isSliding = false;
        isHovering = false;
      });
      wrapper.addEventListener('touchmove', (e) => {
        if (isSliding) slide(e);
      }, { passive: true });

      // Auto Animation Loop
      function autoAnimate() {
        if (!isSliding && !isHovering) {
          autoPosition += autoDirection;
          if (autoPosition >= 80) autoDirection = -0.15;
          if (autoPosition <= 20) autoDirection = 0.15;
          updateSlider(autoPosition);
        }
        requestAnimationFrame(autoAnimate);
      }
      autoAnimate();
    });
  });

  // Global functions to show/hide modal
  let nextUrl = null;

  window.showModal = (title, message, icon = "⚡", redirectPath = null) => {
    const modal = document.getElementById("global-modal");
    if (!modal) return;

    nextUrl = redirectPath;
    document.getElementById("modal-title").innerText = title;
    document.getElementById("modal-message").innerText = message;
    document.getElementById("modal-icon").innerText = icon;
    modal.classList.add("is-active");
  };

  window.closeModal = () => {
    const modal = document.getElementById("global-modal");
    if (modal) modal.classList.remove("is-active");

    if (nextUrl) {
      window.location.href = nextUrl;
      nextUrl = null;
    }
  };

})();