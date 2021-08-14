from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from googletrans import Translator
from gtts import gTTS
from os import listdir,mkdir
import urllib.request

from urllib3.packages.six import b

driver = webdriver.Chrome()

translator = Translator()
driver.get("https://www.google.com/")
class mandarin_json():
    def __init__(self,mandarin,directory):
        self.word = mandarin
        self.meanings = {}
        self.pinyins = {}
        self.HanViet = {}
        self.component_words = []
        self.Examples = {}
        self.folder = directory
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
        #2.get all the meaning,example and pinyin metadata
        try:
            #2.1 the meaning found on website
            self.meanings.update({self.word:driver.find_element_by_xpath(
                '''/html/body/div/main/div/div[3]/table[1]/tbody/tr[1]/td[2]''').text})
            self.pinyins.update({self.word:driver.find_element_by_xpath(
                '''/html/body/div/main/div/div[3]/div[1]/div/span'''
            ).text})
            print("* got meaning and pinyin of the word (first_try)")
            for i in range(1,9):
                print("** getting list of component words...")
                try:
                    component = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,
                        '''/html/body/div/main/div/div[3]/table[2]/tbody/tr[{}]/td[1]/a'''.format(str(i))
                    ))).text
                    self.component_words.append(component)
                    print("***component_word {} : ".format(str(i))+ component)
                except NoSuchElementException and TimeoutException:
                    break
            WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '''/html/body/div/main/div/div[2]/ul/li[3]/a'''))
                ).click()
            example_box = (WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                '''/html/body/div[1]/main/div/div[3]/table[2]/tbody/tr/td'''))).text).split('\n')
            print(example_box)
            num_example = 0
            for i in range(0,len(example_box),2):
                if len(self.Examples) <= 10:
                    num_example += 1
                    print("*Adding Example {}".format(str(num_example)))
                    try:
                        self.Examples.update({example_box[i]:example_box[i+1]})
                        print(self.Examples)
                    except IndexError:
                        break
                else:
                    print("there're 10 examples, can not add more")
                    break
            print("* got the examples of the whole word")
        except NoSuchElementException:
            #2.2 had to devide into multiple letters to find meaning
            print("* coudn't find examples on yellowbridge.com")
            print("""* Couldn't find meaning of whole word,
                        finding the meaning of component words...""")
            googletrans_mean = (translator.translate(self.word,dest="en",src="zh-CN")).text
            self.meanings.update({self.word:googletrans_mean})
            print("* got the google translated meaning of main word")
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
        print("*successfully retrieve pinyins, meanings of main word and/or components word")
        print(str(self.pinyins)+"PINYINS")
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
    def get_Examples(self):
        '''Has to be called after get_Meaning_Pinyin_Example()
        Get examples on se
        https://www.chineseboost.com/chinese-example-sentences?query'''

        driver.get("""https://www.chineseboost.com/chinese-example-sentences?query="""+self.word)
        print("Successfully accesed www.chineseboost.com/chinese-example-sentences")
        num_example = len(self.Examples)
        for i in [1,2,3,4,5]:
            print("Finding EXamples in page "+str(i))
            if len(self.Examples) >10:
                    print("There're 10 examples, can not add more")
                    break
            if i >1:
                driver.get("""https://www.chineseboost.com/chinese-example-sentences?query={}&page={}""".format(self.word,i))
            for i in range(2,22):
                num_example +=1
                if len(self.Examples) >10:
                    print("there're 10 examples, can not add more")
                    break
                try:
                    example_box_text = driver.find_element_by_xpath(
                        '''/html/body/div[2]/div[{}]/div/div'''.format(str(i))).text.split("\n")
                    if len(self.word) == 1:
                        print("Adding Example {}".format(str(num_example)))
                        self.Examples.update({example_box_text[0]:
                        [example_box_text[1],example_box_text[2]]})
                    else:
                        mandarin_in_box_ordered = False
                        for i in self.component_words:
                            if i in example_box_text[0]:
                                mandarin_in_box_ordered = True
                                break
                        if mandarin_in_box_ordered:                    
                            print("Adding Example {}".format(str(num_example)))
                            self.Examples.update({example_box_text[0]:
                            [example_box_text[1],example_box_text[2]]})
                except NoSuchElementException:
                    break
    def get_Examples_components(self):
        print("getting aditional example")
        '''when number of examples of whole word is to below 5
        This function shoul be called'''
        driver.get(
            '''https://www.yellowbridge.com/chinese/dictionary.php'''
        )
        num_Examples = len(self.Examples)
        for i in self.component_words:
            if len(self.Examples) >10:
                    break
            search_bar = '''//*[@id="hwWord{}"]'''
            if num_Examples == len(self.Examples):
                search_bar = search_bar.format('')
            else:
                search_bar = search_bar.format("Top")
            WebDriverWait(
                driver,10).until(
                    EC.presence_of_element_located((
                        By.XPATH,search_bar))).send_keys(
                            i,Keys.ENTER)
            WebDriverWait(
                driver,10).until(
                    EC.presence_of_element_located((
                        By.XPATH,'''/html/body/div/main/div/div[2]/ul/li[3]/a'''))
                        ).click()
            example_box = (driver.find_element_by_xpath(
                '''/html/body/div[1]/main/div/div[3]/table[2]/tbody/tr/td''').text).split('\n')
            for o in range(0,len(example_box),2):
                if len(self.Examples) <= 10:
                    print("*Adding Example {}".format(str(num_Examples)))
                    try:
                        num_Examples += 1
                        self.Examples.update({example_box[o]:example_box[o+1]})
                    except IndexError:
                        break
                else:
                    print("there're 10 examples, can not add more")
                    break                          
    def save_MP3(self):
        directory = self.folder+"/mp3"
        '''turn mandarin to speech, and save in mp3
        default save directory: 
        /home/duriandan/learning/personal project/Anki card adding (Na's ma)/metadata/mp3'''
        tts = gTTS(self.word,lang="zh")
        tts.save(directory+"/"+self.word+".mp3")
    def save_stroke_oder(self):
        directory=self.folder+"/gif"
        '''Get Stroke order of every letter
        Default directory:
        /home/duriandan/learning/personal project/Anki card adding (Na's ma)/metadata/gif'''
        if self.word not in listdir(directory):
            mkdir(directory+"/"+self.word)
            print("directory {} is just added".format(self.word))
        else:
            print("Directory {} is already added".format(self.word))
        for char in self.word:
            print("*Getting stroke order of {}".format(char))
            driver.get('''http://www.strokeorder.info/mandarin.php?q={}'''.format(char))
            # get the image source
            img = driver.find_element_by_xpath('/html/body/div[1]/img')
            src = img.get_attribute('src')
            # download the image
            urllib.request.urlretrieve(src,directory+"/"+self.word+"/"+char+".gif")
