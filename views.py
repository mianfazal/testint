# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render , get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  #LoginRequiredMixin this is used for if anyone directly access page without login then it take to login page it mean login first
                                                                           # UserPassesTestMixin used with function..my funtion is test_func..working of this is only update the post of current user logged
from .models import Post, AddGlasses
from django.views.generic import ( #this is class based View that django already do this for us
                                     ListView,
                                     DetailView,
                                     CreateView,
                                     UpdateView, DeleteView)






# Create your views here.


#dfrnce between class based view function based view,,,how we render html page and fetch data from model
#start def functio or methd
# def home(request): #this is not used now
  #  context={
   #         "posts":Post.objects.all()
    #        }

    # return render(request, 'blog/home.html',context)  #return render(request, 'blog/home.html', {'title':'Home' , "posts":posts})
#end def
#start calss
# class PostListView(ListView):  same work as defination
 #   model = Post
  #  template_name = 'blog/home.html' #<app>/<model>_<viewtype>_html
   # context_object_name = 'posts'
# end classs
#end dfrnce

class PostListView(LoginRequiredMixin, ListView): #class based view used almost predefind variable for perform task in def we explicity make function and perform some task
    model = Post   #there 'model' predefined and take user model that is created and want to show.it is necessary for classes based view
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>_html <- this is tell how is work to access template (PostView.as_view) in urls pattern
                                    # there <app is blog>/<model Post>_<viewtype is List>.html is home.html
                                    #template_name is predefined variable and used by .as_view() in urls pattern
    context_object_name = 'posts'  #take all data by objects also a predefined variable
                                 #'posts'is our custome varibale for used fetching all data and also used in html page by loop to show data
    ordering = ['-date_posted']    #it show list in Descending order also a predefined variable
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5    #5 posts per page now and with style in home.html page where we get pagination in working by adding buttons and click

    def get_queryset(self): #if user want to access any other user who not exist by typing in urls part then it return 404 page
        user = get_object_or_404( User, username=self.kwargs.get('username')) #if user click on profile pic then it get all post of current user by
                                                                            #' user/<str:username>' according to this
                                                                            # if user not exist by writing in urls part thrn it retun 404 oage
        return Post.objects.filter(author=user).order_by('-date_posted')#return all post of current user if exist


class PostDetailView(DetailView):
    model = Post #<app>/<model>_<viewtype>_html  as this it find automatically /post-detail.html page



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields =  ['title', 'content'] #there get all fields of model and get this fields in post_form.html

    def form_valid(self, form):
        form.instance.author = self.request.user #save another new post by the name or instance of current user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields =  ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)     #create and post is almost same until this line

    def test_func(self):                 #this function is used to update post only of current user logged
        post = self.get_object()  #there we get current object
        if self.request.user == post.author: #then we checked acording to current user request to update..are that post is equal to current user post
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' #after click on 'yes,delete' button then it go to home page

    def test_func(self):  #same function is used of PostUpdateView bocz we confirm current user has its own post aor not
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

def about(request):
     return render(request, 'blog/about.html', { 'title' : 'About'})


def livetryon(request):
    getglasses = AddGlasses.objects.all() 
    
    if request.method == 'POST' :
        print("yes post method")
        glasses = request.FILES 
        print(glasses)
        return render(request, 'blog/livetryon.html', {'title': 'Live Tryon',"glass":glasses })
    return render(request, 'blog/livetryon.html', {'title': 'Live Tryon', 'addglasses': getglasses })


def imagetryon(request):
    
    return render(request, 'blog/imagetryon.html', {'title': 'Image Tryon' })
