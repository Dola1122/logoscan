# from django.urls import path
# from backend.views import index, LogoUploadView,ImageAPIView

# urlpatterns = [
#     path('', index),
#     path('upload-logo/', LogoUploadView.as_view(), name='logo-upload'),
#     path('api/image/<str:id>', ImageAPIView.as_view(), name='image_api'),
# ]
from django.urls import path
from backend.views import index, LogoUploadView,  LogoUploadView2, ImageAPIView, DropDownMenuData, AdminAuth, ReviewsView, UserReview

urlpatterns = [
    path('', index),
    path('upload-logo/', LogoUploadView.as_view(), name='logo-upload'),
    path('upload-logo/admin/', LogoUploadView2.as_view(), name='logo-upload2'),
    path('image/<str:id>', ImageAPIView.as_view(), name='image_api'),
    path('dropdown-menu-data/', DropDownMenuData.as_view(),
         name='dropdown-menu-data'),
    path('upload-logo/admin/login', AdminAuth.as_view(), name='admin_auth'),
    path('reviews/', ReviewsView.as_view(), name='reviews'),
    path('user-review/', UserReview.as_view(), name='user-review'),
]
