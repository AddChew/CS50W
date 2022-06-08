import os
import pathlib
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path

# Finds the Uniform Resourse Identifier of a file
def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

# Sets up web driver using Google chrome
service_object = Service(binary_path)
driver = webdriver.Chrome(service=service_object)