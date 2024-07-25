from django.urls import path
from .views import *

urlpatterns = [
    path("new/", ScheduleCreateView.as_view(), name="schedule_new"),
    path("<int:pk>/completed", ScheduleUpdateView.as_view(), name="schedule_completed"),
    path("<int:pk>/delete", ScheduleDestroyView.as_view(), name="schedule_delete"),
    path("", ScheduleListView.as_view(), name="schedule_list"),
    path("<int:pk>/detail", ScheduleRetreiveView.as_view(), name="schedule_detail"),
]
