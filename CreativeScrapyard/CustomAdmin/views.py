from django.shortcuts import render

# Create your views here.
def adminindex(request):
    template='custom-admin/admin-dashboard.html'

    return render(request,template)

def users(request):
    template = 'custom-admin/users.html'
    return render(request,template)

def login(request):
    template = 'custom-admin/login.html'
    return render(request,template)

# def users(request):
#     template = 'custom_admin/users.html'
#     if request.session.get('admin'):
#         users = User.objects.all()
#         return render(request,template,{'users':users})
#     else:
#         return redirect('Admin:login')


# def admin(request):
#     if request.session.get('admin'):
#         template = 'custom_admin/index.html'
#         return render(request,template)
#     else:
#         return redirect('Admin:login')

# def login(request):
#     template = 'custom_admin/login.html'
#     if request.method == 'POST':
#         user = request.POST['username']
#         pwd = request.POST['password']
#         if user=='admin' and pwd=='admin':
#             request.session['admin'] = user
#             return redirect('Admin:admin')
#     return render(request,template)

# def logout(request):
#     template = 'custom_admin/logout.html'
#     if request.session.get('admin') != None:
#         request.session.delete()
#     else:
#         return redirect('Admin:login')
#     return render(request,template)