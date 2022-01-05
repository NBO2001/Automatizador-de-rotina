from time import sleep
import os
from scrapping_boxs import scan_items_in_sys
from utils import element_is_load, reading_folders, verify_folders

from file_monitoration import folder_is_change
from utils import  create_json, reading_json, file_is_exists, convert_url

# Verifica se teve mundaça

def conf_file_upload():

    change, location = folder_is_change()

    upes = reading_json(convert_url('./config/boxs'))

    list_t = list()

    for uep in upes:

        for local in location:

            if uep['index'] == local['index']:

                for bx in uep['boxs']:

                    if bx['index'] == local['box']:

                        list_t.append({
                            "index": uep['index'],
                            "index_box": bx['index'],
                            "id": (bx['link'].split("/")[(len(bx['link'].split("/"))-1)]),
                            "link": bx['link']
                        })

    create_json(convert_url('./config/upload'), list_t)





def up_files(instance, speed, app=False):
    app.situation(f'Lendo arquivos de configuração ...')  if app else print(f'Lendo arquivos de configuração ...')
    upload = reading_json(convert_url('./config/upload'))

    list_up = list()

    for upl in upload:
    
        control_items = reading_json(convert_url(f'./config/folders/{upl["id"]}'))

        instance.driver.get(f'{instance.get_urlBase()}{upl["link"]}')
        element_is_load(instance,"//mat-card/div/div[3]/mat-form-field[1]/div/div[1]/div/input", time_in=60)
        element_is_load(instance,"//mat-table/mat-row[1]/mat-cell[5]/label/input", time_in=60)

        row = 1  

        time_wait = 0
        
        for control in control_items[upl["link"]]:
            
            if control['upload'] == "none":
                location = convert_url(f'{os.getcwd()}/{upl["index"]}/{upl["index_box"]}/{control["name"]}.pdf')
                if not file_is_exists(location):
                    location = convert_url(f'{os.getcwd()}/{upl["index"]}/{upl["index_box"]}/{control["name"]}.PDF')

                list_up.append(control["name"])
                
                time_wait += os.path.getsize(location)

                time_item = (((os.path.getsize(location))/1048576)/speed) * 4

                app.situation(f'Enviando {control["name"]}')  if app else print(f'Enviando {control["name"]}')

                input_file = instance.driver.find_element_by_xpath(f'//mat-table/mat-row[{row}]/mat-cell[5]/label/input')

                input_file.send_keys(location)

                # Timer
                if time_item:
                    staps = time_item/time_item
                    while time_item:
                        app.situation(f'Enviando {control["name"]}... \n Velocidade da internet {speed:.2f} MB/S \nPrevisão de upload: {(time_item):.2f}s , aguarde ...')  if app else print(f'Enviando, previsão de upload em {time_wait}s , aguarde ...') 
                        
                        sleep(staps)

                        time_item = time_item - staps

                        if time_item <= 0:
                            break
            row +=1  

        time_wait = (time_wait/1048576)/speed
        
        if time_wait:
            stps = time_wait/time_wait
            while time_wait:

                app.situation(f'Enviando id: {upl["id"]}... \n Velocidade da internet {speed:.2f} MB/S \nPrevisão de upload: {(time_wait/60):.2f}m , aguarde ...')  if app else print(f'Enviando, previsão de upload em {time_wait}s , aguarde ...') 
                sleep(stps)

                time_wait = time_wait - stps

                if time_wait <= 0:
                    break

        instance.driver.get(f'{instance.get_urlBase()}#/modules/home')
        sleep(1)
        instance.driver.get(f'{instance.get_urlBase()}{upl["link"]}')
        app.situation(f'Aguardando o carregamento da página ...')  if app else print(f'Aguardando o carregamento da página...')
        element_is_load(instance,"//mat-card/div/div[3]/mat-form-field[1]/div/div[1]/div/input", time_in=7200)
        app.situation(f'Arquivos enviados ...')  if app else print(f'Arquivos enviados ...')
        sleep(3)
        app.situation(f'Scanneando items...')  if app else print(f'Scanneando items ...')
        dt = scan_items_in_sys(instance)
        
        app.situation(f'Escrevendo mudanças...')  if app else print(f'Escrevendo mudanças...')
        reading_folders(upl["link"], dt )

        instance.driver.get(f'{instance.get_urlBase()}#/modules/home')
        sleep(5)

    if not len(list_up):
        app.situation("Pegando as informações das pastas ... ") if app else print("Pegando as informações das pastas ... ")
        create_json(convert_url("./config/folders"), verify_folders(convert_url('./')))
        return True
    else:
        return False  