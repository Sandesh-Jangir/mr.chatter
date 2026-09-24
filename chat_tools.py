from ddgs import DDGS

def search_web(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results = 3))
    if not results:
        return "No results found."
    formatted = ""
    for r in results:
        formatted += f"Title: {r['title']}\nSnippet: {r['body']}\nURL: {r['href']}\n\n"
    return formatted