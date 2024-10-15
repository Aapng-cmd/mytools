import zipfile

def crack_password(password_list, zip_file):
    idx = 0
    with open(password_list, 'rb') as file:
        for line in file:
            for word in line.split():
                try:
                    idx += 1
                    zip_file.extractall(pwd=word)
                    print("Password found at line", idx)
                    print("Password is", word.decode())
                    return True
                except:
                    continue
    return False

password_list = "/usr/share/wordlists/rockyou.txt"
zip_file_path = "kotik.jpg"

with zipfile.ZipFile(zip_file_path) as zip_file:
    total_passwords = len(list(open(password_list, "rb")))
    print("There are total", total_passwords, "number of passwords to test")
    
    if not crack_password(password_list, zip_file):
        print("Password not found in this file")
