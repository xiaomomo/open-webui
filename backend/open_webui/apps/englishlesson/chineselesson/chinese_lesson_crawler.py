import requests
from bs4 import BeautifulSoup
import time
import json

class GrimmStoryCrawler:
    def __init__(self):
        self.base_url = "https://www.grimmstories.com"
        self.stories = []

    def get_story_links(self, page=1):
        url = f"{self.base_url}/zh/grimm_tonghua/index?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all story links on the page
        story_links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and '/zh/grimm_tonghua/' in href and 'index' not in href:
                # Check if the href is already a full URL
                if href.startswith('http'):
                    story_links.append(href)
                else:
                    # Remove leading slash if present to avoid double slashes
                    href = href.lstrip('/')
                    story_links.append(f"{self.base_url}/{href}")
        return story_links

    def get_story_content(self, url):
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        # Explicitly set the encoding to UTF-8
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract story title and content using the correct selectors
        title = soup.find('h2', class_='title').text.strip() if soup.find('h2', class_='title') else ""
        content = ""
        story_div = soup.find('div', class_='s')
        if story_div:
            content = story_div.text.strip()
        
        return {
            "title": title,
            "content": content,
            "url": url
        }

    def crawl_stories(self, max_pages=10):
        for page in range(1, max_pages + 1):
            print(f"Crawling page {page}...")
            story_links = self.get_story_links(page)
            
            for link in story_links:
                try:
                    story = self.get_story_content(link)
                    self.stories.append(story)
                    print(f"Crawled: {story}")
                    # Be nice to the server
                    time.sleep(1)
                except Exception as e:
                    print(f"Error crawling {link}: {str(e)}")

    def save_stories(self, filename="grimm_stories.json"):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.stories, f, ensure_ascii=False, indent=2)

def main():
    crawler = GrimmStoryCrawler()
    crawler.crawl_stories()
    crawler.save_stories()

if __name__ == "__main__":
    main()
