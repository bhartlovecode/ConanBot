from cryptography.fernet import Fernet

def load_key():
    return open("enc.key", "rb").read()

def encrypt(message):
    fernet = Fernet(load_key())
    encMessage = fernet.encrypt(message.encode())
    return encMessage
    
def decrypt(message):
    fernet = Fernet(load_key())
    decMessage = fernet.decrypt(message).decode()
    return decMessage