from meta.MetaArray2 import MetaArray
from model.Entity import Entity


class Return(Entity):
    def __init__(self,jsonObject):
        Entity.__init__(self,jsonObject)


MetaArray.types['salesreturn'] = type(Return('1'))