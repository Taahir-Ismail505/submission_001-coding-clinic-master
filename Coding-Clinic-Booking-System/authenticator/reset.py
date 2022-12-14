def reset_main():
    username = input("Please enter your username: ")
    if len(username) > 0:
        with open("authenticator/users.txt", 'r') as usernames:    
            if username in usernames.read():
                with open("authenticator/users.txt", "r") as file:
                    lines = file.readlines()
                with open("authenticator/users.txt", "w") as file:
                    for line in lines:
                        line = line.split(",")
                        if username == line[0]:
                            pass
                        else :
                            file.write("" + line[0] + "," + line[1] + "")
    else :
        return reset_main()
            
reset_main()