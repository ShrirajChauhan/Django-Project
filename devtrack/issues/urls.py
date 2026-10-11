from django.urls import path

from .views import IssueView, ReporterView

urlpatterns = [
    path("issues/", IssueView.as_view(), name="issue-detail"),
    path("reporters/", ReporterView.as_view(), name="reporter-detail"),
]
