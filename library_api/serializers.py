from rest_framework import serializers

from . import models

"""-----------------------------------------------------------------------------"""
"""              Book Management Serializers                                    """
"""-----------------------------------------------------------------------------"""


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = (
            'pk',
            'title',
        )


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publisher
        fields = (
            'pk',
            'name',
        )


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = (
            'pk',
            'name',
        )


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    publisher = PublisherSerializer()
    category = CategorySerializer()

    class Meta:
        model = models.Book
        fields = (
            'pk',
            'title',
            'authors',
            'publisher',
            'category',
            'book_id',
            'isbn',
            'total_number_of_copies',
            'available_number_of_copies',
            'is_textbook',
        )


class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookCopy
        fields = (
            'pk',
            'book',
            'copy_number',
        )


"""-----------------------------------------------------------------------------"""
"""            Member Management Serializers                                    """
"""-----------------------------------------------------------------------------"""


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = (
            'pk',
            'first_name',
            'last_name',
            'member_id',
            'registered_year',
            'email_address',
            'is_staff',
        )


class MemberInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = (
            'first_name',
            'last_name',
            'registered_year',
        )


"""-----------------------------------------------------------------------------"""
"""           Library Management Serializers                                    """
"""-----------------------------------------------------------------------------"""


class BurrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BurrowedBook
        fields = (
            'pk',
            'book_copy',
            'borrow_date',
            'return_date',
            'actual_return_date',
        )


class RequestedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RequestedBook
        fields = (
            'pk',
            'title',
            'author',
            'publisher',
            'requested_date',
        )


class ReservedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReservedBook
        fields = (
            'pk',
            'reserved_date',
            'book',
        )
