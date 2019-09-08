from django.shortcuts import render

# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Challenge: добавляем метрики
    genres_contain = Genre.objects.filter(name__contains='я').count()
    books_contain = Book.objects.filter(title__contains='я').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'genres_contain': genres_contain,
        'books_contain': books_contain,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# создание страницы со списком книг через базовый класс Django ListView
# это даёт больше надежности кода, меньше повторений и гораздо меньше усилий на обслуживание
from django.views import generic

class BookListView(generic.ListView):
    model = Book
