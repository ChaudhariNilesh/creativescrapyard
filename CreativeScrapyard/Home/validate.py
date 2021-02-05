
#  def checkEmail(mail):
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
def validate(**kwargs):
    data={}
    data['errors']=False
   
   #####################       EMAIL     #####################
    if kwargs['email']:
        mail = kwargs['email']
        if not mail.endswith("gmail.com"):
            email = {
                'is_valid':False,
                'msg':"Email is invalid."
            }
            data["errors"]=True
        else:
            email = {
                'is_valid':True,
                'msg':""
            }
        
        data["email"] = email
   
    else:
        email = {
            'is_valid': False,
            'msg': "Blank field is not allowed."
        }
        data["email"] = email

   #####################       FIRSTNAME     #####################
    if kwargs['fname']:
        fname = kwargs['fname']
        if not fname.isalpha():
            first_name = {
                'is_valid': False,
                'msg': "Invalid First Name."
            }
            data["errors"]=True
        else:
            first_name = {
                'is_valid': True,
                'msg': ""
            }
        data["first_name"] = first_name
    else:
        first_name = {
            'is_valid': False,
            'msg': "Blank field is not allowed."
        }
        data["errors"]=True
        data["first_name"] = first_name

   #####################       LASTNAME     #####################
    if kwargs['lname']:
        lname = kwargs['lname']
        
        if not lname.isalpha():
            last_name = {
                'is_valid': False,
                'msg': "Invalid Last Name."
            }
            data["errors"]=True
        else:
            last_name = {
                'is_valid': True,
                'msg': ""
            }
        data["last_name"] = last_name
    else:
        last_name = {
            'is_valid': False,
            'msg': "Blank field is not allowed."
        }
        data["errors"]=True
        data["last_name"] = last_name

    #####################       SUBJECT     #####################
    if kwargs['sub']:
        inp_sub = kwargs['sub']
        
        if not inp_sub.isalpha():
            sub = {
                'is_valid': False,
                'msg': "Invalid Subject Name."
            }
            data["errors"]=True
        else:
            sub = {
                'is_valid': True,
                'msg': ""
            }
        data["sub"] = sub
    else:
        sub = {
            'is_valid': False,
            'msg': "Blank field is not allowed."
        }
        data["errors"]=True
        data["sub"] = sub

   #####################       MESSSAGE     #####################
    # if not kwargs['message']:
    #     inp_msg = kwargs['message']
    #     print(inp_msg)
    #     message = {
    #         'is_valid': True,
    #         'msg': ""
    #     }
    #     data["message"] = message
    # else:
    #     message = {
    #         'is_valid': False,
    #         'msg': "Blank field is not allowed."
    #     }
    #     data["message"] = message
    # #print(data)
    
    return data

