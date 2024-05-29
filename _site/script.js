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


  const contentful = require('contentful')

const client = contentful.createClient({
  space: 'svvcat7jcmtv',
  environment: 'master', // defaults to 'master' if not set
  accessToken: '_DtXKrasaVkrTCtvirC9qN6aKsCagX9skvsMiBpSwKM'
})

client.getEntry('5FHJKkqhWRKMhrB0UH5L9v')
  .then((entry) => console.log(entry))
  .catch(console.error)
