import requests
from bs4 import BeautifulSoup
import time
import winsound
import helpers
import importlib

print('v2')


class AmazonStorePrice:

    def __init__(self):
	## time waiting screen
        self.delay = 50
        self.number_play = 60
        self.MinPrice = 100
        self.MaxPrice = 245
        self.BASE_url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=rx+470&rh=i%3Aaps%2Ck%3Arx+470'
        self.headers  = {
                         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                         "Accept-Encoding": "gzip, deflate, sdch, br",
                         "Accept-Language": "en-US,en;q=0.8",
                         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                         }
        ##List search card
        self.listName = ["470", "480", "570","580"]
        self.max_pages = 4
        self.finding_card = []
        self.proxies = helpers.get_proxy()

        


    def normalize_price(self, price):
        listreplace = ["EUR ", "$", "£"]
        for replacestring in listreplace:
            price = price.replace(replacestring, "")
        price = price.replace(",","")
        return float(price.replace(",", "."))


    def name_is_valid(self, name_card):
        for replacestring in self.listName :
            if replacestring in name_card and True in [i in name_card for i in ['rx','RX','Rx']] : #and 'adeon' in  name_card:
                return True
        return False

    


    def print_status(self, param = 'print_found_items' ):
        if param == 'start':
            print('--------------------------------START-------------------------------------')
            print(time.asctime())
            print()
        elif param == 'end':    
            print()
            print(time.asctime())
            print('---------------------------------END--------------------------------------')
        elif param == 'exeptions':    
            print("!"*50)
            print('EXEPTION')
            print("!"*50)
            
        else:
            ## print_found_items            
            for element in self.finding_card:
                print("~"*50)
                for value, name in element.items():
                    print(name, sep = ' ')




    def start_parse(self):
       
        for it in self.listName:
            time.sleep(5)         
            time_url = self.BASE_url.replace('470',it)
            print(it)
            self.get_one_item_page(time_url)
        print()





    def get_one_item_page(self, url):
        page_count = self.max_pages if self.max_pages <= 3 else self.get_page_count(1)#self.get_html(url))
        page_count = min(page_count,self.max_pages)

        for page in range(1,page_count+1):
            print('[%s]  Парсинг %d%%' % (time.asctime(), (page/page_count* 100)))
            new_url = url + '&page=%d' % page
##            print(new_url)
            html = self.get_html(new_url)
         
            self.finding_card.extend(self.parse_html(html))

            self.check_The_items_found()
            
        
          




    def get_page_count(self, html):
##        soup  = BeautifulSoup(html, "html.parser")
##        count_tag = soup.find('div',class_='pagnHy')
##        paggination = count_tag.find('span',class_='pagnDisabled').text
##
##        return int(paggination)
        return 6





    def get_html(self,url):

    ##      try:
    ##          response = requests.get(url, timeout=(10,10))
    ##      except requests.exceptions.ReadTimeout:
    ##          print('Oops. Read timeout occured')
    ##      except requests.exceptions.ConnectTimeout:
    ##          print('Oops. Connection timeout occured!')

        while True:
            print(".", end = '')
            self.proxies = helpers.get_proxy()
            try:
                req = requests.get(url, headers = self.headers, proxies = self.proxies)
            except requests.exceptions.ProxyError:
                print(self.proxies)
                helpers.commented_proxy(self.proxies)    
                importlib.reload(helpers)
                continue
            except requests.exceptions.SSLError:
                print(self.proxies)
                helpers.commented_proxy(self.proxies)    
                importlib.reload(helpers)
                continue
            except requests.exceptions.ConnectionError:
                print(self.proxies)
                helpers.commented_proxy(self.proxies)    
                importlib.reload(helpers)
                continue
            except:
                print(self.proxies)
                helpers.commented_proxy(self.proxies)    
                importlib.reload(helpers)
                continue
##                proxies = helpers.get_proxy()
##                print('new proxy: {p}'.format(p = proxies))
##                req = requests.get(url, headers = self.headers, proxies = proxies)

            if req.status_code == 503:   
                time.sleep(5)
                print(".", end = '')
            else:
                break
        
        if req.status_code == 200:
            return req.text
        else:
            return req  

        





    def parse_html(self,html):
        soup  = BeautifulSoup(html, "html.parser")
               
        elementsLi = soup.find_all('li',class_='s-result-item celwidget ')
        hrefs = []
        print(len(elementsLi))
        if len(elementsLi) == 0:
            print(self.proxies)
            helpers.commented_proxy(self.proxies)    
            if helpers.debugs:
                print(len(elementsLi))
                print('!'*50)
                print(html)
                print('!'*50)
                
        for row in elementsLi:
##            try:
                #Name
                name_card = row.find('a', class_='a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal').attrs['title']
##                print(name_card)
                if not self.name_is_valid(name_card):
                    continue
                priceAmazon = 0
                priceMoreBuyimg = 0
                #Price
                if not row.find('span', class_="sx-price-whole") == None:
                    priceAmazon = self.normalize_price(row.find('span', class_="sx-price-whole").text)
                
                if not row.find('span', class_="a-size-base a-color-base") == None:
                    priceMoreBuyimg = self.normalize_price(row.find('span', class_="a-size-base a-color-base").text)

                if not (self.MinPrice  < priceAmazon <= self.MaxPrice or self.MinPrice < priceMoreBuyimg <= self.MaxPrice):
                    continue
                
##            except:
##                self.print_status('exeptions')
##                continue
    
                hrefs.append({'href': row.a.attrs['href'],
                          'priceAmazon': priceAmazon,
                          'priceMoreBuyimg' : priceMoreBuyimg })

        
        return hrefs






    def check_The_items_found(self):
        if len(self.finding_card):
            self.print_status('print_found_items')
            self.play_sound()
            return True
        return False
    



    
    def play_sound(self):
        for i in range(1,self.number_play):
            winsound.PlaySound('sound.wav', winsound.SND_FILENAME)




        
    
def main():
  
    parser = AmazonStorePrice()
    while not parser.check_The_items_found():
        parser.print_status('start')
        parser.start_parse()
        parser.check_The_items_found()
        parser.print_status('end')
        time.sleep(parser.delay)
    else:
        parser.print_status()
        parser.play_sound()
        repeat = input("нажать 'r' или '+' чтобы повторить")
        if repeat in 'r+':
            main()   

  



if __name__ == '__main__':
    main()
