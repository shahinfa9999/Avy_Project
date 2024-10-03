import requests
from bs4 import BeautifulSoup
import re
import os
def clear_file_if_not_empty(file_path):
    # Check if the file exists
    if os.path.isfile(file_path):
        # Check if the file is not empty
        if os.path.getsize(file_path) > 0:
            with open(file_path, 'w') as file:
                # Clear the file by opening it in write mode
                file.truncate()  # This line is actually optional as 'w' mode clears the file

# URL of the point forecasts page
url = "https://looper.avalanche.state.co.us/weather/ptfcst-new.php?model=nam&nfcst=24"

# Define the base URL
base_url = "https://looper.avalanche.state.co.us/weather/"

# Make the HTTP request to get the page
response = requests.get(url)

# Parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find all <a> tags with the onclick attribute (for images) and <a> tags linking to .txt files
anchors = soup.find_all('a', href=True)

# Initialize lists to store the URLs and data
txt_files_data = []
image_urls = []

# Create directories for storing images and text files
if not os.path.exists('downloaded_images'):
    os.makedirs('downloaded_images')
if not os.path.exists('downloaded_txt_files'):
    os.makedirs('downloaded_txt_files')
clear_file_if_not_empty('downloaded_images')
clear_file_if_not_empty('downloaded_txt_files')

# Process all anchors
for anchor in anchors:
    href_attr = anchor['href']
    print(href_attr)

    # Check if it's a .txt file
    if '.txt' in href_attr:
        txt_url = base_url + href_attr
        print(f"Downloading {txt_url}")
        
        # Download the .txt file
        txt_response = requests.get(txt_url)
        txt_filename = os.path.join('downloaded_txt_files', os.path.basename(txt_url))
        
        # Save the file locally
        with open(txt_filename, 'w') as txt_file:
            txt_file.write(txt_response.text)
        
        # Add the file content to a list
        txt_files_data.append(txt_response.text)
    
    # Check if it's an image linked via JavaScript onclick
    if 'onclick' in anchor.attrs:
        onclick_attr = anchor['onclick']
        
        # Use regex to capture the URL and other parameters inside new_window()
        match = re.search(r"new_window\('([^']+)',\s*'([^']+)',\s*'([^']+)',\s*'([^']+)'\)", onclick_attr)
        
        if match:
            relative_url = match.group(1)  # First group is the URL
            full_url = base_url + relative_url

            # Store the image URL for later use
            image_urls.append(full_url)

            # Download the image
            image_response = requests.get(full_url)
            image_filename = os.path.join('downloaded_images', os.path.basename(full_url))
            
            # Save the image
            with open(image_filename, 'wb') as img_file:
                img_file.write(image_response.content)
            
            print(f"Saved image: {image_filename}")

# At this point, `txt_files_data` contains the contents of all .txt files
# and the images are saved in the 'downloaded_images' directory.
