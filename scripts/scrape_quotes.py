import requests
from bs4 import BeautifulSoup
# database.py와 같은 상위 폴더에 있으므로 경로를 추가해야 할 수 있습니다.
# 하지만 cron이나 pytest 실행 시 PYTHONPATH를 설정하면 더 깔끔합니다。
# 우선은 상대 경로로 시도합니다。
import sys
import os
# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_engine, save_quote

URL = "http://quotes.toscrape.com"

def run_scraping_task():
    """
    "http://quotes.toscrape.com"에서 명언을 스크레이핑하여
    데이터베이스에 저장하는 핵심 로직。
    """
    engine = get_engine()
    response = requests.get(URL)
    response.raise_for_status()  # Raise an exception for bad status codes
    soup = BeautifulSoup(response.content, 'html.parser')
    
    quotes = soup.find_all('div', class_='quote')
    
    saved_count = 0
    for quote in quotes:
        text = quote.find('span', class_='text').get_text().strip()
        author = quote.find('small', class_='author').get_text().strip()
        if save_quote(engine, text, author):
            print(f'Saved: "{text}" by {author}')
            saved_count += 1
        else:
            print(f'Already exists: "{text}" by {author}')
    
    print(f"Scraping finished. Saved {saved_count} new quotes.")
    return saved_count

if __name__ == '__main__':
    run_scraping_task()