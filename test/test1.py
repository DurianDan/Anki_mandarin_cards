from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
options = Options()
options.page_load_strategy = 'none'
driver = webdriver.Firefox()

driver.get(
            """https://hvdic.thivien.net/whv/%E7%83%B9%E9%A5%AA%E6%96%B9%E5%BC%8F""")

            

try:
    element = driver.find_element_by_xpath("""/html/body/section/div[3]/div[2]/div/p/span[3]""")
    element.click()
    han = driver.find_element_by_xpath('''/html/body/section/div[3]/div[2]/div[2]/div''').text
    print(han)
finally:
    pass 

