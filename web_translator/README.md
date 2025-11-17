# Web Page Translator - Chrome Extension

A Chrome extension that translates web pages paragraph by paragraph, showing the original text and translated text together while preserving images and other media content.

## Features

- 🌐 **Multi-language Support**: Translate to 40+ languages
- 📝 **Paragraph-by-Paragraph Translation**: Each paragraph shows original and translated text side by side
- 🖼️ **Preserves Media**: Images, videos, and other media content remain unchanged
- 🎨 **Clean UI**: Beautiful popup interface with language dropdown
- 💾 **Remember Preferences**: Saves your preferred target language
- ⚡ **Fast Translation**: Uses Google Translate API for quick translations

## Installation

### Method 1: Load Unpacked Extension (For Development)

1. **Download/Clone** this repository to your computer

2. **Open Chrome Extensions Page**:
   - Go to `chrome://extensions/` in your Chrome browser
   - Or navigate: Menu (⋮) → Extensions → Manage Extensions

3. **Enable Developer Mode**:
   - Toggle the "Developer mode" switch in the top-right corner

4. **Load the Extension**:
   - Click "Load unpacked"
   - Navigate to the `web_translator` folder
   - Select the folder and click "Select Folder"

5. **Extension is Ready**:
   - You should see the "Web Page Translator" extension in your extensions list
   - The extension icon should appear in your Chrome toolbar

### Method 2: Create Icon Files (Optional)

The extension references icon files that you'll need to create or add:

1. Create icon files in the `icons/` folder:
   - `icon16.png` (16x16 pixels)
   - `icon48.png` (48x48 pixels)
   - `icon128.png` (128x128 pixels)

2. You can use any image editor or online tool to create these icons. A simple colored square with a "T" or globe symbol works well.

**Note**: If you don't create the icon files, Chrome will show a default icon, and the extension will still work.

## Usage

1. **Open any webpage** you want to translate

2. **Click the extension icon** in your Chrome toolbar

3. **Select a target language** from the dropdown menu

4. **Click "Translate Page"** button

5. **View the translation**:
   - Each paragraph will show the original text (in black)
   - Followed by the translated text (in purple with left border)
   - Images and other media remain in their original positions

6. **Clear translation**: Click "Clear Translation" to restore the original page

## Supported Languages

The extension supports translation to 40+ languages including:

- Spanish, French, German, Italian, Portuguese
- Russian, Japanese, Korean, Chinese (Simplified/Traditional)
- Arabic, Hindi, Dutch, Polish, Turkish, Vietnamese
- And many more...

See the dropdown in the popup for the complete list.

## How It Works

1. **Content Script Injection**: The extension injects a content script into web pages
2. **Text Extraction**: Identifies paragraph and block-level text elements
3. **Translation**: Uses Google Translate API to translate each paragraph
4. **Display**: Shows original and translated text together in a styled container
5. **Media Preservation**: Keeps images, videos, and other media in their original positions

## Technical Details

- **Manifest Version**: 3 (latest Chrome extension format)
- **Translation API**: Google Translate Web API (free tier)
- **Content Scripts**: Injected on page load, runs on demand
- **Storage**: Uses Chrome Storage API to remember language preferences

## File Structure

```
web_translator/
├── manifest.json          # Extension configuration
├── popup.html            # Popup UI
├── popup.css             # Popup styling
├── popup.js              # Popup logic
├── content.js            # Content script (injected into pages)
├── background.js         # Background service worker
├── icons/                # Extension icons
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
└── README.md             # This file
```

## Known Limitations

- Translation speed depends on network connection
- Very long pages may take some time to translate
- Some websites with complex JavaScript may need page reload after translation
- Rate limiting may apply with Google Translate API (free tier)

## Troubleshooting

**Extension not working?**
- Make sure you've loaded the extension in developer mode
- Check the browser console (F12) for any error messages
- Try reloading the webpage after installing the extension

**Translation not showing?**
- Check if the page has text content
- Some pages load content dynamically - try scrolling or waiting a bit
- Click "Translate Page" again if it didn't work the first time

**Icons missing?**
- The extension will work without custom icons
- Create PNG files in the `icons/` folder if you want custom icons

## Privacy

- This extension uses Google Translate API to translate text
- Text is sent to Google's servers for translation
- No other data is collected or stored
- The extension only accesses pages when you click "Translate Page"

## License

This project is open source and available for personal and commercial use.

## Contributing

Feel free to fork, modify, and improve this extension. Suggestions and pull requests are welcome!

## Support

If you encounter any issues or have questions, please check the browser console for error messages and ensure all files are in the correct locations.
