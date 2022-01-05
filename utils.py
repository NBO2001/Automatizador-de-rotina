from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from seach_box import Seach_Box
from time import sleep
import os
from pathlib import Path
from os import path
from os import mkdir
import json
from os import walk
from os import path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sys import platform
from datetime import datetime

def trim(value):
    try:
        return ((value).lstrip()).rstrip()
    except:
        return value

#Verifica se o arquivo existe
def file_is_exists(location):
    return Path(location).is_file()


def get_index(table, value):
    
    for n in range(0, len(table)):
        if (((table[n].span.get_text()).replace(" ", "")).upper())  == (value.replace(" ", "")).upper() :
            return n+1
            
    return 1


def create_json(arq_name,dictionary):
    with open(f'{arq_name}.json', 'w', encoding='utf-8') as fp:
        json.dump(dictionary, fp, ensure_ascii=False, indent=2)


def reading_json(name):
    with open(f'{name}.json', encoding='utf-8') as fp:
        data = json.load(fp)
    
    return data

    
def save_button(instance, validate = False):

    if validate:
        element_is_clickable(instance,"//div[@class='actions']/div[2]/button")

    button_save = instance.driver.find_element_by_xpath("//div[@class='actions']/div[2]/button")
    button_save.click()


def options_fil(instance, indx):
    dep = f'mat-option[{indx}]'
    options_department = instance.driver.find_element_by_xpath("//div[@class='cdk-overlay-pane']/div/div/" + dep)
    return options_department

def option_select(instance, value):

    return options_fil(instance, seach_index(instance, value))


def seach_index(instance, value):
    overlay_pane = instance.driver.find_element_by_xpath("//div[@class='cdk-overlay-pane']/div/div")

    return get_index(get_table(overlay_pane, "mat-option"), value)


def add_informations(instance, depart, subj, indx, data_start, data_end, note_v=""):

    department = instance.driver.find_element_by_xpath("//mat-card/div/div[2]/mat-form-field[4]/div/div[1]/div/mat-select")
    department.click()

    option_select(instance, depart).click()

    subject = instance.driver.find_element_by_xpath("//mat-card/div/div[3]/mat-form-field/div/div[1]/div/input")
    subject.send_keys(subj)

    indexing = instance.driver.find_element_by_xpath("//mat-card/div/div[4]/mat-form-field[1]/div/div[1]/div/input")
    indexing.send_keys(indx)

    start = instance.driver.find_element_by_xpath("//mat-card/div/div[4]/mat-form-field[2]/div/div[1]/div/input")
    start.send_keys(data_start)
    
    end = instance.driver.find_element_by_xpath("//mat-card/div/div[4]/mat-form-field[3]/div/div[1]/div/input")
    end.send_keys(data_end)

    note = instance.driver.find_element_by_xpath("//mat-card/div/div[5]/mat-form-field[1]/div/div[1]/div/input")
    note.send_keys(note_v)


def add_box(instance, galpao, prateleira, code, client):

    input_galpao = instance.driver.find_element_by_xpath("//mat-card/div/div[1]/mat-form-field[1]/div/div[1]/div/mat-select")
    input_galpao.click()

    try:
        option_select(instance, galpao).click()
    except:
        sleep(2)
        input_galpao.click()
        option_select(instance, galpao).click()

    input_prateleira= instance.driver.find_element_by_xpath("//mat-card/div/div[1]/mat-form-field[2]/div/div[1]/div/mat-select")
    input_prateleira.click()

    try:
        option_select(instance,prateleira).click()
    except:
        sleep(2)
        input_prateleira.click()
        option_select(instance,prateleira).click()

    input_cod = instance.driver.find_element_by_xpath("//mat-card/div/div[3]/mat-form-field[1]/div/div[1]/div/input")
    input_cod.clear()
    input_cod.send_keys(code)

    input_client= instance.driver.find_element_by_xpath("//mat-card/div/div[3]/mat-form-field[3]/div/div[1]/div/mat-select")
    input_client.click()

    try:
        option_select(instance, client).click()
    except:
        input_client.send_keys(Keys.RETURN)
        option_select(instance, client).click()

    return True

def get_table(table_conteinner, element="mat-row"):

    table_html = table_conteinner.get_attribute('outerHTML')

    table_bea = BeautifulSoup(table_html, "html.parser")

    table_s = table_bea.find_all(element)

    return table_s


def get_link(instance):
    table_conteinner = instance.driver.find_element_by_xpath("//div[@class='table-container']/mat-table")

    rows = get_table(table_conteinner)[0].find_all("mat-cell")

    link = rows[0].a['href']
    
    return link


def driving_to_box(instance, code):
    instance.driver.get(f'{instance.get_urlBase()}#/modules/pack')
    sleep(1)
    Seach_Box(instance, code)
    sleep(1)
    link = get_link(instance)
    instance.driver.get(f'{instance.get_urlBase()}{link}')
    return link

