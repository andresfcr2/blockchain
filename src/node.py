from flask import Flask, jsonify, request
from uuid import uuid4
from db import MongoDB
from datetime import datetime
import hashlib, json
from flask.json import JSONEncoder
from bson import json_util


app = Flask(__name__)
mongodb = MongoDB()

@app.route('/hw', methods=['GET'])
def hw():
    return 'It works!!!', 200


@app.route('/', methods=['POST'])
def new_transaction():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file part in the request"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected"}), 400
        
        data = request.form.get('data')
        if not data:
            return jsonify({"success": False, "error": "No transation data passed"}), 400
        

        data = json.loads(data)
        required = [
            "issuer",
            "recipient",
            "validity_period",
            "status",
            "metadata",
        ]
        
        missing = [x for x in required if x not in list(data.keys()) ]
        if len(missing) > 0:
            return jsonify({"success": False, "error": f"Missing data: {', '.join(missing)}"}), 400
        
        
        certificate_id = uuid4()
        hex = certificate_id.hex
        certificate_id = certificate_id.__str__()
        
            
        filename = f"{hex}.{file.filename.rsplit('.', 1)[-1]}"
        file.save(f"../uploads/{filename}")
        
        
        file_hash = calculate_file_hash(file)
        
    
        last = mongodb.getLastOne()
        
        print({"last": last})
    
        
        payload = data.copy()
        payload["certificate_id"] = certificate_id
        payload["document_hash"] = file_hash
        payload["timestamp"] = str(datetime.now())
        payload["previous_hash"] = last['document_hash']
        payload["status"] = "ACTIVE"
        
        
        id = mongodb.insert(payload)
        response = {
            "success": True,
            "mongoId": id,
            "certificate_id": certificate_id,
        }

        return jsonify(response), 201
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error":f'An error ocurred while processing request: {e}'}), 201
        
    
@app.route('/', methods=['GET'])
def get_chain():

    document = mongodb.getAll()
    response = {
        'length':len(document),
        'chain': document
    }

    return jsonify(response), 200


@app.route('/last', methods=['GET'])
def getLastRecord():
    return jsonify(mongodb.getLastOne()), 200



def calculate_file_hash(file):
    hash_func = hashlib.new('sha256')
    
    for chunk in iter(lambda: file.read(4096), b""):
        hash_func.update(chunk)
    
    return hash_func.hexdigest()

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj): return json_util.default(obj)
app.json_encoder = CustomJSONEncoder

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)
