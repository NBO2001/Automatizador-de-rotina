from tkinter import *
from tkinter import messagebox


class SetupConfig:
    def __init__(self, master, conf="G"):
        self.mast = master
        self.isConf = conf
        self.dataGlob = {}
        self.dataLoc = {}
        self.mast.title("Setup de configuração")
        self.mast.geometry('300x200')

        self.div = Frame(self.mast)
        self.div['pady'] = 3
        self.div['padx'] = 3
        self.div.pack()

        self.div_a = Frame(self.mast)
        self.div_a['pady'] = 3
        self.div_a['padx'] = 3
        self.div_a.pack()

        self.div_b = Frame(self.mast)
        self.div_b['pady'] = 3
        self.div_b['padx'] = 3
        self.div_b.pack()

        self.div_c = Frame(self.mast)
        self.div_c['pady'] = 3
        self.div_c['padx'] = 3
        self.div_c.pack()

        self.div_d = Frame(self.mast)
        self.div_d['pady'] = 3
        self.div_d['padx'] = 3
        self.div_d.pack()

        self.div_e = Frame(self.mast)
        self.div_e['pady'] = 3
        self.div_e['padx'] = 3
        self.div_e.pack()

        self.label_user = Label(self.div_a, text='Usuário: ')
        self.label_user["width"] = 10

        self.user = Entry(self.div_a)
        self.user['width'] = 30

        self.label_passwd = Label(self.div_b, text='Senha: ')
        self.label_passwd["width"] = 10

        self.passwd = Entry(self.div_b)
        self.passwd['width'] = 30

        self.lab_url = Label(self.div_c, text="Url: ")
        self.lab_url["width"] = 10



        self.url = Entry(self.div_c)
        self.url['width'] = 30

        self.label_client = Label(self.div_d, text="Cliente: ")
        self.label_client["width"] = 10

        self.client = Entry(self.div_d)
        self.client['width'] = 30
        

        self.addInfo = Button(self.div_e)
        self.addInfo['text'] = "Enviar"
        self.addInfo['command'] = self.add_conf

        self.label_client.pack(side=LEFT)
        self.client.pack(side=RIGHT)

        self.addInfo.pack()

    def add_Global(self):
               
        self.label_user.pack(side=LEFT)
        self.user.pack(side=RIGHT)

        self.label_passwd.pack(side=LEFT)
        self.passwd.pack(side=RIGHT)

        self.lab_url.pack(side=LEFT)
        self.url.pack(side=RIGHT)

        self.mast.update()

    def add_conf(self):
        if self.isConf == "G":
            self.user_name = self.user.get()
            self.psswd = self.passwd.get()
            self.url_base = self.url.get()
            self.clin = self.client.get()

            if len(self.user_name) and len(self.psswd) and len(self.url_base) and len(self.clin):

                self.dataGlob = {
                    "user": self.user_name,
                    "passwd": self.psswd ,
                    "url_base": self.url_base                
                }

                self.dataLoc = {
                    "client": self.clin
                }
                
                self.mast.destroy()
            else:
                messagebox.showinfo(title='Alerta', message="Preencha todas as informações")
        
        if self.isConf == "L":
            
            self.clin = self.client.get()

            if len(self.clin):

                self.dataLoc = {
                    "client": self.clin
                }
                
                self.mast.destroy()
            else:
                messagebox.showinfo(title='Alerta', message="Preencha todas as informações")

    def getData(self):
        return self.dataGlob

    def getLocal(self):
        return self.dataLoc