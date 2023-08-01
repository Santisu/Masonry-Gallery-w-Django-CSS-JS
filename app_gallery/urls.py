from django.urls import path
from .views import GaleryView, GetPicture

urlpatterns = [
    path('', GaleryView.as_view(), name="gallery"),
    path('get-picture/<int:pk>/', GetPicture.as_view(), name='picture'),
]