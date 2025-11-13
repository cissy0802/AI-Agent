# Search Query Redirector

A JavaScript utility that extracts search queries from search engine URLs and redirects to alternative search engines with the same query.

## Features

- ✅ Extracts search queries from multiple search engines (Google, Bing, DuckDuckGo, Yahoo, Baidu, Yandex)
- ✅ Automatically detects the current search engine
- ✅ Constructs URLs for alternative search engines
- ✅ Works as a bookmarklet or standalone script
- ✅ Handles URL encoding/decoding automatically

## Files

- `search_query_redirect.js` - Main JavaScript library with full functionality
- `bookmarklet.js` - Minified version for use as a bookmarklet
- `example.html` - Example HTML page demonstrating usage

## Quick Start

### As a Bookmarklet

1. Open `example.html` in your browser
2. Drag the "🔍 Search on DuckDuckGo" link to your bookmarks bar
3. Navigate to a Google search results page
4. Click the bookmarklet to redirect to DuckDuckGo with the same query

### As a Script

Include the script in your HTML:

```html
<script src="search_query_redirect.js"></script>
```

Then use the functions:

```javascript
// Get the current search query
const query = getSearchQuery();
console.log('Query:', query);

// Redirect to an alternative search engine
redirectToAlternativeSearch('duckduckgo');
redirectToAlternativeSearch('bing');
```

## API Reference

### `getSearchQuery()`

Extracts the search query from the current URL.

**Returns:** `string|null` - The search query or null if not found

**Example:**
```javascript
const query = getSearchQuery();
// If on https://www.google.com/search?q=javascript+tutorial
// Returns: "javascript tutorial"
```

### `redirectToAlternativeSearch(targetEngine)`

Redirects to an alternative search engine with the same query.

**Parameters:**
- `targetEngine` (string) - The target search engine name: 'google', 'bing', 'duckduckgo', 'yahoo', 'baidu', or 'yandex'

**Example:**
```javascript
redirectToAlternativeSearch('duckduckgo');
```

### `constructSearchUrl(query, targetEngine)`

Constructs a search URL for the target engine without redirecting.

**Parameters:**
- `query` (string) - The search query
- `targetEngine` (string) - The target search engine name

**Returns:** `string|null` - The constructed URL or null if invalid

**Example:**
```javascript
const url = constructSearchUrl('javascript tutorial', 'bing');
// Returns: "https://www.bing.com/search?q=javascript+tutorial"
```

### `extractSearchQuery(queryParam)`

Extracts a query parameter value from the current URL.

**Parameters:**
- `queryParam` (string) - The query parameter name (default: 'q')

**Returns:** `string|null` - The decoded query value or null if not found

### `detectSearchEngine()`

Detects the current search engine based on the hostname.

**Returns:** `string|null` - The search engine name or null if not recognized

### `getAlternativeEngines()`

Gets a list of available alternative search engines (excluding the current one).

**Returns:** `Array<string>` - Array of search engine names

## Supported Search Engines

| Engine | Query Parameter | Base URL |
|--------|----------------|----------|
| Google | `q` | https://www.google.com/search |
| Bing | `q` | https://www.bing.com/search |
| DuckDuckGo | `q` | https://duckduckgo.com/ |
| Yahoo | `p` | https://search.yahoo.com/search |
| Baidu | `wd` | https://www.baidu.com/s |
| Yandex | `text` | https://yandex.com/search/ |

## Example Use Cases

### 1. Browser Extension

Use this code in a browser extension to add a "Search on [Alternative Engine]" button to search results pages.

### 2. Custom Search Tool

Build a custom search interface that allows users to easily switch between search engines.

### 3. Privacy Tool

Create a privacy-focused tool that redirects searches from tracking-heavy engines to privacy-focused ones.

## Browser Compatibility

- Modern browsers with ES6+ support
- Requires `URLSearchParams` API (supported in all modern browsers)
- Tested on Chrome, Firefox, Edge, and Safari

## License

This code is provided as-is for educational and personal use.

