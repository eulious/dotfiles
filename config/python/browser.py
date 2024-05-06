#!/usr/bin/env python
# coding:utf-8

from os import environ
from time import sleep, time
from pathlib import Path
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.expected_conditions import alert_is_present
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class WebElementWrapper:
    TIMEOUT = 2

    def __init__(self, driver=None, previous=None) -> None:
        self.__driver = driver
        self.__previous = previous
        self.__dom = []
        self.query = {}

    def __getitem__(self, index):
        self.query = {
            "action": "get_item",
            "index": index
        }
        return self.__generate()
    
    def __bool__(self):
        return bool(len(self.reflect()))
    
    def __generate(self):
        return WebElementWrapper(None, self)
    
    def reflect(self):
        previous_doms = [self.__driver] if self.__previous is None else self.__previous
        query = self.query
        if query == {}:
            return previous_doms
        
        if query["action"] == "find_elements":
            fn = lambda d : d.find_elements(query["by"], query["value"])
            return sum(list(map(fn, previous_doms)), [])
        elif query["action"] == "get_item":
            # TODO
            return [previous_doms[query["index"]]] if len(previous_doms) > query["index"] else ""
        elif query["action"] == "text_match":
            if self.__driver:
                # TODO
                return self.__driver.find_elements(By.XPATH, f"//*[text()='")
            else:
                fn = lambda d: d.text == query["pattern"]
                return list(filter(fn, previous_doms))
        elif query["action"] == "text_search":
            if self.__driver:
                # TODO
                return self.__driver.find_elements(By.XPATH, f"//*[text()='")
            else:
                fn = lambda d: d.text == query["pattern"]
                return list(filter(fn, previous_doms))
    
    def __execute(self, is_exist=True, assertion=True):
        started_at = time()
        while time() -started_at < WebElementWrapper.TIMEOUT:
            arr = self.reflect()
            arr = self.__filter_visible(arr)
            if is_exist and len(arr):
                self.__dom = arr
                return arr[0]
            elif not is_exist and not len(arr):
                self.__dom = arr
                return []
            sleep(0.3)
        else:
            self.__dom = []
            if assertion:
                raise Exception(f"Not found: {self.query}")

            else: 
                return []
    
    def __filter_visible(self, arr):
        new_arr = []
        for elm in arr:
            if elm.is_displayed():
                new_arr.append(elm)
        return new_arr
    
    def cls(self, class_name):
        self.query = {
            "action": "find_elements",
            "by": By.CLASS_NAME,
            "value": class_name
        }
        return self.__generate()

    def x(self, expr):
        self.query = {
            "action": "find_elements",
            "by": By.XPATH,
            "value": expr
        }
        return self.__generate()

    def sl(self, expr):
        self.query = {
            "action": "find_elements",
            "by": By.CSS_SELECTOR,
            "value": expr
        }
        return self.__generate()

    def match(self, text):
        self.query = {
            "action": "text_match",
            "pattern": text
        }
        return self.__generate()

    def search(self, text):
        self.query = {
            "action": "text_search",
            "pattern": text
        }
        return self.__generate()

    @property
    def elm(self):
        return self.__execute()
    
    @property
    def elms(self):
        self.__execute(assertion=False)
        return self.__dom
    
    @property
    def text(self):
        elm = self.__execute()
        return elm.text
    
    @property
    def exists(self):
        self.__execute(is_exist=True, assertion=False)
        return bool(len(self.__dom))

    @property
    def not_exists(self):
        self.__execute(is_exist=True, assertion=False)
        return not bool(len(self.__dom))

    def send_file(self, path):
        elm = self.__execute()
        elm.send_keys(str(Path(path).resolve()))

    def click(self):
        elm = self.__execute()
        return elm.click()
    
    def types(self, keys):
        elm = self.__execute()
        return elm.send_keys(keys)


class Driver(WebElementWrapper):
    def __init__(self):
        self.__remove_proxy()
        self.driver = Chrome(
            desired_capabilities=DesiredCapabilities.CHROME.copy() #TODO
        )
        self.actions = ActionChains(self.driver)
        self.waiter = WebDriverWait(self.driver, 15)
        super().__init__(self.driver)
    
    def close(self):
        self.driver.close()
    
    def types(self, keys):
        self.actions.send_keys(keys).perform
    
    def accept(self, keys=""):
        self.waiter.until(alert_is_present())
        alert = Alert(self.driver)
        if keys:
            alert.send_keys(keys)
        alert.accept()

class DriverTimeout():
    pass