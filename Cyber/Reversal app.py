import os
import json
from CyberSource import *
from pathlib import Path
from flask import Flask, request, jsonify, Response
from CyberSource import PaymentsApi, CreatePaymentRequest
from importlib.machinery import SourceFileLoader

config_file = os.path.join(os.getcwd(), "data", "Configuration.py")
configuration = SourceFileLoader("module.name", config_file).load_module()

app = Flask(__name__)

def del_none(d):
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d

@app.route('/process_authorization_reversal', methods=['POST'])
def myprocess_authorization_reversal():
    data = request.json
    
    clientReferenceInformationCode = "Jorge1234"
    clientReferenceInformation = Ptsv2paymentsidreversalsClientReferenceInformation(
        code = clientReferenceInformationCode
    )

    
    orderInformationAmountDetailsTotalAmount = data["amount"]
    orderInformationAmountDetailsCurrency = data["currency"]

    reversalInformationAmountDetailsTotalAmount = "123.50"
    reversalInformationAmountDetails = Ptsv2paymentsidreversalsReversalInformationAmountDetails(
        total_amount = reversalInformationAmountDetailsTotalAmount
    )


    reversalInformationReason = "testingJorge"
    reversalInformation = Ptsv2paymentsidreversalsReversalInformation(
        amount_details = reversalInformationAmountDetails.__dict__,
        reason = reversalInformationReason
    )


    requestObj = AuthReversalRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        reversal_information = reversalInformation.__dict__
    )

    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)

    try:
        id = 7296658339216694903954
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = ReversalApi(client_config)
        return_data, status, body = api_instance.auth_reversal(id, requestObj)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        write_log_audit(status)

        return {'status': status, 'response': body}, 201, {'Content-Type': 'application/json'}
    
    except Exception as e:
        write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling ReversalApi->reversal_payment: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

if __name__ == '__main__':
    app.run()