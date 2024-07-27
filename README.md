# Scraper

This project is a web scraper built with Selenium and integrated with a Flask application. It allows users to scrape data from web pages, handle pagination, and download the scraped data in CSV or JSON format through a web interface.

the sctipt is a web scraper that uses Selenium to scrape data from web pages. It can handle pagination and save the scraped data in CSV or JSON format. The scraper is integrated with a Flask application, allowing users to input the scraping parameters through a web interface.

if can only scrape data from a single page by passing the single page as a number, you can modify the script to handle pagination and scrape multiple pages.

It scrapes data from this website by following website only:
~ https://www.color-hex.com/color-palettes

Use it to scrape data from other websites by modifying the CSS selectors and data extraction logic in the `scraper.py` file.

for UI Demo use the above link to scrape data from the website.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed
- Google Chrome browser installed
- ChromeDriver downloaded and added to your PATH

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/bugemarvin/scraper.git
   cd scraper
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv or python3 -m venv venv
   ```

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Ensure `chromedriver` is available in your PATH. If not, specify its location in `scraper.py` when initializing the WebDriver.

## Project Structure

```
scraper/
│
├── app.py # Flask application
├── scraper.py # Selenium scraper
├── requirements.txt # Required packages
├── test_scraper.py # Unit tests for the scraper
├── uploads/ # Directory for saving scraped files
│ └── (scraped files)
└── templates/
└── index.html # HTML template for the web interface
```

## Usage

1. **Run the Script or Flask Application**

   Run the scraper script directly:

   ```bash
   python3 scraper.py
   ```

   Start the Flask application by running:

   ```bash
   flask run
   ```

   If you're using Windows, set the `FLASK_APP` environment variable first:

   ```bash
   set FLASK_APP=app.py
   flask run
   ```

   Start as a standalone application:

   ```bash
   python3 app.py
   ```

2. **Access the Web Interface**

   Open your web browser and navigate to `http://127.0.0.1:5000`. You should see a web form where you can input the scraping parameters.

3. **Input Scraping Parameters**

   - **URL**: The URL of the website you want to scrape.
   - **Pagination Selector**: The CSS selector for the pagination button/link.
   - **Data Selector**: The CSS selector for the data you want to scrape.
   - **File Format**: Choose between CSV or JSON for the output file format.

4. **Start Scraping**

   Click on the "Scrape" button. The scraper will process the pages, and the data will be available for download once scraping is complete.

## Running Tests

To run the unit tests for the scraper, use:

```bash
python test_scraper.py
```

## Example

Here's an example of how to use the scraper programmatically:

```python
import scraper

url = "https://www.color-hex.com/color-palettes" # Specify the URL to scrape data from (Please note that this URL is subject to change as well as the structure of the website to be scraped from in the future in scraper.py)
num_pages = 1764  # Set the number of pages to scrape per your requirements (1764 pages in this case)
driver = scraper.init_driver() # Initialize the driver
try:
    print("Collecting palette data from the specified URL...")
    palette_data = scraper.collect_palette_data(driver, url, num_pages) # Collect palette data
    print(f"Total palettes extracted: {len(palette_data)}")
    save_data(palette_data, 'data/palette_data.csv') # Save the data to a CSV file
    or
    save_data(palette_data, 'data/palette_data.json') # Save the data to a JSON file
finally:
    # Quit the driver after processing
    driver.quit()
```

### Output

```json
[
  {
    "ID": "1048899",
    "Name": "seafoam essence",
    "HEX": [
      "#ffffff",
      "#fffcfa",
      "#e1f4f6",
      "#b6e3ea",
      "#7bcdd9"
    ],
    "RGB": [
      "rgb(255, 255, 255)",
      "rgb(255, 252, 250)",
      "rgb(225, 244, 246)",
      "rgb(182, 227, 234)",
      "rgb(123, 205, 217)"
    ]
  },
  {
    "ID": "1048898",
    "Name": "Dark Blue-Magenta",
    "HEX": [
      "#0c070d",
      "#221b41",
      "#322971",
      "#747bb4",
      "#a2abca"
    ],
    "RGB": [
      "rgb(12, 7, 13)",
      "rgb(34, 27, 65)",
      "rgb(50, 41, 113)",
      "rgb(116, 123, 180)",
      "rgb(162, 171, 202)"
    ]
  },
    ...
]
```

# License

This project is licensed under the MIT License. See the LICENSE file for more details.
Contributing

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes and commit (git commit -am 'Add new feature').
4. Push to the branch (git push origin feature-branch).
5. Create a new Pull Request.

# Contact

If you have any questions, feel free to reach out to me at bugemarvin@outlook.com.

Save this as `README.md` in your project directory. This file provides comprehensive instructions on how to set up, use, and test the web scraper and Flask application.
