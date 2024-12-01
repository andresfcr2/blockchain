from  pymongo import MongoClient
import json
from bson import json_util

class MongoDB: 
    def __init__(self):
        self._conn = MongoClient('mongo', 27017)
        self._db   = self._conn['Blockchain']
        self.collection = self._db['Certificates']
        
        
    def getAll(self):
        return self.parse_json(self.collection.find())
    
    
    def insert(self, document):
        result = self.collection.insert_one(document)
        return result.inserted_id.__str__()
    
    
    @staticmethod
    def parse_json(data):
        return json.loads(json_util.dumps(data))
        
if __name__ == '__main__':
    database   = MongoDB("Hello")
    collection = database.createCollection("MyTable")