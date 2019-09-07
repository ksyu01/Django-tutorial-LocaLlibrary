from django.contrib import admin

# Register your models here.
from catalog.models import Author, Genre, Book, BookInstance

# admin.site.register(Book)  # SKurbatskiy 20190907 Создаём собственный вид страницы
# admin.site.register(Author)  # SKurbatskiy 20190907 Создаём собственный вид страницы
admin.site.register(Genre)  # SKurbatskiy 20190907 Создаём собственный вид страницы
# admin.site.register(BookInstance)  # SKurbatskiy 20190907 Создаём собственный вид страницы


# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    # Перечисление полей, которые будут показываться вместо предыдущего __str__ из {self.last_name}, {self.first_name}
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


# Точно такой же эффект, как для Author, дают декораторы:
# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # Добавление фильтров для вывода
    list_filter = ('status', 'due_back')
