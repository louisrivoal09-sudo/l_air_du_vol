// ============================================
// IA LOCAL ULTRA-RAPIDE - L'Air du Vol
// Basée sur la base de données du site #codebase
// ============================================

(function() {
  'use strict';

  const aiBtn = document.getElementById('ai-chat-btn');
  const aiModal = document.getElementById('ai-chat-modal');
  const closeBtn = document.getElementById('close-ai-chat');
  const msgs = document.getElementById('ai-chat-messages');
  const input = document.getElementById('ai-input');
  const sendBtn = document.getElementById('ai-send-btn');
  const typing = document.getElementById('typing-indicator');

  if (!aiBtn || !aiModal) return;

  let isOpen = false;
  let waiting = false;

  // Quick DOM helpers
  const toggle = () => isOpen ? close() : open();
  const open = () => {
    aiModal.classList.add('active');
    isOpen = true;
    input.focus();
  };
  const close = () => {
    aiModal.classList.remove('active');
    isOpen = false;
  };

  // Add message to chat
  const addMsg = (text, sender = 'user') => {
    const div = document.createElement('div');
    div.className = `ai-message ai-message-${sender}`;
    div.innerHTML = `<p>${escapeHtml(text)}</p>`;
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
  };

  const showTyping = () => {
    typing.style.display = 'block';
    msgs.scrollTop = msgs.scrollHeight;
  };

  const hideTyping = () => {
    typing.style.display = 'none';
  };

  const escapeHtml = (str) => {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  };

  // Send message to backend
  const send = async () => {
    const msg = input.value.trim();
    if (!msg || waiting) return;

    addMsg(msg, 'user');
    input.value = '';
    input.focus();

    waiting = true;
    showTyping();

    try {
      const res = await fetch('/api/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrf()
        },
        body: JSON.stringify({ message: msg })
      });

      const data = await res.json();
      hideTyping();

      if (data.success || data.message) {
        addMsg(data.message, 'ai');

        // Afficher les résultats s'il y en a
        if (data.results && data.results.length > 0) {
          data.results.forEach(result => {
            let link = '';
            if (result.type === 'article') {
              link = `<a href="/article/${result.slug}/" style="color: #0A2463; text-decoration: underline;">→ Lire</a>`;
            } else if (result.type === 'media') {
              link = `<a href="/media/${result.slug}/" style="color: #0A2463; text-decoration: underline;">→ Voir</a>`;
            } else if (result.type === 'lien') {
              link = `<a href="${result.url}" target="_blank" style="color: #0A2463; text-decoration: underline;">→ Accéder</a>`;
            }

            const div = document.createElement('div');
            div.style.cssText = 'background: #f0f0f0; padding: 0.75rem; margin: 0.5rem 0; border-radius: 0.5rem; border-left: 3px solid #0A2463;';
            div.innerHTML = `<strong style="color: #0A2463;">${escapeHtml(result.titre)}</strong><br><small style="color: #666;">${escapeHtml(result.description)}</small><br>${link}`;
            msgs.appendChild(div);
          });
          msgs.scrollTop = msgs.scrollHeight;
        }
      } else {
        addMsg('Erreur lors de la requête 😔', 'error');
      }
    } catch (err) {
      hideTyping();
      console.error(err);
      addMsg('Désolé, le serveur ne répond pas! 🤖', 'error');
    } finally {
      waiting = false;
    }
  };

  // Get CSRF token
  const getCsrf = () => {
    const name = 'csrftoken';
    let val = null;
    if (document.cookie) {
      document.cookie.split(';').forEach(c => {
        const cookie = c.trim();
        if (cookie.startsWith(name + '=')) {
          val = decodeURIComponent(cookie.substring(name.length + 1));
        }
      });
    }
    return val;
  };

  // Event listeners
  aiBtn.addEventListener('click', toggle);
  closeBtn.addEventListener('click', close);
  sendBtn.addEventListener('click', send);
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  });

  // Close with Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && isOpen) close();
  });

  // Welcome message
  if (msgs.children.length === 0) {
    addMsg('Bienvenue! 👋 Je suis votre assistant personnel. Posez-moi une question sur L\'Air du Vol! ✈️', 'ai');
  }
})();
