from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from gtts import gTTS
from os import listdir

options = Options()
options.page_load_strategy = 'none'
driver = webdriver.Chrome(options=options)

class mandarin_json():
    def __init__(self,mandarin,directory):
        self.word = mandarin
        self.meanings = {}
        self.pinyins = {}
        self.HanViet = {}
        self.component_words = []
        self.Examples = {}
        if {listdir(directory)} == {"pointer(json)",'mp3','gif'}:
            self.folder = directory
        else:
            print('''the folder directory must be divided
            by 3 sub-directories: "pointer(json)","mp3","gif"''')
    def get_Meaning_Pinyin_Example(self):
        '''Get the meaning, pinyin metadata from yellowbridge.com
        Doesn't return any thing'''
        #1 get page 
        driver.get(
            "https://www.yellowbridge.com/chinese/dictionary.php")
        print("* successfully loaded the web page for the first time")
        driver.find_element_by_xpath(
            """//*[@id="hwWord"]""").send_keys(
                self.word,Keys.ENTER)
        print("* sent words to search-translate bar")
        #2.get all the meaning and pinyin metadata
        try:
            self.meanings.update({self.word:driver.find_element_by_xpath(
                '''/html/body/div/main/div/div[3]/table[1]/tbody/tr[1]/td[2]''').text})
            self.pinyins.update({self.pinyins:driver.find_element_by_xpath(
                '''/html/body/div/main/div/div[3]/div[1]/div/span'''
            ).text})
            print("* get meaning and pinyin of the word (first_try)")
        except NoSuchElementException:
            print("""* Couldn't find meaning of whole word,
                        finding the meaning of component words...""")
            for i in range(len(self.word)):
                print("** getting list of component words...")
                try:
                    component = driver.find_element_by_xpath(
                        '''/html/body/div/main/div/div[3]/table[2]/tbody/tr[{}]/td[1]/a'''.format(str(i))
                    ).text
                    self.component_words.append(component)
                    print("***component_word {} : ".format(str(i))+ component)
                except NoSuchElementException:
                    break
            print("***list of component worlds is made!")
            print("**getting meaning and pinyin of component words")
            for comp in self.component_words:
                driver.find_element_by_xpath(
                    '''//*[@id="hwWordTop"]''').send_keys(comp,Keys.ENTER)
                self.meanings.update({comp:driver.find_element_by_xpath(
                '''/html/body/div/main/div/div[3]/table[1]/tbody/tr[1]/td[2]''').text})
                self.pinyins.update({comp:driver.find_element_by_xpath(
                    '''/html/body/div/main/div/div[3]/div[1]/div/span'''
                ).text})
                print("***updated the meaning and pinyin of component word: ",comp)
        print("*successfully retrieve pinyins, meanings of word(or components word")
        driver.quit()
    def get_HanViet(self):
        '''Get Hán Việt meaning of mandarin
        Doesn't return anything'''
        search_web = '''https://hvdic.thivien.net/whv/'''
        for letter in self.word:
            print("getting Hán Việt meanings of ", letter)
            if letter == ' ':
                continue
            driver.get(search_web+letter)
            component_hanviet = [i.strip() for i in
             driver.find_element_by_xpath(
                 '''/html/body/section/div[3]/div[2]/div[1]/div''').text.
                 split('•')][0]
            self.HanViet.update({letter:component_hanviet})
        print("successfully get Hán Việt Meanings")
        driver.quit()     
    def get_Examples(self):
        pass
