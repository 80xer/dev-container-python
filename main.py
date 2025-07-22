import requests
from bs4 import BeautifulSoup
from database import create_table, save_quote

URL = "http://quotes.toscrape.com"

def main():
    create_table()
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    quotes = soup.find_all('div', class_='quote')
    
    for quote in quotes:
        text = quote.find('span', class_='text').get_text().strip()
        author = quote.find('small', class_='author').get_text().strip()
        if save_quote(text, author):
            print(f'Saved: "{text}" by {author}')
        else:
            print(f'Already exists: "{text}" by {author}')

if __name__ == '__main__':
    main()