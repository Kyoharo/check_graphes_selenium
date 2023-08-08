from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
# Set up Chrome options
chrome_options = webdriver.ChromeOptions()

# Add any desired options to the chrome_options object
# For example, to run in headless mode:
# chrome_options.add_argument('--headless')

# Create a WebDriver instance using ChromeOptions
driver = webdriver.Chrome(options=chrome_options)

# Open a URL in the browser
url = 'https://google.com'

driver.get(url)
sleep(5)
# Wait for a while (you can replace this with your desired logic)
driver.implicitly_wait(10)

# Close the browser window
driver.quit()

