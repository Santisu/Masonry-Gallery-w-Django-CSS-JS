from django.urls import path
from .views import GaleryView, GetPicture, csrf, CreateHashtagView

urlpatterns = [
    path('', GaleryView.as_view(), name="gallery"),
    path('get-picture/<int:pk>/', GetPicture.as_view(), name='picture'),
    path('csrf/', csrf),
    path('create-hashtag/', CreateHashtagView.as_view(), name='create_hashtag'),

]