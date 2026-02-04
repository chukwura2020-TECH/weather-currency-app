# test_currency_api.py
"""Test the Currency API"""
from api.currency_api import CurrencyAPI

def test_currency_api():
    api = CurrencyAPI()
    
    # Test exchange rate
    print("Testing USD to EUR exchange rate...")
    rate = api.get_exchange_rate("USD", "EUR")
    
    if rate:
        print(f"✅ Success! 1 USD = {rate} EUR")
    else:
        print("❌ Failed to fetch exchange rate")
    
    # Test conversion
    print("\nTesting conversion: 100 USD to GBP...")
    result = api.convert_currency(100, "USD", "GBP")
    
    if result:
        print(f"✅ Success!")
        print(f"   {result['amount']} {result['from_currency']} = {result['converted']} {result['to_currency']}")
        print(f"   Rate: {result['rate']}")
    else:
        print("❌ Failed to convert")
    
    # Test supported currencies
    currencies = api.get_supported_currencies()
    print(f"\n✅ {len(currencies)} currencies supported")

if __name__ == "__main__":
    test_currency_api()