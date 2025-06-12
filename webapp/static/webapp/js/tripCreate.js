document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ tripCreate.js spuštěn");
    const selected = new Set();
    const gallery = document.getElementById("gallery");
    const hiddenInput = document.getElementById("selected-images");

    gallery.querySelectorAll(".gallery-image").forEach(imgDiv => {
      imgDiv.addEventListener("click", () => {
        const filename = imgDiv.dataset.filename;
        if (selected.has(filename)) {
          selected.delete(filename);
          imgDiv.classList.remove("border-primary");
          imgDiv.classList.add("border-secondary");
        } else {
          selected.add(filename);
          imgDiv.classList.add("border-primary");
          imgDiv.classList.remove("border-secondary");
        }
        hiddenInput.value = Array.from(selected).join(",");
      });
    });
  });