# Scraper

This project is a web scraper built with Selenium and integrated with a Flask application. It allows users to scrape data from web pages, handle pagination, and download the scraped data in CSV or JSON format through a web interface.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed
- Google Chrome browser installed
- ChromeDriver downloaded and added to your PATH

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/web_scraper.git
    cd web_scraper
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure `chromedriver` is available in your PATH. If not, specify its location in `scraper.py` when initializing the WebDriver.

## Project Structure

```
web_scraper/
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

1. **Run the Flask Application**

    Start the Flask application by running:

    ```bash
    python app.py
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
from scraper import WebScraper

scraper = WebScraper('https://example.com', '.pagination-next', '.item')
data = scraper.scrape()
scraper.save_data(data, 'csv', 'data.csv')
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

