from flask import Flask, jsonify
from fetch_html import fetch_html
from extract_product_info import get_product_info
from scrape_reviews import scrape_reviews, save_to_csv
from generate_summary import generate_summary_from_csv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/execute_main_script', methods=['GET'])
def execute_main_script():
    url = 'https://www.flipkart.com/realme-c51-mint-green-64-gb/p/itm0e93bcb87927f?pid=MOBGSQGGC7NY4PXC&lid=LSTMOBGSQGGC7NY4PXCO7WY2Y&marketplace=FLIPKART&store=tyy%2F4io&spotlightTagId=BestsellerId_tyy%2F4io&srno=b_1_1&otracker=browse&fm=organic&iid=846b767b-2c4f-4cfc-adb1-785494f24499.MOBGSQGGC7NY4PXC.SEARCH&ppt=browse&ppn=browse&ssid=aegxunapio0000001698431916885'

    # Fetch product information
    soup = fetch_html(url)
    
    if soup:
        title, image_links, price, rating, num_reviews, description = get_product_info(soup)

        if num_reviews != "Number of Reviews not found":
            review_url = None
            elements = soup.find_all(class_="_3UAT2v _16PBlm")[:3]

            for element in elements:
                parent_a = element.find_parent('a')
                if parent_a and 'href' in parent_a.attrs:
                    href = parent_a['href']
                    review_url = 'https://flipkart.com' + href
                    break

            if review_url:
                reviews = scrape_reviews(review_url)
                if reviews:
                    csv_file_name = "product_reviews.csv"
                    save_to_csv(reviews, csv_file_name)
                    
                    summary = generate_summary_from_csv(csv_file_name, 'Review Description')
                    summary_text = summary[0]['summary_text'] if (summary and len(summary) > 0 and 'summary_text' in summary[0]) else "Summary not generated"
                    
                    product_data = {
                        "Title": title,
                        "Image Links": image_links,
                        "Product Price": price,
                        "Product Rating": rating,
                        "Number of Reviews": num_reviews,
                        "Product Description": description,
                        "Review Summary": summary_text
                    }
                    
                    return jsonify(product_data)
                else:
                    return "No reviews found or an error occurred."
            else:
                return "Review URL not found."
        else:
            return "No reviews available for this product."
    else:
        return "Failed to retrieve product information."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
