const log = document.getElementById("log");
const form = document.getElementById("chat-form");
const input = document.getElementById("msg");
const send = document.getElementById("send");

function add(role, text) {
  const d = document.createElement("div");
  d.className = "msg " + role;
  d.dir = "auto";
  d.textContent = text; // textContent only: never inject LLM/user text as HTML
  log.appendChild(d);
  log.scrollTop = log.scrollHeight;
  return d;
}

function addTrace(bubble, trace) {
  const det = document.createElement("details");
  const sum = document.createElement("summary");
  sum.textContent = "Agent trace";
  const pre = document.createElement("pre");
  pre.textContent = JSON.stringify(trace, null, 2);
  det.append(sum, pre);
  bubble.appendChild(det);
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  add("user", text);
  const bubble = add("bot", "…");
  send.disabled = true;
  try {
    const r = await fetch("/api/chat/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || data.detail || "Request failed");
    bubble.textContent = data.reply;
    if (data.trace) addTrace(bubble, data.trace);
  } catch (err) {
    bubble.textContent = "⚠️ " + err.message;
    bubble.classList.add("error");
  } finally {
    send.disabled = false;
    input.focus();
    log.scrollTop = log.scrollHeight;
  }
});

document.getElementById("reset").addEventListener("click", async () => {
  await fetch("/api/chat/reset/", { method: "POST" });
  log.replaceChildren();
  add("bot", "گفتگوی جدید شروع شد. چطور می‌توانم کمکتان کنم؟");
});