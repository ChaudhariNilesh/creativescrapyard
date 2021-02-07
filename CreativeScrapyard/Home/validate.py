from django.core.validators import validate_email
from django.forms import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
import re
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
    #print(kwargs.items())
   #####################       EMAIL     #####################
    if 'email' in kwargs:    
        if kwargs['email']:
            mail = kwargs['email']
            try:
                #mail="ggg@"
                validate_email(mail)
            except ValidationError as e:
                #print(e)
                email = {
                    'is_valid':False,
                    'msg':str(e)
                }
                data["errors"]=True
                data["email"] = email            
            else:
                if kwargs["chkTakenEmail"]:
                    #istaken_email = User.objects.filter(email__iexact=email).exists()
                    istaken=False
                    if istaken:
                        email = {
                            'is_valid':False,
                            'msg':"Email already exist."
                        } 
                        data["errors"]=True                        
                    else:
                        email = {
                            'is_valid':True,
                            'msg':""
                        }                                  
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
            data["errors"]=True
            data["email"] = email
   #####################       USERNAME     #####################
    if 'username' in kwargs:    
        if kwargs['username']:
            username = kwargs['username']
            try:
                #mail="ggg@"
                #print(username)
                is_username = re.match("^[\w.@+-]+\Z",username)
                if not is_username: 
                    raise ValidationError("Enter a valid username. This value may contain only letters,numbers, and @/./+/-/_ characters.")
            except ValidationError as e:
                print(e)
                username = {
                    'is_valid':False,
                    'msg':str(*e)
                }
                data["errors"]=True
                data["username"] = username            
            else:
                if kwargs["chkTakenUsrname"]:
                    #istaken_email = User.objects.filter(email__iexact=email).exists()
                    istaken=False
                    if istaken:
                        username = {
                            'is_valid':False,
                            'msg':"Username already exist."
                        } 
                        data["errors"]=True                        
                    else:
                        username = {
                            'is_valid':True,
                            'msg':""
                        }                                  
                else:
                    username = {
                        'is_valid':True,
                        'msg':""
                    }
                data["username"] = username           
        else:
            username = {
                'is_valid': False,
                'msg': "Blank field is not allowed."
            }
            data["errors"]=True
            data["username"] = username        
   #####################       FIRSTNAME     #####################
    if 'fname' in kwargs:
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
    if 'lname' in kwargs:
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
    if 'sub' in kwargs:
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


    if 'pswd1' in kwargs and 'pswd1' in kwargs:
        if kwargs["pswd1"] and kwargs["pswd2"]:
            pswd1 = kwargs["pswd1"]
            pswd2 = kwargs["pswd2"]
            if pswd1 == pswd2:
                try:
                   
                   #  validate_password(pswd1)
                    print(pswd1,pswd2)
                    
                except ValidationError as e:
                    print(e)
                    password = {
                        'is_valid':False,
                        'msg':str(e)
                    }
                    data["errors"]=True
                    data["password"] = password
                else:
                    password = {
                        'is_valid': True,
                        'msg': ""
                    }                    
                    #data["errors"]=False
                    data["password"] = password
            else:
                password = {
                    'is_valid': False,
                    'msg': "Passwords do not match"
                }
                data["errors"]=True
                data["password"] = password

        else:
            password = {
                'is_valid': False,
                'msg': "Blank field is not allowed."
            }
            data["errors"]=True
            data["password"] = password    
    
    
    
    #######################################################
    #print(data)
    return data


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

        # if not mail.endswith("gmail.com") :
        #     email = {
        #         'is_valid':False,
        #         'msg':"Email is invalid."
        #     }
        #     data["errors"]=True
        # else:
        #     email = {
        #         'is_valid':True,
        #         'msg':""
        #     }
        
        # data["email"] = email
