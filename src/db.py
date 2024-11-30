from pymongo import MongoClient

try:
    client = MongoClient('localhost', 27017)

    database = client['Blockchain']

    collection = database['Certificates']

    documents = collection.find()
    
    
    documento = {"nombre": "Juan", "edad": 30, "ciudad": "Bogotá"}
    result = collection.insert_one(documento)

    ultimo_documento = collection.find_one(sort=[("_id", -1)]) 
    print({"ultimo_documento": ultimo_documento})

    for document in documents:
        print(document)

except Exception as ex:
    print("Error durante la conexión: {}".format(ex))
finally:
    client.close()
    print("Conexión finalizada.")