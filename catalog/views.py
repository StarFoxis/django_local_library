from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Book, Author, BookInstance, Genre, Language
import datetime

from .forms import RenewBookForm, RenewBookModelForm


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count() # Метод 'all()' применён по умолчанию.
    # Кол-во книг начинающихся с "у" (без учета регистра)
    num_books_startswith_y = Book.objects.filter(title__icontains='У').count()

    visit_count = request.session.get('visit_count', 0)
    visit_count += 1
    request.session['visit_count'] = visit_count

    # отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_books_startswith_y': num_books_startswith_y,
        }
    )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookYearListView(generic.ListView):
    model = Book
    
    def get_queryset(self):
        year = self.kwargs.get('year') or '2022'
        return Book.objects.filter(date_of_published__year=year)

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """ Все книги которые взял пользователь """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user) \
                                   .filter(status__exact='o') \
                                   .order_by('due_back')

class LoanedBooksByUsersListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_all_borrowed_users.html'
    paginate_by = 10
    permission_required = 'catalog.syka'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o') \
                                   .order_by('due_back')

@permission_required('catalog.syka')
def renew_book_librarian(request, pk):
    """ Отображения для изменения даты due_back модели BookInstance """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
    
    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death': '12/10/2016',}
    permission_required = ('catalog.syka')

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = ('catalog.syka')

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    permission_required = ('catalog.syka')
    success_url = reverse_lazy('authors')

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    initial = {'date_of_published': datetime.date.today(), 'language': Language.objects.filter(name='Русский')}
    permission_required = ('catalog.syka')

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ('title', 'author', 'summary', 'genre', 'language', 'date_of_published')
    # exclude = 'isbn'
    permission_required = ('catalog.syka')

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = ('catalog.syka')
    success_url = reverse_lazy('books')