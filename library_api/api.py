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
    pagination_class = StandardResultsSetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('^title', '^authors', '^publisher')


"""-----------------------------------------------------------------------------"""
"""                Library Management Viewset                                   """
"""-----------------------------------------------------------------------------"""


class RequestedBookViewSet(viewsets.ModelViewSet):
    """ ViewSet for RequestedBook class"""
    serializer_class = serializers.RequestedBookSerializer
    pagination_class = StandardResultsSetPagination

    # todo add permission class for RequestedBookViewSet
    # todo customize post method for RequestedBookViewSet

    def get_queryset(self):
        """This view should return a list of all the Requested Books
        for the currently authenticated user."""
        user = self.request.user
        member = models.Member.objects.filter(user=user)
        return models.RequestedBook.objects.filter(burrowed_by=member)


class ReservedBookViewSet(viewsets.ModelViewSet):
    """ ViewSet for ReservedBook class """
    serializer_class = serializers.RequestedBookSerializer
    # todo add permission class for ReservedBookViewSet
    # todo customize post for ReservedBookViewSet
    permission_classes = [AllowMemberOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """This view should return a list of all the Reserved Books
        for the currently authenticated user."""
        user = self.request.user
        member = models.Member.objects.filter(user=user)
        return models.ReservedBook.objects.filter(reserved_by=member)


class BurrowedBooksViewset(viewsets.ModelViewSet):
    """ ViewSet for BurrowedBook class"""
    serializer_class = serializers.BurrowedBookSerializer
    pagination_class = StandardResultsSetPagination

    # todo add permission class
    # todo customize post

    def get_queryset(self):
        """This view should return a list of all the Burrowed Books
        for the currently authenticated user."""
        if self.request.user == 'superuser':
            # Return a list of all burrowed books if the request is from admin.
            return models.BurrowedBook.objects.all()

        # Else Return a list of all the burrowed Book for currently authenticated member.
        user = self.request.user
        member = models.Member.object.filter(user=user)
        return models.BurrowedBook.objects.filter(burrowed_by=member)
