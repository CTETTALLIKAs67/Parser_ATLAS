from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import csv
from selenium.webdriver.common.keys import Keys
import datetime
import pandas as pd

#https://atlasbus.by/Маршруты/Минск/Гродно?date=2026-10-27&passengers=1&returnDate=2026-11-03

#MuiInputBase-input MuiFilledInput-input MuiAutocomplete-input MuiAutocomplete-inputFocused MuiInputBase-inputAdornedEnd MuiFilledInput-inputAdornedEnd
#MuiInputBase-input MuiFilledInput-input MuiAutocomplete-input MuiAutocomplete-inputFocused
#MuiInputBase-input MuiFilledInput-input
#/html/body/div/div/main/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]
#html/body/div/div/main/div/div[3]/div[{i}]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]
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
        self.ratio = []
        self.res = {}

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

        
    def collecting_info(self):
        date1 = pd.date_range(start='2026-10-28', end='2026-11-01', freq='D')
        date_list1 = date1.to_pydatetime().tolist()
        string_dates1 = [i.strftime("%Y-%m-%d") for i in date_list1]
        for k in string_dates1:
            url = f'https://atlasbus.by/Маршруты/Минск/{self.where_to}?date={k}&passengers=1'
            self.driver.get(url)
            self.departure_time.clear()
            self.arrival_time.clear()
            self.acceptCoockie()
            for i in range (1, 50):
                try:
                    #УБЫТИЕ
                    text_1 = WebDriverWait(self.driver, 0.5).until(lambda d: d.find_element(By.XPATH, f"html/body/div/div/main/div/div[2]/div[{i}]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]").text)
                    if text_1:
                        self.departure_time.append(text_1)
                except Exception:
                    try:
                        text_1 = WebDriverWait(self.driver, 0.5).until(lambda d: d.find_element(By.XPATH, f"/html/body/div/div/main/div/div[2]/div[{i}]/div/div[1]/div/div[1]/div/div[1]/div[1]").text)
                        if text_1:
                            self.departure_time.append(text_1)
                    except TimeoutException:
                        continue
                try:
                    #ПРИБЫТИЕ
                    text_2 = WebDriverWait(self.driver, 0.5).until(lambda d: d.find_element(By.XPATH, f"/html/body/div/div/main/div/div[2]/div[{i}]/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div").text)
                    if text_2:
                        self.arrival_time.append(text_2)
                except Exception:
                    try:
                        text_2 = WebDriverWait(self.driver, 0.5).until(lambda d: d.find_element(By.XPATH, f"/html/body/div/div/main/div/div[2]/div[{i}]/div/div[1]/div/div[2]/div/div[1]/div").text)
                        if text_2:
                            self.arrival_time.append(text_2)
                    except TimeoutException:
                        continue
            self.ratio.clear()
            for i in range(0, len(self.departure_time)):
                self.ratio.append(f'{self.departure_time[i]}-{self.arrival_time[i]}')

            self.res[k] = self.ratio

            print(f'THIS IS ratio {k}')
            print(self.ratio)
            print(self.res)
        datd = pd.DataFrame(self.res)
        datd.to_csv(f'res{self.from_where}-{self.where_to}.csv', index=0)

    def __del__(self):
        print ("zakoncheno")
