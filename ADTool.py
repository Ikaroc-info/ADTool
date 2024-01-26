import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

global liste_nom
liste_nom=[]

def scrapper_NDSS(to_search,date_limite):
    global liste_nom
    results=""
    for w_to_search in to_search:
        print(w_to_search)
        w_to_search=w_to_search.replace("_"," ")
        results+=f"#####################µ{w_to_search}µ#####################\n"
        try:
            driver = webdriver.Firefox()
            driver.get("https://www.ndss-symposium.org/")
            time.sleep(3)
            driver.find_element(By.XPATH,"/html/body/header/div/section/section[1]/div/div/figure").click()
            elem=driver.find_element(By.ID,"""is-search-input-9240""")
            elem.send_keys(w_to_search)
            time.sleep(2)
            flag=True
            while flag:
                try:
                    driver.find_element(By.CLASS_NAME,"is-show-more-results-text").click()
                    time.sleep(2)
                except:
                    flag=False

            time.sleep(2)
            data=driver.page_source
            loc=0
            try:
                while 1:
                    loc=data.find("is-ajax-search-post is-ajax-search-post",loc+10)
                    loc_href=data.find("<a href=",loc)
                    url=data[loc_href+9:loc_href+300].split(""""></""")[0]
                    loc_href2=data.find("<a href=",loc_href+10)
                    name=data[loc_href2:loc_href2+300].split('>\n')[1][:-3]
                    name_tab=list(name)
                    flag=True
                    flag_let=-1
                    i=0
                    while i<len(name_tab):
                        if name_tab[i]==" " and flag_let==-1:
                            name_tab[i]=""
                        elif name_tab[i]!=" ":
                            flag_let=i
                        i+=1
                    flag_let+=1
                    while flag_let<len(name_tab):
                        name_tab[flag_let]=""
                        flag_let+=1
                    
                    name=""
                    for lettre in name_tab:
                        name+=lettre
                    if name.find("Call for Paper")==-1 and name.find("Accepted Paper")==-1 and name.find("NDSS")==-1 and name.find("Session")==-1 and name not in liste_nom:
                        liste_nom+=[name]
                        if date_limite:
                            try :
                                loc_annee=url.find("ndss20")
                                if int(url[loc_annee+4:loc_annee+8])>int(date_limite):
                                    results+=f"{url}µ{name}µ{url[loc_annee+4:loc_annee+8]}\n"
                            except:
                                results+=f"{url}µ{name}µXXXX\n"
                        else :
                            try :
                                loc_annee=url.find("ndss20")
                                if int(url[loc_annee+4:loc_annee+8]):
                                    results+=f"{url}µ{name}µ{url[loc_annee+4:loc_annee+8]}\n"
                            except:
                                results+=f"{url}µ{name}µXXXX\n"
            except:
                driver.close()
        except:
            print(f"An error hapened for the word {w_to_search}")
    return results

def html_parser_usenix(html,date_limite):
    global liste_nom
    loc_h3=0
    results_page=""
    while html.find("<h3 class",loc_h3) != -1:
        loc_h3=html.find("<h3 class",loc_h3+2)
        splited=html[loc_h3+33:loc_h3+500].split("""">""")
        url=splited[0]
        titre=splited[1].split('</a')[0]
        if titre not in liste_nom:
            liste_nom+=[titre]
            loc_date=html.find("""<p class="search-info">""",loc_h3+2)
            date=html[loc_date:loc_date+500].split(" ")[6]
            try :
                date=int(date)
                if date_limite: 
                    if date<int(date_limite):
                        continue
            except :
                pass
            if url.find("https://")!=-1 and url.find("speaker")==-1 and url.find("technical-session")==-1 and url.find("workshop")==-1 and url.find("accepted-papers")==-1 and url.find("call-of-papers")==-1:
                results_page+=f"{url}µ{titre}µ{date}\n"
    return results_page

def usenix_data(liste_mots,date):
    results =""
    for to_search_word in to_search:
        results +=f"#####################µ{to_search_word}µ#####################\n"
        to_search_format=to_search_word.replace(" ","%2520")
        print(to_search_format)
        flag=True
        i=0
        while flag:
            with urllib.request.urlopen('https://www.usenix.org/search/site/'+to_search_format+'?page='+str(i)) as response:
                html = str(response.read())
                if len(html)<=52000:
                    response_2=urllib.request.urlopen('https://www.usenix.org/search/site/'+to_search_format+'?page='+str(i))
                    html = str(response_2.read())
                    if len(html)<=52000:
                        flag=False
                        print(f"No more results, {i} page explored")
                    else :
                        i+=1
                        results+=html_parser_usenix(html,date)
                else :
                    i+=1
                    results+=html_parser_usenix(html,date)
    return results

to_search=input("Que voulez vous chercher sur Usenix? [passer pour importer un fichier] ")
if to_search=="":
    file=input("Quel est le nom du fichier que vous souhaitez importer? (le fichier doit-être à l'intérieur du répertoire d'exécution) : ")
    file_liste=open(file)
    lines=file_liste.readlines()
    file_liste.close()
    to_search=[l[:-1] for l in lines]
else :
    to_search=[to_search]
date=input("Voulez-vous une limitation de date? [N ou écrire l'année limite] : ")
if date=="" or date=="N":
    date=False
results="URLµNOMµDATE\n"
results+="#####################µ#####################µ#####################µ\n#####################µUSENIXµ#####################\n#####################µ#####################µ#####################\n"
print("###############################################################\n##################### USENIX #####################\n###############################################################\n")
results+=usenix_data(to_search,date)
results+="#####################µ#####################µ#####################µ\n#####################µNDSSµ#####################\n#####################µ#####################µ#####################\n"
print("###############################################################\n##################### NDSS #####################\n###############################################################\n")
results+=scrapper_NDSS(to_search,date)

f=open("results.txt","w")
f.write(results)
f.close()