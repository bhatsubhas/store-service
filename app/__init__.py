from flask import Flask, request

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 1599
            }
        ]
    }
]

app = Flask(__name__)

@app.get("/stores")
def get_stores():
    return {
        "stores": stores
    }

@app.post("/stores")
def create_stores():
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
        "items": []
    }
    stores.append(new_store)
    return new_store, 201

@app.post("/stores/<string:name>/items")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {
                "name": request_data["name"],
                "price": request_data["price"]
            }
            store["items"].append(new_item)
            return new_item
    return {
        "error": "STORE_NOT_FOUND"
    }, 404