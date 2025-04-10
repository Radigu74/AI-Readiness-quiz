let currentStep = 0;
const steps = document.querySelectorAll(".step");
const progress = document.getElementById("progress");

function nextStep() {
  steps[currentStep].classList.remove("active");
  currentStep++;
  steps[currentStep].classList.add("active");
  progress.style.width = ((currentStep + 1) / steps.length) * 100 + "%";
}

document.getElementById("quizForm").addEventListener("submit", async function(e) {
  e.preventDefault();
  const data = new FormData(this);
  const json = Object.fromEntries(data.entries());

  const res = await fetch("/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(json)
  });

  const result = await res.json();

  document.getElementById("result").innerHTML = `
    <h2>${result.readiness}</h2>
    <p>${result.message}</p>
    <div>${marked.parse(result.summary)}</div>
    <a href="${result.ctaLink}" class="cta-link" target="_blank">${result.ctaText}</a><br/><br/>
    <button onclick="downloadReport('${btoa(JSON.stringify(result))}')">Download Report</button>
  `;
});

function downloadReport(encoded) {
  const blob = new Blob([atob(encoded)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "ai-readiness-report.json";
  link.click();
}
