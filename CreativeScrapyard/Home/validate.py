from django.core.validators import validate_email
from django.forms import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
import re
from Authentication.models import User,Profile

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
                    istaken_email = User.objects.filter(email__iexact=mail).exists()
                    #istaken=False
                    if istaken_email:
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
                    istaken_username= User.objects.filter(username__iexact=username).exists()
                    #istaken=False
                    if istaken_username:
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
            
            if not bool(re.match('^[\.a-zA-Z0-9,\s ]+$',inp_sub)): 
                sub = {
                    'is_valid': False,
                    'msg': "Invalid subject no special character are allowed."
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
########################### MESSAGES #########################            
    if 'msg' in kwargs:
        if kwargs['msg']:
            inp_msg= kwargs['msg']
            
            if not bool(re.match('^[\.a-zA-Z0-9,\s ]+$',inp_msg)): 
                CtMessage = {
                    'is_valid': False,
                    'msg': "Invalid subject no special character are allowed."
                }
                data["errors"]=True
            else:
                CtMessage = {
                    'is_valid': True,
                    'msg': ""
                }
            data["CtMessage"] = CtMessage


    if 'pswd1' in kwargs and 'pswd1' in kwargs:
        if kwargs["pswd1"] and kwargs["pswd2"]:
            pswd1 = kwargs["pswd1"]
            pswd2 = kwargs["pswd2"]
            if pswd1 == pswd2:
                # print(bool(re.match('[A-Za-z0-9@#$%^&+=]{9,}',pswd1)))
                if bool(re.match('[A-Za-z0-9@#$%^&+=]{9,}',pswd1)):
                    try:
                    
                        validate_password(pswd1)
                        #print(pswd1,pswd2)
                        
                    except ValidationError as e:
                        print(e)
                        password = {
                            'is_valid':False,
                            'msg':[*e]
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
                        'msg': "Passwords does not match the given criteria."
                    }
                    data["errors"]=True
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
