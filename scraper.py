from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import os
import time
from webdriver_manager.chrome import ChromeDriverManager

# Configure WebDriver
def init_driver():
    chrome_options = Options() # Initialize Chrome options
    chrome_options.add_argument("--headless")  # Run headless mode
    service = Service(ChromeDriverManager().install()) # Install ChromeDriver
    return webdriver.Chrome(service=service, options=chrome_options) # Initialize Chrome driver

# Convert RGB to HEX
def rgb_to_hex(rgb):
    rgb = [int(x) for x in rgb[4:-1].split(",")] # Convert RGB string to list of integers
    return '#%02x%02x%02x' % tuple(rgb) # Convert RGB to HEX

# Collect palette data from multiple pages
def collect_palette_data(driver, base_url, num_pages):
    data = [] # Initialize data list
    for page in range(1, num_pages + 1):
        try:
            driver.get(f"{base_url}/?page={page}") # Load the page
            palette_elements = driver.find_elements(By.CLASS_NAME, "palettecontainerlist") # Find palette elements on the page by class name
            print(f"Found {len(palette_elements)} palettes on page {page}.")
            for palette in palette_elements:
                print(f"Extracting palette data {palette_elements.index(palette) + 1}...")
                try:
                    anchor = palette.find_element(By.TAG_NAME, "a") # Find the anchor tag within the palette element to extract the ID and name
                    id = anchor.get_attribute("href").split("/")[-1] # Extract the ID from the href attribute
                    palette_name = anchor.get_attribute("title").split(" ") # Extract the palette name from the title attribute
                    palette_name = " ".join(palette_name[2:]) # Join the palette name
                    
                    color_elements = palette.find_elements(By.CLASS_NAME, "palettecolordiv") # Find color elements within the palette element
                    colors_rgb = [] # Initialize list to store RGB colors
                    colors_hex = [] # Initialize list to store HEX colors
                    
                    for color_elem in color_elements:
                        style = color_elem.get_attribute("style") # Get the style attribute of the color element
                        if style and "background-color:" in style:
                            rgb = style.split("background-color: ")[1].split(";")[0] # Extract the RGB value from the style attribute
                            colors_rgb.append(rgb) # Append the RGB value to the list
                            colors_hex.append(rgb_to_hex(rgb)) # Convert RGB to HEX and append to the list
                    
                    print(f"Palette Name: {palette_name}" + "\n" + f"Colors: {colors_rgb}" + "\n" + f"HEX: {colors_hex}")
                    data.append({
                        "ID": id,
                        "Name": palette_name,
                        "HEX": colors_hex,
                        "RGB": colors_rgb
                    }) # Append the palette data to the list
                except NoSuchElementException as e:
                    print(f"Palette elements not found within the container. Error: {e}")
                except IndexError as e:
                    print(f"Error extracting background color. Error: {e}")
        except NoSuchElementException:
            print(f"No palettes found on page {page}.")
        except TimeoutException:
            print(f"Timeout occurred on page {page}.")
        time.sleep(1)  # Delay to prevent being blocked
    return data

# Save data to a file
def save_data(data, filename):
    if not os.path.exists('data'):
        os.makedirs('data') # Create a data directory if it does not exist
    df = pd.DataFrame(data) # Create a DataFrame from the data
    if filename.endswith('.json'):
        # Save data to JSON file
        df.to_json(filename, orient='records') 
    else:
        # Save data to CSV file
        df.to_csv(filename, index=False)

# Main function
def main():
    url = "https://www.color-hex.com/color-palettes" # Specify the URL to scrape data from (Please note that this URL is subject to change as well as the structure of the website to be scraped from in the future in scraper.py)
    num_pages = 1764  # Set the number of pages to scrape per your requirements (1764 pages in this case)
    driver = init_driver() # Initialize the driver
    try:
        print("Collecting palette data from the specified URL...")
        palette_data = collect_palette_data(driver, url, num_pages) # Collect palette data
        print(f"Total palettes extracted: {len(palette_data)}")
        save_data(palette_data, 'data/palette_data.csv') # Save the data to a CSV file
    finally:
        # Quit the driver after processing
        driver.quit()

if __name__ == "__main__":
    main()
