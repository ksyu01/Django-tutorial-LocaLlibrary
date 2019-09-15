import datetime
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
    paginate_by = 10


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


from django.contrib.auth.mixins import PermissionRequiredMixin


# Challenge
# View для страницы группы librarians, работает только если у пользователя есть конкретный permission
class LoanedBooksByLibrariansListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10
    permission_required = ('catalog.can_mark_returned',)

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


# для формы с занесением информации о книге
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
# импорт созданной формы из нашей forms.py
from catalog.forms import RenewBookForm


# ограничиваем доступ к форме только тем, кто имеет доступ к 'can_mark_returned'
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    # по номеру primary key проверяем, существует ли такой BookInstance
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    # это обращение с заполненной формой
    if request.method == 'POST':

        # Create a form instance and populate it with data from request (binding)
        # берём инстанс формы и наполняем его данными из запроса
        form = RenewBookForm(request.POST)

        # check if the form is valid:
        # проверяется в том числе наша функция clean_renewal_date() на границы дат
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            # записываем данные об инстансе в БД
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            # в успешном случае переадресация на другую страницу, ф-ция reverse забирает URL по его имени
            return HttpResponseRedirect(reverse('all-borrowed'))

        # если форма не валидна - уходим в вызов render снова, но теперь с заполненными полями и сообщениями об ошибке

    # If this is a GET (or any other method) create the default form
    # т.е. если это первый вызов формы, то заполняем начальные данные (default), собираем форму и строим html с ней
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    # берём форму и ещё инстанс, данные из которого тоже хотим показывать
    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


# view для управления записями с авторами
# шаблоны ожидаются с именем modelname_form.html, но можно переопределить через template_name_suffix = '_other_suffix'
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    # предлагаемое значение поля
    initial = {'date_of_death': '05/01/2018'}
    # по умолчанию после успешного выполнения будет редирект на страницу author detail
    # страницу можно переопределить с помощью success_url =
    permission_required = ('catalog.can_mark_returned',)


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    # эти две модели ожидают template <model name>_form.html
    permission_required = ('catalog.can_mark_returned',)


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    # эта модель ожидает template <model name>_confirm_delete.html
    permission_required = ('catalog.can_mark_returned',)


# для книг
from catalog.models import Book


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = ('catalog.can_mark_returned',)


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = ('catalog.can_mark_returned',)


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = ('catalog.can_mark_returned',)
