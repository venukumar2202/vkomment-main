import requests
import pandas as pd  # Add the import statement for Pandas here

# Rest of the code remains unchanged


def scrape_reviews(url):
    reviews = []
    base_url = 'https://flipkart.com'
    page = 1
    
    while page <= 10:
        page_url = f"{url}&page={page}"
        print(f"Scraping reviews from page {page}...")
        soup = fetch_html(page_url)
        
        review_blocks = soup.find_all('div', {'class': '_27M-vq'})
        
        for block in review_blocks:
            sum_elem = block.find('div', {'class': 't-ZTKy'})
            if sum_elem:
                review = {
                    'Review Description': sum_elem.text.strip()
                }
                reviews.append(review)
        
        next_button = soup.find('a', {'class': '_1LKTO3'})
        if next_button:
            url = base_url + next_button['href']  # Update the URL to the next page
            page += 1
        
    return reviews


def save_to_csv(reviews, csv_file_name):
    with open(csv_file_name, "w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ['Review Description']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for review in reviews:
            writer.writerow(review)

    print(f"Scraped {len(reviews)} reviews and comments. Saved to {csv_file_name}.")

def generate_summary_from_csv(csv_file_path, column_name):
    API_URL = "https://api-inference.huggingface.co/models/pszemraj/pegasus-x-large-book-summary"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    def read_text_from_csv(file_path, column_name):
        df = pd.read_csv(file_path)
        text_data = df[column_name].tolist()
        combined_text = ' '.join(text_data)
        return combined_text

    file_content = read_text_from_csv(csv_file_path, 'Review Description')

    output = query({"inputs": file_content})
    return output