'味道','酸','辣','咸','甜','苦','清淡','油腻','好吃','烹饪方式','煮','炖','炒','煎','烧烤','蒸','调味料','盐','醋','酱油','鱼酱','辣椒酱','胡椒粉','糖','番茄酱','油']:
for man in [
    mandarin1 = mandarin_json(man,'''/home/duriandan/learning/personal project/Anki card adding (Na's ma)/metadata''')
    mandarin1.get_Meaning_Pinyin_Example()
    mandarin1.get_Examples()
    mandarin1.get_HanViet()
    mandarin1.save_MP3()
    mandarin1.save_stroke_oder()
    if len(mandarin1.component_words) >1 and len(mandarin1.Examples) <= len(mandarin1.component_words):
        mandarin1.get_Examples_components()
    with open('''/home/duriandan/learning/personal project/Anki card adding (Na's ma)/metadata/pointer(json)/{}.txt'''.format(mandarin1.word),"w") as mandarin1text:
        for i in mandarin1.meanings:
            mandarin1text.write("* "+i+": "+mandarin1.meanings[i]+"\n")
        mandarin1text.write("________________________________\n")
        for i in mandarin1.pinyins:
            mandarin1text.write("* "+i+": "+mandarin1.pinyins[i]+"\n")
        mandarin1text.write("__________________________________\n")
        for i in mandarin1.Examples:
            mandarin1text.write("* "+i+": "+str(mandarin1.Examples[i])+"\n")
        mandarin1text.write("__________________________________\n")
        for i in mandarin1.HanViet:
            mandarin1text.write("* "+i+": "+str(mandarin1.HanViet[i])+"\n")
        mandarin1text.write("__________________________________\n")

