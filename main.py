from cryptohandler import CryptoHandler

crypto_handler = CryptoHandler()

if __name__ == "__main__":
    list_currency = crypto_handler.list_specific_crypto(id="fefefe")
    print(list_currency)
