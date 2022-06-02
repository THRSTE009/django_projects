from django.urls import path, re_path
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    # Challenge 1:
    # Consider how you might encode a URL to list all books released in a particular year, month, day,
    # and the RE that could be used to match it.
    # re_path(r'^books/(?P<stub>[-\w]+)$', views.BookDetailView.as_view(), name='books),

    # path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),

    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),

]