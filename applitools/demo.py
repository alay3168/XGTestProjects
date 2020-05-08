from selenium import webdriver
from applitools.selenium import Eyes

class HelloWorld:

    global driver
    eyes = Eyes()

    # Initialize the eyes SDK and set your private API key.
    eyes.api_key = 'AL5GqeGbRnjSh4SPX6HIgH104G8BR3Ir0OniXHw4nSK7o110'

    try:

        # Open a Chrome browser.
        driver = webdriver.Chrome()

        # Start the test and set the browser's viewport size to 800x600.
        eyes.open(driver, "Test app", "First test", {"width": 800, "height": 600})

        # Navigate the browser to the "hello world!" web-site.
        driver.get('https://applitools.com/helloworld')

        # Visual checkpoint #1.
        eyes.check_window('Hello!')

        # Click the 'Click me!' button.
        driver.find_element_by_css_selector('button').click()

        # Visual checkpoint #2.
        eyes.check_window('Click!')

        # End the test.
        eyes.close()

    finally:

        # Close the browser.
        driver.quit()

        # If the test was aborted before eyes.close was called, ends the test as aborted.
        eyes.abort_if_not_closed()

if __name__ == "__main__":
    HelloWorld()