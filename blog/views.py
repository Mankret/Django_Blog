from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse, resolve
from django.views import generic

from blog.forms import RegisterForm, CommentForm, ContactUsForm
from blog.models import Post, Comment
from blog.task import send_system_message, send_system_message_for_author

User = get_user_model()


class HomeBlogView(generic.ListView):
    model = Post
    paginate_by = 3
    template_name = 'home.html'


class RegisterFormView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        user = authenticate(username=user.username, password=form.cleaned_data.get('password1'))
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class UserProfileView(generic.DetailView):
    model = User
    template_name = 'registration/profile.html'


class PostByUserView(generic.ListView):
    model = Post
    paginate_by = 4
    template_name = 'blog/post_by_user.html'

    def get_queryset(self):
        return Post.objects.select_related('author').filter(author_id=self.request.user.id)


class UpdateProfileView(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'registration/update_profile.html'
    fields = ['username', 'email']
    success_url = reverse_lazy('home')
    success_message = "Profile success update"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    fields = ['title', 'short_description', 'description', 'image', 'is_posted']

    def form_valid(self, form):
        form = form.save(commit=False)
        form.author = self.request.user
        form.save()
        send_system_message.delay(subj='New Post', message=f'User {form.author} created a new post,'
                                                           f' check the admin page', email='system@admin.com')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        comment_form = CommentForm()
        comm = context['post'].comments.all()
        pagin = Paginator(comm, per_page=2)
        page = self.request.GET.get('page')
        context['comm_page'] = pagin.get_page(page)
        context['comment_form'] = comment_form
        return context


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    fields = ['title', 'short_description', 'description', 'is_posted', 'image']

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(author=self.request.user)

    # def dispatch(self, request, *args, **kwargs):
    #     handler = super().dispatch(request, *args, **kwargs)
    #     user = self.request.user
    #     post = self.get_object()
    #     if not (post.author == user):
    #         raise PermissionDenied
    #     return handler


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('home')

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(author=self.request.user)


class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/create_comment.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        url = self.request.build_absolute_uri(f'/blog/post/{form.instance.post.id}')
        email = form.instance.post.author.email
        send_system_message.delay(subj='New Comment', message='New comment added, check the admin page',
                                  email='system@admin.com')
        send_system_message_for_author.delay(email=email, url=url)
        form.save()
        return super().form_valid(form)

    success_url = reverse_lazy('home')


# realization contact us with ajax
def contact_us(request):
    data = dict()

    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            data['form_is_valid'] = True
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            data['html_send_form'] = render_to_string('blog/contact_us.html')
            send_system_message.delay(subj='Contact Us', email=email, message=message)
        else:
            data['form_is_valid'] = False
    else:
        form = ContactUsForm()
    context = {'form': form}
    data['html_form'] = render_to_string('blog/contact_us.html', context, request=request)
    return JsonResponse(data)
