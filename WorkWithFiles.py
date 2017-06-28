import unittest
import os
import time
from pathlib import Path




file_name_results = 'results.txt' #add loging daily

def write_results(dict_results, file_name = file_name_results):
    if len(dict_results):
        file = open(file_name, 'w')

        file.write(time.asctime() + '\n')
        for key, item in dict_results.items():

            line = key + ': ' + item
            file.write( line + '\n')
        file.write('-'*50 + '\n\n')






class Test_Files(unittest.TestCase):


    def test_write_results(self):

        file_name = 'test_write_rezults.txt'
        current_dict = {'a' : 'a1',
                        'b' : 'b1'}
        write_results(current_dict,file_name)

        #проверка на наличие файла
        f = Path(file_name)
        self.assertTrue(f.is_file())
        
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name)
##        os.remove(path)
        
        
        




def main():
    print('Work with files')





if __name__ == '__main__':
    main()
    unittest.main()
