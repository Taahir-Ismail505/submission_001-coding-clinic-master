import datetime
import sys, os, inspect
import datetime

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

def create_username_file(username): 
    start_date = datetime.datetime.now()
    end_time = start_date + datetime.timedelta(hours=4)
    with open("username_file", 'w') as file:
        file.write(start_date.strftime("%Y_%m_%d_%H_%M_%S\n"))
        file.write(username)
        file.close()
    print ("Login successful. Token expires in 0 days 3 hours 59 minutes at " + str(end_time.strftime("%Y-%m-%d %H:%M:%S")) + ".")

#make into own function to be called. bool return values
