import requests
from bs4 import BeautifulSoup

def google_search(query, num_results=5):
    """
    Perform a Google search and return summaries of the top results.

    Parameters:
        query (str): The search query.
        num_results (int): Number of results to fetch summaries for.

    Returns:
        list: A list of dictionaries with titles, links, and summaries.
    """
    # Prepare the Google search URL
    query = query.replace(' ', '+')
    url = f"https://www.google.com/search?q={query}&num={num_results}"

    # Add headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Send the GET request
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"Failed to fetch results. Status code: {response.status_code}"

    # Parse the HTML response
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract search result elements
    results = []
    for result in soup.select('.tF2Cxc')[:num_results]:
        title = result.select_one('.DKV0Md').text
        link = result.select_one('.yuRUbf a')['href']
        snippet = result.select_one('.IsZvec').text if result.select_one('.IsZvec') else 'No summary available.'
        results.append({'title': title, 'link': link, 'snippet': snippet})

    # Return results as a list of dictionaries
    return results

def ans(search_query,num_results=5):
    search_results = google_search(search_query, num_results)
    ans = ""
    for i, result in enumerate(search_results, 1):
        ans += "\n"+f"Result {i}:"
        ans += "\n"+f"Title: {result['title']}"
        ans += "\n"+f"Link: {result['link']}"
        ans += "\n"+ f"Summary: {result['snippet']}"
        ans += "\n"

    return ans

if __name__ == "__main__":
    while True:
        print(ans(input("Search something: "),))