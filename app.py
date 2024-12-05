#made by anish
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, static_folder='static')

AGORIC_RPC_URL = 'https://main.rpc.agoric.net'  # Replace with actual Agoric RPC URL
CONTRACT_ADDRESS = '0x43A1ffC542ac525Db3F7C930Ea61d39A1E8fe823'  # Replace with actual contract address

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/buy', methods=['POST'])
def buy_product():
    products = request.json.get('products')
    user_wallet = request.json.get('user_wallet')
    
    if not products or not user_wallet:
        return jsonify({'status': 'error', 'message': 'Invalid request'}), 400

    transaction_hashes = []
    for product in products:
        amount = float(product['price'])  # Ensure amount is a float
        transaction_hash = process_payment(user_wallet, amount)
        transaction_hashes.append(transaction_hash)

    return jsonify({'status': 'success', 'transaction_hashes': transaction_hashes})

def process_payment(user_wallet, amount):
    # Replace with actual Agoric transaction logic
    payload = {
        "tx": {
            "msg": [{
                "type": "cosmos-sdk/MsgSend",
                "value": {
                    "from_address": user_wallet,
                    "to_address": CONTRACT_ADDRESS,
                    "amount": [{
                        "denom": "uagoric",
                        "amount": str(int(amount * 1e6))  # Convert to micro units
                    }]
                }
            }],
            "fee": {
                "amount": [{
                    "denom": "uagoric",
                    "amount": "5000"
                }],
                "gas": "200000"
            },
            "signatures": [],
            "memo": ""
        }
    }

    try:
        response = requests.post(f'{AGORIC_RPC_URL}/broadcast_tx_sync', json={"jsonrpc": "2.0", "id": 1, "method": "broadcast_tx_sync", "params": [payload]})
        response.raise_for_status()
        response_data = response.json()
        print(response_data)
        return response_data.get('result', {}).get('hash', 'unknown')  # Corrected key to 'hash'
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return 'unknown'

@app.route('/swap', methods=['POST'])
def swap_tokens():
    return jsonify({'status': 'error', 'message': 'Swap functionality has been removed'})

if __name__ == '__main__':
    app.run(debug=True)
