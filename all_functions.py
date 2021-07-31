from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from googletrans import Translator
from gtts import gTTS
from os import listdir,mkdir
import urllib.request

options = Options()
options.page_load_strategy = 'none'
driver = webdriver.Chrome(options=options)

translator = Translator()

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
        #2.get all the meaning,example and pinyin metadata
        try:
            #2.1 the meaning found on website
            self.meanings.update({self.word:driver.find_element_by_xpath(
                '''/html/body/div/main/div/div[3]/table[1]/tbody/tr[1]/td[2]''').text})
            self.pinyins.update({self.pinyins:driver.find_element_by_xpath(
                '''/html/body/div/main/div/div[3]/div[1]/div/span'''
            ).text})
            print("* got meaning and pinyin of the word (first_try)")
            (driver.find_element_by_xpath(
                '''/html/body/div/main/div/div[2]/ul/li[3]/a''')).click()
            example_box = (driver.find_element_by_xpath(
                '''/html/body/div[1]/main/div/div[3]/table[2]/tbody/tr/td''').text).split('\n')
            num_example = 0
            for i in range(0,len(example_box),2):
                if len(self.Examples) <= 10:
                    num_example += 1
                    print("*Adding Example {}".format(str(num_example)))
                    self.Examples.update({example_box[i]:example_box[i+1]})
                else:
                    print("there're 10 examples, can not add more")
                    break
            print("* got the examples of the whole word")
        except NoSuchElementException:
            #2.2 had to devide into multiple letters to find meaning
            print("* coudn't find examples on yellowbridge.com")
            print("""* Couldn't find meaning of whole word,
                        finding the meaning of component words...""")
            self.meanings.update({
                self.word:translator(self.word,dest="en",src="zh").text
            })
            print("* got the google translated meaning")
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
        '''get examples on se
        https://www.chineseboost.com/chinese-example-sentences?query'''
        driver.get("""https://www.chineseboost.com/chinese-example-sentences?query={}""".format(self.word))
        num_example = len(self.Examples)
        for i in range(2,12):
            num_example +=1
            if len(self.Examples) >10:
                print("there're 10 examples, can not add more")
                break
            print("Adding Example {}".format(str(num_example)))
            example_box_text = driver.find_element_by_xpath(
                '''/html/body/div[2]/div[{}]/div/div'''.format(str(i))).text.split("\n")
            self.Examples.update({example_box_text[0]:
            [example_box_text[1],example_box_text[2]]})
        driver.quit()
    def save_MP3(self,directory = self.folder+"/mp3"):
        '''turn mandarin to speech, and save in mp3
        default save directory: 
        /home/duriandan/learning/personal project/Anki card adding (Na's ma)/metadata/mp3'''
        tts = gTTS(self.word,lang="zh")
        tts.save(directory+"/"+self.word+"mp3")
    def save_stroke_oder(self,directory=self.folder+"/gif"):
        '''Get Stroke order of every letter
        Default directory:
        /home/duriandan/learning/personal project/Anki card adding (Na's ma)/metadata/gif'''
        if self.word not in listdir(directory):
            mkdir(directory+"/"+self.word)
            print("directory {} is just added".format(self.word))
        else:
            print("Directory is already added")
        for char in self.word:
            print("*Getting stroker order of {}".format(char))
            driver.get('''http://www.strokeorder.info/mandarin.php?q={}'''.format(char))
            # get the image source
            img = driver.find_element_by_xpath('/html/body/div[1]/img')
            src = img.get_attribute('src')
            # download the image
            urllib.request.urlretrieve(src,directory+"/"+self.word+"/"+char+".gif")
        driver.quit()


test1 = mandarin_json('烹饪方式')
test1.get_Meaning_Pinyin_Example()
test1.get_HanViet()
test1.get_Examples()
test1.save_MP3()
test1.save_stroke_oder()

