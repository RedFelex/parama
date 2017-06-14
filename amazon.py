import requests
from bs4 import BeautifulSoup

MaxPrice = 210
BASE_url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=rx+570&rh=i%3Aaps%2Ck%3Arx+570'
listName = ["470", "480", "570","580"]



def get_html(url):
    req = requests.get(url)
    if req.status_code == 503:
        return get_html(url)
    elif req.status_code == 200:
        return req.text
    else:
        return req



def get_page_count(html):
    soup  = BeautifulSoup(html, "html.parser")
    count_tag = soup.find('div',class_='pagnHy')
    paggination = count_tag.find('span',class_='pagnDisabled').text

    return int(paggination)



    
def parse(html):
    soup  = BeautifulSoup(html, "html.parser")
    elementsLi = soup.find_all('li',class_='s-result-item celwidget ')


    hrefs = []
      
    
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

def  validatingName(name_card):
    
    for replacestring in listName:
        if replacestring in name_card and 'adeon' in  name_card:
            return True
    return False





def get_one_item_page(url):
     card = []

     page_count = get_page_count(get_html(url))
     page_count = min(page_count,4)

     for page in range(1,page_count):
         print('Парсинг %d%%' % (page/page_count* 100))
         new_url = url + '&page=%d' % page
         html = get_html(new_url)
         
         card.extend(parse(html))
     return card   
     

def main():
     card = []
     for it in listName:
    
         url = BASE_url.replace('570',it)
         print(url)
         card.extend(get_one_item_page(url))

     print('-----------------------------------------------------------------------/n')    
     print(card)
     

if __name__ == '__main__':
    main()
