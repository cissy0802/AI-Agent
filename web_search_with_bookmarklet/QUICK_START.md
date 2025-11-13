# Quick Start Guide - How to Run the Code

## ⚡ No Server Required!

**The bookmarklet works completely offline and doesn't need any server!** Once you save it to your bookmarks, you can use it anywhere, anytime.

---

## Method 1: Bookmarklet (Recommended - No Server Needed!)

**This is the best method - works offline, no server required!**

1. **Open the setup file:**
   - Navigate to: `AI-Agent/web_search_with_bookmarklet/setup_bookmarklet.html`
   - Double-click to open in your browser (works with `file://` protocol)
   - Or use: `example.html` (same thing)

2. **Show your bookmarks bar:**
   - Press `Ctrl+Shift+B` (Windows) or `Cmd+Shift+B` (Mac)
   - Or right-click the top bar → Check "Bookmarks bar"

3. **Drag the bookmarklet:**
   - Drag the green "🔍 Search on DuckDuckGo" button to your bookmarks bar
   - Done! The bookmarklet is now saved and works forever (no server needed)

4. **Use it:**
   - Go to Google and search for something
   - Click the bookmarklet in your bookmarks bar
   - You'll be redirected to DuckDuckGo with the same query!

**✅ Once saved, this works completely offline - no server, no internet connection to the code needed!**

---

## Method 2: Using Browser Console (No Server Needed)

1. **Open a search results page:**
   - Go to Google: https://www.google.com/search?q=test+query
   - Or any other supported search engine

2. **Open Developer Tools:**
   - Press `F12` (or `Ctrl+Shift+I` on Windows, `Cmd+Option+I` on Mac)
   - Click on the "Console" tab

3. **Load and run the script:**
   ```javascript
   // Option A: Copy and paste the entire search_query_redirect.js file content into console
   // Then run:
   redirectToAlternativeSearch('duckduckgo');
   
   // Option B: Or just test individual functions:
   getSearchQuery();  // See what query is extracted
   ```

## Method 3: Open HTML File Directly (No Server Needed)

1. **Open the example file:**
   - Navigate to: `AI-Agent/web_search_with_bookmarklet/example.html`
   - Right-click → "Open with" → Your browser
   - Works with `file://` protocol (no server needed!)

2. **The bookmarklet link will work** - just drag it to your bookmarks bar

**Note:** Some browsers may show security warnings when opening HTML files directly. This is normal - the bookmarklet itself is safe.

---

## Method 4: Include in Your Own HTML Page (No Server Needed)

1. **Create a simple HTML file:**
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>My Search Redirector</title>
   </head>
   <body>
       <h1>Search Redirector</h1>
       <button onclick="redirectToAlternativeSearch('duckduckgo')">
           Search on DuckDuckGo
       </button>
       <script src="search_query_redirect.js"></script>
   </body>
   </html>
   ```

2. **Save it in the same folder as `search_query_redirect.js`**

3. **Open it directly in your browser** (works with `file://` protocol)

---

## Method 5: Using a Local Web Server (Optional - Only for Development)

If you want to test properly (especially if you encounter CORS issues):

1. **Open PowerShell or Command Prompt**

2. **Navigate to the folder:**
   ```powershell
   cd "C:\Users\cheng\Git\AI-Agent\web_search_with_bookmarklet"
   ```

3. **Start a simple HTTP server:**

   **Option A - Using Python (if installed):**
   ```powershell
   python -m http.server 8000
   ```

   **Option B - Using Node.js (if installed):**
   ```powershell
   npx http-server -p 8000
   ```

4. **Open in browser:**
   - Go to: http://localhost:8000/example.html

## Method 6: Create a Bookmarklet Manually (No Server Needed)

1. **Copy the bookmarklet code:**
   - Open `bookmarklet.js`
   - Copy the entire content (it's all on one line)

2. **Create a new bookmark:**
   - In your browser, create a new bookmark
   - Name it: "Search on DuckDuckGo"
   - For the URL, paste the code from `bookmarklet.js`

3. **Use it:**
   - Go to any search results page
   - Click the bookmarklet
   - You'll be redirected!

## Testing the Code

### Test 1: Extract Query
1. Go to: https://www.google.com/search?q=hello+world
2. Open browser console (F12)
3. Paste the script content
4. Run: `getSearchQuery()`
5. Should output: `"hello world"`

### Test 2: Redirect
1. Go to: https://www.google.com/search?q=javascript
2. Open browser console (F12)
3. Paste the script content
4. Run: `redirectToAlternativeSearch('duckduckgo')`
5. Should redirect to DuckDuckGo with the same query

### Test 3: Construct URL
1. In console, run:
   ```javascript
   constructSearchUrl('test query', 'bing')
   ```
2. Should return: `"https://www.bing.com/search?q=test+query"`

## Troubleshooting

**Problem:** "No search query found"
- **Solution:** Make sure you're on a search results page with a query parameter in the URL

**Problem:** Script doesn't work
- **Solution:** Make sure you're running it on a page with a search query in the URL, or include the script in an HTML page

**Problem:** CORS errors
- **Solution:** Use a local web server (Method 4) instead of opening files directly

**Problem:** Bookmarklet doesn't work
- **Solution:** Make sure you copied the entire bookmarklet code (it should start with `javascript:(function(){`)

## Quick Test Right Now

1. Open your browser
2. Go to: https://www.google.com/search?q=test
3. Press F12 to open console
4. Copy and paste this:
   ```javascript
   const query = new URLSearchParams(window.location.search).get('q');
   console.log('Query:', query);
   window.location.href = `https://duckduckgo.com/?q=${encodeURIComponent(query)}`;
   ```
5. Press Enter - you should be redirected!

