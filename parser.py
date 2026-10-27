from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import csv
from selenium.webdriver.common.keys import Keys
import datetime

#https://atlasbus.by/Маршруты/Минск/Гродно?date=2026-10-27&passengers=1&returnDate=2026-11-03

#
#
#/html/body/div/div/main/div/div[3]/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div
#/html/body/div/div/main/div/div[3]/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div
#/html/body/div/div/main/div/div[3]/div[3]/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div
#/html/body/div/div/main/div/div[3]/div[4]/div/div[1]/div/div[2]/div/div[1]/div
#/html/body/div/div/main/div/div[3]/div[4]/div/div[1]/div/div[2]/div/div[1]/div
#/html/body/div/div/main/div/div[3]/div[7]/div/div[1]/div/div[2]/div/div[1]/div
#/html/body/div/div/main/div/div[3]/div[9]/div/div[1]/div/div[2]/div/div[1]/div
#
#
#
#
#/html/body/div/div/main/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div
#/html/body/div/div/main/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div

class Parser_ATLAS:
    def __init__(self, link, from_where, where_to):
        self.link = link
        self.driver = webdriver.Firefox()
        self.driver.get(self.link)
        self.from_where = from_where
        self.where_to = where_to
        self.departure_time = []
        self.arrival_time = []

    def acceptCoockie(self):
        try:
            clickable_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'cm__btn'))
            )
            clickable_element.click()
            print("Куки успешно приняты.")
            time.sleep(1)
        except TimeoutException:
            print("Элемент '.cm__btn' не найден, продолжаем выполнение кода...")

    def openBus(self):
        url = f'https://atlasbus.by/Маршруты/{self.from_where}/{self.where_to}?date=2026-10-28&passengers=1&returnDate=2026-11-04'
        self.driver.get(url)
        self.acceptCoockie()
        time.sleep(5)
        for i in range (1, 10):
            try:
                self.departure_time.append(self.driver.find_element(By.XPATH, f"/html/body/div/div/main/div/div[3]/div[{i}]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]").text)
            except Exception:
                self.departure_time.append(self.driver.find_element(By.XPATH, f"/html/body/div/div/main/div/div[3]/div[{i}]/div/div[1]/div/div[1]/div/div[1]/div[1]").text)
        for i in range (1, 10):
            try:
                text = WebDriverWait(self.driver, 3).until(lambda d: d.find_element(By.XPATH, f"/html/body/div/div/main/div/div[3]/div[{i}]/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div").text)
                if text:
                    self.arrival_time.append(text)
            except Exception:
                text = WebDriverWait(self.driver, 3).until(lambda d: d.find_element(By.XPATH, f"/html/body/div/div/main/div/div[3]/div[{i}]/div/div[1]/div/div[2]/div/div[1]/div").text)
                if text:
                    self.arrival_time.append(text)
        time.sleep(0.5)
        print(self.departure_time)
        print(self.arrival_time)
        input()

    def __del__(self):
        print ("zakoncheno")
