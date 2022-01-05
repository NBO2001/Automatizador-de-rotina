from os import walk

from utils import  convert_url, reading_json, separator, trim

def prepare_items(data, files):
    
    lis_temp = list()

    for file in files:
        fin = file.split('.')
        if (fin[(len(fin)) - 1]).upper() == "pdf".upper():
            lis_temp.append({
                "name": fin[0],
                "describe": data['describe'],
                "subject": data['subject'],
                "file_name": file
            })
        
    return lis_temp


def get_id_the_folder(location):
    boxs = reading_json(convert_url('./config/boxs'))
    for box in boxs:
        
        if location['index'] == box['index']:
            for bx in box['boxs']:
                if bx['index'] == location['box']:
                    link = bx['link'].split("/")
                    return link[(len(link))-1], bx['link']
                    

def return_items_up(id, data):
    base = reading_json(convert_url(f'./config/folders/{id}'))

    list_back = list()

    for dt in data:
        is_equal = False
        for bs in base:
            for b in base[bs]:
                if trim(b['name']) == trim(dt['name']):
                    is_equal = True

        if not is_equal:
            list_back.append(dt)
    
    return list_back
        

def mapping_it(loc):
    
    for  paths, subpath, files in walk(convert_url(f'./{loc["index"]}/{loc["box"]}')):
        
        datas = reading_json(convert_url(f'./{loc["index"]}/{loc["box"]}/conf'))

        files_in_folder = prepare_items(datas, files)
       
        id, link = get_id_the_folder(loc)
        
        data_up = return_items_up(id, files_in_folder)

        return data_up, link