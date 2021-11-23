from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from . models import Book
from . forms import BookForm
from . BookRecEngine import BookSuggestionEngine

# Create your views here.

def Book_Recommender(request):
    """
    This view utilize autocomplete query to search for specific book in database,
    then if form is submitted get book id from database and redirect to book detail page.
    If multiple id retruned because duplicates in db it takes first id of the book sorted by ids. 
    """
    if "term" in request.GET:
        qs = Book.objects.filter(title__icontains=request.GET.get("term") )
        titles = list()
        for booktitle in qs:
            titles.append(booktitle.title)

        return JsonResponse(titles, safe=False)
    
    elif request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            # get book id by title
            title = form.cleaned_data['book_name']
            get_book = Book.objects.filter(title=title).order_by("id").first()
            book_id = get_book.id

            context = {"data":book_id}

        return redirect("book_detail",pk=book_id)
    else:
        form = BookForm()    

    context = {"form":form}
    return render(request,"index.html",context)


def Book_Detail(request,pk):
    """
    commentary
    """
    obj =Book.objects.get(pk=pk)
    bookname = obj.title
    engine = BookSuggestionEngine(bookname)
    pivot = engine.prepare_data()
    suggested_books = list(pivot)
    
    #get object in database
    #for b in pivot:
        #suggested_books.append(b)
    

    context = {"obj":obj,"suggested_books":suggested_books }
    return render(request,"book.html",context )