/**
 * Bookmarklet version - minified for use as a bookmark
 * Copy this code and create a bookmark with it as the URL
 * 
 * Usage: When on a search results page (e.g., Google), click the bookmarklet
 * to redirect to DuckDuckGo with the same search query
 */

javascript:(function(){
    const engines={google:{param:'q',url:'https://www.google.com/search'},bing:{param:'q',url:'https://www.bing.com/search'},duckduckgo:{param:'q',url:'https://duckduckgo.com/'},yahoo:{param:'p',url:'https://search.yahoo.com/search'}};
    const host=window.location.hostname.toLowerCase();
    let engine=null;
    if(host.includes('google'))engine='google';
    else if(host.includes('bing'))engine='bing';
    else if(host.includes('duckduckgo'))engine='duckduckgo';
    else if(host.includes('yahoo'))engine='yahoo';
    const param=engine?engines[engine].param:'q';
    const query=new URLSearchParams(window.location.search).get(param);
    if(!query){alert('No search query found');return;}
    const target='duckduckgo';
    const targetConfig=engines[target];
    const newUrl=target==='duckduckgo'?`${targetConfig.url}?q=${encodeURIComponent(query)}`:`${targetConfig.url}?${targetConfig.param}=${encodeURIComponent(query)}`;
    window.location.href=newUrl;
})();

