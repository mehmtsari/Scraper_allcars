import requests
from bs4 import BeautifulSoup
import sqlite3


class SQL:
    def __init__(self):
        self.con = sqlite3.connect("CarsDB.db")
        self.cursor = self.con.cursor()
        
        self.create_table()
        
    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS cars(YIL INT,MARKA TEXT,MODEL VE SERI TEXT)")
        self.con.commit()
        
    def add_data(self,yil,marka,model):
        self.cursor.execute("INSERT into cars Values(?,?,?)",(yil,marka,model))
        self.con.commit()


sql = SQL()


main_url = "https://www.cars-data.com"
main_req = requests.get(main_url)
main_req_content = main_req.content
main_soup = BeautifulSoup(main_req_content,"html.parser")
main_content = main_soup.find_all("div",{"class":"col-2"})

main_content.pop(0)

for m in main_content:
    models_req = requests.get(str(m.find("a")["href"]))
    models_req_content = models_req.content
    models_soup = BeautifulSoup(models_req_content,"html.parser")
    models_content = models_soup.find_all("section",{"class":"models"})
    for model in models_content:
        for mod in model.find_all("div",{"class":"col-4"}):
            #print("  #"+m.text.strip() +"  #"+ m.find("a")["href"] +"  #"+ mod.text.strip()+"  #"+ mod.find("a")["href"])
            seri_req = requests.get(str(mod.find("a")["href"]))
            seri_req_content = seri_req.content
            seri_soup = BeautifulSoup(seri_req_content,"html.parser")
            seri_content = seri_soup.find_all("section",{"class":"models"})
            for seri in seri_content:
                for se in seri.find_all("div",{"class":"col-4"}):
                    #print(se.find("a")["href"])
                    if str(se.find("a")["href"]).startswith("https"):
                        surums_req = requests.get(str(se.find("a")["href"]))
                    else:
                        surums_req = requests.get(main_url+str(se.find("a")["href"]))
                    surums_req_content = surums_req.content
                    surums_soup = BeautifulSoup(surums_req_content,"html.parser")
                    surums_content = surums_soup.find_all("div",{"class":"col-8"})
                    for surums in surums_content:
                        for su in surums.find_all("div",{"class":"row"}):
                            surum_bilgileri = str(su.text).split(" ")
                            
                            
                            yil = int(0)
                            isim = ""
                            detay = ""
                            
                            
                            r = 0
                            for i in surum_bilgileri:
                                i = i.strip()
                                if r == 0:
                                    try:
                                        yil = int(i)
                                        r += 1
                                        continue
                                    except:
                                        continue
                                elif r == 1:
                                    isim = i
                                    r += 1
                                    continue 
                                detay += i+" "
                                r += 1
                            sql.add_data(yil,isim,detay)
                            print("Yıl : {} \nMarka: {} \nDetaylar: {} \n".format(yil,isim,detay))   
                             