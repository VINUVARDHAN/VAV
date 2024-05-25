from .models import ExpDetails,CategoryInfo
from VAV.Constants import constructJsonErrorRes,constructJsonSuccessRes
import json
from VAV.models import UserDetails
from django.http import JsonResponse
from django.db.models import Sum
from datetime import datetime
from ExpCal.ExpTrackerConstants import categoryNameVSImage
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def createNewRecord(request,userDetails):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return constructJsonErrorRes("INV_REQ_BODY")
    constructData = dict()
    constructData["userId"] = UserDetails.objects.get(pk=userDetails["userId"])
    mandatoryFields = ["date","categoryId","amount","additional_info"]
    for i in mandatoryFields:
        if i=="additional_info" and i not in data.keys():
            constructData[i] = ""
            continue
        if data["date"]=='':
            data['date'] = datetime.now().date().strftime('%Y-%m-%d')
        if i not in data.keys():
            return constructJsonErrorRes("REQ_FIELDS_NF")
        constructData[i] = data[i]
    try:
        constructData["categoryId"] = CategoryInfo.objects.get(categoryId=constructData["categoryId"])
    except CategoryInfo.DoesNotExist:
        return constructJsonErrorRes("CATEGORY_NOT_FOUND")
    try:
        # ** django will consider each key in the newData as parameter and map values to fileds in models
        new_record = ExpDetails.objects.create(**constructData)
        serialized_data = {
            "expId": new_record.expId,
            "userId": new_record.userId_id,
            "date": new_record.date,  # Convert date to string format
            "categoryId": new_record.categoryId_id,
            "additional_info": new_record.additional_info,
            "amount": float(new_record.amount)
        }
        return constructJsonSuccessRes("REC_ADD_SUC",data=serialized_data)
    except Exception as e:
        return constructJsonErrorRes("I_S_E")
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def getRecordsByIds(ids):
    try:
        records = ExpDetails.objects.filter(expId=ids)
        return records
    except Exception:
        return constructJsonErrorRes("I_S_E")
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def updateRecord(request,userDetails):
    try:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return constructJsonErrorRes("INV_REQ_BODY")
        constructData = dict() 
        expectedFields = ["date","categoryId","amount","additional_info"]
        try:
            expId = int(request.GET["id"])
        except Exception:
            return constructJsonErrorRes("REQ_FIELDS_NF","id")
        for i in expectedFields:
            if i in data:  
                constructData[i] = data[i]
        if constructData is {}:
            return constructJsonSuccessRes("REC_UPD_SUC")
        else:
            userId = int(userDetails["userId"])
            record = ExpDetails.objects.filter(expId=expId, userId=userId).first()
            if record:
                for key, value in constructData.items():
                    if key == 'categoryId':
                        # Fetch the CategoryInfo instance corresponding to the provided categoryId
                        category_id = int(value)
                        try:
                            category_instance = CategoryInfo.objects.get(categoryId=category_id)
                            setattr(record, key, category_instance)
                        except CategoryInfo.DoesNotExist:
                            return constructJsonErrorRes("CATEGORY_NOT_FOUND")
                    else:
                        setattr(record, key, value)
                record.save()
                record = ExpDetails.objects.get(expId=expId, userId=userId)
                # Return success response with updated ExpDetails record
                serialized_record = {
                    "expId": record.expId,
                    "userId": record.userId_id,
                    "date": record.date,
                    "categoryId": record.categoryId_id,
                    "additional_info": record.additional_info,
                    "amount": float(record.amount),
                    "category_name" : record.categoryId.category_name,
                    "category_image" : getImageFromCategoryName(record.categoryId.category_name)
                }
                response_data = {
                    "success": {
                        "name": "Record updated success"
                    },
                    "data": serialized_record
                }
                return JsonResponse(response_data)  # Return response with updated record
            else:
                return constructJsonErrorRes("REC_NOT_FOUND")
    except Exception as e:
        return constructJsonErrorRes("I_S_E",)
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def deleteRecords(id,userId):
    try:
        record = ExpDetails.objects.filter(expId=id,userId=userId)
        if record.exists():
            record.delete()
            return constructJsonSuccessRes("REC_DEL_SUC")
        else:
            return constructJsonErrorRes("REC_NOT_FOUND")
    except Exception as e:
        return constructJsonErrorRes("I_S_E")
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def getRecords(countInPage=10, page=1, userId=None):
    offset = (page - 1) * countInPage
    records = ExpDetails.objects.select_related('userId', 'categoryId').filter(userId=userId).order_by('-date')[offset: offset + countInPage]
    next_page_exists = ExpDetails.objects.filter(userId=userId).count() > offset + countInPage
    data = []
    for record in records:
        data.append({
            "expId": record.expId,
            "userId": record.userId.userId,  # Assuming you want to retrieve the email_id of the user
            "category_name": record.categoryId.category_name,
            "category_image": getImageFromCategoryName(record.categoryId.category_name),
            "category_id": record.categoryId_id,
            "additional_info": record.additional_info,
            "amount": float(record.amount),  # Convert DecimalField to float for JSON serialization
            "date": record.date.strftime('%Y-%m-%d')  # Format date as string
        })
    data = {
        "count" : len(records),
        "data" : data,
        "page" : page,
        "record_per_page" : countInPage,
        "next_page_exists": next_page_exists
    }
    return data
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def getImageFromCategoryName(name):
    return categoryNameVSImage[name]
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def loadRecord(userId,recordId):
    try:
        recordId = int(recordId)
    except ValueError:
        return constructJsonErrorRes("REQ_FIELDS_DT", recordId)
    records = ExpDetails.objects.filter(userId=userId,expId=recordId)
    data = []
    for record in records:
        data.append({
            "expId": record.expId,
            "userId": record.userId.userId,  # Assuming you want to retrieve the email_id of the user
            "category_name": record.categoryId.category_name,
            "category_image": getImageFromCategoryName(record.categoryId.category_name),
            "category_id": record.categoryId_id,
            "additional_info": record.additional_info,
            "amount": float(record.amount),  # Convert DecimalField to float for JSON serialization
            "date": record.date.strftime('%Y-%m-%d')  # Format date as string
        })
    return None if len(data)==0 else data[0]
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def loadRecords(userId,request):
    expectedFields = ["count", "page"]
    constructData = {
        "count": 10,
        "page": 1
    }
    for i in expectedFields:
        try:
            constructData[i] = request.GET[i]
        except Exception:
            pass
        try:
            constructData[i] = int(constructData[i])
        except ValueError:
            return constructJsonErrorRes("REQ_FIELDS_DT", i)
    DO = getRecords(countInPage=constructData["count"], page=constructData["page"], userId=userId)
    return DO
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def getCategorys():
    records = CategoryInfo.objects.all()
    data = []
    for record in records:
        data.append({
            "category_name": record.category_name,
            "category_id": record.categoryId
        })
    return data
