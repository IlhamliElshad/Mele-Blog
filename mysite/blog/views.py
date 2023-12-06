from django.shortcuts import render, get_object_or_404
from blog.models import Post, Comment
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView
from blog.forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
# Create your views here.
from django.db.models import Count

class PostListView(ListView):

    queryset = Post.published.all()
    paginate_by = 2
    context_object_name = "posts"
    template_name = 'blog/post/list.html'


def post_list(request,tag_slug = None):
    posts = Post.published.all()
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
        
    paginator = Paginator(posts, 2)
    page = request.GET.get("page", 1)
    try:
        posts = paginator.page(page)
    except:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {"posts": posts,"tag":tag})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug,
                             status='PB'
                             )
    comments = post.comments.filter(active=True)
    form = CommentForm()
    tags_ids = post.tags.values_list("id",flat=True)#[1,3]
    similar_posts = Post.published.filter(tags__in=tags_ids).exclude(pk=post.pk)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
    .order_by('-same_tags','-publish')[:4]
    
    context = {
        'post':post,
        "comments":comments,
        "form":form,
        "similar_posts":similar_posts
    }
    return render(request, 'blog/post/detail.html',context)


def post_share(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    sent = False

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
            send_mail(subject, message, 'no-reply@win-score.com', (cd['to'],))
            sent = True

    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, "sent": sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    comment = None

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)

        comment.post = post

        comment.save()

    return render(request, 'blog/post/comment.html',
                    {'post': post,
                    'form': form,
                    'comment': comment})
