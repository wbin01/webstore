#!/usr/bin/env python3
import os
from pathlib import Path
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class XTestCase(LiveServerTestCase):
    def setUp(self) -> None:
        base_dir = Path(__file__).resolve().parent.parent
        self.browser = webdriver.Chrome(os.path.join(base_dir, 'chromedriver'))

    def tearDown(self) -> None:
        self.browser.quit()

    def test_x(self):
        pass
