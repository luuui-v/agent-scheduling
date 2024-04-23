document.addEventListener("DOMContentLoaded", function() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const script = document.createElement("script");
          script.src = "https://assets.calendly.com/assets/external/widget.js";
          script.async = true;
          document.body.appendChild(script);
          observer.disconnect();
        }
      });
    });
    const calendlyDiv = document.querySelector(".calendly-inline-widget");
    observer.observe(calendlyDiv);
  });
