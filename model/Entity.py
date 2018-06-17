from meta.MetaArray2 import timeFromString


class Entity:
    def __init__(self,jsonObject):
        self.isDirty = False
        self._js = jsonObject

    def getAttributeById(self,id):
        if not 'attributes' in self._js:
            return None
        for attr in self._js['attributes']:
            if attr['id'] == id:
                return attr['value']
        raise Exception()
        return None

    def getId(self):
        print('getting id',id)
        return self._js['id']

    def getType(self):
        return self._js['meta']['type']

    def getHRef(self):
        return self._js['meta']['href']

    def setAttributeById(self,id,value):
        for attr in self._js['attributes']:
            if attr['id'] == id:
                if not attr['id']==value:
                    attr['value'] = value
                    self.isDirty = True
        return self.isDirty

    def getUpdated(self):
        return timeFromString(self._js['updated'])

    def getExternalCode(self):
        return self._js['externalCode']

    def setName(self,name):
        if not self.__name == name:
            self.__name = name
            self._js['name'] = name
            self.isDirty = True
        return self.isDirty

    def getName(self):
        return self._js['name']

    def getArchived(self):
        return bool(self._js['archived'])

    def setArchived(self, arch):
        if not self.archived==arch:
            self.archived = arch
            self._js['archived'] = arch
            self.isDirty = True
        return self.isDirty
    def getSum(self):
        return self._js['sum']/100.0


    href = property(getHRef, None)
    type = property(getType, None)
    updated = property(getUpdated, None)
    externalCode = property(getExternalCode, None)
    name = property(getName, setName)
    archived = property(getArchived, setArchived)
    id = property(getId, None)

    def __str__(self):
        return self.getName() + "\t" + self.getType() + "\t" + self.getExternalCode() + "\n" + self.id + "\t" + \
               "архивный =" + str(self.getArchived()) + "\t" + "обновлен = " + str(self.getUpdated())