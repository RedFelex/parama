import unittest
import os
import time
from pathlib import Path
import settings



file_name_results = settings.file_name_results #add loging daily

def write_results(list_results, file_name = file_name_results):
    if len(list_results):
        file = open(file_name, 'w')

        file.write(time.asctime() + '\n'*2)
        for dict_results in list_results: 
            for key, item in dict_results.items():

                line = str(key).upper() + ': ' + str(item)
                file.write( line + '\n'*2)
        file.write('-'*50 + '\n'*2)
        file.close()





def ReplaceLineInFile(fileName, sourceText, replaceText):
    file = open(fileName, 'r')                          #Opens the file in read-mode
    text = file.read()                                  #Reads the file and assigns the value to a variable
    file.close()                                        #Closes the file (read session)
    file = open(fileName, 'w')                          #Opens the file again, this time in write-mode
    file.write(text.replace(sourceText, replaceText))   #replaces all instances of our keyword
                                                        # and writes the whole output when done, wiping over the old contents of the file
    file.close()                                        #Closes the file (write session)
    



############################# TEST ############################################
class Test_Files(unittest.TestCase):


    def test_write_results(self):

        file_name = 'test_write_rezults.txt'
        test_list = []
        current_dict = {'a' : 'a1',
                        'b' : 'b1'}
        test_list.append(current_dict)
        write_results(test_list,file_name)

        #проверка на наличие файла
        f = Path(file_name)
        self.assertTrue(f.is_file())
        
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name)
        os.remove(path)
        
        
        




def main():
    print('Work with files')





if __name__ == '__main__':
    main()
    unittest.main()
