import unittest
import settings
import random
import os
import WorkWithFiles
from pathlib import Path

list_proxy = []
Path_Helpers = settings.Path_Helpers



def read_proxy_file():
        
    file_name    = settings.file_name_List_proxy
    File_path    = Path_Helpers+file_name
    
    if not file_name:
        return list_proxy
    else:
        
        f = Path(File_path)
        if not f.is_file():
            print('Add file proxy: ', File_path)    
            open(File_path, "w+")

    with open(File_path, 'r') as file:
        text = file.readlines()
        

        with open(File_path,'w') as f:
            for line in text:
                line = line.strip()
                if not line or not '.' in line: #or line.startswith("#") 
                    continue  # skip blank and commented out lines

                if ':' in line and not '\t' in line:
                    split_str_Proxy = line.split(':')
                else:    
                    split_str_Proxy = line.split('\t')
                              
                f.write(split_str_Proxy[0]+'\t' + split_str_Proxy[1]+'\n')
                if line.startswith("#"):
                    continue
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




def clear_file_proxy():
    if settings.debug:
        print('clear_file_proxy')
    file_name    = settings.file_name_List_proxy
    Path_Helpers = settings.Path_Helpers
    File_path    = Path_Helpers+file_name
    
    file_name_bad_proxy = 'bad_proxy.txt'

    if not file_name:
        return True
    with open(File_path, 'r') as file:
        text = file.readlines()
        with open(File_path,'w') as f:
            for line in text:
                if line == '\n':
                    print(1)
                elif not line.startswith("#"):
                    line = str(line)
                    f.write(line)
                    
        with open(Path_Helpers+file_name_bad_proxy, 'a') as bf:
            for line in text:
                if line.startswith("#"):
                    line = str(line)
                    bf.write(line)    

 





def commented_proxy(proxy):
    if proxy:
        #http:\\11.11.11.11: 2222
        proxy_ip = proxy.get('http').split(':')[1][2:] #bad code
        if settings.debug:
            print()
            print('commented proxy: ',proxy_ip)
            print()
        WorkWithFiles.ReplaceLineInFile(settings.Path_Helpers + settings.file_name_List_proxy, proxy_ip,'#'+proxy_ip)
        clear_file_proxy() 
    



##start_file = os.path.join(current_dir, "proxies.txt")


def get_list_ignore_item():
    file_name    = settings.file_name_ignore
    Path_Helpers = settings.Path_Helpers
    File_path    = Path_Helpers+file_name

    list_ignore_Items = []

    if not file_name:
        return list_ignore_Items
    else:
        
        f = Path(File_path)
        if not f.is_file():
            open(File_path, "w+")

    with open(File_path, 'r') as file:
        text = file.readlines()

        for line in text:
            line = line.strip()
            
            if not line or line.startswith("#") or not '.' in line:
                continue  # skip blank and commented out lines

            list_ignore_Items.append(line)
            
    #print(list_ignore_Items)            
    return list_ignore_Items






def add_ignore_links(list_results):
    file_name    = settings.file_name_ignore
    Path_Helpers = settings.Path_Helpers
    File_path    = Path_Helpers+file_name
  
    file = open(File_path, 'a')
    
    for dict_results in list_results: 
        for key, item in dict_results.items():
            if key = 'href':
                line = str(item)
                file.write( line + '\n')
    
    file.close()


##########################   TESTS   ################################

class Test_read_proxy_file(unittest.TestCase):

   
    ## повинен бути файл з проксі
    def test_file_exist(self):
        if settings.file_name_List_proxy:
            f = Path(settings.Path_Helpers + settings.file_name_List_proxy)
            self.assertTrue(f.is_file())


    ## якщо файл є повинна бути правильна структура х.х.х.х:уу
    def test_proper_structure_file_proxys(self):
        if settings.file_name_List_proxy:
            with open(settings.file_name_List_proxy, "r") as f:

                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue  # skip blank and commented out lines

                    #with self.subTest(True):
                    if True:
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
    read_proxy_file()
    get_list_ignore_item()
    
    