def add_folders(instance, boxs, app=False):
    input_code = instance.driver.find_element_by_xpath("//app-pack-itens/mat-card/div/div[1]/mat-form-field/div/div[1]/div/input")
    button_code = instance.driver.find_element_by_xpath("//app-pack-itens/mat-card/div/div[1]/div/button")
    boxs_send = dict()
    for box in boxs:
        app.situation(f'Envindo a pasta: {box["index"]}') if app else print(f'Envindo a pasta: {box["index"]}') 
        input_code.send_keys(f'{trim(box["index"])}')
        button_code.click()
        sleep(1)
        input_code.clear()
        alert_remove(instance)
        boxs_send[box["index"]] = []
    
    return boxs_send

def add_values_in_dictionary(table):
    datas = list()
    
    dicty = dict()
    for tab in table:
        rows = tab.find_all("mat-cell")

        dicty = {
            "index": trim(rows[0].text),
            "link": trim(rows[0].a['href'])
        }

        datas.append(dicty.copy())

    return datas


def bea_json(folders, datas):
    for folder in folders:

        if trim(folders[folder]['type']) == "Caixa":
            
            datas[trim(folder)] = {}
            for attr in folders[folder]:    
                datas[trim(folder)][attr] = folders[folder][attr]
            
            datas[trim(folder)]["boxs"] = {}

        else:
            datas[trim(folder)[:-2]]['boxs'][trim(folder)] = {}

            temp = {}

            for attr in folders[folder]:    
                temp[attr]  = folders[folder][attr]
            
            datas[trim(folder)[:-2]]['boxs'][trim(folder)] = temp

    return datas

def create_folder(father_code, children={}, location="./"):

    if not path.exists(convert_url(f'{location}{father_code}')):
        mkdir(convert_url(f'{location}{father_code}'), 0o777)

    for kid in children:
        if not path.exists(convert_url(f'{location}{father_code}/{kid["index"]}')):
            mkdir(convert_url(f'{location}{father_code}/{kid["index"]}',), 0o777)
        
        create_json(convert_url(f'{location}{father_code}/{kid["index"]}/conf'), {
            "describe": "",
            "subject": ""
        })

# Modificar depois

def add_configuration():
    
    fileObj = Path(convert_url("./config/monitoration.json"))

    if fileObj.is_file():
        configurations = reading_json(convert_url('./config/monitoration'))
        configurations['scan'] = os.path.getmtime(convert_url("./scan.xlsx"))
        create_json(convert_url('./config/monitoration'), configurations)
    else:
        configurations = {}
        configurations['scan'] = os.path.getmtime(convert_url("./scan.xlsx"))
        create_json(convert_url('./config/monitoration'), configurations)

def retun_md(location):
    return path.getmtime(location)

def verify_folders(location="./"):
    
    lis = list()

    for  paths, subpath, files in walk(location):
        name = paths.split(separator())[1]

        if name != "config" and name != "":
            if len(subpath):
                
                lis.append({
                    "index": name,
                    "boxs": subpath
                })

    for li in lis:
        li['modification'] = path.getmtime(convert_url(f'./{li["index"]}'))
        temp = list()

        for box in li['boxs']:
            temp.append({
                box: path.getmtime(convert_url(f'./{li["index"]}/{box}'))
            })
        
        li['boxs'] = temp
        
        
    return lis


def is_exists_uep(seach):
    datas = reading_json(convert_url('./config/boxs'))
    for data in datas:
        if trim(data['index']) == trim(seach):
            return True
    return False


def reading_folders(link, list_it):
    
    create_folder(convert_url('./config/folders'))

    links = link.split('/')
    name = convert_url(f'./config/folders/{links[3]}')
    try:
        dtas = reading_json(name)
    except:
        dtas = dict()
    finally:
        dtas[link] = list_it
        create_json(name, dtas)

def convert_url(value):
    
    if platform.upper() == "LINUX":
        return value
    else:
        return "\\".join(value.split("/"))

def separator():
    
    if platform.upper() == "LINUX":
        return "/"
    else:
        return "\\"


def is_load_select(instance):
    try:
        WebDriverWait(instance.driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='cdk-overlay-pane']/div/div"))
        )
        
        return True
    except:
        
        return False


def element_is_load(instance, location, time_in=20):
    try:
        WebDriverWait(instance.driver, time_in).until(
            EC.presence_of_element_located((By.XPATH, location))
        )
        
        return True
    except:
        
        return False

def element_is_clickable(instance, location, time_in=20):
    try:
        WebDriverWait(instance.driver, time_in).until(
            EC.element_to_be_clickable((By.XPATH, location))
        )
        
        return True
    except:
        
        return False


def element_is_visibility(instance, location, time_in=10):
    try:
        WebDriverWait(instance.driver, time_in).until(
            EC.visibility_of_element_located((By.XPATH, location))
        )
        
        return True
    except:
        
        return False

def alert_remove(instance):
    if element_is_visibility(instance, "//simple-notifications/div/simple-notification/div"):
        try:
            instance.driver.find_element_by_xpath("//simple-notifications/div/simple-notification/div").click()
            return True
        except:
            return False

def insert_arq_log(texto):
    
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if file_is_exists(convert_url("./config/app.log")):
        file = open(convert_url("./config/app.log"), 'a')
        file.write(f'{date} : {texto} \n')
        file.close()
    else:
        file = open(convert_url("./config/app.log"), 'w')
        file.write(f'{date} : {texto} \n')
        file.close()
                