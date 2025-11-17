// Popup script to handle language selection and translation control

document.addEventListener('DOMContentLoaded', async () => {
  const languageSelect = document.getElementById('language-select');
  const translateBtn = document.getElementById('translate-btn');
  const clearBtn = document.getElementById('clear-btn');
  const status = document.getElementById('status');

  // Load saved language preference
  const saved = await chrome.storage.local.get(['targetLanguage']);
  if (saved.targetLanguage) {
    languageSelect.value = saved.targetLanguage;
  }

  // Show status message
  function showStatus(message, type = 'info') {
    status.textContent = message;
    status.className = `status show ${type}`;
    setTimeout(() => {
      status.classList.remove('show');
    }, 3000);
  }

  // Translate button handler
  translateBtn.addEventListener('click', async () => {
    const targetLanguage = languageSelect.value;
    
    if (!targetLanguage) {
      showStatus('Please select a target language', 'error');
      return;
    }

    // Save language preference
    await chrome.storage.local.set({ targetLanguage });

    // Get active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    if (!tab) {
      showStatus('Unable to access current tab', 'error');
      return;
    }

    // Disable button during translation
    translateBtn.disabled = true;
    showStatus('Translating page...', 'info');

    try {
      // Check if we can inject scripts on this page
      if (tab.url.startsWith('chrome://') || tab.url.startsWith('chrome-extension://') || tab.url.startsWith('edge://')) {
        showStatus('Cannot translate Chrome/Edge internal pages', 'error');
        translateBtn.disabled = false;
        return;
      }

      // Inject content script if not already injected
      try {
        await chrome.scripting.executeScript({
          target: { tabId: tab.id },
          files: ['content.js']
        });
      } catch (injectError) {
        // Script might already be injected, or injection failed
        console.log('Content script injection:', injectError.message);
      }

      // Wait a moment for script to initialize
      await new Promise(resolve => setTimeout(resolve, 100));

      // Send message to content script
      try {
        await chrome.tabs.sendMessage(tab.id, {
          action: 'translate',
          targetLanguage: targetLanguage
        });
        showStatus('Translation completed!', 'success');
      } catch (messageError) {
        // If message fails, try injecting and sending again
        console.log('First message attempt failed, retrying...');
        await chrome.scripting.executeScript({
          target: { tabId: tab.id },
          files: ['content.js']
        });
        await new Promise(resolve => setTimeout(resolve, 200));
        await chrome.tabs.sendMessage(tab.id, {
          action: 'translate',
          targetLanguage: targetLanguage
        });
        showStatus('Translation completed!', 'success');
      }
    } catch (error) {
      console.error('Translation error:', error);
      showStatus('Error: ' + error.message + '. Try refreshing the page.', 'error');
    } finally {
      translateBtn.disabled = false;
    }
  });

  // Clear button handler
  clearBtn.addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    if (!tab) {
      showStatus('Unable to access current tab', 'error');
      return;
    }

    try {
      // Check if we can inject scripts on this page
      if (tab.url.startsWith('chrome://') || tab.url.startsWith('chrome-extension://') || tab.url.startsWith('edge://')) {
        showStatus('Cannot clear translation on Chrome/Edge internal pages', 'error');
        return;
      }

      // Try to inject content script first
      try {
        await chrome.scripting.executeScript({
          target: { tabId: tab.id },
          files: ['content.js']
        });
        await new Promise(resolve => setTimeout(resolve, 100));
      } catch (injectError) {
        console.log('Content script injection:', injectError.message);
      }

      // Send clear message
      try {
        await chrome.tabs.sendMessage(tab.id, {
          action: 'clear'
        });
        showStatus('Translation cleared!', 'success');
      } catch (messageError) {
        // Try injecting and sending again
        await chrome.scripting.executeScript({
          target: { tabId: tab.id },
          files: ['content.js']
        });
        await new Promise(resolve => setTimeout(resolve, 200));
        await chrome.tabs.sendMessage(tab.id, {
          action: 'clear'
        });
        showStatus('Translation cleared!', 'success');
      }
    } catch (error) {
      console.error('Clear error:', error);
      showStatus('Error: ' + error.message + '. Try refreshing the page.', 'error');
    }
  });
});
