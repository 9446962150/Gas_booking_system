from datetime import date
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
# Create your views here.
from . forms import CreateUserForm, UserProfileForm, LoginForm
from .models import *
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta,date
from django.db.models import Count
# - Authentication models and functions
from django.contrib.auth.models import auth ,User
from django.contrib.auth import authenticate, login, logout

import calendar
from calendar import HTMLCalendar
from django.http import HttpResponseRedirect
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, inch

import io
from reportlab.lib.pagesizes import letter, inch
from reportlab.pdfgen import canvas
from django.http import FileResponse
from .models import Orders, UserProfile



def homepage(request):

    return render(request, 'gas/index.html')



@login_required(login_url="adminlogin")
def register(request):
    error = ""

    form = CreateUserForm()
    profile_form = UserProfileForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid():

            user=form.save()

            profile=profile_form.save(commit=False)
            profile.User=user
            profile.save()
            error = "no"
        else:
            error = "yes"
                


    return render(request, 'gas/register.html', locals())


def adminlogin(request):
    error = ""

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            try:
                if user is not None and user.is_staff==True:

                    auth.login(request, user)
                    error = "no"
                else:
                    error = "yes"
            except:
                error = "yes"
            
    return render(request, 'gas/adminlogin.html', locals())



def my_login(request):
    error = ""

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            try:
                if user is not None and user.is_staff==False:
                    auth.login(request, user)
                    error = "no"
                else:
                    error = "yes"
            except:
                error = "yes"

    return render(request, 'gas/my-login.html', locals())


def user_logout(request):

    auth.logout(request)

    return redirect(" ")


@login_required(login_url="adminlogin")
def admindashboard(request):
    if request.user is not None:
        #return render(request, 'gas/adminlogin.html')
        users = User.objects.filter(username=request.user).values()
        count = User.objects.filter(is_staff=False).count()
        return render(request, 'gas/admindashboard.html', {'users': users ,'count' : count})


@login_required(login_url="my-login")
def dashboard(request):
    users = User.objects.filter(username=request.user).values()
    return render(request, 'gas/dashboard.html', {'users': users})

    #return render(request, 'gas/users.html',{'user':request.user})


@login_required(login_url="my-login")
def userdetails(request):
    # Filter users based on the currently logged-in user
    current_user = request.user
    users = User.objects.filter(username=current_user.username)
    return render(request, 'gas/users.html', {'users': users})

def about(request):
    return render(request, 'gas/about.html')

@login_required(login_url="my-login")
def editPassword(request):
    if not request.user.is_authenticated:
        return redirect(" ")
    error = ""
    user = request.user
    if request.method == "POST":
        old = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(username=request.user)
            if user.check_password(old):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request,'gas/editpassword.html', locals())

@login_required(login_url="my-login")
def editUser(request):
    if not request.user.is_authenticated:
        return redirect('my-login')
    user = User.objects.get(username=request.user)
    prof= UserProfile.objects.get(User=request.user)
    error = False
    if request.method == 'POST':
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        email = request.POST['email']
        address = request.POST['address']
        mobile = request.POST['mobile']

        user.first_name = fn
        user.last_name = ln
        user.email = email
        prof.address = address
        prof.mobile = mobile
        user.save()
        prof.save()
        error = True

    d = {'user': user, 'error': error}
    return  render(request, 'gas/edituser.html', locals())

@login_required(login_url="adminlogin")
def customerdetails(request):
    nonusers = User.objects.filter(is_staff=False).all()    
    return render(request, 'gas/customer-details.html',{'user':nonusers})

@login_required(login_url="admin_login")
def editcustomers(request, user):
    user1 = User.objects.get(username=user)
    prof= UserProfile.objects.get(User=user1)
    error = False
    if request.method == 'POST':
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        email = request.POST['email']
        address = request.POST['address']
        mobile = request.POST['mobile']

        user1.first_name = fn
        user1.last_name = ln
        user1.email = email
        prof.address = address
        prof.mobile = mobile
        user1.save()
        prof.save()
        error = True
        return redirect('customer-details')

    d = {'user1': user1, 'error': error}
    return  render(request, 'gas/editcustomers.html', locals())


