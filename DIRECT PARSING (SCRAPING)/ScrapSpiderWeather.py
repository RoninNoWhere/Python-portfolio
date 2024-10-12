# Import necessary libraries
from selenium import webdriver  # Import the webdriver module to control the browser
from selenium.webdriver.common.by import By  # Import By to locate elements
from selenium.webdriver.chrome.service import Service  # Import Service to manage ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager  # Import to manage ChromeDriver automatically
from selenium.webdriver.support.ui import WebDriverWait  # Import WebDriverWait for waiting
from selenium.webdriver.support import expected_conditions as EC  # Import expected_conditions for waiting conditions

# Set up the Chrome WebDriver
service = Service(ChromeDriverManager().install())  # Initialize the Service with the installed ChromeDriver
driver = webdriver.Chrome(service=service)  # Initialize the Chrome browser with the service

# Open the weather page for Warsaw
driver.get('https://openweathermap.org/city/756135')  # Navigate to the specified URL

try:
    # Wait for the temperature element to be present in the DOM
    temp_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'current-temp'))  # Wait until the element is present
    )
    
    # If found, get the temperature text from the heading element inside temp_element
    temperature = temp_element.find_element(By.CLASS_NAME, 'heading').text.strip()  # Extract and clean the temperature text
    print(f"Temperature in Warsaw: {temperature}")  # Print the temperature

except Exception as e:
    print(f"An error occurred: {e}")  # Print any error that occurs

finally:
    # Close the WebDriver and the browser
    driver.quit()  # End the session and close the browser
