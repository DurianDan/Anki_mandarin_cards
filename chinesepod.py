from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://www.chinesepod.com/dictionary?search=清淡")

meaning_1 = driver.find_element_by_xpath("""//*[@id="vocabulary"]/div[1]/a/div/div[1]""")
meaning_1.click()

pinyin = driver.find_element_by_xpath("""//*[@id="wrapper"]/main/div/div[2]/section[1]/div/div/div[1]/div/div[2]/div[1]""").text
print(pinyin)
meaning = driver.find_element_by_xpath("""//*[@id="wrapper"]/main/div/div[2]/section[2]/div/div/div/div/ol""").text
print(meaning)

