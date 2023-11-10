import time, datetime, os, re, sys, warnings
from selenium import webdriver #AUTOMATIZATION LIB
from selenium.webdriver.common.keys import Keys #SPECIAL KEYS MODULE
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

#SETING ENV VARIABLES
CHROME_PATH = r'C:\Users\miche\AppData\Local\Google\Chrome\User Data\Default'
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
IS_DEBUG = True

def loading(message, lines=3, dots=3, speed = 200/1000): 
    print(message, '\n')
    for _ in range(0,lines):
        for _ in range(0,dots):
            sys.stdout.write('.'+' ')
            sys.stdout.flush()
            time.sleep(speed)
        print('\n')
        
def send_msg(msg):
    driver.implicitly_wait(2)
    campoMensagem = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')
    campoMensagem.click()
    for m in msg:
        campoMensagem.send_keys(m) 
        time.sleep(0.5)        
        campoMensagem.send_keys(Keys.ENTER)
        time.sleep(1)        

def isEnquete(row):
    if ('/11' in row['Mensagem']):
        poll_data_container = '//*[@id="app"]/div/div/div[6]/span/div/span/div/div'

def get_toother_value_counts(messages:list) -> list:
    if messages:
        print(messages)
        df = pd.DataFrame.from_dict(messages)
        if df.empty:
            print('data from messages is empty')
            get_toother_value_counts(None)
    else:
        saved_tooths_path = 'data/libertadores_do_tooth.xlsx'
        if not os.path.isfile(saved_tooths_path):
            return None

        df = pd.read_excel(saved_tooths_path)
        if df.empty:
            print('eita')
            return None
    # Get the value_counts sorted descending for the 'Toother' column
    if isinstance(df, pd.DataFrame):
        print('\nColunas:', list(df.columns))
        toother_value_counts = df.value_counts('Toother', ascending=False)

        # Return the top names that are repeats in some rows of the excel sheet
        header = '   Top Toother  |  No.Tooths'
        message_to_send = ['Placar Libertadores do Tooth', header]
        for position, (i, v) in enumerate(toother_value_counts.items(), start=1):
            row = f'{str(position)}.   {i}           {str(v)}'
            message_to_send.append(row)
        return message_to_send
    

def convert_time(timestr):
    time_format = '%H:%M %p, %d/%m/%Y'
    return datetime.datetime.strptime(timestr, time_format)


def save_messages(messages, filename='data/libertadores_do_tooth.xlsx'):
    # Create or open the Excel file
    df = pd.DataFrame.from_dict(messages)
    if not df.empty:
        df.to_excel(filename)
    return None

def parse_message_string(message_string):
    # Remove the square brackets and split the string into time_date and sender
    message_string = message_string.translate(str.maketrans('','','[],'))  # Expected output: "8:09 PM, 07/11/2023 Igor Michetti"
    message_split = message_string.split(" ")
    daytime = ' '.join(message_split[:2])
    date = message_split[2]
    dt_str = f'{daytime}, {date}'
    sender_list = message_split[3:-1]
    if isinstance(sender_list, list):
        sender = ' '.join(message_split[3:-1])
    else: sender = sender_list
    sender = sender.translate(str.maketrans('','',':'))
   
    return dt_str, sender

def get_diff(saved_messages: pd.DataFrame, new_messages: pd.DataFrame) -> pd.DataFrame:
    if not saved_messages.empty and isinstance(saved_messages, pd.DataFrame):
        rows_to_delete = new_messages.eq(saved_messages).all(axis=1)
        return new_messages.drop(rows_to_delete[rows_to_delete == True].index)

def get_date_poll(input_text):
    # Define a regex pattern to match the unwanted parts
    pattern = re.compile(r'Enquete enviada por (\w+ \d+:\d+ [APMapm]{2} \d+/\d+ )Opções mais votadas: ')

    # Use the regex pattern to replace the unwanted parts with an empty string
    cleaned_text = re.sub(pattern, r'\1', input_text)
    listed_text = cleaned_text.split(' ')
    return [p for p in listed_text if '/' in p]

def is_checkbox(element):
    if element.get_attribute("type"):
        return "checkbox" in element.get_attribute("type")
    else:
        return False

