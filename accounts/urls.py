from django.conf.urls import url
from accounts import views
# SET THE NAMESPACE!
app_name = 'accounts'
urlpatterns=[
    url(r'^signup/$',views.signup,name='register'),
    url(r'^login/$',views.user_login,name='user_login'),
]
