from django.contrib import admin

# Register your models here.
from catalog.models import Author, Genre, Book, BookInstance

# admin.site.register(Book)  # SKurbatskiy 20190907 Создаём собственный вид страницы
# admin.site.register(Author)  # SKurbatskiy 20190907 Создаём собственный вид страницы
admin.site.register(Genre)
# admin.site.register(BookInstance)  # SKurbatskiy 20190907 Создаём собственный вид страницы


# Для показа данных по книгам на детальной странице с авторами
class BooksInline(admin.TabularInline):
    model = Book
    # Сколько добавить пустых Instance для заполнения (по умолчанию почему-то ставит 3)
    extra = 1


# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    # Перечисление полей, которые будут показываться вместо предыдущего __str__ из {self.last_name}, {self.first_name}
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # То, что сгруппирована в tuple, показывается горизонтально рядом друг с другом (не друг под другом)
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    # ссылка на класс, определенный выше, для подгрузки списка книг по этому автору
    inlines = [BooksInline]


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


# Для показа данных по Instance в BookAdmin
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    # Сколько добавить пустых Instance для заполнения (по умолчанию почему-то ставит 3)
    extra = 1


# Точно такой же эффект, как для Author, дают декораторы:
# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    # Ссылка на определенный раньше класс для показа Instance в BookAdmin
    inlines = [BooksInstanceInline]

# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # Добавление фильтров для вывода
    list_filter = ('status', 'due_back')

    # Если хотим разделить данные по секциям
    # Первым идёт название секции (или None, если название не нужно)
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

    # Challenge - добавить на лист со списком инстансов поля book, status, due back date, and id
    # вместо стандартного __str__()
    list_display = ('book', 'status', 'due_back', 'id')