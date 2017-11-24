import collections
import requests
import json
from .models import *

keys = json.load(open("Django_Multiple/credentials.json"))
headers = {
        #The first three are from my developer account
        "X-PAYPAL-SECURITY-USERID":keys["user_id"],
        "X-PAYPAL-SECURITY-PASSWORD":keys["password"],
        "X-PAYPAL-SECURITY-SIGNATURE":keys["signature"],
        "X-PAYPAL-APPLICATION-ID": "APP-80W284485P519543T",
        "X-PAYPAL-SERVICE-VERSION":"1.1.0",
        "X-PAYPAL-REQUEST-DATA-FORMAT":"JSON",
        "X-PAYPAL-RESPONSE-DATA-FORMAT":"JSON"
        }
# Store your paypal credentials in a separate file (my example:
# "credentials.json" in paypal_project folder) and add that file to .gitignore.
# Retrieve credentials like so:



def payment(recipient_email, dollars, customer):
    params = collections.OrderedDict()
    params = {
        "actionType":"PAY",    #Specify the payment action
        "currencyCode":"USD",
        "receiverList":{"receiver":[{ "amount":"", "email":""}]  # The payment Receiver's email address
    },
        # Where the Sender is redirected to after approving a successful payment
        "returnUrl":"http://ec2-52-74-218-145.ap-southeast-1.compute.amazonaws.com:2000/paypal-order-placed/",
        # Where the Sender is redirected to upon a canceled payment
        "cancelUrl":"http://ec2-52-74-218-145.ap-southeast-1.compute.amazonaws.com:2000/order-cancel/",
        "requestEnvelope":{
        "errorLanguage":"en_US",
        "detailLevel":"ReturnAll"
    }
    }
    # Assign recipients email and paid amount in dollars to appropriate params:
    params["receiverList"]["receiver"][0]["email"] = "manoj.dutt@mobiloitte.in"
    params["receiverList"]["receiver"][0]["amount"] = str(int(float(dollars)))
    for vendor in recipient_email:
        params["receiverList"]["receiver"].append(vendor)

    # Send a Pay request to PayPal
    url = "https://svcs.sandbox.paypal.com/AdaptivePayments/Pay"
    response = requests.post(url, data=json.dumps(params), headers=headers)

    # Check the response:
    print(response.content.decode())
    response_string = response.content.decode("utf-8")
    response_dict = json.loads(response_string)
    payKey = response_dict.get("payKey")
    if response_dict['responseEnvelope']['ack'] == 'Success':
        CustomerTransactionDetails.objects.create(customer=customer,
                                                  pay_key=payKey)
        data = {}
        data['ack'] = response_dict['responseEnvelope']['ack']
        data['url'] = "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_ap-payment&paykey=" + payKey
        return data
    else:

        return response_dict


def paypal_payment_details(paykey):
    url = "https://svcs.sandbox.paypal.com/AdaptivePayments/PaymentDetails"
    params = collections.OrderedDict()
    params = {"payKey": paykey,
                "requestEnvelope":{
                    "errorLanguage":"en_US",
                    "detailLevel":"ReturnAll"   # Error detail level
                }}
    response = requests.post(url, data=json.dumps(params), headers=headers)
    return response.content
