import requests

LANGSEARCH_API_KEY = "sk-b55b99ffd3984587ad824fd09c4ea6b2"
LANGSEARCH_ENDPOINT = "https://api.langsearch.com/v1/web-search"

def run_langsearch(query, max_results=3, include_metadata=False):
    """
    Uses LangSearch API to fetch semantically ranked web results.
    Returns a list of formatted strings or dicts for agent consumption.
    """
    headers = {
        "Authorization": f"Bearer {LANGSEARCH_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "query": query,
        "summary": True,
        "count": max_results,
        "timeRange": "noLimit"
    }

    try:
        response = requests.post(
            LANGSEARCH_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return [f"LangSearch error: {response.status_code} - {response.text}"]

        data = response.json()
        results = data.get("webPages", {}).get("value", [])

        if not results:
            return [f"No useful results found for: {query}"]

        if include_metadata:
            return [
                {
                    "title": r.get("name", "Untitled"),
                    "summary": r.get("summary", r.get("snippet", "No summary available")),
                    "url": r.get("url", "No URL")
                }
                for r in results
            ]

        return [
            f"🔍 **{r['name']}**\n{r.get('summary', r.get('snippet', 'No summary available'))}"
            for r in results
        ]

    except Exception as e:
        return [f"LangSearch error: {str(e)}"]
