import os
from sys import platform
from utils import convert_url, create_folder, create_json, reading_json, verify_folders
from get_data import Get_data
from scrapping_boxs import scrapping_b
from scan_informais_in_system import scan
from create_xlsx import add_xlsx
from tkinter import *
from SetupWizard import SetupConfig

class GlobalConfig:

    def __init__(self):
        try:
            self.global_ = reading_json(f'{convert_url("./config/Global")}')
        except:
            if self.generation_config():
                self.global_ = reading_json(f'{convert_url("./config/Global")}')
            else:
                self.global_ = False
                
        self.platform = self.getSystem()
        

    def is_error(self):
        if not self.global_:
            return True
        else:
            return False

    def getSystem(self):
        return platform.upper()
    

    def getUser(self):
        return self.global_['user']


    def getPassword(self):
        return self.global_['passwd']


    def getUrlBase(self):
        return self.global_['url_base']


    def getClient(self):
        return self.global_['client']


    def generation_config(self):
        root = Tk()
        myapp = SetupConfig(root)
        root.mainloop()

        dt_my = myapp.getData()
        if len(dt_my):
            create_folder('config', {}, convert_url("./"))
            create_json(f'{convert_url("./config/Global")}', dt_my)
            return True
        else:
            return False

    def mapping_boxs(self, instance, app_info=False):

        app_info.situation("Mapiando caixas ... ") if app_info else print("Mapiando caixas ... ")

        mapping = Get_data(instance, instance.getClient(), "Caixa")
        
        ult_json = []
        try:
            lista_values = scrapping_b(instance, mapping.get_datas())
            if lista_values:
                ult_json = lista_values
        except:
            create_json(convert_url( "./config/boxs"),{"Ult_reg":ult_json,  "error": "Row 64"} )
            return False

        try:
            app_info.situation("Mapiando elementos ...") if app_info else print("Mapiando elementos ...")

            dt = scan(instance, lista_values, app_info)

            app_info.situation("Finalizado o mapiamento de elementos ...") if app_info else print("Finalizado o mapiamento de elementos ...") 
            if dt:
                ult_json = dt
                
        except:
            create_json(convert_url( "./config/boxs"),{"ult_reg": ult_json,  "error": "Row 76"} )
            return False


        app_info.situation("Criando arquivos de configuração ...") if app_info else print("Criando arquivos de configuração ...")
        create_json(convert_url("./config/boxs"),ult_json )

        app_info.situation("Criando excel ...") if app_info else print("Criando excel ...")
        add_xlsx()

        app_info.situation("Criando pastas . . .") if app_info else print("Criando pastas . . .") 
        for data in dt:
            create_folder(data['index'], data['boxs'])
        
        app_info.situation("Pegando as informações das pastas ... ") if app_info else print("Pegando as informações das pastas ... ")
        create_json(convert_url("./config/folders"), verify_folders(convert_url("./")))

