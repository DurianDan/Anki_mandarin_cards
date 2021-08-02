from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
options = Options()
options.page_load_strategy = 'none'
driver = webdriver.Chrome(options=options)
for i in ['辣','咸','甜','苦','咸','甜','苦']:
    driver.get("""https://www.chineseboost.com/chinese-example-sentences""")
    driver.find_element_by_xpath(
        '''/html/body/div[2]/form/div/input'''
    ).send_keys(i,Keys.ENTER)