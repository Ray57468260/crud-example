from django.urls import path
from .views import CrudView

urlpatterns = [
    path('', CrudView.as_view())
]
