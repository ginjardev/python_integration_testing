from samples.currency_postcode_apis.currency_converter import CurrencyConverter
from samples.currency_postcode_apis.postcode_validator import PostcodeValidator
from samples.currency_postcode_apis.cost_delivery_calculator import CostDeliveryCalcalculator
import pytest
import os
from conftest import set_test_status


API_KEY = os.getenv("API_KEY")

# currency converter fixture
@pytest.fixture
def currency_converter():
    return CurrencyConverter(api_key=API_KEY)

# postcode validator fixture
@pytest.fixture
def postcode_validator():
    return PostcodeValidator()

# product and delivery cost fixture
@pytest.fixture
def cost_delivery_calculator():
    return CostDeliveryCalcalculator()


@pytest.mark.parametrize('numbers, expected', [((10, 'USD', 'GBP'), 7.73)])
def test_currency_converter_api(currency_converter, numbers, expected, set_test_status):
    assert currency_converter.convert(numbers[0], numbers[1], numbers[2]) == expected
    set_test_status(status="passed", remark="API builds metadata returned")



@pytest.mark.parametrize('postcode, expected', [('SW1A1AA', True)])
def test_postcode_validator_api(postcode_validator, postcode, expected, set_test_status):
    assert postcode_validator.is_london_postcode(postcode) == expected
    set_test_status(status="passed", remark="API builds metadata returned")


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
def test_delivery_cost_calculator_flow(postcode_validator, currency_converter, cost_delivery_calculator,test_data, set_test_status):
    # caliculate delivery cost in USD
    delivery_cost = cost_delivery_calculator.calculate_delivery_cost(test_data['amount'], postcode_validator, test_data['postcode'])
    # convert delivery cost to GBP
    delivery_cost_pounds = currency_converter.convert(delivery_cost, test_data['base_currency'], test_data['target_currency'])
    # conveert product amount to GBP
    converted_amount_pounds = currency_converter.convert(test_data['amount'], test_data['base_currency'], test_data['target_currency'],)
    # print(converted_amount_pounds)
    # calculate cost of delivery and product amount
    cost_delivery_pounds = delivery_cost_pounds + converted_amount_pounds

    # assertion for London postcode
    if test_data['postcode'] == 'SW1A2HQ':
        assert delivery_cost == 0, f"Expected delivery cost is 0 but got {delivery_cost}"
        assert delivery_cost_pounds == 0, f"Expected converted cost is 0 but got {delivery_cost_pounds}"
        assert converted_amount_pounds == 15.45, f"Expected converted amount (pounds) cost is 0 but got {converted_amount_pounds}" 
        assert cost_delivery_pounds == 15.45, f"Expected converted amount (pounds) cost is 0 but got {cost_delivery_pounds}" 
        set_test_status(status="passed", remark="API builds metadata returned")                              

    else:
        # assertion for postcode outside London
        assert delivery_cost == 5, f"Expected cost is 15.44 but got {delivery_cost}"
        assert delivery_cost_pounds == 3.86, f"Expected converted cost is 3.86 but got {delivery_cost_pounds}"
        assert converted_amount_pounds == 38.63, f"Expected converted amount (pounds) cost is 38.63 but got {converted_amount_pounds}"
        assert cost_delivery_pounds == 42.49, f"Expected cost and delivery (pounds) cost is 42.49 but got {cost_delivery_pounds}" 
        set_test_status(status="passed", remark="API builds metadata returned")
    

    
