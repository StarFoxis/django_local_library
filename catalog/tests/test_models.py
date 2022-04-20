from django.test import TestCase

import datetime
from uuid import uuid4
from catalog.models import Author, Book, Genre, Language, BookInstance

class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Big', last_name='Bob')
    
    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'died')
    
    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name} {author.first_name}'
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1/')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'last name')
    
    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label, 'date of birth')
    
    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 100)

class BookModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        language = Language.objects.create(name='Russian')        
        genre = Genre.objects.create(name='Roman')        
        author = Author.objects.create(first_name='Big', last_name='Bob')        
        book = Book.objects.create(title='Book name', 
                            author=author,
                            summary='text summary',
                            isbn='123',
                            # genre=genre, # на прямую с ManyToManyField нельзя
                            # language=language, # используй метод set
                            date_of_published=datetime.date.today())
        book.genre.set((genre, ))
        book.language.set((language, ))
    
    def test_object_name_is_title(self):
        book = Book.objects.get(id=1)
        expected_object_name = book.title
        self.assertEquals(expected_object_name, str(book))

    def test_method_book_is_display_genre(self):
        book = Book.objects.get(id=1)
        display_genre = book.display_genre()
        self.assertEquals(display_genre, 'Roman')
    
    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        self.assertEquals(book.get_absolute_url(), '/catalog/book/1/')

class BookInstanceModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        language = Language.objects.create(name='Russian')        
        genre = Genre.objects.create(name='Roman')        
        author = Author.objects.create(first_name='Big', last_name='Bob')        
        book = Book.objects.create(title='Game Pupa Task 1', 
                            author=author,
                            summary='text summary',
                            isbn='123',
                            # genre=genre, # на прямую с ManyToManyField нельзя
                            # language=language, # используй метод set
                            date_of_published=datetime.date.today())
        book.genre.set((genre, ))
        book.language.set((language, ))
        BookInstance.objects.create(id=uuid4(),
                                    book=book,
                                    imprint='yes',
                                    due_back=datetime.date.today() + datetime.timedelta(weeks=3),
                                    status='o')                                  
        BookInstance.objects.create(id=uuid4(),
                                    book=book,
                                    imprint='yes',
                                    due_back=datetime.date.today() - datetime.timedelta(weeks=3),
                                    status='r')

    def test_object_name_is_id_and_book_title(self):
        bookinst = BookInstance.objects.first()
        expected_object_name = f'{bookinst.id} ({bookinst.book.title})'
        self.assertEquals(expected_object_name, str(bookinst))

    def test_method_is_overdue_in_date_last(self):
        bookinst = BookInstance.objects.last()
        self.assertFalse(bookinst.is_overdue)
    
    def test_method_is_overdue_in_date_fast(self):
        bookinst = BookInstance.objects.first()
        self.assertTrue(bookinst.is_overdue)



