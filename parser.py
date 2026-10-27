from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import csv
from selenium.webdriver.common.keys import Keys
import datetime
import pandas as pd

log_file = "parser_log.txt"

def log_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Текущее время
        
        # Открываем файл в режиме 'a' (append — дописывание в конец)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] Старт: {func.__name__}\n")
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start
            timestamp_end = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp_end}] Финиш: {func.__name__} | Время: {duration:.2f} сек.\n\n")
    
    return wrapper

class Parser_ATLAS:
    @log_time
    def __init__(self, link, from_where, where_to):
        self.link = link
        options = Options()
        #47.89.184.18:3128
        # options.set_preference("network.proxy.type", 1)
        # options.set_preference("network.proxy.http", "47.89.184.18")
        # options.set_preference("network.proxy.http_port", 3128)
        # options.set_preference("network.proxy.ssl", "47.89.184.18")
        # options.set_preference("network.proxy.ssl_port", 3128)
        # options.set_preference("network.proxy.no_proxies_on", "localhost, 127.0.0.1")
        # options.set_preference("general.useragent.override", "Mozilla/5.0 (Linux Ubuntu 22.04 LTS; x64; rv:121.0) Gecko/20100101 Firefox/121.0")

        self.driver = webdriver.Firefox(options=options)
        self.driver.get(self.link)
        self.from_where = from_where
        self.where_to = where_to
        self.departure_time = []
        self.arrival_time = []
        self.ratio = []
        self.res = {}

    @log_time
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

    @log_time
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
                    text_1 = WebDriverWait(self.driver, 0.5).until(lambda d: d.find_element(By.XPATH, f"/html/body/div/div/main/div/div[2]/div[{i}]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]").text)
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
        datd = pd.DataFrame(self.res)
        datd.to_csv(f'res{self.from_where}-{self.where_to}.csv', index=0)

    @log_time
    def __del__(self):
        print ("zakoncheno")
