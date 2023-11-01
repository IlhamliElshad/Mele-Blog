from django.urls import path
from blog.views import post_detail,post_list,PostListView




app_name = 'blog'

urlpatterns = [
    path("",PostListView.as_view(),name='post_list'),
    path("<int:year>/<int:month>/<int:day>/<slug>/",post_detail,name='post_detail'),
]
