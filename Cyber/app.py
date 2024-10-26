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

@app.route('/dm_with_decisionprofilereject_response', methods=['POST'])
def mydm_with_decisionprofilereject_response():
    data = request.json
    
    clientReferenceInformationCode = "123455"
    clientReferenceInformation = Riskv1decisionsClientReferenceInformation(
        code = clientReferenceInformationCode
    )


    paymentInformationCardNumber = "4444444444444448"
    paymentInformationCardExpirationMonth = "12"
    paymentInformationCardExpirationYear = "2030"
    paymentInformationCard = Riskv1decisionsPaymentInformationCard(
        number = paymentInformationCardNumber,
        expiration_month = paymentInformationCardExpirationMonth,
        expiration_year = paymentInformationCardExpirationYear
    )

    paymentInformation = Riskv1decisionsPaymentInformation(
        card = paymentInformationCard.__dict__
    )

    orderInformationAmountDetailsTotalAmount = data["amount"]
    orderInformationAmountDetailsCurrency = data["currency"]
    orderInformationAmountDetails = Riskv1decisionsOrderInformationAmountDetails(
        currency = orderInformationAmountDetailsCurrency,
        total_amount = orderInformationAmountDetailsTotalAmount
    )

 
    orderInformationBillToAddress1 = "96, powers street"
    orderInformationBillToAdministrativeArea = "NH"
    orderInformationBillToCountry = "US"
    orderInformationBillToLocality = "Clearwater milford"
    orderInformationBillToFirstName = "James"
    orderInformationBillToLastName = "Smith"
    orderInformationBillToPhoneNumber = "7606160717"
    orderInformationBillToEmail = "assesment@reject.com"
    orderInformationBillToPostalCode = "03055"
    orderInformationBillTo = Riskv1decisionsOrderInformationBillTo(
        address1 = orderInformationBillToAddress1,
        administrative_area = orderInformationBillToAdministrativeArea,
        country = orderInformationBillToCountry,
        locality = orderInformationBillToLocality,
        first_name = orderInformationBillToFirstName,
        last_name = orderInformationBillToLastName,
        phone_number = orderInformationBillToPhoneNumber,
        email = orderInformationBillToEmail,
        postal_code = orderInformationBillToPostalCode
    )

    orderInformation = Riskv1decisionsOrderInformation(
        amount_details = orderInformationAmountDetails.__dict__,
        bill_to = orderInformationBillTo.__dict__
    )

    riskInformationProfileName = "profile2"
    riskInformationProfile = Ptsv2paymentsRiskInformationProfile(
        name = riskInformationProfileName
    )

    riskInformation = Riskv1decisionsRiskInformation(
        profile = riskInformationProfile.__dict__
    )


    requestObj = CreateBundledDecisionManagerCaseRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        payment_information = paymentInformation.__dict__,
        order_information = orderInformation.__dict__,
        risk_information = riskInformation.__dict__
    )

    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)

    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = DecisionManagerApi(client_config)
        return_data, status, body = api_instance.create_bundled_decision_manager_case(requestObj)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        print("Transaction rejectedt due to email address ", orderInformationBillTo._email)

        write_log_audit(status)

        return {'status': status, 'response': body}, 201, {'Content-Type': 'application/json'}
    
    except Exception as e:
        write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling DecisionManagerApi->create_bundled_decision_manager_case: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

if __name__ == '__main__':
    app.run()