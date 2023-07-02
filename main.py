from time import sleep
from bs4 import BeautifulSoup
import requests
from pushbullet import Pushbullet

API_KEY = "o.OEPnVNqDtVuAqMbelP4RSbImI7yFIB8d"
pb = Pushbullet(API_KEY)

while True:
    sleep(5)

    r = requests.get("https://www.geev.com/fr/recherche/objets?location=46.566297%2C0.372686&categories=clothing%2Cfashion%2Cfootwear%2Celectronics%2Ctv_audio_telephony%2Ccables_cases%2Cvideo_game&type=donation&distance=8000")
    
    # r = requests.get('https://www.geev.com/fr/recherche/objets?location=46.566297%2C0.372686&type=donation&distance=50000')
    soup = BeautifulSoup(r.text, 'lxml')
    articles_soup = soup.find_all('molecule-ad-card')

    list_data, new_articles = [],[]

    for elt in articles_soup:
        list_data.append((elt.get_attribute_list("id")[0],"https://www.geev.com"+str(elt.find('a').get_attribute_list("href")[0]),str(elt.find('span').text)[:-2]))

    print(list_data)
    file = open("data.txt", 'r').read().split(',')
    for i in range(len(list_data)):
        if list_data[i][0] not in file:
            new_articles.append(list_data[i])

    for elt in new_articles:
        text = "Nouvel article : "+elt[1]
        push = pb.push_note(elt[2], text)
        with open("data.txt", 'a') as f:
            f.write(str(elt[0])+',')