def is_poll(container, text):
    if '/11' not in text:
        return
    substring = "Enquete enviada por"
    if poll := container.find_element(
        By.XPATH, f".//*[@aria-label[contains(., '{substring}')]]"
    ):
        aria_label = poll.get_attribute('aria-label')
        mostrar_votos = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[title='Mostrar votos']")))
        if mostrar_votos and not is_checkbox(mostrar_votos):
            mostrar_votos.click()
        poll_info_container = driver.find_element(By.CSS_SELECTOR, "[class$='bs7a17vp']")
        poll_rows = poll_info_container.find_elements(By.CSS_SELECTOR, "[class$='gx1rr48f']")
        poll_tooths = []
        voted = []
        for n, row in enumerate(poll_rows):
            row_names = row.find_elements(By.CSS_SELECTOR, ".ggj6brxn.gfz4du6o.r7fjleex.g0rxnol2.lhj4utae.le5p0ye3.enbbiyaj._11JPr")
            row_tooths = [r.get_attribute('title') for r in row_names if row_names]
            row_tooths = [{r : n} for r in row_tooths if r not in voted]
            voted.append([r for r in row_tooths if r not in voted])
            if row_tooths:
                print(f'\n{n}: {row_tooths[0]}')
                poll_tooths.append(row_tooths[0])

        poll_results = {get_date_poll(aria_label)[0] : poll_tooths}
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='button'][aria-label='Fechar']")))
        # Perform the click action
        close_button.click()
        return poll_results
    
if __name__ == '__main__':
    # Open Whatsapp Web
    options = webdriver.ChromeOptions()
    options.add_argument(r"user-data-dir=C:\Users\miche\AppData\Local\Google\Chrome\User Data\Default")
    driver = webdriver.Chrome(executable_path=r"C:\Users\miche\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe", chrome_options=options)
    loading('Acessando o WhatsApp Web', 8, 8)
    driver.get('https://web.whatsapp.com/')
    grupo = WebDriverWait(driver, 20)\
        .until(EC.visibility_of_element_located((By.XPATH,'//*[@id="pane-side"]/div/div/div/div[1]/div/div')))
    if not is_checkbox(grupo):
        grupo.click()
    time.sleep(2)  # Adjust the sleep duration as needed
    c = 0
    # Continuously check for new messages
    while True:
        total_polls = []
        c += 1
        main_container = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'main')))
        if not is_checkbox(main_container):
            main_container.click()
        # Use ActionChains to press and hold the HOME key, then sleep for 2 seconds, and release the key
        actions = ActionChains(driver)
        actions.key_down(Keys.HOME).perform()
        time.sleep(2)  # Adjust the sleep duration as needed
        actions.key_up(Keys.HOME).perform()

        # Wait for message containers to appear
        containers = WebDriverWait(main_container, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "CzM4m")))
        # Iterate through message containers
        all_messages = []
        for n, container in enumerate(containers):
            time.sleep(0.2)
            # Extract data-pre-plain-text attribute
            print('n', n)
            if n < 3: continue
            focusable_list_items = container.find_element(By.CSS_SELECTOR, '.focusable-list-item')
            data_pre_plain_text = focusable_list_items.find_element(By.CLASS_NAME, 'copyable-text').get_attribute('data-pre-plain-text')
            # Extract text from child span within the copyable-text div
            text_element = focusable_list_items.find_element(By.CSS_SELECTOR, '.copyable-text ._11JPr.selectable-text.copyable-text span')
            text = text_element.text
            if not text:
                if emoji_element := container.find_element(
                    By.CSS_SELECTOR, 'img[alt="💩"]'
                ):
                    text = emoji_element.get_attribute("data-plain-text")
                else:
                    text = '!! ? !!'

            if not is_poll(container, text):
                date_time, sender = parse_message_string(data_pre_plain_text)
                row = {'index': n-4,
                        'Data': date_time,
                        'Toother': sender,
                        'Mensagem': text}
                print(f'\n{n}: {row}')
                all_messages.append(row)

            else:
                print('is poll:',  is_poll(container, text))
                total_polls.append(is_poll(container, text))

        last_message = all_messages[-1]
        print('last message:', last_message)
        message_to_send = str(total_polls)
        print('\nmessage to send ', message_to_send)
        if message_to_send:
            save_messages(all_messages, 'data/all_messages.xlsx')
            if last_message['Mensagem'] == '/placar':
                    send_msg(message_to_send)
                    print('Mensagem enviada:', sum(total_polls))

        print('total pools', total_polls)
        print(all_messages)
        time.sleep(20)