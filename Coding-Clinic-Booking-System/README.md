# Coding-Clinic-Booking-System

# Getting started
Step 1: Go to the projects main directory. THIS IS IMPORTANT!

Step 2: Type in "source bash.sh" into your terminal from the project directory. This installs all required packages and sets aliases.

Step 3: Type in the 'wtc-clinic register' command and follow the prompts to create your Code Clinics account (make sure you save your password in a safe place.).

Step 4: Type in the 'wtc-clinic login' command and follow the prompts to login to your code clinics account. This will create a token thats valid for 4 hours.
        After which it will expire and will prompt you to login again. Run the 'wtc-clinic login'

The user is is able to use the program by running any of the modules in either the clinicians 
or the patients module. But when running any of those modules the user will need to provide valid args.
Here is how you run each of the modules.

# Python modules/Packages

## Clinicians:
    wtc-clinic clinician create [date (yyyy/mm/dd)] [time e.g 14:00] - creates a slot as a clinician.
    wtc-clinic clinician delete [slot id] - deletes slot youve created as a clinician.
    wtc-clinic clinician view - views all the slots youve created as a clinician.

## Patients:
    wtc-clinic patient view - views all the slots youve signed up to as a patient.
    wtc-clinic patient slots - views all the slots you can sign up to as a patient.
    wtc-clinic patient delete [slot id] - removes you as a patient from the slot youve signed up to.
    wtc-clinic patient signup [description, what you need help with] [slot id] - signs you up as a patient to a slot of your choice.

## Authentication:
    wtc-clinic register - prompts you to input your student username and create a password.
    wtc-clinic login - prompts you to enter the username and password you registered with, then create a token file that is valid for 4 hours after which you'll be     prompted to login again.
