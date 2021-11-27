import csv
from csv import writer

from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import argparse

def crawl_data(driver, page_threshold=2, country_name_list=None):
    # page_threshold = 2
    if country_name_list is None:
        country_name_list = []
    page_count = 1
    for country_name in country_name_list:
        # Find the city
        write_to_csv(country_name+"_data.csv", "country_name", "place_name", "review_header", "review", "written_date")
        driver.find_element(By.XPATH, '//*[@id="component_1"]/div/div/form/input[1]').send_keys(country_name)
        sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="component_1"]/div/div/form/input[1]').send_keys(Keys.ARROW_DOWN)
        sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="component_1"]/div/div/form/input[1]').send_keys(Keys.ENTER)
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH,
                            '//*[@id="lithium-root"]/main/span/div/div[3]/div/div/div/span/div/div/div[2]/div/div/section[3]/div/span/div/div[3]/div/a').click()
        sleep(1)
        # //*[@id="lithium-root"]/main/span/div/div[3]/div/div/div/span/div/div[2]/div[2]/div/div/section[2]/div/span/div/article/div[2]/header/div/div/a[1]
        # //*[@id="lithium-root"]/main/div[1]/div[2]/div[1]/header/div[3]/div[1]/div/h1
        driver.switch_to.window(driver.window_handles[-1])
        sleep(1)
        # Click on each link
        while page_count <= page_threshold:
            ad_counter = 1  # To avoid adplaceholder
            for i in range(2, 39):
                if ad_counter == 5:
                    ad_counter = 1
                    continue
                # //*[@id="lithium-root"]/main/span/div/div[3]/div/div/div/span/div/div[2]/div[2]/div/div/section[38]
                # tabs = driver.window_handles
                # print(len(tabs))
                # //*[@id="lithium-root"]/main/span/div/div[3]/div/div/div/span/div/div[2]/div[2]/div/div/section[3]/div/span/div/article/div[2]/header/div/div/a[1]
                else:
                    ad_counter += 1
                    driver.find_element(By.XPATH,
                                        '//*[@id="lithium-root"]/main/span/div/div[3]/div/div/div/span/div/div['
                                        '2]/div[2]/div/div/section[' + str(i) + ']/div/span/div/article/div['
                                                                                '2]/header/div/div/a[1]').click()
                    driver.switch_to.window(driver.window_handles[-1])
                    sleep(3)
                    # get_review(driver, 30, country_name)
                    # driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.COMMAND + "w")
                    driver.close()
                    driver.switch_to.window(driver.window_handles[-1])
                    sleep(1)

            # click on next page
            # //*[@id="lithium-root"]/main/span/div/div[3]/div/div/div/span/div/div[2]/div[2]/div/div/section[39]/span/div[1]/div/div[1]/div[2]/div/a
            driver.find_element(By.XPATH,
                                '//*[@id="lithium-root"]/main/span/div/div[3]/div/div/div/span/div/div[2]/div[2]/div/div/section[39]/span/div[1]/div/div[1]/div[2]/div/a').click()
            # driver.implicitly_wait(10)
            sleep(5)
            page_count += 1


# driver.get('https://www.tripadvisor.com/Attraction_Review-g187147-d188150-Reviews-Musee_d_Orsay-Paris_Ile_de_France.html')
# # driver.fullscreen_window()
# driver.implicitly_wait(10)


# This section is to get the reviews on a place
def get_review(driver, page_threshold=2, country=""):
    page_counter = 1
    name_place = driver.find_element(By.XPATH,
                                     '//*[@id="lithium-root"]/main/div[1]/div[2]/div[1]/header/div[3]/div[1]/div/h1').text
    # driver.implicitly_wait(1)

    file_name = country + "_data.csv"
    # print(name_place, region_place)
    while page_counter <= page_threshold:
        # Get the reviews in one page
        for i in range(1, 11):
            try:
                header = driver.find_element(By.XPATH, '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div[' + str(
                    i) + ']/span/span/a/div/span').text
                try:
                    review = driver.find_element(By.XPATH, '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div[' + str(
                        i) + ']/span/span/div[5]/div[1]/div/span').text
                    try:
                        written = driver.find_element(By.XPATH,
                                                      '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div[' + str(
                                                          i) + ']/span/span/div[7]/div[1]').text
                    except:
                        written = ""
                except:
                    review = ""

            except Exception:
                header = ""

            # print(header, review, written, '\n')
            write_to_csv(file_name, country, name_place, header, review, written)
        # Click the next page

        try:
            # driver.implicitly_wait(2)
            next_button = driver.find_element(By.XPATH,
                                '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div[11]/div[1]/div/div[1]/div[2]/div/a')
            # driver.implicitly_wait(2)
            # WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div[11]/div[1]/div/div[1]/div[2]/div/a'))).click()
            next_button.click()
            page_counter += 1
            driver.implicitly_wait(4)
        except:
            break


def write_to_csv(filename, country, place_name, review_header, review, date_review):
    with open(filename, 'a', newline='') as file:
        writer_obj = writer(file)
        writer_obj.writerow([country,place_name, review_header, review, date_review])


options = Options()
# options.add_argument("--headless")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


parser = argparse.ArgumentParser()

parser.add_argument('--c', dest='country', type=str)
args = parser.parse_args()


country_list = [args.country]

driver.get('https://www.tripadvisor.com/Attractions')
driver.implicitly_wait(3)
crawl_data(driver, 50, country_list)

