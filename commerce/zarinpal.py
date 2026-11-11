import requests
from django.conf import settings


def gateway_urls():
    if settings.ZARINPAL_SANDBOX:
        api = "https://sandbox.zarinpal.com/pg/v4/payment"
        start = "https://sandbox.zarinpal.com/pg/StartPay"
    else:
        api = "https://api.zarinpal.com/pg/v4/payment"
        start = "https://www.zarinpal.com/pg/StartPay"
    return api, start


def request_payment(amount, order_id):
    api, start = gateway_urls()
    response = requests.post(f"{api}/request.json", json={
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": amount,
        "description": f"SHD Shop order #{order_id}",
        "callback_url": settings.ZARINPAL_CALLBACK_URL,
    }, timeout=15)
    response.raise_for_status()

    data = response.json().get("data", {})
    if data.get("code") != 100:
        raise ValueError("Zarinpal did not create the payment.")

    authority = data["authority"]
    return authority, f"{start}/{authority}"


def verify_payment(authority, amount):
    api, _ = gateway_urls()
    response = requests.post(f"{api}/verify.json", json={
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": amount,
        "authority": authority,
    }, timeout=15)
    response.raise_for_status()

    data = response.json().get("data", {})
    if data.get("code") not in (100, 101):
        raise ValueError("Payment verification failed.")
    return str(data.get("ref_id", ""))

