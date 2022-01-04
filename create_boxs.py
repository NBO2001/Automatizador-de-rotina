from utils import add_box, alert_remove, element_is_load, is_exists_uep
from time import sleep
from utils import save_button, element_is_clickable,element_is_visibility
from utils import driving_to_box
from utils import add_folders
from utils import option_select
from utils import get_table
from utils import add_values_in_dictionary
from utils import add_informations
from utils import trim


def add_item(instance,data, app=False):

    instance.driver.get(f'{instance.get_urlBase()}#/modules/pack/create')
    sleep(2)
    
    if not is_exists_uep(data['index']):
        app.situation(f'Envindo a caixa: {data["index"]}') if app else print(f'Envindo a caixa: {data["index"]}') 
        add_box(instance, data['galpao'], data['prateleira'], data['index'], data['client'])
        save_button(instance,True)
        alert_remove(instance)

    
    driving_to_box(instance, data['index'])

    element_is_load(instance,"//mat-card/div/div[3]/mat-form-field[3]/div/div[1]/div/mat-select")
    add_folders(instance,data['boxs'],app)

    table_conteinner = instance.driver.find_element_by_xpath("//app-pack-itens/mat-card/div/div[2]/mat-table")

    table = get_table(table_conteinner)

    datas = add_values_in_dictionary(table)

    for box in data['boxs']:

        for dt in datas:
            if trim(dt['index']) == box['index']:
                instance.driver.get(f'{instance.get_urlBase()}{dt["link"]}')
                print("Comecar spl 2, Row 40")
                sleep(2)
                depart = box["department"]
                subject = box["subject"]
                indexing = box["indexing"]

                date_start = box["date_start"].split("/")
                date_start = f'{date_start[1]}/{date_start[0]}/{date_start[2]}'

                date_end = box["date_end"].split("/")
                date_end = f'{date_end[1]}/{date_end[0]}/{date_end[2]}'

                if box['obs']:
                    obs = box["obs"]
                else:
                    obs = ""
                app.situation(f'Envindo a pasta: {box["index"]}') if app else print(f'Envindo a pasta: {box["index"]}') 
                add_informations(instance,depart, subject, indexing, date_start, date_end, obs)
                save_button(instance, True)
                alert_remove(instance)

    instance.driver.get(f'{instance.get_urlBase()}#/modules/home')