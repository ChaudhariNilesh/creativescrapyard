from django.http.response import JsonResponse
from CreativeScrapyard import settings
from django.shortcuts import render,redirect,HttpResponse
from .forms import *
# Create your views here.

def creativeSingleItem(request):
    template = 'Shop/single-item.html'
    return render(request,template,{'is_creative':True})

def scrapSingleItem(request):
    template = 'Shop/single-item.html'
    return render(request,template,{'is_scrap':True})

def reportIssue(request):
    issue_msg=""
    issue_sub=""
    if request.method == "POST":
        # print(request.POST)
        issueForm = ReportIssueForm(request.POST)
        if issueForm.is_valid():
            if request.POST.get("issue_type")=='1':
                    issue = issueForm.save(commit=False)
                    print(issue)
                    issue.crt_item = int(request.POST.get("crt_item_id",None))  #find crt the product.     
                    issue.reported_user_id=None           
                    issue.user = request.user
                    issue.save()
                    
            elif request.POST.get("issue_type")=='2':
                    issue = issueForm.save(commit=False)
                    issue.reported_user_id=None
                    issue.scp_item = int(request.POST.get("scp_item_id",None))
                    issue.user = request.user
                    issue.save()

            elif request.POST.get("issue_type")=='3':
                print("USER")
                issue = issueForm.save(commit=False)
                user_id=request.POST.get("user_id")
                if User.objects.filter(user_id=user_id).exists():
                    reportee = User.objects.get(user_id=user_id)
                    issue.reported_user_id = reportee.user_id # find the product related user.
                    issue.user = request.user
                    issue.save()

            return JsonResponse({"errors":False})

        else:
        
            if 'issue_sub' in issueForm.errors:
                issue_sub=issueForm.errors["issue_sub"].as_text()
            if 'issue_msg' in issueForm.errors:
                issue_msg=issueForm.errors["issue_msg"].as_text()
            msg={
                "issue_sub":issue_sub,
                "issue_msg":issue_msg,
            }
            return JsonResponse({"errors":msg})
        
        
        # return redirect("Home:Items:creativeSingleItem")
    