from django.shortcuts import render,get_object_or_404
from blog.models import Post 
# Create your views here.


def post_list(request):
    posts =Post.published.all()
    return render(request,'blog/post/list.html', {"posts":posts})



def post_detail(request, pk):
    post = get_object_or_404(Post,pk=pk,status='PB')
    return render(request, 'blog/post/detail.html',{"post":post})
