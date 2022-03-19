#!/usr/bin/env python
# coding: utf-8

# In[18]:


import smtplib
from email.message import EmailMessage
import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import datetime

# Parte de um projeto pessoal de lib para automações, não contem todas as funções.
import lib

src_folder = os.getcwd()[:os.getcwd().find("src") + 3]


# # MAIN
# Este bloco é responsável por executar o robô.

# In[16]:


def main():

    file_helper = lib.FileHelper

    # Procura arquivos de carga
    while True:
        
        try:
            new_mail_json = file_helper(fr"{src_folder}\SEND_MAIL\Entrance").get_oldest("*.json")
        except lib.NoFileFound:
            time.sleep(5)
            continue
    
        # Instancia classe de manipulação do arquivo .json
        new_mail_json_helper = file_helper(new_mail_json)
        
        # Json para dicionário
        with open(new_mail_json, 'r') as json_file:
            dict_new_mail = json.load(json_file)

        # Instancia classe do e-mail
        if any(True if not value else False for _, value in dict_new_mail["SENDER_CREDENTIALS"].items()):
            raise Exception("Sem credenciais do e-mail de envio.")

        email = Email(dict_new_mail["SENDER_CREDENTIALS"]["address"], dict_new_mail["SENDER_CREDENTIALS"]["password"])

        # Captura as ofertas de trabalho do dia
        job_offers_payload = get_todays_job_offers()
        
        # Cria planilha para envio
        df = pd.DataFrame(job_offers_payload)

        xlsx_name = create_file_name(dict_new_mail["EXPECTED_SHEET_NAME"])

        df.to_excel(xlsx_name)
        
        # Envia planilha para o e-mail solicitado
        email.send_email(subject=dict_new_mail["MESSAGE"]["subject"],
                         sender=dict_new_mail["SENDER_CREDENTIALS"]["address"],
                         receiver=dict_new_mail["MESSAGE"]["to"],
                         body=dict_new_mail["MESSAGE"]["body"],
                         attachments=[xlsx_name]
                        )
        email.disconect()

        new_mail_json_helper.move_to(fr"{src_folder}\SEND_MAIL\Sent")


# ## [Func] create_file_name()

# In[13]:


def create_file_name(expected_name:str) -> str:

    if not expected_name:
        return fr"{src_folder}\sheets_folder\available_job_offers_{datetime.datetime.now().strftime('%d%m%y%H%M%S')}.xlsx"

    if "\\" in expected_name:
        expected_name = expected_name.split("\\")[-1]

    if not expected_name.endswith(".xlsx"):
        expected_name = f"{expected_name}.xlsx"

    return fr"{src_folder}\sheets_folder\{expected_name}"


# ## [Func] get_todays_job_offers()

# In[14]:


def get_todays_job_offers(*, timeout=60) -> dict:
    
    # Configurações adicionais do webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("no-first-run")
    chrome_options.add_argument("no-default-browser-check")
    chrome_options.add_argument('--start-maximized')
    

    # Instancia driver
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service,
                              options=chrome_options)
    

    # Acessa plataforma Cadmus
    wait = WebDriverWait(driver, timeout)
    old_url = driver.current_url
    driver.get("https://cadmus.com.br/vagas-tecnologia/")
    wait.until(EC.url_changes(old_url))
    

    # Captura as informações
    payload = {
        "Nome": [],
        "Local": [],
        "Descrição": []
    }

    timer = lib.Timer(timeout)
    while timer.not_expired:
        try:
            div_pfolio = wait.until(EC.presence_of_element_located((By.ID, "pfolio")))
            box_divs = div_pfolio.find_elements(By.CLASS_NAME, "box")
            if len(box_divs) > 0:
                break
        except:
            pass
    else:
        raise Exception("Não conseguiu capturar os elementos das vagas.")

    for div in box_divs:
        
        name = driver.execute_script("return arguments[0].getElementsByTagName('h3')[0].innerText;", div)
        payload["Nome"].append(name)
        work_place = driver.execute_script("return arguments[0].getElementsByClassName('local')[0].innerText;", div)
        payload["Local"].append(work_place)

    for idx, value in enumerate(payload["Nome"]):

        box_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "box")))
        box = next((b for b in box_divs if value in b.get_attribute("innerText")), None)
        driver.execute_script("arguments[0].getElementsByTagName('a')[0].click();", box)
        div_vaga = wait.until(EC.presence_of_element_located((By.ID, "boxVaga")))
        job_description = driver.execute_script("return arguments[0].getElementsByTagName('p')[0].innerText;", div_vaga)
        normalized_job_description = lib.string_normalizer(job_description, remove_break_lines=True)
        payload["Descrição"].insert(idx, normalized_job_description)
        driver.back()
        wait.until(EC.presence_of_element_located((By.ID, "pfolio")))

    return payload


# ## [Class] send_email()

# In[15]:


class Email:

    def __init__(self, address:str, password:str):
        self.smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        self.smtp.login(address, password)

    def send_email(self, *, subject:str, sender:str, receiver:list, body:str, attachments:list=[]):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver
        msg.set_content(body)
        for file in attachments:
            with open(file, "rb") as f:
                file_data = f.read()
                file_name = f.name
            if "\\" in file_name:
                file_name = file_name.split("\\")[-1]
            msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
        self.smtp.send_message(msg)
    
    def disconect(self):
        self.smtp.close()


# In[ ]:


if __name__ == '__main__':
    main()