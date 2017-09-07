import requests
from bs4 import BeautifulSoup
import time
import winsound
import helpers
import importlib
import settings
import WorkWithFiles

print('v4')


class AmazonStorePrice:

    def __init__(self):
	## time waiting screen
        self.delay          = settings.delay
        self.number_play    = settings.number_play
        self.MinPrice       = settings.MinPrice
        self.MaxPrice       = settings.MaxPrice
        self.BASE_url       = settings.BASE_url
        self.headers        = settings.headers
        self.listName       = settings.listName
        self.max_pages      = settings.max_pages
        self.finding_card   = []
        self.proxies        = helpers.get_proxy()
        self.new_url        = ''
        self.listIgnore     = helpers.get_list_ignore_item()
        

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
            print(time.asctime()+ '\n')
        elif param == 'end':    
            print('\n' + time.asctime())
            print('---------------------------------END--------------------------------------')
        elif param == 'exeptions':    
            print('!'*50+'\n'+'!'*50)
            print('EXEPTION')
            print('!'*50+'\n'+'!'*50)
            
        else:
            ## print_found_items            
            for element in self.finding_card:
                print("~"*50)
                for value, name in element.items():
                    print(name, sep = ' ')
            WorkWithFiles.write_results(self.finding_card)
            




    def start_parse(self):
       
        for it in self.listName:
            try:
                time_url = self.BASE_url.replace('470',it)
                print(it)
                self.get_one_item_page(time_url)
                time.sleep(5)
                importlib.reload(settings)
            except:
                print("ERROR PARSE")
        print()





    def get_one_item_page(self, url):
        page_count = self.max_pages if self.max_pages <= 3 else self.get_page_count(1)#self.get_html(url))
        page_count = min(page_count,self.max_pages)

        for page in range(1,page_count+1):

            print('[%s]  Парсинг %d%%' % (time.asctime(), (page/page_count* 100)))
            self.new_url = url + '&page=%d' % page

            if settings.debug:
                print()
                print()
                print("URL:")
                print(self.new_url)
                print()
                print()
                
            html = self.get_html(self.new_url)
         
            self.finding_card.extend(self.parse_html(html))

            self.check_The_items_found()
            
        
          




    def get_page_count(self, html):
        #soup  = BeautifulSoup(html, "html.parser")
        #count_tag = soup.find('div',class_='pagnHy')
        #paggination = count_tag.find('span',class_='pagnDisabled').text
        #return int(paggination)
    
        return 6





    def get_html(self,url):

        ##      try:
        ##          response = requests.get(url, timeout=(10,10))
        ##      except requests.exceptions.ReadTimeout:
        ##          print('Oops. Read timeout occured')
        ##      except requests.exceptions.ConnectTimeout:
        ##          print('Oops. Connection timeout occured!')
        useProxy = True
        while True:
            
            self.proxies = helpers.get_proxy()
            
                
            if self.proxies is None:
                useProxy = not useProxy 
                #print('Proxy none')
            if settings.debug:
                print('useProxy:'  ,useProxy) 
                print('Try proxy: ',self.proxies)
                
            try:
                #if settings.debug:
                #    print() 
                #    print('url: ',url)
                #    print()
                if useProxy:            
                    req = requests.get(url, headers = self.headers, proxies = self.proxies)
                else:
                    req = requests.get(url)
                    
            except requests.exceptions.ProxyError:
                self.except_get_html()
                if settings.debug: print('ProxyError')
                continue
            except requests.exceptions.SSLError:
                self.except_get_html()
                if settings.debug: print('SSLError')
                continue
            except requests.exceptions.ConnectionError:
                if settings.debug: print('ConnectionError')
                self.except_get_html()
                continue
            except:
                if settings.debug: print('except')
                self.except_get_html()
                continue
            #    proxies = helpers.get_proxy()
            #    print('new proxy: {p}'.format(p = proxies))
            #    req = requests.get(url, headers = self.headers, proxies = proxies)

            if req.status_code == 503:   
                time.sleep(5)
                print(".", end = '')
            else:
                break
        
        if req.status_code == 200:
##            if settings.debug:
##                text = helpers.replace_astral(req.text)
##                print('req.status_code == 200: ',text)
##                return text
            return req.text
        else:
            if settings.debug: print('req.status_code == else: ',req)  
            return req  





    def except_get_html(self): 
        if settings.debug:
            print('except_get_html  ' ,self.proxies)
            
        helpers.commented_proxy(self.proxies)    
        importlib.reload(helpers)




    def parse_html(self,html):
        soup  = BeautifulSoup(html, "html.parser")
               
        elementsLi = soup.find_all('li',class_='s-result-item celwidget ')
        
        hrefs = []
        if settings.debug:
            print()
            print('Count elements "li": {C}'.format(C = len(elementsLi)))
            print()

        if len(elementsLi) == 0:
            if settings.debug:
                print('parse_html:~',self.proxies)

            if not self.proxies is None:
                helpers.commented_proxy(self.proxies)    
            
            if settings.debug:
                print()
                print(len(elementsLi))
                print('parse_html:~'+'!'*50)
                try:
                    print(html)
                except:
                    print("НЕ удалось отобразить страницу")
                print('!'*50)
    
            return self.parse_html(self.get_html(self.new_url))                
        else:
            print(len(elementsLi))
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

                    link = row.a.attrs['href']
                    if  link in self.listIgnore:
                        if settings.debug:
                            print()
                            print('Ignore link:' ,link)
                            print()
                        continue
                    
                    hrefs.append({'href': link,
                              'priceAmazon': priceAmazon,
                              'priceMoreBuyimg' : priceMoreBuyimg })

        
        return hrefs






    def check_The_items_found(self):
        if len(self.finding_card):
            self.print_status('print_found_items')
            WorkWithFiles.ShowRusults()
            self.play_sound()
            return True
        return False
    



    
    def play_sound(self):
        for i in range(1,self.number_play):
            winsound.PlaySound('sound.wav', winsound.SND_FILENAME)




        
    
def main():
    if settings.debug:
        print("Debug mode ON")
        print()
        
    parser = AmazonStorePrice()

    while not parser.check_The_items_found():
        parser.print_status('start')
        parser.start_parse()
        parser.check_The_items_found()
        parser.print_status('end')
        time.sleep(parser.delay)
    else:
        parser.print_status()
        WorkWithFiles.ShowRusults()
        parser.play_sound()
        answer = input("нажать '+' чтобы повторить, 'i' - чтобы игнорировать ссылку")
        if answer == '+':
            main()
        elif answer == 'i':
            for item in self.finding_card:
                helpers.add_ignore_links(self.finding_card) #todo
            main()
  



if __name__ == '__main__':
    main()
