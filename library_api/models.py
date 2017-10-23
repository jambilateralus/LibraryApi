from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

"""-----------------------------------------------------------------------------"""
"""                   Book Management Models                                    """
"""-----------------------------------------------------------------------------"""


class Category(models.Model):
    # Fields
    title = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bookmanager_category_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('bookmanager_category_update', args=(self.pk,))


class Publisher(models.Model):
    # Fields
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('bookmanager_publisher_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('bookmanager_publisher_update', args=(self.pk,))


class Author(models.Model):
    # Fields
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('bookmanager_author_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('bookmanager_author_update', args=(self.pk,))


class Book(models.Model):
    # Fields
    title = models.CharField(max_length=1000)
    book_id = models.IntegerField(unique=True, primary_key=True)
    isbn = models.CharField(unique=True, max_length=15)
    total_number_of_copies = models.IntegerField()
    available_number_of_copies = models.IntegerField()
    is_textbook = models.BooleanField(default=False)

    # Relationship Fields
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    category = models.ForeignKey(Category)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bookmanager_book_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('bookmanager_book_update', args=(self.pk,))


class BookCopy(models.Model):
    # Fields
    copy_number = models.IntegerField()

    # Relationship Fields
    book = models.ForeignKey(Book)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return str(self.book)

    def get_absolute_url(self):
        return reverse('bookmanager_bookcopy_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('bookmanager_bookcopy_update', args=(self.pk,))


"""-----------------------------------------------------------------------------"""
"""                 Member Management Models                                    """
"""-----------------------------------------------------------------------------"""


class Member(models.Model):
    # Fields
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    member_id = models.IntegerField(unique=True, primary_key=True)
    registered_year = models.DateField()
    email_address = models.EmailField()
    is_staff = models.BooleanField(default=False)

    # Relationship Fields
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_absolute_url(self):
        return reverse('membermanager_member_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('membermanager_member_update', args=(self.pk,))


"""-----------------------------------------------------------------------------"""
"""                 Library Management Models                                   """
"""-----------------------------------------------------------------------------"""


class BurrowedBook(models.Model):
    # Fields
    borrow_date = models.DateField()
    return_date = models.DateField()
    actual_return_date = models.DateField()

    # Relationship Fields
    book_copy = models.OneToOneField(BookCopy)
    burrowed_by = models.ForeignKey(Member)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return str(self.book_copy)

    def get_absolute_url(self):
        return reverse('librarymanager_burrowedbook_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('librarymanager_burrowedbook_update', args=(self.pk,))


class RequestedBook(models.Model):
    # Fields
    title = models.CharField(max_length=200, unique=True)
    author = models.CharField(max_length=400)
    publisher = models.CharField(max_length=200)
    requested_date = models.DateField()

    # Relationship Fields
    requested_by = models.ForeignKey(Member)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.title + " written by " + self.author

    def get_absolute_url(self):
        return reverse('librarymanager_requestedbook_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('librarymanager_requestedbook_update', args=(self.pk,))


class ReservedBook(models.Model):
    # Fields
    reserved_date = models.DateTimeField()

    # Relationship Fields
    book = models.ForeignKey(Book)
    reserved_by = models.ManyToManyField(Member)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.book + " is  reserved by " + self.reserved_by

    def get_absolute_url(self):
        return reverse('librarymanager_reservedbook_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('librarymanager_reservedbook_update', args=(self.pk,))
