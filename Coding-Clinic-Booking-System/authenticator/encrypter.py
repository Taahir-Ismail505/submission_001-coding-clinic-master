import whirlpool 


def encrypt_password(password):
    """
    recieves password as a variable. encoding password with utf-8, there after using a hexdigest to create a hashed password.
    """

    text = password
    h1 = whirlpool.new(text.encode('utf-8'))
    hashed_output = h1.hexdigest()

        
    return hashed_output