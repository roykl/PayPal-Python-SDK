# Create Payment Using PayPal Sample against endpoint 
# that only allows an acceptable highest TLS version
from paypalrestsdk as paypal
import logging
logging.basicConfig(level=logging.INFO)

paypal.configure({
  "mode": "security-test-sandbox", # sandbox or live
  "client_id": "<CLIENT_ID>",
  "client_secret": "<CLIENT_SECRET>" })

# Payment
# A Payment Resource; create one using
# the above types and intent as 'sale'
payment = paypal.Payment({
    "intent": "sale",

    # Payer
    # A resource representing a Payer that funds a payment
    # Payment Method as 'paypal'
    "payer": {
        "payment_method": "paypal"},

    # Redirect URLs
    "redirect_urls": {
        "return_url": "http://localhost:3000/payment/execute",
        "cancel_url": "http://localhost:3000/"},

    # Transaction
    # A transaction defines the contract of a
    # payment - what is the payment for and who
    # is fulfilling it.
    "transactions": [{

        # ItemList
        "item_list": {
            "items": [{
                "name": "item",
                "sku": "item",
                "price": "5.00",
                "currency": "USD",
                "quantity": 1}]},

        # Amount
        # Let's you specify a payment amount.
        "amount": {
            "total": "5.00",
            "currency": "USD"},
        "description": "This is the payment transaction description."}]})

# Create Payment and return status
if payment.create():
    print("Payment[%s] created successfully" % (payment.id))
    # Redirect the user to given approval url
    for link in payment.links:
        if link.method == "REDIRECT":
            # Convert to str to avoid google appengine unicode issue
            # https://github.com/paypal/rest-api-sdk-python/pull/58
            redirect_url = str(link.href)
            print("Redirect for approval: %s" % (redirect_url))
else:
    print("Error while creating payment:")
    print(payment.error)
