import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from scraper import collect_palette_data
from webdriver_manager.chrome import ChromeDriverManager

class TestCollectPaletteData(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.base_url = "https://www.color-hex.com/color-palettes"
        self.num_pages = 2

    def test_collect_palette_data(self):
        data = collect_palette_data(self.driver, self.base_url, self.num_pages)
        self.assertEqual(len(data), 4)  # Check if the correct number of palettes are collected

        # Check if the collected data has the expected structure
        self.assertEqual(data[0]["Name"], "Color palette 420 shades of green")
        self.assertEqual(data[0]["Colors"], ['rgb(91, 160, 54)', 'rgb(36, 101, 41)', 'rgb(90, 129, 40)', 'rgb(19, 67, 20)', 'rgb(85, 118, 32)'])
        self.assertEqual(data[1]["Name"], "Color palette Pink and Grey Chic")
        self.assertEqual(data[1]["Colors"], ['rgb(201, 0, 118)', 'rgb(112, 128, 144)', 'rgb(255, 102, 178)', 'rgb(69, 129, 142)', 'rgb(166, 77, 121)'])
        self.assertEqual(data[2]["Name"], "Color palette DTI usages")
        self.assertEqual(data[2]["Colors"], ['rgb(253, 228, 242)', 'rgb(225, 225, 221)', 'rgb(249, 206, 231)', 'rgb(192, 173, 140)', 'rgb(255, 175, 214)'])
        self.assertEqual(data[3]["Name"], "Color palette foggy cloudy day")
        self.assertEqual(data[3]["Colors"], ['rgb(201, 220, 214)', 'rgb(162, 187, 186)', 'rgb(128, 151, 154)', 'rgb(67, 100, 105)', 'rgb(45, 73, 69)']);

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()