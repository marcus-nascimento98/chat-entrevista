function getCSRFToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute("content");
}

function scrollToBottom() {
  const el = document.getElementById("messages");
  el.scrollTop = el.scrollHeight;
}

function showTypingIndicator() {
  const userInput = document.getElementById("user-message");
  userInput.disabled = true;

  const messagesContainer = document.getElementById("messages");

  const typingDiv = document.createElement("div");
  typingDiv.className = "chat-message";
  typingDiv.id = "typing-indicator";

  typingDiv.innerHTML = `
          <div class="flex items-end">
            <div class="flex flex-col space-y-2 text-xs max-w-xs mx-2 order-2 items-start">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        `;

  messagesContainer.appendChild(typingDiv);
  scrollToBottom();
}

function hideTypingIndicator() {
  const typingIndicator = document.getElementById("typing-indicator");
  if (typingIndicator) {
    typingIndicator.remove();
  }

  const userInput = document.getElementById("user-message");
  userInput.disabled = false;
  userInput.focus();
}

function addMessageToChat(message, isUser) {
  const messagesContainer = document.getElementById("messages");

  const messageDiv = document.createElement("div");
  messageDiv.className = "chat-message";

  if (isUser) {
    messageDiv.innerHTML = `
            <div class="flex items-end justify-end">
              <div class="flex flex-col space-y-2 text-xs max-w-xs mx-2 order-1 items-end">
                <div><span class="px-4 py-2 rounded-lg inline-block rounded-br-none bg-blue-600 text-white">${message}</span></div>
              </div>
            </div>
          `;
  } else {
    messageDiv.innerHTML = `
            <div class="flex items-end">
              <div class="flex flex-col space-y-2 text-xs max-w-xs mx-2 order-2 items-start">
                <div><span class="px-4 py-2 rounded-lg inline-block rounded-bl-none bg-gray-300 text-gray-600">${message}</span></div>
              </div>
            </div>
          `;
  }

  messagesContainer.appendChild(messageDiv);
  scrollToBottom();
}

async function sendMessage() {
  const userMessage = document.getElementById("user-message").value.trim();
  if (!userMessage) return;

  addMessageToChat(userMessage, true);

  document.getElementById("user-message").value = "";

  showTypingIndicator();

  try {
    const chatUrl = document.body.dataset.chatUrl;

    const response = await fetch(chatUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": getCSRFToken(),
      },
      body: `user_message=${encodeURIComponent(userMessage)}`,
    });

    if (!response.ok) {
      throw new Error("Erro na resposta do servidor");
    }

    const data = await response.json();

    hideTypingIndicator();

    if (data.bot_response) {
      addMessageToChat(data.bot_response, false);
    }
  } catch (error) {
    console.error("Erro:", error);
    hideTypingIndicator();
    addMessageToChat("Desculpe, ocorreu um erro ao processar sua mensagem.", false);
  }
}

document.addEventListener("DOMContentLoaded", function () {
  scrollToBottom();

  document.getElementById("send-button").addEventListener("click", sendMessage);
  document.getElementById("user-message").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });
});
