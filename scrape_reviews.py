import requests
from bs4 import BeautifulSoup
from fetch_html import fetch_html

def scrape_reviews(url):
    reviews = []
    base_url = 'https://flipkart.com'
    page = 1

    while page <= 10:  # Loop through a maximum of 10 pages for reviews
        page_url = f"{url}&page={page}"
        print(f"Scraping reviews from page {page}...")
        soup = fetch_html(page_url)  # You might need to import the fetch_html function here
        
        review_blocks = soup.find_all('div', {'class': '_27M-vq'})

        for block in review_blocks:
            sum_elem = block.find('div', {'class': 't-ZTKy'})
            if sum_elem:
                review = {'Review Description': sum_elem.text.strip()}
                reviews.append(review)

        next_button = soup.find('a', {'class': '_1LKTO3'})
        if next_button:
            url = base_url + next_button['href']  # Update the URL to the next page
            page += 1
        else:
            break  # Exit the loop if no next page is found

    return reviews
import csv

def save_to_csv(reviews, csv_file_name):
    with open(csv_file_name, "w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ['Review Description']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for review in reviews:
            writer.writerow(review)

    print(f"Scraped {len(reviews)} reviews and comments. Saved to {csv_file_name}")