@login_required(login_url="admin_login")
def deletecustomers(request, user):
    user_to_delete = User.objects.get(username=user)
    user_to_delete.delete()
    return redirect('customer-details')



@login_required(login_url="admin_login")
def everyOrders(request):
    # Get query parameters for order date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Filter orders based on order date range
    orders = Orders.objects.all()
    if start_date and end_date:
        # Convert strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        # Filter orders within the date range
        orders = orders.filter(order_date__range=[start_date, end_date])
    
    return render(request, 'gas/everyorders.html', {'orders': orders})




@login_required(login_url="admin_login")
def view_products(request):
    products = Product.objects.all()
    return render(request, 'gas/view_products.html', {'products': products})

@login_required(login_url="admin_login")
def editproduct(request):
    products = Product.objects.get()
    error = False
    if request.method == 'POST':
        price = request.POST['price']
        quantity = request.POST['quantity']
        subsidy = request.POST['subsidy']

        products.price = price
        products.quantity = quantity
        products.subsidy = subsidy
        products.save()
        error = True
        return redirect('view_products')

    d = {'products': products, 'error': error}
    return  render(request, 'gas/editproduct.html', locals())


@login_required(login_url="my-login")
def booking(request):
    error = ""
    products = Product.objects.get()  # Fetch all products
    product_id = products.Gid
    user = request.user
    paymode=""
    order=""
    current_date = date.today().day
    date1=date.today()-timedelta(days=(current_date-1))
    last_month_orders = Orders.objects.filter(User=user,order_date__gte=date1).count()

    last=date.today()-timedelta(days=14)
    lastorder=Orders.objects.filter(User=user,order_date__gte=last).count()
        # Check if the user has booked any order in the last month
        
    if request.method == 'POST':
        error = "yes"
        if lastorder > 0 :
            error="yes"
        else:
            quantity = 1
            paymode = request.POST.get('paymode')
            

            if quantity > products.quantity:
                return HttpResponse('Quantity exceeds available stock.')
            

            total_amount = calculate_total_amount(products.price, quantity,last_month_orders,products.subsidy)
            
            order = Orders.objects.create(User=user, Gid=products, quantity=quantity,
                                        amount=total_amount, order_status='Ordered Succesfully',
                                        order_date=date.today(), pay_mode=paymode, pay_status='Not Paid')
            order.save()
            if paymode=='cashondelivery':
                qty=products.quantity
                p=Product.objects.filter().update(quantity=qty-quantity)
                
            error = "no"

    return render(request, 'gas/booking.html', {'products': products,'order':order, 'error': error,'last_month_orders':last_month_orders,'paymode':paymode,'lastorder':lastorder})

def calculate_total_amount(price, quantity,last_month_orders,subsidy):
    if last_month_orders==0:
        total_amount = price * quantity
        total_amount -= (total_amount * (subsidy / 100))  # Apply subsidy reduction
        return total_amount
    else:
        total_amount = price * quantity  #no subsidy 
        return total_amount

@login_required(login_url="my-login")
def payment(request,id):
    error=""
    orders = Orders.objects.get(id=id)
    prod=Product.objects.get()
    if request.method == 'POST':
        error="yes"
        quantity=orders.quantity
        qty=prod.quantity
        p=Product.objects.filter().update(quantity=qty-quantity)
        o=Orders.objects.filter(id=id).update( pay_status='Paid')
        error="no"
    return render(request, 'gas/payment.html', locals())


