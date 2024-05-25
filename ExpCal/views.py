from django.shortcuts import render
from VAV.UserUtil import getUserDetailsFromRequestSession
from VAV.Constants import constructJsonErrorRes,constructJsonSuccessRes,icons_vs_element,companyDetails
from ExpCal.RecordsUtil import createNewRecord,updateRecord,deleteRecords,loadRecord,loadRecords,getCategorys,generateExpensesData
from django.views.decorators.csrf import csrf_exempt
import VAV.settings as settings
from VAV.views import signout,getEntryPage
from django.template.loader import render_to_string
import json
from ExpCal.ExpTrackerConstants import appDetails
METHODS = ["POST","GET","PUT","DELETE"]
#----------------------------------------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
def recordAction(request):
    try:
        userDetails = getUserDetailsFromRequestSession(request)
        if userDetails is not None:
            method = request.method
            if method in METHODS:
                if method == "POST":
                    return createNewRecord(request,userDetails)
                elif method == "PUT":
                    return updateRecord(request,userDetails)
                else:
                    if method == "DELETE":
                        payload = json.loads(request.body)
                        try:
                            id = payload.get('id')
                        except KeyError as e:
                            return constructJsonErrorRes("REQ_FIELDS_NF", "id")
                        try:
                            id = int(id)
                        except ValueError:
                            return constructJsonErrorRes("REQ_FIELDS_DT", "ids")
                        return deleteRecords(id=id,userId=userDetails["userId"])
                    else:
                        idValue = request.GET.get("id", None)
                        if idValue is None:
                            data = loadRecords(userId=userDetails["userId"], request=request)
                            data["icons"] = icons_vs_element
                            rendered_html = render_to_string('RecordDisplay.html', data)
                            data = {'html': rendered_html}
                            return constructJsonSuccessRes(success="REC_FETCHED_SUC",data=data)
                        else:
                            data = loadRecord(userId=userDetails["userId"],recordId=idValue)
                            if data is not None:
                                data["categories"] = getCategorys()
                                rendered_html = render_to_string('EditPage.html', data)
                                data = {'html': rendered_html}
                                return constructJsonSuccessRes(success="REC_FETCHED_SUC", data=data)
                            else:
                                return constructJsonErrorRes(error="REC_NOT_FOUND")
            else:
                return constructJsonErrorRes("REQ_MET_NOT_PROP")
        else:
            return signout(request=request)
    except Exception as e:
        return constructJsonErrorRes("I_S_E")

#----------------------------------------------------------------------------------------------------------------------------------------------------------

def expTrackerHome(request):
    try:
        userDetails = getUserDetailsFromRequestSession(request)
        if userDetails is not None:
            context = {
                'categories' : getCategorys(),
                'appDetails' : appDetails,
                'userInfo' : userDetails,
                'icons' : icons_vs_element,
                'companyDetails':companyDetails,
                'baseURL': settings.BASEURL
            }
            return render(request,"Home.html",context)
        else:
            return getEntryPage(request=request)
    except Exception as e:
        return constructJsonErrorRes("I_S_E")
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def generateExpensesDataCompletely(request):
    try:
        userDetails = getUserDetailsFromRequestSession(request)
        if userDetails is not None:
            year = generateExpensesData(userId=userDetails["userId"])
            data = {"report" : year}
            data["headName"] = "Report"
            data["icons"] = icons_vs_element
            rendered_html = render_to_string('CompleteReport.html', data)
            data = {'html': rendered_html}
            return constructJsonSuccessRes(success="REC_FETCHED_SUC", data=data)
        else:
            return signout(request=request)
    except Exception as e:
        return constructJsonErrorRes("I_S_E")
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------

    