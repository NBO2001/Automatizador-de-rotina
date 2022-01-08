from tkinter.constants import TRUE
from utils import add_box, alert_remove, element_is_load, is_exists_uep,get_table, add_values_in_dictionary
from utils import save_button, insert_arq_log, driving_to_box, add_folders, add_informations, trim

from time import sleep

def add_item(instance,data, app=False):

    moni = {
        data['index'] : {}
    }

    try:
        instance.driver.get(f'{instance.get_urlBase()}#/modules/pack/create')
        sleep(2)
        
        if not is_exists_uep(data['index']):
            app.situation(f'Envindo a caixa: {data["index"]}') if app else print(f'Envindo a caixa: {data["index"]}') 
            add_box(instance, data['galpao'], data['prateleira'], data['index'], data['client'])
            save_button(instance,True)
            alert_remove(instance)
            moni[data['index']]['isADD'] = True
        else:
            moni[data['index']]['isADD'] = False
        
        moni[data['index']]['link'] = driving_to_box(instance, data['index'])

        moni['link'] = (moni[data['index']]['link'])

        element_is_load(instance,"//mat-card/div/div[3]/mat-form-field[3]/div/div[1]/div/mat-select")

        try:
           boxs_add = add_folders(instance,data['boxs'],app)
        except Exception as error:
            insert_arq_log(f'{error}')
            return False
        table_conteinner = instance.driver.find_element_by_xpath("//app-pack-itens/mat-card/div/div[2]/mat-table")

        table = get_table(table_conteinner)

        datas = add_values_in_dictionary(table)
        send_infos = list()
        try:
            for box in data['boxs']:

                for dt in datas:
                    if trim(dt['index']) == box['index']:
                        instance.driver.get(f'{instance.get_urlBase()}{dt["link"]}')
                        sleep(2)
                        depart = box["department"]
                        subject = box["subject"]
                        indexing = box["indexing"]

                        try:
                            date_start = f'{box["date_start"].month}/{box["date_start"].day}/{box["date_start"].year}'
                        except Exception as error:
                            date_start = box["date_start"].split("/")
                            date_start = f'{date_start[1]}/{date_start[0]}/{date_start[2]}'

                        try:
                            date_end = f'{box["date_end"].month}/{box["date_end"].day}/{box["date_end"].year}'
                        except Exception as error:
                            date_end = box["date_end"].split("/")
                            date_end = f'{date_end[1]}/{date_end[0]}/{date_end[2]}'

                        if box['obs']:
                            obs = box["obs"]
                        else:
                            obs = ""
                        
                        app.situation(f'Adicionando informações a pasta: {box["index"]}') if app else print(f'Adicionando informações a pasta: {box["index"]}') 
                        add_informations(instance,depart, subject, indexing, date_start, date_end, obs)
                        save_button(instance, True)
                        alert_remove(instance)
                        send_infos.append(box["index"])
                    
            instance.driver.get(f'{instance.get_urlBase()}#/modules/home')
        except Exception as error:
            insert_arq_log(f'{error}')
            listDel = list()
            for sends in send_infos:
                del boxs_add[sends]

            for inx in boxs_add:
                listDel.append(inx)

            moni['Error'] = True
            moni[data['index']]['dell'] = listDel
            insert_arq_log(f'{listDel}')
            
            return moni
    except Exception as error:
        insert_arq_log(f'{error}')
        moni['Error'] = True
        
        return moni
    else:
        moni['Error'] = False
        
        return moni 