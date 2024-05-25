from django.shortcuts import render
import json
from .Constants import constructJsonSuccessRes,constructJsonErrorRes
from VAV.UserUtil import checkLoginDetails,createNewUser,createSession
from django.views.decorators.csrf import csrf_exempt
from .settings import BASEURL
from VAV.Constants import companyDetails
from ExpCal.ExpTrackerConstants import appDetails
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def getEntryPage(request):
    return getLoginOrSignupPage(request)
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def getLoginOrSignupPage(request):
    return render(request, 'LoginAndSignup.html')
#----------------------------------------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
def login(request):
    try:
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError as e:
                return constructJsonErrorRes("INV_REQ_BODY")
            requiredFieldsInList = ["email","password"]
            for i in requiredFieldsInList:
                if i not in data.keys():
                    return constructJsonErrorRes("REQ_FIELDS_NF",addExtra=i)
                if str(data[i]).strip() in ["",None]:
                    return constructJsonErrorRes("REQ_FIELDS_EMP")
            email = data["email"]
            password = data["password"]
            if checkLoginDetails(email_id=email,password=password):
                createSession(request=request,email=email,password=password)
                url = BASEURL + "/"+ companyDetails["apiName"] + "/" + appDetails["apiName"]
                return constructJsonSuccessRes("Login_Success",url)
            else:
                return constructJsonErrorRes("NO_USER_FOUND")
        else:
            return constructJsonErrorRes("REQ_MET_NOT_PROP")
    except Exception as e:
        return constructJsonErrorRes("I_S_E")
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def signup(request):
    try:
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError as e:
                return constructJsonErrorRes("INV_REQ_BODY")
            requiredFieldsInList = ["email","passWord","firstName","lastName"]
            for i in requiredFieldsInList:
                if i not in data.keys():
                    return constructJsonErrorRes("REQ_FIELDS_NF")
                if data[i].strip() in ["",None]:
                    return constructJsonErrorRes("REQ_FIELDS_EMP")
            email = data["email"].strip()
            password = data["passWord"].strip()
            if createNewUser(email=email,password=password,first_name=data["firstName"].strip(),last_name=data["lastName"].strip()):
                createSession(request=request,email=email,password=password)
                url = BASEURL + "/"+ companyDetails["apiName"] + "/" + appDetails["apiName"]
                return constructJsonSuccessRes("Signup_Success",url)
            else:
                return constructJsonErrorRes("DUP_USER")
        else:
            return constructJsonErrorRes("REQ_MET_NOT_PROP")
    except Exception as e:
        return constructJsonErrorRes("I_S_E")
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def handleUnhandledURL(request,unmatchedPath):
    return render(request,'PageNotFound.html')
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def signout(request):
    request.session.flush()
    return constructJsonSuccessRes("Signout_Success",f"{BASEURL}/LoginOrSignupPage")
#----------------------------------------------------------------------------------------------------------------------------------------------------------