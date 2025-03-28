"""This module converts product amount from Base Currency (USD) to Pounds Sterling (GBP)"""

import freecurrencyapi

class CurrencyConverter:
    def __init__(self, api_key):
        """
        Initialize the currency converter with a base API URL
        """
        self.API_KEY = api_key
    
    def get_exchange_rate(self, base_currency, target_currency):
        """
        Fetch the current exchange rate between two currencies

        :param base_currency: Base Currency (USD)
        :param target_currency: Target Currency (GBP)
        """
        try:
            client = freecurrencyapi.Client(api_key=self.API_KEY)
            result = client.latest(base_currency=base_currency, currencies=[target_currency])
            data = result['data']
            return data[target_currency]
        except:
            return None
    
    def convert(self, amount, base_currency, target_currency):
        """
        Convert an amount from one currency to another

        :param amount: Product Cost
        :param base_currency: Base Currency (USD)
        :param target_currency: Target Currency (GBP)
        """
        rate = self.get_exchange_rate(base_currency, target_currency)
        return round(amount * rate, 2)

