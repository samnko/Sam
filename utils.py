import re

def validate_password(password):
#cette fonction doit nous renvoyer True ou False 
    if len(password) < 8:
        return False
    elif re.search('[0-9]',password) is None:
        return False
    elif re.search('[A-Z]',password) is None: 
        return False
    elif re.search('[a-z]',password) is None:
        return False
    else:
        return True

# re = regex , permet de rechercher dans une string


       

