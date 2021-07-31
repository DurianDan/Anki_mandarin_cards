from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from gtts import gTTS
driver = webdriver.Chrome()
driver.get("https://www.yellowbridge.com/chinese/dictionary.php")
myText = "清淡清淡" 


searchbar = driver.find_element_by_xpath("""//*[@id="hwWord"]""")
searchbar.send_keys("清淡清淡",Keys.ENTER)

eng_meaning = driver.find_element_by_xpath("/html/body/div/main/div/div[3]/table[1]/tbody/tr[1]/td[2]").text
pinyin = driver.find_element_by_xpath("/html/body/div/main/div/div[3]/table[1]/tbody/tr[4]/td[2]/span").text
print(pinyin)
print(eng_meaning)
driver.get(" ")
'''hanviet = driver.find_element_by_xpath("/html/body/section/div[3]/div[2]/div[4]/div[1]/div[2]/p[1]/a").text
print(hanviet)'''

'''lang = "zh"
output = gTTS(text = myText,lang = lang,slow= False)
output.save("test.mp3")'''