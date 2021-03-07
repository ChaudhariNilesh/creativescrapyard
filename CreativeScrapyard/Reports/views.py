from django.shortcuts import render
from Authentication.models import User
from django.core.serializers import serialize


# Create your views here.
def reports(request):
    users = User.objects.filter(is_superuser=False)
    # data = list(users.values())
    data = serialize("json",users,fields=("user_id,username,email,date_created,is_active,is_verified")) 
    print(data)
    context={"user":data}
    return render(request, 'Reports/report.html',context )