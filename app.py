from flask import Flask, request, jsonify, render_template

from web3 import Web3, HTTPProvider

# import flask cors
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Replace with the appropriate Ethereum network URL
ETHEREUM_NETWORK_URL = "http://127.0.0.1:7545"

# Replace with the ABI (JSON interface) of the deployed contract
PRODUCT_INFO_ABI = [
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_name",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_userAddress",
                "type": "string"
            },
            {
                "internalType": "enum ProductInfo.ProductType",
                "name": "_productType",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "_quantity",
                "type": "uint256"
            },
            {
                "internalType": "enum ProductInfo.SourceType",
                "name": "_sourceType",
                "type": "uint8"
            }
        ],
        "name": "storeUserInfo",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getAllUsers",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "userId",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "name",
                        "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "userAddress",
                        "type": "string"
                    },
                    {
                        "internalType": "enum ProductInfo.ProductType",
                        "name": "productType",
                        "type": "uint8"
                    },
                    {
                        "internalType": "uint256",
                        "name": "quantity",
                        "type": "uint256"
                    },
                    {
                        "internalType": "enum ProductInfo.SourceType",
                        "name": "sourceType",
                        "type": "uint8"
                    }
                ],
                "internalType": "struct ProductInfo.UserInfo[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_userId",
                "type": "uint256"
            }
        ],
        "name": "getUserInfo",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            },
            {
                "internalType": "enum ProductInfo.ProductType",
                "name": "",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "enum ProductInfo.SourceType",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Replace with the address of the deployed contract
PRODUCT_INFO_ADDRESS = "0x85C2fe10aF2FF30687Fb22f61e19cFd0cD6F2Fbd"

w3 = Web3(HTTPProvider(ETHEREUM_NETWORK_URL))

# Replace with your Ethereum account's private key
PRIVATE_KEY = "0x593fb0fbba2345c257d9b2796cff84e082e73eb6597270b095146d12e6b15bd2"

# Replace with your Ethereum account's address
FROM_ADDRESS = "0x2EEACe322cE73a24fa3FA67b4e797f6c6DAec7dA"

product_info_contract = w3.eth.contract(
    address=PRODUCT_INFO_ADDRESS, abi=PRODUCT_INFO_ABI)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/store_user_info", methods=["POST"])
def store_user_info():
    # make it get data from json type
    name = request.json["name"]
    user_address = request.json["user_address"]
    product_type = int(request.json["product_type"])
    quantity = int(request.json["quantity"])
    source_type = int(request.json["source_type"])

    nonce = w3.eth.getTransactionCount(FROM_ADDRESS)
    txn = product_info_contract.functions.storeUserInfo(name, user_address, product_type, quantity,
                                                        source_type).buildTransaction({
                                                            'from': FROM_ADDRESS,
                                                            'gas': 2000000,
                                                            'gasPrice': w3.eth.gasPrice,
                                                            'nonce': nonce
                                                        })

    signed_txn = w3.eth.account.signTransaction(txn, PRIVATE_KEY)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    return jsonify({"transaction_hash": txn_hash.hex()}), 200


@app.route("/get_user_info/<int:user_id>", methods=["GET"])
def get_user_info(user_id):
    user_info = product_info_contract.functions.getUserInfo(user_id).call()
    return jsonify({
        "user_id": user_info[0],
        "name": user_info[1],
        "user_address": user_info[2],
        "product_type": user_info[3],
        "quantity": user_info[4],
        "source_type": user_info[5]
    }), 200


@app.route("/get_all_users", methods=["GET"])
def get_all_users():
    data = []
    all_users = product_info_contract.functions.getAllUsers().call()
    for user in all_users:
        data.append({
            "user_id": user[0],
            "name": user[1],
            "user_address": user[2],
            "product_type": user[3],
            "quantity": user[4],
            "source_type": user[5]
        })
    return jsonify(data), 200


if __name__ == "__main__":
    print('running on http://localhost:5000')
    app.run(debug=True)


# Uncaught (in promise) SyntaxError: Unexpected token '<', "<!doctype "... is not valid JSON