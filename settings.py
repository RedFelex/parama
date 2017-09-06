import os

current_dir = os.path.dirname(os.path.realpath(__file__))

debug = False
#debug = True


#Parsing
delay = 40
number_play = 60
MinPrice = 100
MaxPrice = 245
BASE_url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=rx+470&rh=i%3Aaps%2Ck%3Arx+470'

listName = ["470", "480", "570","580"]
max_pages = 4






# Request
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
}





# Proxies

file_name_List_proxy = 'Proxy_list.txt'
##proxies = [
##    # your list of proxy IP addresses goes here
##    # check out https://proxybonanza.com/?aff_id=629
##    # for a quick, easy-to-use proxy service
##    {proxy_ip     : '198.50.219.230',
##     proxy_ip_port: '3128'},
##    ]


# Results

file_name_results = 'results.txt'
file_name_ignore = 'ignore_item.txt'





if __name__ == '__main__':
    print('Settings')
