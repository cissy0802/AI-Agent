// Background service worker for Chrome extension

chrome.runtime.onInstalled.addListener(() => {
  console.log('Web Page Translator extension installed');
});

// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
  // This is handled by the popup, but we can add additional logic here if needed
  console.log('Extension icon clicked on tab:', tab.url);
});
