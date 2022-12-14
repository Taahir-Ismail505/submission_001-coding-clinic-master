import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from authenticator import expired_check


def check_if_credentials_have_expired():
    """[Calls the 'is_program_expired' function, which checks if the token is has expired and 
    and the user needs to login again]

    Returns:
        [bool]: [Return either true or false depending on whether the token has expired.]
    """    
    expired = expired_check.is_program_expired()
    return expired

