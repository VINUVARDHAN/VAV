from .models import CategoryInfo,ExpDetails

def getExpDetails(user_id, start_row, end_row):
    # Convert start_row, end_row, and user_id to integers
    start_row = int(start_row)
    end_row = int(end_row)
    user_id = int(user_id)

    exp_details = ExpDetails.objects.filter(userId=user_id).order_by('-date').select_related('categoryId')[
                  start_row:end_row]

    data = []
    for exp_detail in exp_details:
        data.append({
            'user_id': exp_detail.userId.userId,
            'expId': exp_detail.userId.expId,
            'date': exp_detail.date.strftime('%Y-%m-%d'),
            'category_id': exp_detail.categoryId.categoryId,
            'category_name': exp_detail.categoryId.category_name,
            'additional_info': exp_detail.additional_info,
            'amount': exp_detail.amount,
        })
    return data

def getCategoryDetails(user_id):
    try:
        categories = CategoryInfo.objects.filter(userId=user_id)
        return categories
    except CategoryInfo.DoesNotExist:
        return None