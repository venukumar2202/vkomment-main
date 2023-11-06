import random
import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    with open('user-agents.txt', 'r') as file:
        user_agents = file.read().splitlines()

    selected_user_agent_index = random.randint(0, len(user_agents) - 1)
    selected_user_agent = user_agents[selected_user_agent_index]
    print(f"User Agent Number: {selected_user_agent_index}")
    
    headers = {
        'User-Agent': selected_user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Success!")
    else:
        print("Failed to retrieve the product page.")
        exit()

    return BeautifulSoup(response.content, "html.parser")
