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

#MuiInputBase-input MuiFilledInput-input MuiAutocomplete-input MuiAutocomplete-inputFocused MuiInputBase-inputAdornedEnd MuiFilledInput-inputAdornedEnd
#MuiInputBase-input MuiFilledInput-input MuiAutocomplete-input MuiAutocomplete-inputFocused
#MuiInputBase-input MuiFilledInput-input
#MuiInputBase-input MuiFilledInput-input
#
#
#/html/body/div/div/header/div/div[2]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div/div/div/div/button

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

    def choosing_route (self):
        where_field = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, 'MuiInputBase-inputAdornedEnd')))
        where_field.send_keys(self.from_where)
        where_field.send_keys(Keys.ENTER)
        time.sleep(3)

        to_field = self.driver.switch_to.active_element
        to_field.send_keys(self.where_to)
        to_field.send_keys(Keys.ENTER)
        time.sleep(3)

    def openBus(self):
        self.acceptCoockie()
        self.choosing_route()
        input()
        time.sleep(5)
        for i in range (1, 50):
            try:
                text_1 = WebDriverWait(self.driver, 0.5).until(lambda d: d.find_element(By.XPATH, f"html/body/div/div/main/div/div[3]/div[{i}]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]").text)
                if text_1:
                    self.departure_time.append(text_1)
            except Exception:
                try:
                    text_1 = WebDriverWait(self.driver, 0.5).until(lambda d: d.find_element(By.XPATH, f"/html/body/div/div/main/div/div[3]/div[{i}]/div/div[1]/div/div[1]/div/div[1]/div[1]").text)
                    if text_1:
                        self.departure_time.append(text_1)
                except TimeoutException:
                    continue
            try:
                text_2 = WebDriverWait(self.driver, 0.5).until(lambda d: d.find_element(By.XPATH, f"/html/body/div/div/main/div/div[3]/div[{i}]/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div").text)
                if text_2:
                    self.arrival_time.append(text_2)
            except Exception:
                try:
                    text_2 = WebDriverWait(self.driver, 0.5).until(lambda d: d.find_element(By.XPATH, f"/html/body/div/div/main/div/div[3]/div[{i}]/div/div[1]/div/div[2]/div/div[1]/div").text)
                    if text_2:
                        self.arrival_time.append(text_2)
                except TimeoutException:
                    continue
        print(self.departure_time)
        print(len(self.departure_time))
        print(self.arrival_time)
        print(len(self.arrival_time))
        input()


    def __del__(self):
        print ("zakoncheno")
