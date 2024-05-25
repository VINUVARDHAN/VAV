from django.urls import path
from . import views
from ExpCal.ExpTrackerConstants import appDetails
app_name = appDetails['urlRedirectingNameSpace']
urlpatterns = [
    path("",views.expTrackerHome),
    path("Records/",views.recordAction),
    path("Records/CompleteReport",views.generateExpensesDataCompletely)
]
