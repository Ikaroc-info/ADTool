import json
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def add_double_liste(l1,l2):
    return [l1[0]+l2[0],l1[1]+l2[1]]

def Usenix(words_to_search,date_limit,history):
    pad="#####################µ"
    results=["",pad*3+"\n"+pad+"USENIXµ"+pad+"\n"+pad*3+"\n"]
    for to_search_word in words_to_search:
        results[1] +=pad+to_search_word+"µ"+pad+"\n"
        to_search_format=to_search_word.replace(" ","_")
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
                        results=add_double_liste(results,USENIX_html_parser(html,date_limit,history))
                else :
                    i+=1
                    results=add_double_liste(results,USENIX_html_parser(html,date_limit,history))
    return results

def USENIX_html_parser(html,date_limit,history):
    loc_h3=0
    results_page=["",""]
    while html.find("<h3 class",loc_h3) != -1:
        loc_h3=html.find("<h3 class",loc_h3+2)
        splited=html[loc_h3+33:loc_h3+500].split("""">""")
        url=splited[0]
        titre=splited[1].split('</a')[0]
        loc_date=html.find("""<p class="search-info">""",loc_h3+2)
        date=html[loc_date:loc_date+500].split(" ")[6]
        try :
            date=int(date)
            if date_limit: 
                if date<int(date_limit):
                    continue
        except :
            pass
        if url.find("https://")!=-1 and url.find("speaker")==-1 and url.find("technical-session")==-1 and url.find("workshop")==-1 and url.find("accepted-papers")==-1 and url.find("call-of-papers")==-1 and titre not in history:
            results_page=add_double_liste(results_page,[titre,f"{url}µ{titre}µ{date}\n"])
    return results_page

def NDSS(words_to_search,date_limit,history):
    pad="#####################µ"
    results=["",pad*3+"\n"+pad+"NDSSµ"+pad+"\n"+pad*3+"\n"]
    for w_to_search in words_to_search:
        print(w_to_search)
        results[1]+=pad+w_to_search+"µ"+pad+"\n"
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
                    if name.find("Call for Paper")==-1 and name.find("Accepted Paper")==-1 and name.find("NDSS")==-1 and name.find("Session")==-1 and name not in history:
                        if date_limit:
                            try :
                                loc_annee=url.find("ndss20")
                                if int(url[loc_annee+4:loc_annee+8])>int(date_limit):
                                    results=add_double_liste(results,[name,f"{url}µ{name}µ{url[loc_annee+4:loc_annee+8]}\n"])
                            except:
                                results=add_double_liste(results,[name,f"{url}µ{name}µXXXX\n"])
                        else :
                            try :
                                loc_annee=url.find("ndss20")
                                if int(url[loc_annee+4:loc_annee+8]):
                                    results=add_double_liste(results,[name,f"{url}µ{name}µ{url[loc_annee+4:loc_annee+8]}\n"])
                            except:
                                results=add_double_liste(results,[name,f"{url}µ{name}µXXXX\n"])
            except:
                driver.close()
        except:
            print(f"An error hapened for the word {w_to_search}")
    return results

def IEEE_ACM(words_to_search,date_limit,limite_IEEE_page,history):
    pad="#####################µ"
    results=["",pad*3+"\n"+pad+"IEEE ACMµ"+pad+"\n"+pad*3+"\n"]
    for word in words_to_search:
        results[1]+=pad+word+"µ"+pad+"\n"
        flag=True
        pn=1
        while flag and pn<limite_IEEE_page:
            driver = webdriver.Firefox()
            complement_url=""
            for elt in word.split(" "):
                complement_url+=f"%20AND%20(%22Abstract%22:{elt})"
            driver.get(f"https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&newsearch=true&matchBoolean=true&queryText=(%22All%20Metadata%22:ACM){complement_url}&ranges={date_limit}_2024_Year&highlight=false&returnFacets=ALL&returnType=SEARCH&matchPubs=true&pageNumber={pn}")
            time.sleep(4)
            data=driver.page_source
            driver.close()
            if len(data)>200000:
                results=add_double_liste(results,IEEE_html_parser(data,history))
                print(f"Page number {pn} checked!")
                pn+=1
            else:
                flag=False
    return results

def IEEE_html_parser(data,history):
    results=["",""]
    loc=0
    flag=True
    while flag:
        try:
            loc=data.index('xplanchortagroutinghandler="" xplhighlight="" xplmathjax="" class="fw-bold"',loc+100)
            url=data[loc:loc+400].split('href="')[1].split('"')[0]
            url="https://ieeexplore.ieee.org"+url
            name=data[loc:loc+300].split("""/">""")[1].split("""</a>""")[0]
            name=name.replace("""<span class="highlight">""","")
            name=name.replace("""</span>""","")
            if name not in history:
                results=add_double_liste(results,[name,f"{url}µ{name}µ\n"])
        except:
            flag=False
    return results


with open("conf.json", "r") as f:
    data = json.load(f)
    sites=data["site_to_search"] #sites à explorer
    word_to_search=data["word_to_search"] #mots à chercher
    date_limit=data["limit_date"] # dates limites basse
    limite_IEEE_page=data["limit_IEEE_page"] #limites pages IEEE (pouvant être très élevé donc mieux de poser une limite)
    history_file=data["history_file"] #fichier historique si besoin
    print(sites,word_to_search,date_limit, history_file)
    if history_file != "None":
        history_f=open(history_file,"r")
        history=history_f.read()
        history_f.close()
    else:
        history=""
    
    results=["",""]
    for site in sites:
        if site=="Usenix":
            results=add_double_liste(results,Usenix(word_to_search,date_limit,history))
        elif site=="NDSS":
            results=add_double_liste(results,NDSS(word_to_search,date_limit,history))
        elif site=="IEEE_ACM":
            results=add_double_liste(results,IEEE_ACM(word_to_search,date_limit,limite_IEEE_page,history))
        else :
            print(f"Oups! {site} is not in our current proposition! (cf README)")
    f=open("results.txt","w")
    f.write(results[1])
    f.close()

    if history_file != "None":
        f_h=open(history_file,"a")
        f_h.write(results[0])
        f_h.close()
    