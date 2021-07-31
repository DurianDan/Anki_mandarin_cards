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
            "https://www.yellowbridge.com/chinese/dictionary.php")
print("* successfully loaded the web page for the first time")
driver.find_element_by_xpath(
    """//*[@id="hwWord"]""").send_keys(
        '调味料',Keys.ENTER)
(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '''/html/body/div/main/div/div[2]/ul/li[3]/a'''))
    )).click()


print(type((driver.find_element_by_xpath('''/html/body/div[1]/main/div/div[3]/table[2]/tbody/tr/td''').text).strip("\n")))
