from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Book, Borrow
from .serializers import BookSerializer, BorrowSerializer
from accounts.permissions import IsAdmin, IsLibrarian

# ----------------------------
# Book ViewSet with role-based access & caching
# ----------------------------
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdmin | IsLibrarian]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        # Cache all books
        cache_key = 'books_list'
        books = cache.get(cache_key)
        if not books:
            print("Cache MISS: fetching books from DB")
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            books = serializer.data
            cache.set(cache_key, books, timeout=60*5)
        else:
            print("Cache HIT: fetching books from cache")
        return Response(books)

# ----------------------------
# Borrow / Return Books
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if not book.is_available:
        return Response({'error': 'Book is already borrowed.'}, status=400)

    Borrow.objects.create(user=request.user, book=book)
    book.is_available = False
    book.save()

    # Clear relevant caches
    cache.delete('books_list')
    cache.delete('books_available')
    cache.delete('books_borrowed')
    cache.delete('borrows_active')

    return Response({'message': f'{book.title} borrowed successfully!'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def return_book(request, book_id):
    borrow = Borrow.objects.filter(user=request.user, book_id=book_id, is_returned=False).first()
    if not borrow:
        return Response({'error': 'No borrowed record found for this book.'}, status=404)

    borrow.is_returned = True
    borrow.save()
    borrow.book.is_available = True
    borrow.book.save()

    # Clear relevant caches
    cache.delete('books_list')
    cache.delete('books_available')
    cache.delete('books_borrowed')
    cache.delete('borrows_active')

    return Response({'message': f'{borrow.book.title} returned successfully!'})


# ----------------------------
# List all borrowed books (Admin or Librarian only) with caching
# ----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def borrowed_books_list(request):
    if not (IsAdmin().has_permission(request, None) or IsLibrarian().has_permission(request, None)):
        return Response({'detail': 'You do not have permission to view this list.'}, status=403)

    cache_key = 'borrows_all'
    borrows = cache.get(cache_key)
    if borrows:
        print("CACHE HIT: borrows_all")
        return Response(borrows)

    print("CACHE MISS: borrows_all")
    queryset = Borrow.objects.select_related('book', 'user').all()
    serializer = BorrowSerializer(queryset, many=True)
    cache.set(cache_key, serializer.data, timeout=60)
    return Response(serializer.data)


# ----------------------------
# List user’s own borrowed books with caching
# ----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_borrowed_books(request):
    cache_key = f'my_borrows_{request.user.id}'
    borrows = cache.get(cache_key)
    if borrows:
        print(f"CACHE HIT: {cache_key}")
        return Response(borrows)

    print(f"CACHE MISS: {cache_key}")
    queryset = Borrow.objects.filter(user=request.user, is_returned=False).select_related('book')
    serializer = BorrowSerializer(queryset, many=True)
    cache.set(cache_key, serializer.data, timeout=60)
    return Response(serializer.data)


# ----------------------------
# Optional: cached available / borrowed books via Book manager
# ----------------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def available_books(request):
    cache_key = 'books_available'
    books = cache.get(cache_key)
    if not books:
        print("CACHE MISS: available books")
        queryset = Book.objects.available()
        serializer = BookSerializer(queryset, many=True)
        books = serializer.data
        cache.set(cache_key, books, timeout=60)
    else:
        print("CACHE HIT: available books")
    return Response(books)


@api_view(['GET'])
@permission_classes([AllowAny])
def borrowed_books(request):
    cache_key = 'books_borrowed'
    books = cache.get(cache_key)
    if not books:
        print("CACHE MISS: borrowed books")
        queryset = Book.objects.borrowed()
        serializer = BookSerializer(queryset, many=True)
        books = serializer.data
        cache.set(cache_key, books, timeout=60)
    else:
        print("CACHE HIT: borrowed books")
    return Response(books)
