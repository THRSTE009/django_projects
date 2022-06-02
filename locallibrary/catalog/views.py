from django.shortcuts import render

# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
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
    paginate_by = 2

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

    template_name = 'books/my_arbitray_template_name_list.html' # Specify your own template name/location.



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