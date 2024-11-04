from cryptohandler import CryptoHandler

crypto_handler = CryptoHandler()

if __name__ == "__main__":
    list_currency = crypto_handler.get_total_volume(base_currency="usd")
    print(list_currency)
