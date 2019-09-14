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

    # Number of visits to this view, as counted in the session variable. Количество визитов
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'genres_contain': genres_contain,
        'books_contain': books_contain,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# создание страницы со списком книг через базовый класс Django ListView
# это даёт больше надежности кода, меньше повторений и гораздо меньше усилий на обслуживание
from django.views import generic


class BookListView(generic.ListView):
    model = Book
    paginate_by = 3


# детальная страница для книг
class BookDetailView(generic.DetailView):
    model = Book


# страница списка авторов
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 3


# детальная страница для авторов
class AuthorDetailView(generic.DetailView):
    model = Author


# View для создания страницы со списком взятых книг для конкретного пользователя
# LoginRequiredMixin - один из способов ограничить доступ только для тех, кто авторизован под этим пользователем
# ещё один способ - декоратор @login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    # задаём template - чтобы не стандартный *model*_list, так как сможем делать несколько разных шаблонов
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
