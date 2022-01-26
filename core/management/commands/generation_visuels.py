import glob, os

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

        options = webdriver.ChromeOptions()
        options.add_argument("no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=800,600")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")


        driver = webdriver.Remote(
                    command_executor='http://selenium-hub:4444/wd/hub',   desired_capabilities={'browserName': 'chrome', 'javascriptEnabled': True})

        driver.get("http://www.python.org")
        driver.save_screenshot('screenshot.png')
        driver.quit()
