from flask import Flask, render_template, request, redirect, url_for, flash
import iota_client
import math
import os

app = Flask(__name__)

#IOTA
IOTA_NODE = os.environ.get('IOTA_NODE','https://multiverse.dlt.green')
SHIMMER_NODE = os.environ.get('SHIMMER_NODE','https://api.shimmer.network')

client = iota_client.IotaClient({'nodes': [SHIMMER_NODE]})

# Path: /
@app.route('/address/<address>')
def verify_address(address):
    return str(client.is_address_valid(address))
  
def si_unit_iota(val):
    val = float(val)
    if val == 0: return "0 IOTA"
    if math.floor(math.log10(val)) < 3: 
        return f"{int(val)} IOTA"
    elif math.floor(math.log10(val)) < 3*2: 
        return f"{int(val/(10**(3)))} KIOTA"
    elif math.floor(math.log10(val)) < 3*3: 
        return f"{int(val/(10**(3*2)))} MIOTA"
    elif math.floor(math.log10(val)) < 3*4: 
        return f"{int(val/(10**(3*3)))} GIOTA"
    elif math.floor(math.log10(val)) < 3*5: 
        return f"{int(val/(10**(3*4)))} TIOTA"
    elif math.floor(math.log10(val)) < 3*6: 
        return f"{int(val/(10*(3*5)))} PIOTA"
def si_unit_smr(val):
    val = float(val)
    if val == 0: return "0 SMR"
    if math.floor(math.log10(val)) < 3: 
        return f"{int(val)} uSMR"
    elif math.floor(math.log10(val)) < 3*2: 
        return f"{int(val/(10**(3)))} mSMR"
    elif math.floor(math.log10(val)) < 3*3: 
        return f"{int(val/(10**(3*2)))} SMR"
    elif math.floor(math.log10(val)) < 3*4: 
        return f"{int(val/(10**(3*3)))} KSMR"
    elif math.floor(math.log10(val)) < 3*5: 
        return f"{int(val/(10**(3*4)))} GSMR"
    elif math.floor(math.log10(val)) < 3*6: 
        return f"{int(val/(10*(3*5)))} TSMR"

@app.route('/balance/<address>')
def get_balance(address: str):
    if not client.is_address_valid(address):
        return {'error': 'Not a valid address'}
    elif address[:4]=="iota":
        return si_unit_iota(get_iota_balance(address))
    elif address[:3]=="smr":
        return si_unit_smr(get_smr_balance(address))
    else:
        return {'error': 'This token is not supported'}
def get_smr_balance(address):
    output_ids = client.basic_output_ids([{"address": address},
                                        {"hasExpiration": False},
                                        {"hasTimelock": False},
                                        {"hasStorageDepositReturn": False}, ])
    outputs = client.get_outputs(output_ids)
    total_amount = 0
    for output_response in outputs:
        output = output_response['output']
        total_amount += int(output['amount'])
    return str(total_amount)

def get_iota_balance(address):
    domain = IOTA_NODES
    endpoint = f"{domain}api/v1/addresses/{address}"
    logging.warning(endpoint)
    r = requests.get(endpoint)
    if r.status_code==200 and 'data' in r.json():
        return str(r.json()['data']['balance'])
    else:
        return {'error': 'No balance for this address', 'data': r.text}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5055, debug=True)