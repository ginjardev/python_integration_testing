import freecurrencyapi
import requests
import os

API_KEY = os.getenv("API_KEY")

print(API_KEY)
# Modules being tested
def convert_currency(base_currency, target_currency, amount):
    """Integrates with currency conversion API"""
    client = freecurrencyapi.Client(api_key=API_KEY)
    # print(client.status())
    try:
        result = client.latest(base_currency=base_currency, currencies=[target_currency])
    except ValueError as e:
        print(f"Currency {target_currency} not found")
    rate = result['data'][target_currency]
    print(rate * amount)
    

convert_currency('USD', 'GPJ', 20)

    # response = requests.get(
    #     f"https://api.finance.com/convert?amount={amount}&target={target_currency}"
    # )
    # response.raise_for_status()
    # return response.json()["converted_amount"]

# def validate_address(zipcode: str) -> dict:
#     """Integrates with postal validation API"""
#     response = requests.get(f"https://api.postal.com/validate/{zipcode}")
#     response.raise_for_status()
#     return response.json()


