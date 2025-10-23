import os

from agents import function_tool
from tavily import TavilyClient

try:
    tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
except KeyError:
    print("FATAL: TAVILY_API_KEY not found in .env file.")
    tavily_client = None


@function_tool
def scan_webpage_tool(urls: list[str]) -> str:
    """
    Fetches the full, clean content of a webpages using Tavily's 'extract' API.

    Args:
        urls: The URLs of the webpages to extract.

    Returns:
        The full, raw content of the webpages as a string.
    """
    if not tavily_client:
        return "Error: Tavily Client is not initialized. Missing TAVILY_API_KEY."

    web_contents = []
    for url in urls:
        print(f"[Tavily Extract Tool] Extracting: {url}")
    try:
        response = tavily_client.extract(url, format="markdown")
        if response and response.get("results"):
            results = response.get("results")

            web_contents = []

            for res in results:
                content = f"\n--- Content from {res.get('url')} ---\nTitle: {res.get('title')}\nRaw Content:\n{res.get('raw_content')}\n"
                web_contents.append(content)

            contents = "\n################################\n".join(web_contents)

            return contents

        elif response and response.get("failed_results"):
            print(f"[Tavily Extract Tool] API Error: {response['failed_results']}")
            return f"Tavily failed to extract content. Error: {response['failed_results']}"
        else:
            return f"Tavily returned no content or an unexpected response for {url}."

    except Exception as e:
        print(f"[Tavily Extract Tool] General Error: {e}")
        return f"A general error occurred: {e}"
