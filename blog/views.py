from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View, generic
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin

from .forms import CommentForm, FeedbackForm, PostForm, RegisterForm
from .models import Comment, Post, User


def index(request):
    users = User.objects.filter(is_staff=False, is_superuser=False).aggregate(Count('id'))
    posts = Post.objects.aggregate(Count('id'))
    comments = Comment.objects.aggregate(Count('id'))
    most_commented_posts = Comment.objects.values('post', 'post__heading').annotate(comments=Count('post')).order_by(
        '-comments')[:5]
    return render(request, 'blog/index.html', {'users': users,
                                               'posts': posts,
                                               'comments': comments,
                                               'most_commented_posts': most_commented_posts})


class UserRegistrationView(SuccessMessageMixin, generic.FormView):
    form_class = RegisterForm
    fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('blog:index')
    success_message = 'Welcome to our blog!!!'

    def form_valid(self, form):
        user = form.save()
        user.save()
        return super().form_valid(form)


class MyProfileUpdate(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'email']
    template_name = 'blog/my_profile_form.html'
    success_message = 'Your profile info has been successfully saved!!!'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('blog:profile_update', kwargs={'pk': pk})

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class AuthorDetail(generic.DetailView):
    model = User
    fields = ['first_name', 'username', 'last_login']
    template_name = 'blog/author_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_posts'] = Post.objects.filter(author_id=self.kwargs['pk']).aggregate(Count('id'))
        return context


class PostCreate(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Post
    fields = ['heading', 'short_definition', 'text', 'image', 'is_published']
    template_name = 'blog/post_form.html'

    def post(self, request, *args, **kwargs):
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_form.instance.author = self.request.user
            is_published = post_form.cleaned_data['is_published']
            post_form.instance.is_published = is_published
            new_post = post_form.save()
            new_post.save()
            messages.success(self.request, 'Your post has been successfully created!!!')
            return redirect('blog:posts_list')
        return super().post(request, *args, **kwargs)


class MyPostUpdate(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Post
    fields = ['heading', 'short_definition', 'text', 'image', 'is_published']
    template_name = 'blog/my_post_update_form.html'
    success_url = reverse_lazy('blog:index')
    success_message = 'Your post has been successfully updated!!!'

    def get_object(self, queryset=None):
        post_initial = Post.objects.select_related('author').get(id=self.kwargs['pk'])
        if post_initial.author != self.request.user:
            raise Http404
        return post_initial

    def form_valid(self, post_form):
        post_form.instance.author = self.request.user
        is_published = post_form.cleaned_data['is_published']
        post_form.instance.is_published = is_published
        return super().form_valid(post_form)


class PostDetails(generic.DetailView):
    model = Post
    template_name = 'blog/post_details.html'

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['pk'])
        if not post.is_published:
            messages.warning(self.request, "This post isn't published, or doesn't exist!!!")
            return redirect('blog:index')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.select_related('author').prefetch_related(
            Prefetch('comments', Comment.objects.filter(is_published=True).order_by('-pub_date'))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class PostList(generic.ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.select_related('author').filter(is_published=True).order_by('-pub_date')


class MyPostsListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'blog/my_posts_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(author__id=self.request.user.id).order_by('-pub_date')


class CommentFormView(SuccessMessageMixin, SingleObjectMixin, FormView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/post_details.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = comment_form.cleaned_data['text']
            author = comment_form.cleaned_data['author']
            new_comment = Comment(text=text, author=author, post_id=kwargs['pk'])
            new_comment.save()
            messages.success(self.request, "Your comment will be added soon!")
            return redirect('blog:post_details', pk=kwargs['pk'])
        return super().post(request, *args, **kwargs)


class CommentsList(generic.ListView):
    model = Comment
    template_name = 'blog/comments_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['pk'], is_published=True).order_by('-pub_date')


class PostView(View):

    def get(self, request, *args, **kwargs):
        view = PostDetails.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentFormView.as_view()
        return view(request, *args, **kwargs)


class FeedbackView(SuccessMessageMixin, FormView):
    form_class = FeedbackForm
    template_name = 'blog/send_feedback.html'
    success_url = reverse_lazy('blog:index')
    success_message = 'Thanks for your feedback!!!'

    # def form_valid(self, feedback_form):
    #     author = feedback_form.cleaned_data['author']
    #     title = feedback_form.cleaned_data['title']
    #     text = feedback_form.cleaned_data['text']
    #     score = feedback_form.cleaned_data['evaluate_the_blog']
    #     reply = feedback_form.cleaned_data['reply_me']
    #     return super().form_valid(feedback_form)
