import sys, os, inspect
import csv
import encrypter
import user_file_gen as gen
# import replacer
import stdiomask



currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


def main():
    """
    Main login system
    """
    with open("authenticator/users.txt","r") as file:
        file_reader = csv.reader(file)
        if user_find(file_reader) == True:
            file.close()
        else :
            print("\nPlease make sure you are registered.\n")

def user_find(file):
    """
    check through the users file for the username inputted.

    file is the file we are using to store user data.
    """
    username1 = input("Enter your username: ")
    username = username1.lower()
    for row in file:
        if row[0] == username:
            print("\n username found " + username +"\n")
            user_found = [row[0],row[1]]
            pass_check(user_found)
            gen.create_username_file(username)
            return True
        else:
            continue

def pass_check(user_found):
    """
    checking users input against saved data

    user_found is the row the function is working with.
    """
    password = ''
    while password != user_found[1]:
        password = stdiomask.getpass(prompt="Please enter your password: ", mask='*')
        pass1 = encrypter.encrypt_password(password)
        if user_found[1] == pass1:
            return "\nPassword match\n"
        else:
            print("\nPassword do not match\n")

main()