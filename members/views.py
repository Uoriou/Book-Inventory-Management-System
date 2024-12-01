from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import serializers
from .models import Books
import json
from django import forms
#Testing
import requests



# Create your views here
#This function is mapped to a URL
#Unit test is compulsory -- >Available in Python Library 


#Serializer class to convert any model to JSON format
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = "__all__"
#Form to allow the user input 
class NameForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = "__all__"

def filter_author(request,name):
    
    #This is the template method
    """
    form = NameForm(request.POST)
    if form.is_valid():
        
        print(form.data['name'])
        books = Books.objects.filter(name = form.data['name']).values()
        serializer = UserSerializer(books,many=True)
        return HttpResponse(json.dumps(serializer.data),status=status.HTTP_200_OK)
    else:
        form = NameForm()
        
    return render(request, "test.html", {"form": form})
    """

    author = Books.objects.filter(name = name).values()
    print(author)
    if author: 
        serializer = UserSerializer(author,many=True)
        return HttpResponse(json.dumps(serializer.data),status=status.HTTP_202_ACCEPTED)
    else:
        return HttpResponse("<h1>Author not found <h1>")
    
#@api_view(['GET'])  
def get_books(request):
    books = Books.objects.all()
    serializer = UserSerializer(books,many =True)
    return JsonResponse(serializer.data,safe=False)
   
   
def get_sorted_books(request,option,sort):
    #Sorting the title first
    
    try:
        #This is just testing 
        all_books = Books.objects.all()
        map = {}
        chars = [] 
        sorted_title = []
        for i in all_books:
            map[i.title[0]] = i.title
            chars.append(i.title[0])
            
        for j in sorted(map.keys()):
            sorted_title.append(map.get(j))         
        print(sorted_title)
        try:
            if str(option) == 'title':
                sorted_books = Books.objects.all().order_by('title')
                serialized = UserSerializer(sorted_books,many=True)
                return JsonResponse(serialized.data,safe=False)
            elif str(option) == 'price':#Ascending and Descending ?
                sorted_books = Books.objects.all().order_by('price')
                serialized = UserSerializer(sorted_books,many=True)
                return JsonResponse(serialized.data,safe=False)
            elif str(option) == '-price':
                sorted_books = Books.objects.all().order_by('-price')
                serialized = UserSerializer(sorted_books,many=True)
                return JsonResponse(serialized.data,safe=False) 
            else:
                return HttpResponse('<h1>Invalid Option Selected</h1>')
          
        except:
            HttpResponse('<h1>Invalid option Selected</h1>') 
    
    except:
       return HttpResponse('<h1>Something went wrong</h1>') 
   
    return HttpResponse('<h1></h1>') 
    

def add_books(request,name,title,price):
    
    #This is the template method 
    """
    form = NameForm(request.POST)
    print(request)
    if form.is_valid():
        print(form.data)
        form.save()
    else:
        form = NameForm()
    return render(request, "test.html", {"form": form})
    """
   
    #Url  direct manipulation
    all_books = Books.objects.all()
    list = []
    books_map = {}
    #Checking for a duplicate record but it is not working
    for i in all_books:
        books_map[i.title] = 1
        if i.title in books_map:
            print("Ok")
        list.append(i.title)
    if title in list:
        return HttpResponse("<h1>Title Duplicates found<h1>")
    else:
        books = Books()
        books.name = name
        books.title = title
        books.price = price
        #print(books.name)
        if books.name and books.title:# Try catch error to handle a malicious input
            books.save()
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

