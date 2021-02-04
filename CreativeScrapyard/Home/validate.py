# def checkEmail(mail):
#     if len(mail) > 20:
#         is_valid = True
#     is_valid=True
#     return is_valid
#
# def checkName(mail):
#     if len(mail) < 20:
#         is_valid = True
#     is_valid=False
#     return is_valid
data={}
def validate(**kwargs):
    if kwargs['email']!=None or kwargs['email']!="":
        mail = kwargs['email']
        if not mail.endswith("gmail.com"):
            email = {
                'valid':False,
                'msg':"Email is invalid."
            }
        else:
            email = {
                'valid':True,
                'msg':""
            }
        data["email"] = email
    else:
        email = {
            'valid': False,
            'msg': "Blank field is not allowed."
        }
        data["email"] = email


    if kwargs['name']!=None or kwargs['name']!="":
        name = kwargs['name']
        if name.isdigit():
            print(name.isdigit())
            name = {
                'valid': False,
                'msg': "Numbers are not allowed."
            }
        else:
            name = {
                'valid': True,
                'msg': "VALID"
            }
        data["name"] = name
    else:
        name = {
            'valid': False,
            'msg': "Blank field is not allowed."
        }
        data["name"] = name


    return data