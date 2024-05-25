from .models import UserDetails
from django.utils import timezone
from VAV import settings
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def getAuthenticatedUser(request):
    return request.session.get("userId")
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def checkLoginDetails(email_id=None,password=None):
    return True if UserDetails.objects.filter(email_id=email_id, password=password).exists() else False
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def getUserDetailsByEmailPassword(email_id=None,password=None):
    if email_id is None or password is None:
        return None
    else:
        try:
            user = UserDetails.objects.get(email_id=email_id, password=password)
            user = {
                'userId': user.userId,
                'email': user.email_id,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'lastLoginTime' : timezone.now().isoformat(),
                'profileImageLink' : user.profile_image.url
            }
        except UserDetails.DoesNotExist:
            user = None
        return user
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def getUserDetailsFromRequestSession(request):
    user_details = request.session.get('VAVuser')
    if user_details:
        last_login_time = user_details.get('lastLoginTime')
        if last_login_time:
            # Convert last login time from string to datetime object
            last_login_time = timezone.datetime.fromisoformat(last_login_time)
            # Calculate the time difference in seconds
            time_difference_seconds = (timezone.now() - last_login_time).total_seconds()
            # Check if the time difference is less than 60 seconds
            if time_difference_seconds < settings.SESSION_EXPIRE_TIME:
                return user_details
    return None

#----------------------------------------------------------------------------------------------------------------------------------------------------------
import random
def createNewUser(email, first_name, last_name, password):
    try:
        UserDetails.objects.get(email_id=email)
        return False
    except UserDetails.DoesNotExist:
        UserDetails.objects.create(
            email_id=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            profile_image= "profile_images/avatar"+str(random.randint(1, 6))+".jpg"
        )
        return True
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def createSession(request,email,password):
    request.session['VAVuser'] = getUserDetailsByEmailPassword(email_id=email, password=password)
#----------------------------------------------------------------------------------------------------------------------------------------------------------