#----------------------------------------------------------------------------------------------------------------------------------------------------------
import copy
def generateExpensesData(userId):
    distinctYears = ExpDetails.objects.filter(userId=userId).dates('date', 'year')
    categoryIdVsName = {category.categoryId: category.category_name for category in CategoryInfo.objects.all()}
    categoryWiseExpenseStructure = {c : 0 for c in categoryIdVsName.values()}
    otherDetailsStructure = {
        "totalExpense" : 0,
        "categoryWiseExpense" : copy.deepcopy(categoryWiseExpenseStructure) 
    }

    allMonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthWiseExpenseStructure = {month : {
                           "categoryWiseExpense" : copy.deepcopy(categoryWiseExpenseStructure) ,
                            "otherDetails" : {
                                    "totalExpense" : 0,
                            }
                        } for month in allMonths
                    }
    yearWiseExpenseStructure = {
        "monthWiseExpense" : copy.deepcopy(monthWiseExpenseStructure) ,
        "otherDetails" : copy.deepcopy(otherDetailsStructure)
    }
    completeReport = {
        "yearWiseExpense" :{},
        "otherDetails" : copy.deepcopy(otherDetailsStructure),
    }
    for year in distinctYears:
        curYearString = str(year.year)
        completeReport["yearWiseExpense"][curYearString] = copy.deepcopy(yearWiseExpenseStructure)
        distinctMonthsOfGivenYear = ExpDetails.objects.filter(userId=userId, date__year=year.year).dates('date', 'month')
        for month in distinctMonthsOfGivenYear:
            curMonthString = month.strftime('%b')
            monthlyExpenses = ExpDetails.objects.filter(userId=userId, date__year=year.year, date__month=month.month) \
                .values('categoryId') \
                .annotate(total_amount=Sum('amount'))
            
            for expense in monthlyExpenses:
                currAmount = float(expense['total_amount'])
                completeReport["yearWiseExpense"][curYearString]["monthWiseExpense"][curMonthString]["categoryWiseExpense"][categoryIdVsName[expense['categoryId']]] += currAmount
                completeReport["yearWiseExpense"][curYearString]["monthWiseExpense"][curMonthString]["otherDetails"]["totalExpense"] += currAmount

                completeReport["yearWiseExpense"][curYearString]["otherDetails"]["categoryWiseExpense"][categoryIdVsName[expense['categoryId']]] += currAmount
                completeReport["yearWiseExpense"][curYearString]["otherDetails"]["totalExpense"] += currAmount

                completeReport["otherDetails"]["categoryWiseExpense"][categoryIdVsName[expense['categoryId']]] += currAmount
                completeReport["otherDetails"]["totalExpense"] += currAmount
    return completeReport

