#   Notes:
#   1. We must use pk as the name for our captured primary key value, as this is the parameter name
#       expected by the view classes.

from django.shortcuts import render

from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic

#   Tutorial 8 imports
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

#   Tutorial 9 imports
#   Forms
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm

#   ModelForms
from django.forms import ModelForm
from catalog.models import BookInstance

#   Generic Editing Views
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# reverse_lazy() is a lazily executed version of reverse(),
# used here because we're providing a URL to a class-based view attribute.
from django.urls import reverse_lazy
from catalog.models import Author


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count() # The 'all()' is implied by default.

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# ListView is a class-based generic list view that inherits from an existing view which follows Django best-practice.
#   Making it more robust, less code, less repetition and less maintenance than standard views.
class BookListView(generic.ListView):
    """This generic view queryies the db to get all records for the specified model (Book) then it renders a template."""
    # Template location: /locallibrary/catalog/templates/catalog/book_list.html
    # Within the template you can access the list of books with the template variable named "object_list" OR "book_list"
    # (i.e. generically "<the model name>_list").

    model = Book
    paginate_by = 10

    # context_object_name = 'book_list' # custom name for the list as a template variable.
        # context passed by default as "object_list" or "book_list".
    def get_context_data(self, **kwargs):
        #1. Call the base implementation first to get the context.
        context = super(BookListView, self).get_context_data(**kwargs)
        #2. Create any data and add it to the context.
        context['some_data'] = 'This is just some data'
        return context #3. Return new (updated) context.

    # Option 1:
        # queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title 'war'.
    # Option 2:
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5]

    # template_name = 'books/my_arbitray_template_name_list.html' # Specify your own template name/location.


# def book_detail_view(request, primary_key):   *CLASS-BASED ALTERNATIVE FOR THE DETAIL VIEW*
#     book = get_object_or_404(Book, pk=primary_key)
#     return render(request, 'catalog/book_detail.html', context={'book': book})


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    """This generic view queryies the db to get all records for Author then it renders a template."""
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author

    # num_instances = BookInstance.objects.filter(__str__=author).count()
    #
    # def get_context_data(self, **kwargs):
    #     context = super(AuthorListView, self).get_context_data(**kwargs)
    #     context['num_instances'] = 'num_instances'
    #     return context


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        # 'o' is stored code for 'on loan'. Ordered by the due_back date so that the oldest items are displayed first.
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllLoanedBooksListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_users.html'
    paginate_by = 10

    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        # 'o' is stored code for 'on loan'. Ordered by the due_back date so that the oldest items are displayed first.
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


#   FUNCTIONAL FORM VIEW 1:
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

    permission_required = 'catalog.can_mark_returned'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)

    permission_required = 'catalog.can_mark_returned'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

    permission_required = 'catalog.can_mark_returned'

#   TUTORIAL 9 CHALLENGE:
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

    permission_required = 'catalog.can_mark_returned'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__' # Not recommended (potential security issue if more fields added)

    permission_required = 'catalog.can_mark_returned'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')

    permission_required = 'catalog.can_mark_returned'