from cryptohandler import CryptoHandler

crypto_handler = CryptoHandler()

if __name__ == "__main__":
    list_currency = crypto_handler.list_crypto_currencies()
    print(list_currency)
