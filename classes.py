import csv
import hashlib

def encrypt_string(hash_string):
    sha_signature= hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature
def sign_up(file_name,account,password):
    with open(file_name,'a',newline='') as file:
        writer= csv.writer(file)
        writer.writerow([account,encrypt_string(password)])

def login(file_name, account,password)
    en_password=encrypt_string(password)
    with open(file_name,'r',newline='') as file:
        reader= csv.reader(file)
        for row in reader:
            r_account, r_password=row
            if account==r_account and en_password==r_password:
                return True
    return False









class Player:
    def __init__(self):
        self.identifiers=[]
    def sign_up(self, identifier, password):
        self.identifiers.append(identifier,password)

    def login(self,identifier,password)
        for element in self.identifiers:



