import datetime

from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route, api_view
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from . import models
from . import serializers
from .pagination import StandardResultsSetPagination
from .permissions import CreatePutDeleteAdminOnly, AllowMemberOnly


@api_view(["POST"])
def member_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    member = models.Member.objects.filter(user=user)
    if not member:
        return Response({"error": "Login failed"}, status=status.HTTP_400_BAD_REQUEST)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": str(token.key)}, status=status.HTTP_200_OK)


@api_view(["GET"])
def member_info(request):
    user = request.user
    member = models.Member.objects.filter(user=user)
    serializer = serializers.MemberInfoSerializer(member, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def reserve_book(request, book_pk):
    user = request.user
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    book = models.Book.objects.get(pk=book_pk)
    member = models.Member.objects.get(user=user)

    if member and book:
        reserved_books = models.ReservedBook.objects.filter(reserved_by=member)
        already_reserved = models.ReservedBook.objects.filter(reserved_by=member, book=book)

        if already_reserved:
            return Response({"message": "You have already reserved this book."}, status=status.HTTP_200_OK)

        if reserved_books.count() < 3:
            res_book = models.ReservedBook.objects.create(book=book,
                                                          reserved_date=date)

            res_book.reserved_by.add(member)
            return Response({"message": "Book reserved"},
                            status=status.HTTP_200_OK)

        return Response({"message": "You have already reserved 3 books."},
                        status=status.HTTP_200_OK)

    return Response({"message": "Invalid"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def request_new_book(request):
    user = request.user
    member = models.Member.objects.get(user=user)
    current_date = datetime.datetime.today().strftime('%Y-%m-%d')

    data = {
        'title': request.data['title'],
        'author': request.data['author'],
        'publisher': request.data['publisher'],
        'requested_by': member.pk,
        'requested_date': current_date
    }

    serializer = serializers.RequestedBookSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""-----------------------------------------------------------------------------"""
"""                   Book Management Viewset                                   """
"""-----------------------------------------------------------------------------"""


class AuthorViewSet(viewsets.ModelViewSet):
    """ViewSet for the Author class"""
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    permission_classes = [CreatePutDeleteAdminOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class PublisherViewSet(viewsets.ModelViewSet):
    """ViewSet for the Publisher class"""
    queryset = models.Publisher.objects.all()
    serializer_class = serializers.PublisherSerializer
    permission_classes = [CreatePutDeleteAdminOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the Category class"""
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [CreatePutDeleteAdminOnly]

    @detail_route(['GET'])
    def book_list(self, request, pk=None):
        """This view should return a list of all the Books
        for the given category."""
        category = self.get_object()  # retrieve an object by pk provided
        books = models.Book.objects.filter(category=category)
        serializer = serializers.BookSerializer(books, many=True)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    """ ViewSet for Book class """
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes = [CreatePutDeleteAdminOnly]
    # pagination_class = StandardResultsSetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('^title',)


"""-----------------------------------------------------------------------------"""
"""                Library Management Viewset                                   """
"""-----------------------------------------------------------------------------"""


class RequestedBookViewSet(viewsets.ModelViewSet):
    """ ViewSet for RequestedBook class"""
    serializer_class = serializers.RequestedBookSerializer

    # todo add permission class for RequestedBookViewSet
    # todo customize post method for RequestedBookViewSet

    def get_queryset(self):
        """This view should return a list of all the Requested Books
        for the currently authenticated user."""
        user = self.request.user
        member = models.Member.objects.filter(user=user)
        return models.RequestedBook.objects.filter(requested_by=member)


class ReservedBookViewSet(viewsets.ModelViewSet):
    """ ViewSet for ReservedBook class """
    serializer_class = serializers.ReservedBookSerializer
    # todo add permission class for ReservedBookViewSet
    # todo customize post for ReservedBookViewSet
    permission_classes = [AllowMemberOnly]

    def get_queryset(self):
        """This view should return a list of all the Reserved Books
        for the currently authenticated user."""
        user = self.request.user
        member = models.Member.objects.filter(user=user)
        return models.ReservedBook.objects.filter(reserved_by=member)


class BurrowedBooksViewset(viewsets.ModelViewSet):
    """ ViewSet for BurrowedBook class"""
    serializer_class = serializers.BurrowedBookSerializer

    # todo customize post

    def get_queryset(self):
        """This view should return a list of all the Burrowed Books
        for the currently authenticated user."""
        if self.request.user.is_superuser:
            # Return a list of all burrowed books if the request is from admin.
            self.pagination_class = StandardResultsSetPagination
            return models.BurrowedBook.objects.all()

        # Else Return a list of all the burrowed Book for currently authenticated member.
        self.serializer_class = serializers.BurrowedBooksForAppSerializer
        user = self.request.user
        member = models.Member.objects.filter(user=user)
        return models.BurrowedBook.objects.filter(burrowed_by=member)


"""
@api_view(['GET', 'POST'])
def category_list(request):
    # List all category or add new category.
    if request.method == 'GET':
        if request.user.is_authenticated:
            categories = models.Category.objects.all()
            serializer = serializers.CategorySerializer(categories, many=True)
            return Response(serializer.data)
        return Response({"message": "not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'POST':
        if request.user.is_superuser:
            serializer = serializers.CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "not authorized"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    # Retrieve, update or delete a Category instance.
    try:
        category = models.Category.objects.get(pk=pk)
    except models.Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
