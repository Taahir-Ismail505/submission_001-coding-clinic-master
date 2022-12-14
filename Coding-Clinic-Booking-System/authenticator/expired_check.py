import os, datetime, re
import csv


def is_program_expired():
    """
    registry expiration check
    """
    # Query date of first lauch in given file
    if os.path.exists("username_file"):
        with open("username_file", 'r') as file:
            lines = csv.reader(file)
            for line in lines:
                line1 = str(line)[2:-2]
                # start_date = datetime.datetime.strptime(line, "%H")
                start_date = datetime.datetime.strptime(line1, "%Y_%m_%d_%H_%M_%S")
                # Check if current time is greater than time limit
                expire_date = start_date + datetime.timedelta(hours=4)
                if datetime.datetime.now() > expire_date:
                    file.close()
                    os.remove("username_file")
                    print("Your login has expired. Please login again.")
                    return True
                else :
                    return False
    else:
        print("Your login has expired. Please login again.")
        return True
        

# is_program_expired()
