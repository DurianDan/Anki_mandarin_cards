from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
options = Options()
options.page_load_strategy = 'none'
driver = webdriver.Chrome(options=options)

driver.get(
            "https://www.chineseboost.com/chinese-example-sentences?query=烹饪方式")
print("* successfully loaded the web page for the first time")

search_resault = 0

search_resault = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '''/html/body/div[2]/div[7]/div/div'''))
    )

words = search_resault.text.split("\n")
print(words)


