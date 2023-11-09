from flask import Flask, jsonify, request
from fetch_html import fetch_html  # Import your defined functions
from extract_product_info import get_product_info
from scrape_reviews import scrape_reviews, save_to_csv
from generate_summary import generate_summary_from_csv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/execute_main_script": {"origins": "*"}})  # All origins are allowed here

@app.route('/execute_main_script', methods=['GET'])
def execute_main_script():
    url = request.args.get('url')  # Get the URL from the query parameter

    # Logic to fetch product information
    soup = fetch_html(url)  # Function to fetch HTML from the provided URL
    
    if soup:
        # Logic to extract information from 'soup'
        title, image_links, price, rating, num_reviews, description = get_product_info(soup)

        if num_reviews != "Number of Reviews not found":
            # Logic to fetch and process reviews
            review_url = "https://flipkart.com/sample-review"  # Replace this with the URL of reviews
            reviews = [{"review_id": 1, "review_text": "Great product!"}]  # Replace this with actual reviews
            csv_file_name = "product_reviews.csv"  # Your CSV file name

            # Generate summary from CSV
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
            return "No reviews available for this product."
    else:
        return "Failed to retrieve product information."

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://your-frontend-domain.com')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)  # Change the port as per your requirements
