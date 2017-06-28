import unittest
import settings
import random
import os
from pathlib import Path



debugs = False#True



def read_proxy_file():
    list_proxy = []
    if not settings.file_name_List_proxy:
        return list_proxy
    
    with open(settings.file_name_List_proxy, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or not '.' in line:
                continue  # skip blank and commented out lines

            if ':' in line and not '\t' in line:
                split_str_Proxy = line.split(':')
            else:    
                split_str_Proxy = line.split('\t')
        
            list_proxy.append(
                            {'protocol':'http',
                             'proxy_ip': split_str_Proxy[0],
                             'proxy_port': split_str_Proxy[1]
                             })
            
    return list_proxy





def get_proxy():
    # choose a proxy server to use for this request, if we need one
    list_proxy = read_proxy_file()
    if len(list_proxy) == 0:
        return None
    proxy_ip = random.choice(list_proxy)

    if proxy_ip.get('protocol') == 'socks5':
        proxy_url = "socks5://{user}:{passwd}@{ip}:{port}/".format(
            user=settings.proxy_user,
            passwd=settings.proxy_pass,
            ip=proxy_ip,
            port=settings.proxy_port,
        )
    else:        
        proxy_url = "http://{ip}:{port}/".format(
            ip  = proxy_ip.get('proxy_ip'),
            port = proxy_ip.get('proxy_port'),

    )
    return {
        "http": proxy_url,
        "https": proxy_url
    }

def commented_proxy(proxy):
##    print(proxy)
    if proxy:
        proxy_ip = proxy.get('http').split(':')[1][2:]
##    print('#',proxy_ip )
        ReplaceLineInFile(settings.file_name_List_proxy,proxy_ip,'#'+proxy_ip)
    


def ReplaceLineInFile(fileName, sourceText, replaceText):
    file = open(fileName, 'r')                          #Opens the file in read-mode
    text = file.read()                                  #Reads the file and assigns the value to a variable
    file.close()                                        #Closes the file (read session)
    file = open(fileName, 'w')                          #Opens the file again, this time in write-mode
    file.write(text.replace(sourceText, replaceText))   #replaces all instances of our keyword
                                                        # and writes the whole output when done, wiping over the old contents of the file
    file.close()                                        #Closes the file (write session)
    

##start_file = os.path.join(current_dir, "proxies.txt")




##########################   TESTS   ################################

class Test_read_proxy_file(unittest.TestCase):


    ## повинен бути файл з проксі
    def test_file_exist(self):
        if settings.file_name_List_proxy:
            f = Path(settings.file_name_List_proxy)
            self.assertTrue(f.is_file())


    ## якщо файл є повинна бути правильна структура х.х.х.х:уу
    def test_proper_structure_file_proxys(self):
        if settings.file_name_List_proxy:
            with open(settings.file_name_List_proxy, "r") as f:

                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or not '.' in line:
                        continue  # skip blank and commented out lines

                    with self.subTest(True):
                        #має бути ip та порт
                        splitProxy = line.split('\t')
                        self.assertEqual(len(splitProxy),2)
                        try:
                            int(splitProxy[1])
                        except:
                            self.assertIsInstance(splitProxy[1],int)    
                        
                        
                        splitIp = splitProxy[0].split('.')
                        self.assertEqual(len(splitIp),4)
                        for partIp in splitIp: 
                            try:
                                int(partIp)
                            except:
                                self.assertIsInstance(partIp,int)
                    
    def test_commented_proxy(self):
        pass




if __name__ == '__main__':
    unittest.main()
    
