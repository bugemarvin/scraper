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

# Collect palette data from multiple pages
def collect_palette_data(driver, base_url, num_pages):
    data = []
    for page in range(1, num_pages + 1):
        try:
            driver.get(f"{base_url}/?page={page}")
            palette_elements = driver.find_elements(By.CLASS_NAME, "palettecontainerlist")
            print(f"Found {len(palette_elements)} palettes on page {page}.")
            for palette in palette_elements:
                print("Extracting palette data...")
                try:
                    anchor = palette.find_element(By.TAG_NAME, "a")
                    palette_name = anchor.get_attribute("title")
                    color_elements = palette.find_elements(By.CLASS_NAME, "palettecolordiv")
                    colors = [color_elem.get_attribute("style").split("background-color: ")[1].split(";")[0] for color_elem in color_elements]
                    print(f"Palette Name: {palette_name}" + "\n" + f"Colors: {colors}")
                    data.append({
                        "Name": palette_name,
                        "Colors": colors
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
    if '.json' in filename:
        df.to_json(filename, orient='records')
    df.to_csv(filename, index=False)

# Main function
def main():
    url = "https://www.color-hex.com/color-palettes"
    num_pages = 10  # Set the number of pages to scrape
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