#Bulk operation 
@api_view(['GET','POST'])
def add_multiple_books(request,number):
    #Call Google API to extract a number of books and then do a batch operation on it 
    #And add book on each batch 
    #API key = AIzaSyArBcVO54LmaymPHUZU5-IpHk9t62R7s3I
    #http://127.0.0.1:8000/members/multiple/10/?q=Python
    query = request.GET.get('q', '')  # Get the search query from the URL
    api = requests.get(
        "https://www.googleapis.com/books/v1/volumes?/q={query}",
        params={'q':query,'maxResult':number,}
        
    )
    all_data = api.json()
    
    try:
        author_map = {}
        book_title_list = []
        book_authors_list = []
        book_date_list = []
        book_price_list = []
        id_list = []
        for i in range(number):
            #Need to map every detail to an author id
            book_item = all_data['items'][i]
            id = book_item['id']#Treat it as a primary key
            book_authors = book_item['volumeInfo']['authors']#Its a list already
            book_title = book_item['volumeInfo']['title']
            
            if 'saleInfo' in book_item:
                book_price = book_item['saleInfo']
                book_price_list.append(book_price)
            else:
                print("sale info not found for:")  
                print(book_authors) 
            if 'publishedDate' in book_item['volumeInfo']:
                book_date = book_item['volumeInfo']['publishedDate']
                book_date_list.append(book_date)
            else:
                print("Published date not found :")
                print(book_authors)
                
            book_title_list.append(book_title)
            book_authors_list.append(book_authors)
            id_list.append(id)
           
        #print(id_list)
        #print(book_title_list)
        #print(book_authors_list)#Nested list and it is a problem
        #print(book_date_list)
        #print(book_price_list)
        
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        
    #Saving the retrieved data to the models
    try:
       #price = 10
       for i in range(number):
           add_books(request,book_authors_list[i],book_title_list[i],i)
    except Exception as err:
        print(f"Unexpected storing data {err=}, {type(err)=}")   
    
    #return JsonResponse(book_item)
    return HttpResponse("<h1>OK</h1>")
    
    
def update_books(request,id,option,new_record):
    
    all_books = Books.objects.all()
    for iter in all_books:
        print(iter.id)#Debugging 
    if all_books:
        #Switch statement?
        if option == "title":
            print("Title change opted")
            print(update_title(id,new_record))
            
        if option == "name":
            print("Name change opted")
            print(update_name(id,new_record))
        #Retrieve again the db and show the updated version
        serializer = UserSerializer(all_books,many=True)
        return HttpResponse(json.dumps(serializer.data),status=status.HTTP_202_ACCEPTED)
        
def update_title(id,new_title):
    
    books = Books.objects.all()
    record = books.get(id=id)
    record.title = new_title
    record.save()
    return 1

def update_name(id,new_name):
    books = Books.objects.all()
    record = books.get(id=id)
    record.name = new_name
    record.save()
    return 1
    
def delete_books(request,id):
    #Make sure to do the input type validation 
    all_books = Books.objects.all()
    list = []
    try:
        for i in all_books:
            list.append(i.id)
            print(list)
        if id not in list: 
            return HttpResponse("<h1>Record not found<h1>") 
        else:
            book_to_del = 0
            book_to_del = all_books.get(id = id)
            book_to_del.delete()
                
            return HttpResponse("<h1>Book successfully deleted<h1>")    
    except:
        HttpResponse("<h1>Something went wrong</h1>")
        
    
    # template method 
    """
    form = NameForm(request.POST)
    if form.is_valid():
        print(form.data)
        book = Books.objects.get(name = form.data['name'])
        book.delete()
        
    return render(request, "test.html", {"form": form})
    """
def delete_multiple_books(request,list):#list == ids 
    #(?P<student_list>)
    id_list = list.split(',')#Input list
    print(id_list)

    all_books = Books.objects.all()
    id_from_db = []
    failed = 0
    try:
        for i in all_books:
            id_from_db.append(str(i.id))#Ids already in the db
        #Return an empty set if the matching is not detected
        if set(id_from_db) & set(id_list) == set():
            failed-=1
            return HttpResponse("<h1>One or more records not found<h1>") 
        
    except Exception as record_check_err:
        print(f"Unexpected checking the data {record_check_err=}, {type(record_check_err)=}")  
        return HttpResponse("<h1>Data checking failed</h1>")
    try:
        if failed != -1:
            books_to_del = []
            for i in range(len(id_list)):
                books_to_del.append(all_books.get(id = id_list[i]))
                books_to_del[i].delete()
            return HttpResponse("<h1>Books successfully deleted<h1>")    
        
    except Exception as err:
        print(f"Unexpected deleting data {err=}, {type(err)=}")  
        return HttpResponse("<h1>Something went wrong</h1>")
         
    
    
