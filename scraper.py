import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time
import re
def format_title(title):
    """Remove leading non-capital alphabetical characters and capitalize the first letter."""
    title = re.sub(r'^[^A-Z]+', '', title)
    title = title.capitalize()
    return title

def extract_titles_and_values(arr):
    """Extract titles and values from a list of strings and return a list of [title, value] pairs."""
    pattern = r'([^:]+?) : ([\d.]+|yes|no|none|)'
    result = []
    
    for item in arr:
        matches = re.findall(pattern, item, re.IGNORECASE)
        for match in matches:
            title = match[0].strip()
            value = match[1].strip().lower()  # Convert to lowercase for consistency

            # Format the title
            title = format_title(title)
            
            # Default empty value to 'yes' for "Most Efficient"
            if title.lower() == 'most efficient' and value == '':
                value = 'yes'
            elif value == '':
                value = 'yes'
            else:
                # Try to convert value to float if possible, otherwise keep as string
                try:
                    value = float(value)
                except ValueError:
                    if value not in ['yes', 'no', 'none']:
                        value = value  # Keep as string if it's not "yes", "no", or "none"
                    
            result.append([title, value])
    
    return result

def filter_titles(data, titles_to_include):
    """Filter data to include only specified titles, defaulting missing titles to 'yes'."""
    filtered_data = []
    title_map = {title.lower(): title for title in titles_to_include}

    # Process each item to match the titles we're interested in
    for item in data:
        title, value = item
        title_lower = title.lower()
        if title_lower in title_map:
            filtered_data.append([title_map[title_lower], str(value)])
    
    # Ensure that all desired titles are included, even if they are missing
    for title in titles_to_include:
        if not any(item[0] == title for item in filtered_data):
            filtered_data.append([title, 'yes'])

    return filtered_data

def split_and_process_array(array):
    """Split the array into two parts, process each part, and filter the second part."""
    split_index = next((i for i, s in enumerate(array) if 'Features' in s), len(array))
    array1 = array[:split_index]
    array2 = array[split_index:]
    
    # Process both arrays
    processed_data1 = extract_titles_and_values(array1)
    processed_data2 = extract_titles_and_values(array2)
    
    # Modify the first entry of processed_data1 to omit the first word of its title
    if processed_data1:
        first_entry = processed_data1[0]
        title = first_entry[0].split(' ', 1)[-1]  # Omit the first word
        processed_data1[0] = [title, first_entry[1]]
    
    # Filter the second array to include only specific titles
    titles_to_include = ["Most Efficient", "ENERGY STAR Certified"]
    processed_data2 = filter_titles(processed_data2, titles_to_include)
    
    return processed_data1, processed_data2


def scrape_energystar_product(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the product name
        #product_name = soup.find('h1').text.strip()

        # Extract all text in elements with class "item-list"
        item_list_elements = soup.find_all(class_='item-list')

        # Select the second and the third last "item-list" elements
        if len(item_list_elements) >= 4:
            selected_elements = [item_list_elements[1], item_list_elements[-3]]
        else:
            selected_elements = []

        item_list_texts = []
        for element in selected_elements:
            item_list_texts.append(element.get_text(separator=' ', strip=True))

        # Output the extracted information
        return item_list_texts
    else:
        return None

def get_results(search_term):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    url = "https://www.energystar.gov/"
    browser = webdriver.Chrome(options=options) #options=options
    browser.get(url)
    search_box= browser.find_element(By.ID,"query")
    search_box.send_keys(search_term)
    search_box.submit()
    links = browser.find_elements(By.TAG_NAME, "h4")  # Ensure this class is correct
    #print(links)
    results = []
    for link in links:
        a_tag = link.find_element(By.TAG_NAME, "a")
        href = a_tag.get_attribute("href")
        if (href[len(href)-5:].isdigit()) : 
            return href
        
    return None

x = get_results("ELFW7738AA")
print("HELlo")
print(x)
print("WHATSUP")
y = (scrape_energystar_product(x))
a,b = split_and_process_array(y)

print("Processed Data 1:")
for item in a:
    print(item)

print("\nProcessed Data 2:")
for item in b:
    print(item)



