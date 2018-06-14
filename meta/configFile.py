import base64
import configparser
import os

config = configparser.ConfigParser()
my_path = os.path.abspath(os.path.dirname(__file__))
config.read(os.path.join(my_path,'ms.ini'))
#print("config = ",configFile.get('moysklad','auth_header'))



def picture_file_to_base64(filename):
    content = ''
    try:
        with open(filename, 'rb') as image_file:
            content = base64.b64encode(image_file.read())
            image_file.close()

    except:
        print('файл [' + filename + '] не найден')
    return content