"""This module calculates product and delivery cost for with London and outside London"""

class CostDeliveryCalcalculator:
    
    def calculate_delivery_cost(self, amount, postcode_validator, postcode):
        """
        Calculate cost of item and delivery fee based on converted amount

        :param amount: Product Cost
        :param postcode_validator: PostcodeValidator Instance
        :param postcode: Postcode
        """
        is_london = postcode_validator.is_london_postcode(postcode)

        if is_london:
            return 0
        else:
            return round(amount * 0.1, 2)
    
    def get_total_cost_with_delivery_in_pounds(self, amount, base_currency, target_currency, postcode, postcode_validator, currency_converter):
        """
        Calculate total cost including delivery

        :param amount: Product Cost
        :param base_currency: Base Currency (USD)
        :param target_currency: Target Currency (GBP)
        :param postcode: Postcode
        :param postcode_validator: PostcodeValidator Instance
        :param currency_converter: CurrencyConverter Instance
        """
        delivery_cost = self.calculate_delivery_cost(amount, postcode_validator, postcode)

        converted_delivery_cost = currency_converter.convert(delivery_cost, base_currency, target_currency)
        
        converted_amount = currency_converter.convert(amount, base_currency, target_currency)
        
        total_cost_pounds = converted_delivery_cost + converted_amount

        return total_cost_pounds
