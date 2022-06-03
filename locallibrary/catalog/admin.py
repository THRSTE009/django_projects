from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Author, Genre, Book, BookInstance, Language, User


"""Minimal registration of Models.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)
admin.site.register(Language)
"""

admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(User, UserAdmin)

class BooksInline(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Book
    extra = 0


class BooksInstanceInline(admin.TabularInline):
    """Defines format of inline book instance insertion (used in BookAdmin)"""
    model = BookInstance
    extra = 0


# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Administration object for Book models.
        Defines:
         - fields to be displayed in list view (list_display)
         - adds inline addition of book instances in book view (inlines)
        """
    list_display = ('title', 'author', 'display_genre')
    list_filter = ('title', 'author')
    inlines = [BooksInstanceInline]


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    """Administration object for BookInstance models.
       Defines:
        - fields to be displayed in list view (list_display)
        - filters that will be displayed in sidebar (list_filter)
        - grouping of fields into sections (fieldsets)
       """
    list_display = ('book', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Administration object for Author models.
        Defines:
         - fields to be displayed in list view (list_display)
         - orders fields in detail view (fields),
           grouping the date fields horizontally
         - adds inline addition of books in author view (inlines)
        """
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    inlines = [BooksInline]

    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

