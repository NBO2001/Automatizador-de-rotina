from utils import get_table, add_values_in_dictionary
from login import Login
from time import sleep

def undoing(instance,item, app=False):
    del item['Error']
    ky = item

    for k in ky:
        link = ky[k]['link']
        sleep(3)
        instance.driver.get(f'{instance.get_urlBase()}{link}')
        sleep(3)
        for itn in ky[k]['dell']:
            table_conteinner = instance.driver.find_element_by_xpath("//app-pack-itens/mat-card/div/div[2]/mat-table")

            table = get_table(table_conteinner)

            datas = add_values_in_dictionary(table)
            row = 1

            for dt in datas:
                if dt['index'] == itn:
                    
                    app.situation(f'Apgando: {itn}') if app else  print(f'dell {itn} in row:{row}')
                   
                    dell_in = instance.driver.find_element_by_xpath(f'//app-pack-itens/mat-card/div/div[2]/mat-table/mat-row[{row}]/mat-cell[3]/button[2]')
                    dell_in.click()
                    sleep(1)
                    file_diag = instance.driver.find_element_by_xpath(f'//mat-dialog-container/app-dialog/div/mat-dialog-actions/button[2]')
                    file_diag.click()
                    sleep(2)
                row +=1
