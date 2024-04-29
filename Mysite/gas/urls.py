from django.urls import path

from . import views

urlpatterns = [

    path('', views.homepage, name=" "),

    path('register/', views.register, name="register"),

    path('my-login/', views.my_login, name="my-login"),

    path('dashboard/', views.dashboard, name="dashboard"),

    path('user-logout/', views.user_logout, name="user-logout"),

    path('userdetails/', views.userdetails, name="userdetails"),
    
    path('edituser/', views.editUser, name='edituser'),

    path('about/', views.about, name="about"),

    path('adminlogin/', views.adminlogin, name="adminlogin"),

    path('admindashboard/', views.admindashboard, name="admindashboard"),

    path('editpassword/', views.editPassword, name="editpassword"),

    path('customer-details/', views.customerdetails, name="customer-details"),

    path('editcustomers/<str:user>/', views.editcustomers, name="editcustomers"),

    path('deletecustomers/<str:user>/', views.deletecustomers, name="deletecustomers"),

    path('view_products/', views.view_products, name="view_products"),

    path('editproduct/', views.editproduct, name="editproduct"),

    path('booking/', views.booking, name="booking"),

    path('payment/<int:id>', views.payment, name="payment"),
    
    path('vieworders/', views.view_orders, name='view_orders'),
    
    path('everyorders/', views.everyOrders, name='everyorders'),

    path('editorders/<int:id>', views.editorders, name="editorders"),

    path('deleteorder/<int:id>', views.deleteorder, name="deleteorder"),

    path('invoice/<int:id>', views.invoice, name="invoice"),

    path('feedback_submission/', views.feedback_submission, name="feedback_submission"),

    path('view_feedback/', views.view_feedback, name="view_feedback"),
    
]


