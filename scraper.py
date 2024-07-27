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
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless mode
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

# Convert RGB to HEX
def rgb_to_hex(rgb):
    rgb = [int(x) for x in rgb[4:-1].split(",")]
    return '#%02x%02x%02x' % tuple(rgb)

# Collect palette data from multiple pages
def collect_palette_data(driver, base_url, num_pages):
    data = []
    for page in range(1, num_pages + 1):
        try:
            driver.get(f"{base_url}/?page={page}")
            palette_elements = driver.find_elements(By.CLASS_NAME, "palettecontainerlist")
            print(f"Found {len(palette_elements)} palettes on page {page}.")
            for palette in palette_elements:
                print(f"Extracting palette data {palette_elements.index(palette) + 1}...")
                try:
                    anchor = palette.find_element(By.TAG_NAME, "a")
                    id = anchor.get_attribute("href").split("/")[-1]
                    palette_name = anchor.get_attribute("title").split(" ")
                    palette_name = " ".join(palette_name[2:])
                    
                    color_elements = palette.find_elements(By.CLASS_NAME, "palettecolordiv")
                    colors_rgb = []
                    colors_hex = []
                    
                    for color_elem in color_elements:
                        style = color_elem.get_attribute("style")
                        if style and "background-color:" in style:
                            rgb = style.split("background-color: ")[1].split(";")[0]
                            colors_rgb.append(rgb)
                            colors_hex.append(rgb_to_hex(rgb))
                    
                    print(f"Palette Name: {palette_name}" + "\n" + f"Colors: {colors_rgb}" + "\n" + f"HEX: {colors_hex}")
                    data.append({
                        "ID": id,
                        "Name": palette_name,
                        "HEX": colors_hex,
                        "RGB": colors_rgb
                    })
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
        os.makedirs('data')
    df = pd.DataFrame(data)
    if filename.endswith('.json'):
        df.to_json(filename, orient='records')
    else:
        df.to_csv(filename, index=False)

# Main function
def main():
    url = "https://www.color-hex.com/color-palettes"
    num_pages = 1764  # Set the number of pages to scrape
    driver = init_driver()
    try:
        print("Collecting palette data from the specified URL...")
        palette_data = collect_palette_data(driver, url, num_pages)
        print(f"Total palettes extracted: {len(palette_data)}")
        save_data(palette_data, 'data/palette_data.csv')
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
