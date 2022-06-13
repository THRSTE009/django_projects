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

    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.AllLoanedBooksListView.as_view(), name='all-borrowed'),
]

#   Tutorial 9 URLs
urlpatterns += [
# The URL configuration will redirect URLs with the format /catalog/book/<bookinstance_id>/renew/ to
    # the function named renew_book_librarian() in views.py, and send the BookInstance id as the parameter named pk.
    # The pattern only matches if pk is a correctly formatted uuid.
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),

    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),

    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]