
import uuid

class JObj:
    def __init__(meo):
        meo.id = uuid.uuid4().hex

    def __setattr__(self, name, value):
        newVal = value
        self.__dict__[name] = newVal

    def getAttr(self, name):
        return self.__dict__[name]

    def update(self, obj, mapper, newDoc, rawDoc):
        mapper(self, obj, newDoc, rawDoc)
        #self.__dict__.update(obj._asdict().items())      
   
