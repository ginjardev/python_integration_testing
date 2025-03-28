"""This module validates postcodes within the UK especially London """

import requests

class PostcodeValidator:
    def __init__(self):
        """
        Initialize postcode validator for a specific country
        """
        self.base_url = f'https://api.postcodes.io/postcodes/'
    
    def validate_uk_postcode(self, postcode):
        """
        Validate UK postcode format

        :param postcode: Postcode
        """
        api_endpoint = self.base_url + f'{postcode}'
        response = requests.get(api_endpoint)
        result = response.json()
        if result['status'] != 200:
            raise ValueError(f'{postcode} is not a valid postcode')
        city = result['result']['nhs_ha']
        return city
    

    def is_london_postcode(self, postcode):
        """
        Check if a postcode is in London

        :param postcode: Postcode
        """
        city = self.validate_uk_postcode(postcode)

        if city == 'London':
            return True
        else:
            return False