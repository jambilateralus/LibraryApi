# Create your views here.

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
