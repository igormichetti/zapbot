import time
import os
import sys
import warnings
import random
import coinmarketcapapi #API MODULE
from dotenv import load_dotenv #ENVARIOMENT VARIABLES LIB
from selenium import webdriver #AUTOMATIZATION LIB
from webdriver_manager.chrome import ChromeDriverManager #MODULE FOR CHROME
from selenium.webdriver.common.keys import Keys #SPECIAL KEYS MODULE
from selenium.common import exceptions  

#SETING ENV VARIABLES
load_dotenv()
CHROME_PATH = os.environ.get('CHROME_PATH')

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
IS_DEBUG = False 


def loading(message, lines=3, dots=3, speed = 200/1000): 
    print(message, '\n')
    for i in range(0,lines):
        for i in range(0,dots):
            sys.stdout.write('.'+' ')
            sys.stdout.flush()
            time.sleep(speed)
        print('\n')
        
def send_msg(msg):
    campoMensagem = driver.find_elements_by_css_selector("div[contenteditable='true']")[1]
    campoMensagem.click()
    time.sleep(1)
    campoMensagem.send_keys(msg) 
    time.sleep(1)
    campoMensagem.send_keys(Keys.ENTER)

def read_msg(user, log_msg, log_time, x):
  l = -1
  new_log_msg = []
  new_log_time = []
  all_msgs = []
  for n in range(0,x):
    new_log_msg.append(log_msg[l])
    new_log_time.append(log_time[n*(-1)-1])
    l -= 2
  new_log_msg.reverse()
  new_log_time.reverse()   
  for msg in new_log_msg:
      if '@zapbot' in msg:
          all_msgs.append(msg)
  all_msgs = (' '.join(all_msgs))
  all_msgs = all_msgs.split()
  all_msgs = list(filter(lambda a: a != '@zapbot', all_msgs))
  print('Mensagens recebidas: ', all_msgs)
  return all_msgs

def call_faq(user_response):
    bot_response = ''
    user_response=user_response.lower()
    while True:
        
        if(not isEnding(user_response)):
            if(isThanks(user_response)):
                bot_response = "Disponha. Estou aqui para lhe ajudar."
                break
            else:
                if(greeting(user_response) != None):
                    bot_response = greeting(user_response)
                    break
                else:
                    # In case its a valid coin.
                    if user_response in coinmarketcapapi.get_coins():
                        bot_response = coinmarketcapapi.get_info(user_response)
                        break
        else:
            bot_response = "Até mais!"
            break
    return bot_response        

def user_find(name='afk'):
    search_tab = driver.find_elements_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
    search_tab = search_tab[-1]
    search_tab.click()
    time.sleep(1)
    search_tab.send_keys(name) 
    time.sleep(1)
    search_tab.send_keys(Keys.ENTER)
    
def greeting(sentence):
    saudacoes = ("olá", "oi", "ei", "blz", "bom dia", "boa tarde", "boa noite")
    respostas = ["Oi", "Olá"]
    for word in sentence.split():
        if word.lower() in saudacoes:
            return random.choice(respostas)

def isThanks(sentence):
    agradecimentos = ("obrigado", "muito obrigado", "obrigada", "muito obrigada", "agradecido", "agradecida", "vlw", "obg")
    for word in sentence.split():
        if word.lower() in agradecimentos:
            return True
    return False

def isEnding(sentence):
    despedidas = ("tchau", "até logo", "fui", "adeus", "até mais")
    for word in sentence.split():
        if word.lower() in despedidas:
            return True
    return False


# Open Whatsapp Web
options = webdriver.ChromeOptions() 
options.add_argument(CHROME_PATH) #Path to your chrome profile
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
loading('Acessando o WhatsApp Web', 4, 4)
driver.get('https://web.whatsapp.com/')
time.sleep(10) #Wait for connection

# Variables

i = True
log_msg = []
a = 0
user_msg = ''

if __name__ == '__main__':

    while True:
        contatos = driver.find_elements_by_css_selector("span[aria-label]") ##LIST of NON-READ-MESSAGES BOXES
        for contato in contatos:    
            try:
               time.sleep(5)
               contato.click()
               username = driver.find_elements_by_xpath('//*[@id="main"]/header/div[2]/div[1]/div/span') #CONTACT NAME by TITLE
               user = username[0].text
               nrm = int(contato.text)  ##NUMBER of NON-READ-MESSAGES by User
               print(f'\nMensagens nao lidas de {user}: {nrm}')
               tim_msg = driver.find_elements_by_class_name("kOrB_") ##LIST of elements of MESSAGE-TIME
               log_time = []        ##LIST of MESSAGE-TIME in STR FORMAT
               for t in tim_msg:
                   log_time.append(t.text)
               all_msg = driver.find_elements_by_css_selector(".copyable-text") ##LIST of elements of MESSAGE
               last_msg = all_msg[-2]
               for n, msg in enumerate(all_msg):
                   if msg != last_msg:
                      message = all_msg[n].text
                      log_msg.append(message)
                   else:
                      break 
               user_responde = read_msg(user, log_msg, log_time, nrm)
               for m in user_responde:
                       user_msg = m
                       print('user: ', user_msg)
                       bot_msg = call_faq(user_msg)
                       time.sleep(2)
                       print('bot :', bot_msg)
                       send_msg(bot_msg)
            except exceptions.StaleElementReferenceException:
                continue
            except:
                print('...')
                user_find() 
                time.sleep(5)
                continue


