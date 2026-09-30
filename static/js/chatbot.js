/* ==========================================================================
   AI Business Solutions - Working AI Assistant Demo
   Operates locally with FAQ / intent matching without external paid APIs
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initAIAssistant();
});

function initAIAssistant() {
  const messagesBox = document.getElementById('chatMessages');
  const chatInput = document.getElementById('chatInput');
  const chatSendBtn = document.getElementById('chatSendBtn');
  const promptChips = document.querySelectorAll('.chip-btn');
  const floatingTrigger = document.getElementById('floatingChatTrigger');
  const chatSection = document.getElementById('ai-assistant');

  if (!messagesBox || !chatInput || !chatSendBtn) return;

  // Floating trigger button scrolls to assistant demo
  if (floatingTrigger && chatSection) {
    floatingTrigger.addEventListener('click', () => {
      chatSection.scrollIntoView({ behavior: 'smooth' });
      chatInput.focus();
    });
  }

  // Bind suggestion chips
  promptChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const prompt = chip.getAttribute('data-prompt') || chip.textContent.trim();
      chatInput.value = prompt;
      sendMessage(prompt);
    });
  });

  // Send button click
  chatSendBtn.addEventListener('click', () => {
    const text = chatInput.value.trim();
    if (text) {
      sendMessage(text);
    }
  });

  // Enter key in input
  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      const text = chatInput.value.trim();
      if (text) {
        sendMessage(text);
      }
    }
  });

  async function sendMessage(text) {
    // Append user message
    appendMessage(text, 'user');
    chatInput.value = '';

    // Show typing indicator
    const typingIndicator = showTypingIndicator();

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ message: text })
      });

      const data = await response.json();

      // Remove typing indicator
      if (typingIndicator && typingIndicator.parentNode) {
        typingIndicator.parentNode.removeChild(typingIndicator);
      }

      if (response.ok && data.status === 'success') {
        appendMessage(data.reply, 'ai', data.action, data.suggestions);
      } else {
        appendMessage(
          "I'm currently updating my knowledge base. Please feel free to use the contact form below to get in touch with our team directly!",
          'ai',
          { text: "Contact Team", target: "#contact" }
        );
      }
    } catch (err) {
      console.error('Chat error:', err);
      if (typingIndicator && typingIndicator.parentNode) {
        typingIndicator.parentNode.removeChild(typingIndicator);
      }
      appendMessage(
        "Could not connect to the assistant service. You can reach out directly via our contact form below!",
        'ai',
        { text: "Go to Contact Form", target: "#contact" }
      );
    }
  }

  function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.innerHTML = '<span></span><span></span><span></span>';
    messagesBox.appendChild(indicator);
    messagesBox.scrollTop = messagesBox.scrollHeight;
    return indicator;
  }

  function appendMessage(text, sender, action = null, suggestions = null) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message-bubble ${sender === 'user' ? 'message-user' : 'message-ai'}`;

    if (sender === 'user') {
      msgDiv.textContent = text;
    } else {
      // Parse markdown-style formatting (bold, bullets, breaks)
      let formatted = escapeHtml(text);
      formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      formatted = formatted.replace(/\n\n/g, '<br><br>');
      formatted = formatted.replace(/\n• /g, '<br>• ');
      formatted = formatted.replace(/\n/g, '<br>');

      msgDiv.innerHTML = formatted;

      // Add Action Button if provided
      if (action && action.text && action.target) {
        const actionBtn = document.createElement('div');
        actionBtn.style.marginTop = '0.85rem';
        actionBtn.innerHTML = `
          <a href="${action.target}" class="btn btn-outline-glow btn-sm" style="display: inline-flex; text-decoration: none;">
            ${action.text} &rarr;
          </a>
        `;
        msgDiv.appendChild(actionBtn);
      }

      // Add clickable suggested follow-ups
      if (suggestions && suggestions.length > 0) {
        const suggContainer = document.createElement('div');
        suggContainer.style.marginTop = '0.85rem';
        suggContainer.style.display = 'flex';
        suggContainer.style.flexWrap = 'wrap';
        suggContainer.style.gap = '0.4rem';

        suggestions.forEach(sugg => {
          const suggBtn = document.createElement('button');
          suggBtn.className = 'chip-btn';
          suggBtn.style.fontSize = '0.75rem';
          suggBtn.style.padding = '0.25rem 0.6rem';
          suggBtn.textContent = sugg;
          suggBtn.addEventListener('click', () => {
            chatInput.value = sugg;
            sendMessage(sugg);
          });
          suggContainer.appendChild(suggBtn);
        });

        msgDiv.appendChild(suggContainer);
      }
    }

    messagesBox.appendChild(msgDiv);
    messagesBox.scrollTop = messagesBox.scrollHeight;
  }

  function escapeHtml(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }
}
