from django.urls import path
from . import views

urlpatterns = [
    # в параметрах URL pattern
    # функция, которую нужно будет искать в модуле views и вызывать её
    # name - имя этого конкретного URL-маппинга
    # .as_view() - чтобы использовать класс как view
    path('', views.index, name='index'),
    # ссылка на страницу со всеми книгами. view в виде класса, чтобы наследовать нужные свойства и не писать их заново
    path('books/', views.BookListView.as_view(), name='books'),
    # ссылка на страницы с книгами book detail
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    # Challenge: создаем страницу со списком авторов
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    # странциа author detail
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    # страница со списком взятых книг для пользователя
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    # страница со списком взятых книг для группы librarians
    path('borrowed/', views.LoanedBooksByLibrariansListView.as_view(), name='all-borrowed'),
    # страницы формы с книгами
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew_book_librarian'),
    # страницы форм с редактированием авторов
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    # challenge страницы форм с редактированием книг
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
]