from tkinter import *
from GlobalConfig import GlobalConfig
from login import Login
from send_registers import send_rg_in_base
from undoing_change import undoing
from scan_informais_in_system import scan
from utils import (
    alter_data_the_itens,
    convert_url, 
    file_is_exists, 
    create_json, 
    insert_arq_log, 
    reading_json,
    )
from reading_xml import update_xlsx
from file_monitoration import plan_is_change
from create_boxs import add_item
from time import sleep
from scrapping_boxs import scrapping_b
from file_monitoration import folder_is_change
from upload import conf_file_upload, up_files
from SituationView import SituationView
import speedtest
from time import time

# Code ..

class App:

    def start(self):
        self.conf = GlobalConfig()

        if not self.conf.is_error():
            
            self.root = Tk()
            self.app = SituationView(self.root)

            try:
                self.boxs = file_is_exists(convert_url("./config/boxs.json"))
            except:
                self.boxs = False

            try:    
                change, self.foldrs = folder_is_change()
            except:
                change = False

            if not self.boxs or plan_is_change(self.conf) or change:

                self.app.situation("Esperando página carregar ...")
            
                try:
                    self.lg = Login(self.conf.getUrlBase(),self.conf.getUser(),self.conf.getPassword(), self.conf.getClient(), True, self.app)
                except Exception as erro:
                    insert_arq_log(f'{erro}')
                    self.app.situation(f'Error: {erro.__cause__}')
                    self.app.buttonExit()
                else:
                    if self.lg.is_logout():
                        self.app.situation("Login feito com sucesso")
                        
                self.app.situation("Esperando página carregar ...")
                try:
                    if self.lg.authentication_validation():
                        self.app.situation("Página carregada")
                    
                    if not self.boxs:
                        self.box_change()

                    if plan_is_change(self.conf):
                        self.plan_change()

                    if change:
                        self.send_rg()
                except Exception as erro:

                    insert_arq_log(f'{erro}')
                    self.app.situation(f'Error: {erro.__cause__}')
                    self.lg.driver.close()
                    self.app.buttonExit()

                else:
                    self.lg.driver.close()
                    self.app.situation("Conexão fechada")
                    sleep(2)
                    self.app.ext()
            else:
                self.app.situation("Nenhuma mudança encontrada!!!")
                sleep(3)
                self.app.ext()
            self.root.mainloop()

    def box_change(self):
        self.app.situation("Começando a criação dos arquivos de configuração!!")
        self.conf.mapping_boxs(self.lg, self.app)
        

    def plan_change(self):
        self.alters = list()
        try:
            self.app.situation("Lendo arquivos de configuração ...")
            dt = reading_json(convert_url('./config/boxs'))
            
            try:
                if len(dt):
                    dt = dt[(len(dt))-1]
                    if len(dt['boxs']):
                        try:
                            dt['boxs'] = dt['boxs'][(len(dt['boxs']))-1]
                        except Exception as error:
                            insert_arq_log(f'App: Row 102 {error} ; Val: {dt}')
                    else:
                        dt['boxs'] = {
                            "index" : False
                        }
                else:
                    dt =  {}
            except Exception as error:
                insert_arq_log(f'App: Row 106: {error} ; Val: {dt}')

            self.app.situation("Preparando tudo para o envio ...")
            try:
                upl = update_xlsx(dt)
            except Exception as error:
                insert_arq_log(f'App: Row 115: {error}')
            
            self.app.situation(f'Preparando para enviar {len(upl)} caixas')

            for up in upl:

                resul = add_item(self.lg, up, self.app)
                if resul['Error']:
                    self.alters.append(resul['link'])
                    insert_arq_log(f'App: Row 126: {resul}')
                    undoing(self.lg,resul, self.app)
                    break
                else:
                    self.alters.append(resul['link'])
            
        except Exception as error:
            insert_arq_log(f'App: Row 123: {error}')
        finally:
            if len(self.alters):       
                self.app.situation(f'Mapiando as informações ...')   
                lista_values = scrapping_b(self.lg, self.alters)
                self.app.situation("Mapiando elementos ...") if self.app else print("Mapiando elementos ...")

                dt = scan(self.lg, lista_values, self.app)

                self.app.situation("Finalizado o mapiamento de elementos ...") if self.app else print("Finalizado o mapiamento de elementos ...") 

                self.app.situation(f'Escrevendo mudanças') if self.app else print(f'Escrevendo mudanças')

                origen = reading_json(convert_url('./config/boxs'))

                _new_dic = alter_data_the_itens(origen, dt)

                self.conf.configuration_arq_create(_new_dic, self.app) if self.app else  self.conf.configuration_arq_create(_new_dic) 

                self.app.situation(f'Finalizado') if self.app else print(f'Finalizado')

    def send_rg(self):
        self.app.situation(f'Preparando para adicionar registros no sistema ...')
        try:   
            send_rg_in_base(self.lg, self.foldrs, self.app)
        except Exception as error:
            insert_arq_log(f'{error}')
            self.app.situation(f'Mapiando as informações ...')    
            self.conf.mapping_boxs(self.lg, self.app)
            self.app.situation(f'Finalizado')
            self.lg.driver.close()
            self.app.buttonExit()
        else:
            try:  
                while True:
                    self.app.situation(f'Configurando arquivo para upload...')   
                    conf_file_upload()
                    self.app.situation(f'Verificando velocidade da internet ... ')
                    st = speedtest.Speedtest() 
                    st.get_best_server()
                    bytes_val = st.upload()
                    Megabits = bytes_val/1048576
                    MegaBytes = Megabits/8
                    self.app.situation(f'Velocidade da internet {MegaBytes:.2f}... ')
                    self.app.situation(f'Começando upload..')   
                    if up_files(self.lg, MegaBytes, self.app):
                        break
            except Exception as error:
                insert_arq_log(f'{error}')
                self.app.situation(f'Mapiando as informações ...')    
                self.conf.mapping_boxs(self.lg, self.app)
                self.lg.driver.close()
                self.app.buttonExit()

try:
    start = time()    
    init = App()
    init.start()
except Exception as error:
    insert_arq_log(f'{error}')
finally:
    insert_arq_log(f'Execucao em: {(((time() - start))/60):.2f}m')