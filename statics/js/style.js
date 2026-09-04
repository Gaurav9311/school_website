const chatBox = document.getElementById("chat-box");
const form = document.getElementById("chat-form");
const input = document.getElementById("message");
const chips = document.getElementById("chips");
const clearChatButton = document.getElementById("clear-chat");
const welcomeMessage = "Namaste! I'm the S.S.V. Public School assistant. Ask me about admissions, facilities, academics, or anything else about the school.";

function escapeAndBreak(text) {
  return (text || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\n/g, "<br>");
}

function addMessage(sender, text) {
  const el = document.createElement("div");
  el.className = `msg ${sender}`;
  el.innerHTML = escapeAndBreak(text);
  chatBox.appendChild(el);
  chatBox.scrollTop = chatBox.scrollHeight;
  return el;
}

function addTyping() {
  const el = document.createElement("div");
  el.className = "msg bot typing";
  el.innerHTML = "<span></span><span></span><span></span>";
  chatBox.appendChild(el);
  chatBox.scrollTop = chatBox.scrollHeight;
  return el;
}

async function sendMessage(text) {
  const message = text.trim();
  if (!message) return;

  addMessage("user", message);
  input.value = "";

  const typingEl = addTyping();

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    typingEl.remove();
    addMessage("bot", data.reply || "Sorry, I couldn't process that.");

    if (!response.ok) {
      console.error("Chat request failed:", response.status, data);
    }
  } catch (err) {
    typingEl.remove();
    addMessage("bot", "Unable to connect to the chatbot server. Please check that Flask is running and try again.");
    console.error(err);
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage(input.value);
});

chips.addEventListener("click", (e) => {
  const btn = e.target.closest(".chip");
  if (!btn) return;
  sendMessage(btn.dataset.q);
});

clearChatButton.addEventListener("click", () => {
  chatBox.replaceChildren();
  addMessage("bot", welcomeMessage);
  input.focus();
});

window.addEventListener("DOMContentLoaded", () => {
  addMessage("bot", welcomeMessage);
});
