from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import serializers
from .models import Books
import json
from django import forms
import requests
import threading



# Create your views here
#These functions are mapped to the URLs
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
    
    author = Books.objects.filter(name = name).values()
    print(author)
    if author: 
        serializer = UserSerializer(author,many=True)
        return HttpResponse(json.dumps(serializer.data),status=status.HTTP_202_ACCEPTED)
    else:
        return HttpResponse("<h1>Author not found <h1>")
    
#http://127.0.0.1:8000/members/list/
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
    #Url  direct manipulation
    all_books = Books.objects.all()
    list = []
    #Checking for a duplicate record but it is not working
    for i in all_books:
        list.append(i.title)
        if title in list:
            return HttpResponse("<h1>Title duplicates found<h1>")
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

#Bulk operation using Google books API 
#http://127.0.0.1:8000/members/multiple/10/?q=Python


@api_view(['GET','POST'])
def add_multiple_books(request,number):
   
    query = request.GET.get('q', '')  # Get the search query from the URL
    api = requests.get(
        "https://www.googleapis.com/books/v1/volumes?/q={query}",
        params={'q':query,'maxResults':number}
    )
    
    all_data = api.json()
  
    
    book_title_list = []
    book_authors_list = []
    book_date_list = []
    book_price_list = []
    id_list = []
    
    #print(len(all_data['items']))
    
    try:    
        for i in range(number):
            
            book_item = all_data['items'][i]
            id = book_item['id']#primary key
            #book_authors = book_item['volumeInfo']['authors']#Its a list already
            book_title = book_item['volumeInfo']['title']
            if 'saleInfo' in book_item:
                book_price = book_item['saleInfo']
                book_price_list.append(book_price)
            else:
                print("sale info not found for:")  
                #print(book_authors) 
            if 'publishedDate' in book_item['volumeInfo']:
                book_date = book_item['volumeInfo']['publishedDate']
                book_date_list.append(book_date)
            else:
                print("Published date not found :")
                #print(book_authors)
                
            book_title_list.append(book_title)
            #book_authors_list.append(book_authors)
            id_list.append(id)
        
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    print(len(book_title_list))
    #print(book_title_list)
    #Saving the retrieved data to the models
   
    try:
        for i in range(number):
            print(i)
            add_books(request,"null",book_title_list[i],i)
        return  JsonResponse({"success":"Books added successfully"},status=status.HTTP_200_OK)
    except Exception as err:
        print(f"Unexpected storing data {err=}, {type(err)=}")   
        return JsonResponse({"error":"Failed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
   
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
    
    all_books = Books.objects.all()
    list = []
    try:
        for i in all_books:
            list.append(i.id)
            print(list)
        if id not in list: 
            return JsonResponse({"error":"No matching records found"},status=status.HTTP_404_NOT_FOUND)
        else:
            book_to_del = 0
            book_to_del = all_books.get(id = id)
            book_to_del.delete()
                
            return JsonResponse({"success":"Book deleted successfully"},status=status.HTTP_200_OK)
    except:
        return JsonResponse({"error":"Failed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Also try to delete the books based on the titles
def delete_multiple_books(request,list):#list == ids 
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
            return JsonResponse({"error":"No matching records found"},status=status.HTTP_404_NOT_FOUND) 
        
    except Exception as record_check_err:
        print(f"Unexpected checking the data {record_check_err=}, {type(record_check_err)=}")  
        return JsonResponse({"error":"Failed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        if failed != -1:
            books_to_del = []
            for i in range(len(id_list)):
                books_to_del.append(all_books.get(id = id_list[i]))
                books_to_del[i].delete()
            return JsonResponse({"success":"Books deleted successfully"},status=status.HTTP_200_OK)  
        
    except Exception as err:
        print(f"Unexpected deleting data {err=}, {type(err)=}")  
        return JsonResponse({"error":"Failed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     
def delete_all(request):
    all_books = Books.objects.all()
    try:
        for i in all_books:
            i.delete()
        return JsonResponse({"success":"All books deleted successfully"},status=status.HTTP_200_OK)
    except:
        return JsonResponse({"error":"Failed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)