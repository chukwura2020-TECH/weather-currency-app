# api/currency_api.py
"""
Currency conversion API integration using ExchangeRate-API.
"""
import requests
from config import CURRENCY_API_KEY

class CurrencyAPI:
    """Handles currency conversion and exchange rate fetching"""
    
    def __init__(self):
        self.api_key = CURRENCY_API_KEY
        self.base_url = f"https://v6.exchangerate-api.com/v6/{self.api_key}"
    
    def get_exchange_rate(self, from_currency, to_currency):
        """
        Get exchange rate between two currencies.
        
        Args:
            from_currency (str): Source currency code (e.g., "USD")
            to_currency (str): Target currency code (e.g., "EUR")
            
        Returns:
            float: Exchange rate or None if error
        """
        try:
            url = f"{self.base_url}/pair/{from_currency}/{to_currency}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data['result'] == 'success':
                return data['conversion_rate']
            else:
                print(f"API Error: {data.get('error-type', 'Unknown error')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exchange rate: {e}")
            return None
    
    def convert_currency(self, amount, from_currency, to_currency):
        """
        Convert amount from one currency to another.
        
        Args:
            amount (float): Amount to convert
            from_currency (str): Source currency
            to_currency (str): Target currency
            
        Returns:
            dict: Conversion result with rate and converted amount
        """
        rate = self.get_exchange_rate(from_currency, to_currency)
        
        if rate:
            converted = amount * rate
            return {
                'from_currency': from_currency,
                'to_currency': to_currency,
                'amount': amount,
                'rate': rate,
                'converted': round(converted, 2)
            }
        else:
            return None
    
    def get_supported_currencies(self):
        """
        Get list of supported currency codes.
        
        Returns:
            list: List of currency codes
        """
        # Common currencies (you can expand this list)
        return [
            'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY',
            'SEK', 'NZD', 'MXN', 'SGD', 'HKD', 'NOK', 'KRW', 'TRY',
            'INR', 'RUB', 'BRL', 'ZAR', 'DKK', 'PLN', 'THB', 'IDR',
            'HUF', 'CZK', 'ILS', 'CLP', 'PHP', 'AED', 'SAR', 'MYR',
            'NGN', 'ARS', 'TWD', 'VND', 'UAH', 'BDT', 'PKR', 'EGP'
        ]