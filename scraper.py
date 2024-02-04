import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_images(url, output_folder):
    # path to Firefox profile
    firefox_profile_path = '/home/marwa254/snap/firefox/common/.mozilla/firefox/sgbnj5o8.Okumu'
    
    # Set up Firefox options with the specified profile
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument(f'--profile={firefox_profile_path}')

    # Use Selenium with Firefox
    driver = webdriver.Firefox(options=firefox_options)
    driver.get(url)
    page_source = driver.page_source
    driver.quit()

    # Parse the HTML content
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')

    # Download each image
    for img_tag in img_tags:
        # Check if 'src' attribute exists in the current image tag
        if 'src' in img_tag.attrs:
            img_url = urljoin(url, img_tag['src'])
            img_name = os.path.join(output_folder, os.path.basename(img_url))

            # Download the image
            img_data = requests.get(img_url).content
            with open(img_name, 'wb') as img_file:
                img_file.write(img_data)

            print(f"Downloaded: {img_name}")
        else:
            print("Image tag does not have 'src' attribute.")

if __name__ == "__main__":
    # Set the URL of the website with skin images
    website_url = "https://dermnetnz.org/#gsc.tab=1&gsc.q=skin%20lesions"

    # Set the folder where you want to save the images
    output_folder = "./data"

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Call the function to download images
    download_images(website_url, output_folder)
