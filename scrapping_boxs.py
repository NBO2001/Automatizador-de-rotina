from time import sleep
from utils import element_is_load, get_table, add_values_in_dictionary,trim

def scrapping_b(instance, links):
    base_url = instance.get_urlBase()
    dic_values = dict()

    lista_values = list()

    for link in links:

        instance.driver.get(f'{base_url}{link}')
        
        if not element_is_load(instance, "//mat-card/div/div[1]/mat-form-field[3]/div/div[1]/div/mat-select/div/div[1]/span/span"):
            return False
            
        input_local = instance.driver.find_element_by_xpath("//mat-card/div/div[1]/mat-form-field[1]/div/div[1]/div/input")
        local = input_local.get_attribute("value")

        input_galpao = instance.driver.find_element_by_xpath("//mat-card/div/div[1]/mat-form-field[2]/div/div[1]/div/mat-select/div/div[1]/span/span")
        galpao = input_galpao.get_attribute("innerHTML")

        input_prateleira = instance.driver.find_element_by_xpath("//mat-card/div/div[1]/mat-form-field[3]/div/div[1]/div/mat-select/div/div[1]/span/span")
        prateleira = input_prateleira.get_attribute("innerHTML")
        
        input_code= instance.driver.find_element_by_xpath("//mat-card/div/div[3]/mat-form-field[1]/div/div[1]/div/input")
        _code = input_code.get_attribute("value")

        input_type = instance.driver.find_element_by_xpath("//mat-card/div/div[3]/mat-form-field[2]/div/div[1]/div/mat-select/div/div[1]/span/span")
        _type = input_type.get_attribute("innerHTML")

        input_customer = instance.driver.find_element_by_xpath("//mat-card/div/div[3]/mat-form-field[3]/div/div[1]/div/mat-select/div/div[1]/span/span")
        _customer = input_customer.get_attribute("innerHTML")

        dic_values = {
            'index': _code,
            'link': link,
            'type': _type,
            'local': local,
            'galpao': galpao,
            'prateleira':prateleira,
            'client': _customer
        }
        
        sleep(2)
        table_conteinner = instance.driver.find_element_by_xpath("//app-pack-itens/mat-card/div/div[2]/mat-table")

        table = get_table(table_conteinner)

        dats = add_values_in_dictionary(table)

        dic_values['boxs'] = dats

        lista_values.append(dic_values.copy())

        instance.driver.get(f'{base_url}#/modules/home')

    return lista_values


def scrapping_folders_inf(instance, link):
    sleep(2)
    values_data = dict()
    try:
        in_codigo = instance.driver.find_element_by_xpath("//mat-card/div/div[2]/mat-form-field[1]/div/div[1]/div/input")
        code = in_codigo.get_attribute("value")
    except:
        code = "S/N"

    try:
        in_type = instance.driver.find_element_by_xpath("//mat-card/div/div[2]/mat-form-field[2]/div/div[1]/div/mat-select/div/div[1]/span/span")
        type = in_type.get_attribute("innerHTML")
    except:
        type = "S/N"

    try:
        in_client = instance.driver.find_element_by_xpath("//mat-card/div/div[2]/mat-form-field[3]/div/div[1]/div/mat-select/div/div[1]/span/span")
        client = in_client.get_attribute("innerHTML")
    except:
        client = "S/N"
        
    try:
        in_depart = instance.driver.find_element_by_xpath("//mat-card/div/div[2]/mat-form-field[4]/div/div[1]/div/mat-select/div/div[1]/span/span")
        depart = in_depart.get_attribute("innerHTML")
    except:
        depart = "S/N"
        
    try:
        in_subject = instance.driver.find_element_by_xpath("//mat-card/div/div[3]/mat-form-field[1]/div/div[1]/div/input")
        subject = in_subject.get_attribute("value")
    except:
        subject = "S/N"

    try:
        in_indx = instance.driver.find_element_by_xpath("//mat-card/div/div[4]/mat-form-field[1]/div/div[1]/div/input")
        indx = in_indx.get_attribute("value")
    except:
        indx = "S/N"

    try:
        in_date = instance.driver.find_element_by_xpath("//mat-card/div/div[4]/mat-form-field[2]/div/div[1]/div/input")
        date = in_date.get_attribute("value")
    except:
        date = "S/N"

    try:
        in_date_end = instance.driver.find_element_by_xpath("//mat-card/div/div[4]/mat-form-field[2]/div/div[1]/div/input")
        date_end = in_date_end.get_attribute("value")
    except:
        date_end = "S/N"

    try:
        in_obs = instance.driver.find_element_by_xpath("//mat-card/div/div[5]/mat-form-field[1]/div/div[1]/div/input")
        obs = in_obs.get_attribute("value")
    except:
        obs = "S/N"

    values_data = {
        "index": trim(code),
        "type": trim(type),
        "client": trim(client),
        "department": trim(depart),
        "subject": trim(subject),
        "indexing": trim(indx),
        "date_start": trim(date),
        "date_end": trim(date_end),
        "obs": trim(obs),
        "link": trim(link)
    }
    return values_data



def scan_items_in_sys(instance):
    list_items = list()

    element_is_load(instance, "//mat-table/mat-row[1]", 10)
    
    table_element = instance.driver.find_element_by_xpath("//mat-table")
    
    table = get_table(table_element)


    for tab in table:
        rows = tab.find_all("mat-cell")
        list_items.append({
            "upload": trim(rows[0].text),
            "link": trim(rows[1].a['href']),
            "name": trim(rows[1].text),
            "subject": trim(rows[2].text),
            "describe": trim(rows[3].text)
        })
        
    return list_items