@login_required(login_url="my-login")
def invoice(request, id):
    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    
    # Set fonts and sizes
    c.setFont("Helvetica-Bold", 16)
    # Draw "INVOICE" at the center of the first line
    c.drawCentredString(4.25 * inch, .5 * inch, "INVOICE")
    
    try:
        # Get the order with the given ID
        product = Product.objects.get()
        order = Orders.objects.get(id=id)
        user_profile = UserProfile.objects.get(User=order.User)
        
        # Add user details
        c.setFont("Helvetica", 12)
        # Draw user details on the left part of the second line
        c.drawString(inch, 1.5 * inch, f"To ,  ")
        # Draw user address on the left part of the third line
        c.drawString(inch, 1.7 * inch, f"      {order.User.first_name} {order.User.last_name}")
        c.drawString(inch, 1.9 * inch, f"      {user_profile.address}")
        
        # Add vendor details
        # Draw vendor address on the left part of the fourth line
        c.drawString(inch, 2.3 * inch, "From , ")
        c.drawString(inch, 2.5 * inch, "      Indane Gas Booking System")
        c.drawString(inch, 2.7 * inch, "      Kottaramattom P.O , Pala")
        
        # Add invoice number
        # Draw invoice number on the left part of the fifth line
        c.drawString(inch, 3 * inch, f"Invoice Number: {order.id}")
        
        # Add table headers
        # Draw table headers starting from the left part of the seventh line
        # Set fonts and sizes for the table headers
        c.setFont("Helvetica-Bold", 13)
        # Draw horizontal line above the table headers
        c.drawString(inch, 3.2 * inch, "--------------------------------------------------------------------------------------------------------------")
        # Draw table headers
        c.drawString(1.2 * inch, 3.3 * inch, "Quantity")
        c.drawString(3.0 * inch, 3.3 * inch, "Amount per Unit")
        c.drawString(5.5 * inch, 3.3 * inch, "Total Amount")
        # Draw horizontal line below the table headers
        c.drawString(inch, 3.4 * inch, "--------------------------------------------------------------------------------------------------------------")

        # Draw vertical lines to separate the col

        # Set fonts and sizes for the table data
        c.setFont("Helvetica", 12)
        # Draw table data
        c.drawString(1.5 * inch, 3.5 * inch, f"{order.quantity}")
        c.drawString(3.5 * inch, 3.5 * inch, f"{order.Gid.price}")
        c.drawString(5.6 * inch, 3.5 * inch, f"{order.amount}")
        if product.price > order.amount :
            c.drawString(5.6 * inch, 3.68 * inch, "(Subsidy)")

        
        # Add authorized signatory
        # Draw authorized signatory on the right bottom part of the page
        c.drawString(5 * inch, 6 * inch, "Paid")
        c.drawString(5 * inch, 6.2 * inch, "Authorized Signatory")
        
        # Add digitally valid text
        # Draw digitally valid text just below the authorized signatory
        c.drawString(5 * inch, 6.4 * inch, "Digitally Valid")

        c.drawString(inch, 6.2 * inch, "Place : Pala")
        c.drawString(inch, 6.4 * inch, f"Date : {order.order_date}")
        
        # Show the page and save the canvas
        c.showPage()
        c.save()
        
        # Move the buffer pointer to the beginning
        buf.seek(0)
        
        # Return the PDF file as a response
        return FileResponse(buf, as_attachment=True, filename='invoice.pdf')
    
    except Orders.DoesNotExist:
        # Handle the case where the order with the given ID does not exist
        return HttpResponse("Order not found", status=404)




@login_required(login_url="my-login")
def view_orders(request):
    orders = Orders.objects.filter(User=request.user).all
    #deliverydate=datetime.now()+timedelta(days=4)
    return render(request, 'gas/vieworder.html', {'orders': orders})

@login_required(login_url="admin_login")
def editorders(request, id):
    error=""
    order = Orders.objects.get(id=id)

    if request.method == 'POST':
        error="yes"
        order_status = request.POST.get('orderStatus')
        pay_status = request.POST.get('payStatus')

        order.order_status = order_status
        if order_status=="Delivered Successfully":
            order.delivery_date= date.today()
        order.pay_status = pay_status
        order.save()
        error="no"

    return render(request, 'gas/editorders.html',locals())

@login_required(login_url="admin_login")
def deleteorder(request, id):
    order = Orders.objects.get(id=id)
    order.delete()
    return redirect('admindashboard')


@login_required(login_url="my-login")
def feedback_submission(request):
    if request.method == 'POST':
        user = request.user
        description = request.POST.get('description')
        feedback = Feedback(User=user, description=description)
        feedback.save()
        return redirect('dashboard')  # Redirect to dashboard or any other page after submission

    return render(request, 'gas/feedback_submission.html')


@login_required(login_url="my-login")
def view_feedback(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'gas/view_feedback.html', {'feedbacks': feedbacks})

