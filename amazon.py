import requests
from bs4 import BeautifulSoup
import time
import winsound
import WorkWithFiles

## time waiting screen
delay = 30
##
number_play = 60

MaxPrice = 240

BASE_url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=rx+470&rh=i%3Aaps%2Ck%3Arx+470'

##List search card
listName = ["470", "480", "570","580"]

max_pages = 1


def get_html(url):
##    try:
##      try:
##          response = requests.get(url, timeout=(10,10))
##      except requests.exceptions.ReadTimeout:
##          print('Oops. Read timeout occured')
##      except requests.exceptions.ConnectTimeout:
##          print('Oops. Connection timeout occured!')
     
      req = requests.get(url)
      while req.status_code == 503:
         time.sleep(5)   
         req = requests.get(url)
         print(".", end = '')

##      print(req.status_code)
      if req.status_code == 503:
          return get_html(url)
      elif req.status_code == 200:
          return req.text
      else:
          return req
####    except:
####        return get_html(url)

def get_page_count(html):
##    soup  = BeautifulSoup(html, "html.parser")
##    count_tag = soup.find('div',class_='pagnHy')
##    paggination = count_tag.find('span',class_='pagnDisabled').text
##
##    return int(paggination)
    return 2


    
def parse(html):
    soup  = BeautifulSoup(html, "html.parser")
    elementsLi = soup.find_all('li',class_='s-result-item celwidget ')


    hrefs = []
      
    #print(elementsLi)
    for row in elementsLi:

        try:
            
            #Name
            name_card = row.find('a', class_='a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal').attrs['title']
            if not validatingName(name_card):
                continue
            
            priceAmazon = 0
            priceMoreBuyimg = 0
            
            #Price
            if not row.find('span', class_="sx-price-whole") == None:
                priceAmazon = int(row.find('span', class_="sx-price-whole").text)
                              
                
                    
            priceMoreBuyimg = normalize_price(row.find('span', class_="a-size-base a-color-base").text)
            if not (0 < priceAmazon <= MaxPrice or 0 < priceMoreBuyimg <= MaxPrice):
                continue
        except:
            continue
    
        

        hrefs.append({'href': row.a.attrs['href'],
                      'priceAmazon': priceAmazon,
                      'priceMoreBuyimg' : priceMoreBuyimg })


    return hrefs



        
def normalize_price(price):
    listreplace = ["EUR ", "$", "£"]
    for replacestring in listreplace:
        price = price.replace(replacestring, "")
    return float(price.replace(",", "."))

def validatingName(name_card):
    
    for replacestring in listName:
        if replacestring in name_card and 'adeon' in  name_card:
            return True
    return False



def get_one_item_page(url):
    card = []

    page_count = max_pages if max_pages <= 3 else get_page_count(get_html(url))
    page_count = min(page_count,max_pages)

    for page in range(1,page_count+1):
        print('[%s]  Парсинг %d%%' % (time.asctime(), (page/page_count* 100)))
        new_url = url + '&page=%d' % page
##        print(new_url)
        html = get_html(new_url)
         
        card.extend(parse(html))

        if len(card):
            print_card(card)
            play_sound(number_play)

        
    return card   
     
def play_sound(number_play):

    while number_play > 0: 
        winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
        number_play -=1

def print_card(card):

   
      
    for element in card:
        print("~"*50)
        for value, name in element.items():
            print(name, sep = ' ')
    WorkWithFiles.write_results(card)     


def main():

    print('--------------------------------START-------------------------------------')
    print(time.asctime())
    print()

    card = []
    for it in listName:
        time.sleep(3)     
        url = BASE_url.replace('470',it)
##        print(url)
        print(it)
        card.extend(get_one_item_page(url))

    print()
    print(time.asctime())
    print('---------------------------------END--------------------------------------')
    print()
    
    if not len(card):
        time.sleep(delay)
        main()
    else:    
        print_card(card)
        play_sound(number_play)
        repeat = input("нажать 'r' или '+' чтобы повторить")
        if repeat in 'r+':
            main()

          

if __name__ == '__main__':
    main()
