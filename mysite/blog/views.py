from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView
from blog.forms import EmailPostForm
from django.core.mail import send_mail
# Create your views here.


class PostListView(ListView):

    queryset = Post.published.all()
    paginate_by = 2
    context_object_name = "posts"
    template_name = 'blog/post/list.html'


def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 2)
    page = request.GET.get("page", 1)
    try:
        posts = paginator.page(page)
    except:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {"posts": posts})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug,
                             status='PB'
                             )

    return render(request, 'blog/post/detail.html', {"post": post})


def post_share(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    sent= False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
            post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
            f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'no-reply@win-score.com',(cd['to'],))
            sent = True
            
    else:
        form = EmailPostForm()
    
    return render(request,'blog/post/share.html', {'post': post,'form': form,"sent":sent})
