from bs4 import BeautifulSoup

def get_product_info(soup):
    title_element = soup.find('span', {'class': 'B_NuCI'})
    title = title_element.get_text().strip() if title_element else "Title not found"

    price_element = soup.find('div', {'class': '_30jeq3'})
    price = price_element.get_text().strip() if price_element else "Price not found"

    rating_element = soup.find('div', {'class': '_3LWZlK'})
    rating = rating_element.text if rating_element else "Rating not found"

    num_reviews_element = soup.find('span', {'class': '_2_R_DZ'})
    num_reviews = num_reviews_element.text if num_reviews_element else "Number of Reviews not found"

    description_element = soup.find('div', {'class': '_1mXcCf'})
    description = description_element.get_text().strip() if description_element else "Description not found"

    image_links = []
    image_elements = soup.find_all('img', {'class': '_396cs4'})
    for img in image_elements:
        if 'src' in img.attrs:
            image_links.append(img['src'])

    return title, image_links, price, rating, num_reviews, description
