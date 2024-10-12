This code scraping weather info from web site openweathermap.org

This code was created for educational purposes only.


1. First version looked like This, but it couldn't find the class cause it dosent shows up in HTML code cause it dynamicly uploading with JavaScript. 
In this case better use the API strategi.
import requests
from bs4 import BeautifulSoup

    # URL page OpenWeatherMap
url = 'https://openweathermap.org/city/756135'  # Warsaw

    # executing a request
response = requests.get(url)

    # success check
if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print(soup.prettify())

        # looking for a temo class
        temp_element = soup.find('div', class_='current-temp')
        
        if temp_element:
            temperature = temp_element.find('span', class_='heading').text.strip()
            print(f"Temperature in Warsaw: {temperature}")
        else:
            print("Can't find a temperature element. Pls contact the developer")
else:
        print(f"Error code: {response.status_code}")

2.  But for educational purposes i'm still trying the direct parsing
in this case i used Selenium library 