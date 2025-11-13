/**
 * Search Query Redirector
 * Extracts search query from current URL and redirects to alternative search engine
 */

// Mapping of search engines and their query parameter names
const SEARCH_ENGINES = {
    google: { param: 'q', baseUrl: 'https://www.google.com/search' },
    bing: { param: 'q', baseUrl: 'https://www.bing.com/search' },
    duckduckgo: { param: 'q', baseUrl: 'https://duckduckgo.com/' },
    yahoo: { param: 'p', baseUrl: 'https://search.yahoo.com/search' },
    baidu: { param: 'wd', baseUrl: 'https://www.baidu.com/s' },
    yandex: { param: 'text', baseUrl: 'https://yandex.com/search/' }
};

/**
 * Extracts the search query from the current URL
 * @param {string} queryParam - The query parameter name (e.g., 'q', 'p', 'wd')
 * @returns {string|null} - The decoded search query or null if not found
 */
function extractSearchQuery(queryParam = 'q') {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get(queryParam);
    return query ? decodeURIComponent(query) : null;
}

/**
 * Detects the current search engine based on the hostname
 * @returns {string|null} - The search engine name or null if not recognized
 */
function detectSearchEngine() {
    const hostname = window.location.hostname.toLowerCase();
    
    if (hostname.includes('google')) return 'google';
    if (hostname.includes('bing')) return 'bing';
    if (hostname.includes('duckduckgo')) return 'duckduckgo';
    if (hostname.includes('yahoo')) return 'yahoo';
    if (hostname.includes('baidu')) return 'baidu';
    if (hostname.includes('yandex')) return 'yandex';
    
    return null;
}

/**
 * Constructs a search URL for the target search engine
 * @param {string} query - The search query
 * @param {string} targetEngine - The target search engine name
 * @returns {string|null} - The constructed URL or null if invalid
 */
function constructSearchUrl(query, targetEngine) {
    if (!query || !targetEngine) return null;
    
    const engine = SEARCH_ENGINES[targetEngine.toLowerCase()];
    if (!engine) return null;
    
    const encodedQuery = encodeURIComponent(query);
    
    // DuckDuckGo uses a different URL format
    if (targetEngine.toLowerCase() === 'duckduckgo') {
        return `${engine.baseUrl}?q=${encodedQuery}`;
    }
    
    return `${engine.baseUrl}?${engine.param}=${encodedQuery}`;
}

/**
 * Redirects to an alternative search engine with the same query
 * @param {string} targetEngine - The target search engine name
 */
function redirectToAlternativeSearch(targetEngine = 'duckduckgo') {
    // Try to detect current search engine
    const currentEngine = detectSearchEngine();
    let query = null;
    
    if (currentEngine) {
        // Use the known query parameter for the current engine
        const currentEngineConfig = SEARCH_ENGINES[currentEngine];
        query = extractSearchQuery(currentEngineConfig.param);
    } else {
        // Fallback: try common query parameters
        query = extractSearchQuery('q') || 
                extractSearchQuery('p') || 
                extractSearchQuery('wd') || 
                extractSearchQuery('text');
    }
    
    if (!query) {
        console.error('No search query found in URL');
        alert('No search query found in the current URL.');
        return;
    }
    
    const newUrl = constructSearchUrl(query, targetEngine);
    
    if (newUrl) {
        console.log(`Redirecting to ${targetEngine} with query: ${query}`);
        window.location.href = newUrl;
    } else {
        console.error(`Invalid target engine: ${targetEngine}`);
        alert(`Invalid target search engine: ${targetEngine}`);
    }
}

/**
 * Gets the search query from URL (for use in other contexts)
 * @returns {string|null} - The search query or null if not found
 */
function getSearchQuery() {
    const currentEngine = detectSearchEngine();
    
    if (currentEngine) {
        const currentEngineConfig = SEARCH_ENGINES[currentEngine];
        return extractSearchQuery(currentEngineConfig.param);
    }
    
    // Fallback: try common query parameters
    return extractSearchQuery('q') || 
           extractSearchQuery('p') || 
           extractSearchQuery('wd') || 
           extractSearchQuery('text');
}

/**
 * Gets available alternative search engines (excluding current one)
 * @returns {Array<string>} - Array of available search engine names
 */
function getAlternativeEngines() {
    const currentEngine = detectSearchEngine();
    const engines = Object.keys(SEARCH_ENGINES);
    
    if (currentEngine) {
        return engines.filter(engine => engine !== currentEngine);
    }
    
    return engines;
}

// Example usage:
// redirectToAlternativeSearch('duckduckgo');  // Redirect to DuckDuckGo
// redirectToAlternativeSearch('bing');         // Redirect to Bing
// const query = getSearchQuery();              // Just get the query without redirecting

// Export for use in modules (if using ES6 modules)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        extractSearchQuery,
        detectSearchEngine,
        constructSearchUrl,
        redirectToAlternativeSearch,
        getSearchQuery,
        getAlternativeEngines,
        SEARCH_ENGINES
    };
}

