from django.urls import path
from . import views
from django.contrib import admin
#Mapping of the file path / url on the right side
#url would look like http://127.0.0.1:8000/members/list/ 
urlpatterns = [
    #Get 
    path('list/', views.get_books, name='books'),
    #Add
    path('a/<str:name>/<str:title>/<int:price>/',views.add_books,name='add'),
    path('multiple/<int:number>/',views.add_multiple_books,name='google book api'),
    path('p',admin.site.urls),
    #Filter
    path('f/<str:name>/',views.filter_author,name = 'filter'),
    #Sort
    path('list/<str:option>/<str:sort>',views.get_sorted_books,name='sort'),
    #Delete
    path('d/<int:id>/',views.delete_books,name='delete'),
    path('d/<list>/',views.delete_multiple_books,name = 'multiple delete'),
    path('delall/',views.delete_all,name='delete_all'),
    #Update
    path('list/<int:id>',views.update_books,name='update'),
    path('list/<int:id>/<str:option>/',views.update_books,name='update'),#A option If the title needs to be changed
    path('list/<int:id>/<str:option>/<str:new_record>/',views.update_books,name='update'),#new title 
]