from django.urls import path
from .views import ScrapUpdateView,ScrapCreateView,ScrapDestroyView,ScrapListView,ScrapRetreiveView

urlpatterns = [
    path("/new", ScrapCreateView.as_view(),name="scrap_new"),
    path("/<int:pk>/edit", ScrapUpdateView.as_view(), name="scrap_edit"),
    path("/<int:pk>/delete", ScrapDestroyView.as_view(), name="scrap_delete"),
    path("", ScrapListView.as_view(), name="scraps_list"),
    path("/<int:pk>/detail", ScrapRetreiveView.as_view(), name="scrap_detail"),
]
