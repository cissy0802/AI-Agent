// Content script to translate web page text paragraph by paragraph

(function() {
  'use strict';

  // Prevent duplicate initialization of data structures
  if (!window.webTranslatorData) {
    window.webTranslatorData = {
      translatedElements: new Map(),
      isTranslating: false
    };
  }

  const translatedElements = window.webTranslatorData.translatedElements;
  let isTranslating = window.webTranslatorData.isTranslating;

  // Detect page language
  function detectPageLanguage() {
    const htmlLang = document.documentElement.lang || '';
    const bodyText = document.body.innerText || '';
    
    // Try to detect from HTML lang attribute
    if (htmlLang.length >= 2) {
      return htmlLang.substring(0, 2).toLowerCase();
    }
    
    // Default to 'auto' for automatic detection
    return 'auto';
  }

  // Extract text nodes from an element
  function getTextNodes(element) {
    const textNodes = [];
    const walker = document.createTreeWalker(
      element,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode: function(node) {
          // Skip script and style content
          const parent = node.parentElement;
          if (!parent || 
              parent.tagName === 'SCRIPT' || 
              parent.tagName === 'STYLE' ||
              parent.tagName === 'NOSCRIPT') {
            return NodeFilter.FILTER_REJECT;
          }
          // Skip empty or whitespace-only nodes
          if (!node.textContent || !node.textContent.trim()) {
            return NodeFilter.FILTER_REJECT;
          }
          return NodeFilter.FILTER_ACCEPT;
        }
      }
    );

    let node;
    while (node = walker.nextNode()) {
      textNodes.push(node);
    }
    return textNodes;
  }

  // Wrap text node in a container if needed
  function wrapTextNode(textNode) {
    const parent = textNode.parentElement;
    if (!parent) return null;

    // If parent already has our translation wrapper, return it
    if (parent.classList.contains('translator-wrapper')) {
      return parent;
    }

    // Create wrapper
    const wrapper = document.createElement('span');
    wrapper.className = 'translator-wrapper';
    wrapper.setAttribute('data-original', textNode.textContent.trim());
    
    parent.insertBefore(wrapper, textNode);
    wrapper.appendChild(textNode);
    
    return wrapper;
  }

  // Translate text using Google Translate API (free web version)
  async function translateText(text, targetLang, sourceLang = 'auto') {
    try {
      // Use Google Translate web API
      const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${sourceLang}&tl=${targetLang}&dt=t&q=${encodeURIComponent(text)}`;
      
      const response = await fetch(url);
      const data = await response.json();
      
      if (data && data[0] && data[0][0] && data[0][0][0]) {
        return data[0].map(item => item[0]).join('');
      }
      
      return text; // Return original if translation fails
    } catch (error) {
      console.error('Translation error:', error);
      return text;
    }
  }

  // Translate a single element
  async function translateElement(wrapper, targetLang, sourceLang) {
    const originalText = wrapper.getAttribute('data-original') || wrapper.innerText.trim();
    
    if (!originalText || originalText.length === 0) {
      return;
    }

    try {
      const translatedText = await translateText(originalText, targetLang, sourceLang);
      
      // Create translation display
      const originalSpan = document.createElement('span');
      originalSpan.className = 'translator-original';
      originalSpan.textContent = originalText;
      originalSpan.style.cssText = 'display: block; margin-bottom: 4px; color: #333;';
      
      const translatedSpan = document.createElement('span');
      translatedSpan.className = 'translator-translated';
      translatedSpan.textContent = translatedText;
      translatedSpan.style.cssText = 'display: block; color: #667eea; font-weight: 500; border-left: 3px solid #667eea; padding-left: 8px; margin-top: 4px;';
      
      // Clear wrapper and add both texts
      wrapper.innerHTML = '';
      wrapper.appendChild(originalSpan);
      wrapper.appendChild(translatedSpan);
      
      translatedElements.set(wrapper, {
        original: originalText,
        translated: translatedText
      });
      
    } catch (error) {
      console.error('Error translating element:', error);
    }
  }

  // Clear translation from an element
  function clearElementTranslation(wrapper) {
    const original = wrapper.getAttribute('data-original');
    if (original) {
      // Get the original div content
      const originalDiv = wrapper.querySelector('.translator-original');
      if (originalDiv) {
        wrapper.innerHTML = originalDiv.innerHTML;
        wrapper.classList.remove('translator-wrapper');
        wrapper.removeAttribute('data-original');
        translatedElements.delete(wrapper);
      }
    }
  }

  // Main translation function
  async function translatePage(targetLang) {
    if (window.webTranslatorData.isTranslating) {
      console.log('Translation already in progress');
      return;
    }

    window.webTranslatorData.isTranslating = true;
    isTranslating = true;
    const sourceLang = detectPageLanguage();
    
    console.log(`Translating from ${sourceLang} to ${targetLang}`);

    // Find all paragraph and block-level text elements
    // Priority: paragraphs, headings, list items, table cells, etc.
    const selectors = [
      'p',
      'h1, h2, h3, h4, h5, h6',
      'li',
      'td, th',
      'blockquote',
      'figcaption',
      'label',
      'span[role="text"], div[role="text"]',
      'span, div, a'
    ];

    const allElements = [];
    for (const selector of selectors) {
      allElements.push(...document.querySelectorAll(selector));
    }

    // Filter elements to translate
    const elementsToTranslate = [];
    const processedElements = new Set();

    for (const element of allElements) {
      // Skip if already processed or inside a processed parent
      if (processedElements.has(element)) continue;
      
      // Check if parent was already processed
      let parent = element.parentElement;
      let shouldSkip = false;
      while (parent && parent !== document.body) {
        if (processedElements.has(parent)) {
          shouldSkip = true;
          break;
        }
        parent = parent.parentElement;
      }
      if (shouldSkip) continue;

      // Get text content (excluding nested elements' text)
      const text = element.childNodes.length === 1 && element.firstChild.nodeType === Node.TEXT_NODE
        ? element.textContent.trim()
        : Array.from(element.childNodes)
            .filter(node => node.nodeType === Node.TEXT_NODE)
            .map(node => node.textContent.trim())
            .filter(text => text.length > 0)
            .join(' ');

      if (!text || text.length < 3) continue;

      // Skip already translated elements
      if (element.classList.contains('translator-wrapper')) continue;

      // Skip script and style elements
      if (element.tagName === 'SCRIPT' || element.tagName === 'STYLE' || 
          element.tagName === 'NOSCRIPT') continue;

      // Skip elements in header, nav, footer (optional - uncomment if needed)
      // if (element.closest('header, nav, footer')) continue;

      elementsToTranslate.push(element);
      processedElements.add(element);
    }

    console.log(`Found ${elementsToTranslate.length} elements to translate`);

    // Translate elements paragraph by paragraph
    for (const element of elementsToTranslate) {
      try {
        // Get the original text
        const originalText = element.textContent.trim();
        
        if (!originalText || originalText.length === 0) continue;

        // Translate the text
        const translatedText = await translateText(originalText, targetLang, sourceLang);
        
        // Store original HTML structure (to preserve images, links, etc.)
        const originalHTML = element.innerHTML;
        const hasNestedElements = element.querySelector('img, video, canvas, svg, iframe, audio') !== null;

        // Create wrapper
        const wrapper = document.createElement(element.tagName.toLowerCase());
        wrapper.className = element.className + ' translator-wrapper';
        wrapper.setAttribute('data-original', originalText);

        // Preserve original element attributes
        Array.from(element.attributes).forEach(attr => {
          if (attr.name !== 'class') {
            wrapper.setAttribute(attr.name, attr.value);
          }
        });

        // Create original text display
        const originalDiv = document.createElement('div');
        originalDiv.className = 'translator-original';
        
        if (hasNestedElements) {
          // Preserve original HTML including images and other media
          originalDiv.innerHTML = originalHTML;
        } else {
          // Just show the text
          originalDiv.textContent = originalText;
        }
        originalDiv.style.cssText = 'display: block; margin-bottom: 8px; color: #333; line-height: 1.6;';

        // Create translated text display (only text, no images)
        const translatedDiv = document.createElement('div');
        translatedDiv.className = 'translator-translated';
        translatedDiv.textContent = translatedText;
        translatedDiv.style.cssText = 'display: block; color: #667eea; font-weight: 500; border-left: 3px solid #667eea; padding-left: 12px; margin-top: 8px; line-height: 1.6;';

        // Build the wrapper content
        wrapper.appendChild(originalDiv);
        wrapper.appendChild(translatedDiv);

        // Replace element with wrapper
        element.parentNode.replaceChild(wrapper, element);
        
        translatedElements.set(wrapper, {
          original: originalText,
          translated: translatedText
        });

        // Small delay to avoid rate limiting
        await new Promise(resolve => setTimeout(resolve, 150));

      } catch (error) {
        console.error('Error translating element:', error, element);
      }
    }

    window.webTranslatorData.isTranslating = false;
    isTranslating = false;
    console.log('Translation completed');
  }

  // Clear all translations
  function clearTranslations() {
    translatedElements.forEach((value, wrapper) => {
      clearElementTranslation(wrapper);
    });
    translatedElements.clear();
    console.log('Translations cleared');
  }

  // Listen for messages from popup (register listener only once)
  if (!window.webTranslatorListenerRegistered) {
    window.webTranslatorListenerRegistered = true;
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.action === 'translate') {
        translatePage(request.targetLanguage)
          .then(() => sendResponse({ success: true }))
          .catch(error => sendResponse({ success: false, error: error.message }));
        return true; // Keep channel open for async response
      }
      
      if (request.action === 'clear') {
        clearTranslations();
        sendResponse({ success: true });
        return true;
      }
    });
  }

  // Inject CSS for translation styling (only once)
  if (!document.getElementById('web-translator-styles')) {
    const style = document.createElement('style');
    style.id = 'web-translator-styles';
    style.textContent = `
      .translator-wrapper {
        display: block;
        width: 100%;
        margin: 12px 0;
        padding: 12px;
        background: #fafafa;
        border-radius: 6px;
        border: 1px solid #e0e0e0;
      }
      .translator-original {
        display: block;
        margin-bottom: 8px;
        color: #333;
        line-height: 1.7;
        font-size: inherit;
      }
      .translator-translated {
        display: block;
        color: #667eea;
        font-weight: 500;
        border-left: 3px solid #667eea;
        padding-left: 12px;
        margin-top: 8px;
        line-height: 1.7;
        font-size: inherit;
      }
      /* Preserve images within translated content */
      .translator-wrapper img,
      .translator-wrapper video,
      .translator-wrapper canvas,
      .translator-wrapper svg {
        max-width: 100%;
        height: auto;
        margin: 8px 0;
      }
    `;
    document.head.appendChild(style);
  }
})();
