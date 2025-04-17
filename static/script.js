// /static/script.js

document.addEventListener("DOMContentLoaded", () => {
  let currentStep = 0;
  const intro = document.getElementById("introScreen");
  const form = document.getElementById("quizForm");
  const steps = document.querySelectorAll(".step");
  const progress = document.getElementById("progress");
  const resultDiv = document.getElementById("result");

  // 1) Start button: hide intro, show quiz
  document.getElementById("startButton").addEventListener("click", () => {
    intro.style.display = "none";
    form.style.display = "block";
    updateStepDisplay();
  });

  // 2) Advance function
  function updateStepDisplay() {
    steps.forEach((step, i) => step.classList.toggle("active", i === currentStep));
    progress.style.width = `${(currentStep / (steps.length - 1)) * 100}%`;
    const counter = document.getElementById("stepCounter");
    if (counter) counter.textContent = currentStep === 0 ? "" : `Step ${currentStep+1} of ${steps.length}`;
  }

  function nextStep() {
    const select = steps[currentStep].querySelector("select");
    if (select && !select.value) {
      select.focus();
      select.style.border = "2px solid red";
      return;
    }
    select && (select.style.border = "");
    if (currentStep < steps.length - 1) {
      currentStep++;
      updateStepDisplay();
    }
  }

  // 3) Wire your “Next” buttons
  document.querySelectorAll(".next-btn").forEach(btn => {
    btn.addEventListener("click", nextStep);
  });

  // 4) Handle form submission
  form.addEventListener("submit", async e => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());

    // Show loading
    resultDiv.innerHTML = `
      <div class="result loading">
        <p>💬 Analyzing your responses...</p>
        <div class="dots"><span>.</span><span>.</span><span>.</span></div>
      </div>`;
    progress.style.width = "100%";

    try {
      const res = await fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      const result = await res.json();
      if (result.error) throw new Error(result.error);

      // Build observations
      const obs = [];
      if (data.q1==="extensive") obs.push("✅ Strong use of automation");
      else if (data.q1==="some") obs.push("⚙️ Partial automation in place");
      else obs.push("🛠️ Mostly manual processes");

      if (data.q2==="low") obs.push("⚠️ Team lacks AI confidence");
      else if (data.q2==="medium") obs.push("🤔 Team is warming up to AI");
      else obs.push("💪 Team is confident with AI");

      if (data.q3==="active") obs.push("📊 Data is actively used");
      else if (data.q3==="collect") obs.push("📦 Data is collected but underused");
      else obs.push("📭 No structured data usage");

      if (data.q4==="yes") obs.push("🧠 Already using AI tools");
      else if (data.q4==="testing") obs.push("🧪 Experimenting with AI tools");
      else obs.push("🆕 Yet to explore AI tools");

      // Show insights
      let insight = `<div class="result insights"><h3>Here’s what we found:</h3>`;
      obs.forEach(line => insight += `<p>${line}</p>`);
      insight += `<p>🤖 Calculating your AI readiness...</p></div>`;

      setTimeout(() => {
        resultDiv.innerHTML = insight;

        // Final result
        setTimeout(() => {
          resultDiv.innerHTML = `
            <div class="result-box">
              <h2 class="readiness-title">Your AI Readiness Stage:</h2>
              <div class="readiness-badge">${result.readiness}</div>
              <p class="readiness-message">${result.message}</p>
              <a href="${result.ctaLink}" target="_blank" class="cta-button">${result.ctaText}</a>
            </div>`;
        }, 2000);

      }, 1500);

    } catch (err) {
      resultDiv.innerHTML = `
        <div class="result error">
          <h3>Oops!</h3><p>${err.message}</p>
        </div>`;
    }
  });
});

