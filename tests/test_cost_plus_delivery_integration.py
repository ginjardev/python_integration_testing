from samples.currency_postcode_apis.currency_converter import CurrencyConverter
from samples.currency_postcode_apis.postcode_validator import PostcodeValidator
from samples.currency_postcode_apis.DeliveryCostCalculator import DeliveryCostCalculator
import pytest
import os


API_KEY = os.getenv("API_KEY")

@pytest.fixture
def currency_converter():
    return CurrencyConverter(api_key=API_KEY)


@pytest.fixture
def postcode_validator():
    return PostcodeValidator()


@pytest.fixture
def delivery_cost_calculator():
    return DeliveryCostCalculator()


@pytest.mark.parametrize('numbers, expected', [((10, 'USD', 'GBP'), 7.72)])
def test_currency_converter_api(currency_converter, numbers, expected):
    assert currency_converter.convert(numbers[0], numbers[1], numbers[2]) == expected


@pytest.mark.parametrize('postcode, expected', [('SW1A1AA', True)])
def test_postcode_validator_api(postcode_validator, postcode, expected):
    assert postcode_validator.is_london_postcode(postcode) == expected


@pytest.mark.parametrize('test_data', [
    {
        "amount": 20,
        "base_currency": "USD",
        "target_currency": "GBP",
        "postcode": "SW1A2HQ",
    },
    {
        "amount": 50,
        "base_currency": "USD",
        "target_currency": "GBP",
        "postcode": "EH216UU",
    },    
])
def test_delivery_cost_calculator_flow(postcode_validator, currency_converter, delivery_cost_calculator,test_data):
    delivery_cost = delivery_cost_calculator.calculate_delivery_cost(test_data['amount'], postcode_validator, test_data['postcode'])
    delivery_cost_pounds = currency_converter.convert(delivery_cost, test_data['base_currency'], test_data['target_currency'])
    converted_amount_pounds = currency_converter.convert(test_data['amount'], test_data['base_currency'], test_data['target_currency'],)
    cost_plus_delivery_pounds = delivery_cost_pounds + converted_amount_pounds

    if test_data['postcode'] == 'SW1A2HQ':
        assert delivery_cost == 0, f"Expected cost is 0 but got {delivery_cost}"
        assert delivery_cost_pounds == 0, f"Expected converted cost is 0 but got {delivery_cost_pounds}"
        assert converted_amount_pounds == 15.44, f"Expected converted amount pounds cost is 0 but got {converted_amount_pounds}" 
        assert converted_amount_pounds == 15.44, f"Expected converted amount pounds cost is 0 but got {cost_plus_delivery_pounds}" 
    else:
        assert delivery_cost == 5, f"Expected cost is 15.44 but got {delivery_cost}"
        assert delivery_cost_pounds == 3.86, f"Expected converted cost is 3.86 but got {delivery_cost_pounds}"
        assert converted_amount_pounds == 38.61, f"Expected converted amount pounds cost is 38.61 but got {converted_amount_pounds}"
        assert cost_plus_delivery_pounds == 42.47, f"Expected converted amount pounds cost is 0 but got {cost_plus_delivery_pounds}" 

    
