import csv
from csv import writer

from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def crawl_data(driver, page_threshold=2):
    # page_threshold = 2
    page_count = 1
    for city_name in city_name_list:
        # Find the city
        driver.find_element(By.XPATH, '//*[@id="component_1"]/div/div/form/input[1]').send_keys(city_name)
        sleep(1)
        driver.find_element(By.XPATH, '//*[@id="component_1"]/div/div/form/input[1]').send_keys(Keys.ARROW_DOWN)
        sleep(1)
        driver.find_element(By.XPATH, '//*[@id="component_1"]/div/div/form/input[1]').send_keys(Keys.ENTER)
        sleep(1)
        driver.find_element(By.XPATH,
                            '//*[@id="lithium-root"]/main/span/div/div[3]/div/div/div/span/div/div/div[2]/div/div/section[4]/div/span/div/div[3]/div/a').click()
        sleep(1)
        driver.switch_to.window(driver.window_handles[-1])

        sleep(1)
        # Click on each link
        while page_count <= page_threshold:
            ad_counter = 1  # To avoid adplaceholder
            for i in range(2, 3):
                if ad_counter == 5:
                    ad_counter = 1
                    continue

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
                    sleep(4)
                    get_review(driver, 2)
                    # driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.COMMAND + "w")
                    driver.close()
                    driver.switch_to.window(driver.window_handles[-1])
                    sleep(1)

            # click on next page

            driver.find_element(By.XPATH,
                                '//*[@id="lithium-root"]/main/span/div/div[3]/div/div/div/span/div/div[2]/div[2]/div/div/section[39]/span/div[1]/div/div[1]/div[2]/div/a').click()
            driver.implicitly_wait(10)
            sleep(5)
            page_count += 1


# driver.get('https://www.tripadvisor.com/Attraction_Review-g187147-d188150-Reviews-Musee_d_Orsay-Paris_Ile_de_France.html')
# # driver.fullscreen_window()
# driver.implicitly_wait(10)


# This section is to get the reviews on a place
def get_review(driver, page_threshold=2):
    page_counter = 1
    name_place = driver.find_element(By.XPATH,
                                     '//*[@id="lithium-root"]/main/div[1]/div[2]/div[1]/header/div[3]/div[1]/div/h1').text
    region_place = driver.find_element(By.XPATH,
                                       '/html/body/div/main/div[1]/div[2]/div[2]/div/div/span/section[5]/div/div/div[2]/div[1]/span/div/div/div[1]/button/span').text

    file_name = "~/data/" + name_place + " " + region_place + " " + "data.csv"
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
            write_to_csv(file_name, name_place, region_place, header, review, written)
        # Click the next page

        driver.find_element(By.XPATH,
                            '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div[11]/div[1]/div/div[1]/div[2]/div/a').click()
        page_counter += 1


def write_to_csv(filename, place_name, region_place, review_header, review, date_review):
    with open(filename, mode='w') as file:
        writer_obj = writer(file)
        writer_obj.writerow([place_name, region_place, review_header, review, date_review])
        file.close()


options = Options()
# options.add_argument("--headless")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

city_name_list = ['Paris']

driver.get('https://www.tripadvisor.com/Attractions')
driver.implicitly_wait(3)
crawl_data(driver, 10)
