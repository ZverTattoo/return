import json
import logging
import os
from datetime import datetime

from meta.MetaArray2 import MetaArray
from meta.configFile import config
from meta.configFile import picture_file_to_base64
import requests

from meta.Meta import Meta
from model.Entity import Entity
import base64

imLog = logging.getLogger("image_set_in_product")
hdlr = logging.FileHandler('image_set_in_product.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
imLog.addHandler(hdlr)
imLog.setLevel(logging.WARNING)

class Product(Entity):
    #noImage_content=picture_file_to_base64(config['static']['no-image'])
    #noImage_name=config['static']['no-image'].split('/')[-1].split('.')[0]

    def __init__(self,jsonObject):
        Entity.__init__(self,jsonObject)
        if not 'image' in self._js:
            self._js['image'] = {}
            self._js['image']['filename'] = ''
        self.productFolderHref = self._js['productFolder']['meta']['href']

    def getTM(self):
        return bool(self.getAttributeById(Meta.productattribute_TMall['id']))

    def getTP(self):
        return bool(self.getAttributeById(Meta.productattribute_TPort['id']))

    def setTM(self,TM):
        if not self.getAttributeById(Meta.productattribute_TMall['id']) == TM:
            self.setAttributeById(Meta.productattribute_TMall['id'],bool(TM))
            self.isDirty = True
        return self.isDirty

    def setImageFromFile(self,filename):
        content=picture_file_to_base64(filename)

        if self._js['image']['filename'].split('@')[0] == filename.split("/")[-1].split('.')[0]:
            self._js['image']['filename']= filename.split('\\')[-1].split('.')[0] + datetime.now().strftime('@%Y-%m-%d_%H-%M-%S@.jpg')
            self._js['image']['content']=content.decode('UTF-8')
            self.isDirty = True
        return self.isDirty

    def setNullImage(self):
        self.setImageFromFile(Product.noImage_name)



    def setImageFromURL(self,urlname,size=400):
        if urlname==None:
            return "none"
        print('urlname *** ',urlname)
        if urlname.split('/')[-1].split('.')[0] == self._js['image']['filename'].split('@')[0]:
            print('картинка совпадает')
            return self.isDirty
        try:
            print('картинка не совпадает')
            r = requests.get(urlname+"?crop=1&w={}&h={}".format(size,size))
            if r.status_code!=200:
                return r.text
            content = r.content
            self._js['image']['filename']= urlname.split('/')[-1].split('.')[0] + datetime.now().strftime('@%Y-%m-%d_%H-%M-%S@.jpg')
            self._js['image']['content']=base64.b64encode(content).decode('UTF-8')
            self.isDirty = True
        except:
            return 'ошибка скачивания файла ['+urlname+'] '+r.text
        return self.isDirty

    def setImage(self,urlname,size=400):
        if not 'image' in self._js:
            imLog.warning(self.getName,urlname)
            print("NNNNNNNNNNNNNNNNNNNNNNNN",self.getName,urlname)
        if urlname==None:
            if self._js['image']['filename'].split('@')[0].split('.')[0]== Product.noImage_name:
                return self.isDirty
            return self.setNullImage(self)
        for im in urlname:
            print('+++ ',im,size)
            if type(self.setImageFromURL(im, size))!=str:
                return self.isDirty
        return 'ни одна картинка не подошла! Ахтунг!'




    def setTP(self,TP):
        if not self.getAttributeById(Meta.productattribute_TPort['id']) == TP:
            self.setAttributeById(Meta.productattribute_TPort['id'],bool(TP))
            self.isDirty = True
        return self.isDirty

    def setPFolderHref(self,folder_href):
        self.productFolderHref = folder_href
        self._js['productFolder']['meta']['href'] = folder_href

    def toString(self):
        return Entity.toString(self)+"\n"+str(self.sellPrice)+" руб "+str(self.buyPrice)+" руб " +" TP="+str(self.getTP())+"\tTM="+str(self.getTM())

    def getJson(self):
        return self._js

MetaArray.types['product'] = type(Product('1'))