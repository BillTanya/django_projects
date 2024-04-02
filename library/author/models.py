from django.db import models

from book.models import Book


class Author(models.Model):
    """
        This class represents an Author. \n
        Attributes:
        -----------
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes last name of the author
        type surname: str max_length=20
        param patronymic: Describes middle name of the author
        type patronymic: str max_length=20
    """
    name = models.CharField(blank=True, max_length=20)
    surname = models.CharField(blank=True, max_length=20)
    patronymic = models.CharField(blank=True, max_length=20)
    books = models.ManyToManyField(Book, related_name='authors')
    id = models.AutoField(primary_key=True)

    def display_books(self):
        return ', '.join([book.name for book in self.books.all()[:3]])

    display_books.short_description = 'Books'

    def authors_books(self):
        b = self.books.all()
        books = ''
        if len(b) == 1:
            for book in self.books.all():
                books += str(book.name)
        elif len(b) > 1:
            for i in range(len(self.books.all())-1):
                books += str(b[i].name)+', '
            books += str(b[len(b)-1].name)
        else:
            books += 'no book yet'
        return books


    def get_books(self):
        last_book = None
        books = list(self.books.all())
        if len(books) == 1:
            last_book = books[0]
            books = None
        elif len(books) > 1:
            last_book = books[-1]
            books = books[::-1][1:]
        return {'books': books, 'last_book': last_book}

    def __str__(self):
        """
        Magic method is redefined to show all information about Author.
        :return: author id, author name, author surname, author patronymic
        """
        if self.patronymic:
            return f"{self.name} {self.patronymic} {self.surname}"
        else:
            return f"{self.name} {self.surname}"
        # return f"\'id\': {self.pk}, \'name\': \'{self.name}\'," \
        #        f" \'surname\': \'{self.surname}\', \'patronymic\': \'{self.patronymic}\'"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Author object.
        :return: class, id
        """
        if self.patronymic:
            return f"{self.name} {self.patronymic} {self.surname}"
        else:
            return f"{self.name} {self.surname}"

    @staticmethod
    def get_by_id(author_id):
        """
        :param author_id: SERIAL: the id of a Author to be found in the DB
        :return: author object or None if a user with such ID does not exist
        """
        # return Author.objects.filter(id=author_id)
        # return Author.get_by_id(author_id)
        # return  Author.get_object_or_404()
        try:
            return Author.objects.get(id=author_id)
        except:
            return None

    @staticmethod
    def delete_by_id(author_id):
        """
        :param author_id: an id of a author to be deleted
        :type author_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        try:
            author = Author.objects.get(pk=author_id)
            book = None
            for b in Book.objects.all():
                for aut in b.authors.all():
                    if aut.id == author.id:
                        book = b
                        raise ValueError
            author.delete()
            return True
        except ValueError:
            return book
        except:
            return None

    @staticmethod
    def create(name, surname, patronymic):
        """
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes surname of the author
        type surname: str max_length=20
        param patronymic: Describes patronymic of the author
        type patronymic: str max_length=20
        :return: a new author object which is also written into the DB
        """
        try:
            if name and len(name) <= 20 and surname and len(surname) <= 20:
                if patronymic and len(patronymic) <= 20:
                    for aut in Author.objects.all():
                        if aut.name == name and aut.surname == surname and aut.patronymic == patronymic:
                            raise ValueError
                    Author(name=name, surname=surname, patronymic=patronymic).save()
                else:
                    for aut in Author.objects.all():
                        if aut.name == name and aut.surname == surname:
                            raise ValueError
                    Author(name=name, surname=surname).save()
                return None
        except:
            return False

    def to_dict(self):
        """
        :return: author id, author name, author surname, author patronymic
        :Example:
        | {
        |   'id': 8,
        |   'name': 'fn',
        |   'surname': 'mn',
        |   'patronymic': 'ln',
        | }
        """
        # return self.__dict__

    def update(self,
               name=None,
               surname=None,
               patronymic=None):
        """
        Updates author in the database with the specified parameters.\n
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes surname of the author
        type surname: str max_length=20
        param patronymic: Describes patronymic of the author
        type patronymic: str max_length=20
        :return: None
        """

        if name and len(name) <= 20:
            self.name = name
        if surname and len(surname) <= 20:
            self.surname = surname
        if patronymic and len(patronymic) <= 20:
            self.patronymic = patronymic
        self.save()

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all authors
        """
        return Author.objects.all()
