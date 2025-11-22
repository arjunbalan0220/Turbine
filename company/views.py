import razorpay
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from .models import Company, Vehicle ,SPARE, Order, Cart , ProductRating
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from razorpay.errors import BadRequestError, ServerError
from logp.models import RegistrationForm 
from django.contrib.auth import authenticate, login



def index(request):
    return render(request,"index.html")


def spare(request):
    if request.method == 'POST':
        veh=request.POST.get('id')
        spr = SPARE.objects.filter(spare_id=veh)
        return render(request,"spare.html", {'spr': spr})
    return render(request,"spare.html", {'spr': []})

@login_required(login_url='signin')
def create_order(request, spare_id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in first.")
        return redirect("log")
   
    spare = get_object_or_404(SPARE, spare_id=spare_id)

    user = request.user
    user = get_object_or_404(RegistrationForm, email=request.user.email)

    
    order = Order.objects.create(product=spare, user=user, total_price=spare.price)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment_data = {
        "amount": int(order.total_price * 100),
        "currency": "INR",
        "receipt": str(order.order_id),
        "payment_capture": 1
    }

    try:
        payment = client.order.create(payment_data)
        if 'id' in payment:
            order.payment_id = payment['id']
            order.save()
        else:
            messages.error(request, "Payment processing failed. Please try again.")
            return redirect("spare")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("spare")

    context = {
        "order": order,
        "user": user,
        "spare": spare,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "payment_id": payment['id'],
    }
    return render(request, "create_order.html", context)


def company_login(request):
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        password = request.POST.get("password")

        print(f"Attempting login with Company ID: {company_id}")
        print(f"Entered Password: {password}")

        try:
            comp = Company.objects.get(company_id=company_id)
            print(f"Company found: {comp.company_name}")
            print(f"Stored Password Hash: {comp.password}")

            
            if check_password(password, comp.password):
                print("Password check successful")
                request.session['company_id'] = comp.company_id
                return redirect('company_home')
            else:
                print("Password check failed")
                messages.error(request, "Invalid Company ID or Password")
        except Company.DoesNotExist:
            print(f"No company found with ID: {company_id}")
            messages.error(request, "Company does not exist")

    return render(request, 'company_login.html')

def company_logout(request):
    request.session.flush()  
    return redirect('company_login')


def company_home(request):
    company_id = request.session.get('company_id')
    
    if not company_id:
        messages.error(request, "Please log in first")
        return redirect('company_login')

    try:
        comp = Company.objects.get(company_id=company_id)
    except Company.DoesNotExist:
        messages.error(request, "Company does not exist")
        return redirect('company_login')

    vehicles = Vehicle.objects.filter(company=comp)
    return render(request, 'company_home.html', {'comp': comp, 'vehicles': vehicles})



def company_add(request):
    company_id = request.session.get('company_id')
    
    if not company_id:
        messages.error(request, "Please log in first")
        return redirect('company_login')

    try:
        comp = Company.objects.get(company_id=company_id)
    except Company.DoesNotExist:
        messages.error(request, "Company does not exist")
        return redirect('company_login')

    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle_id")  
        vehicle_name = request.POST.get("vehicle_name")  
        wheel = request.POST.get("wheel")
        year = request.POST.get("year")  
        Fuel = request.POST.get("Fuel")
        Type = request.POST.get("Type")
        image = request.FILES.get("image")

        Vehicle.objects.create(
            Vehicle_id=vehicle_id,  
            company=comp,  
            company_name=comp.company_name,  
            Vehicle_name=vehicle_name,  
            Wheel=wheel,  
            Year=year,  
            Fuel=Fuel,  
            Type=Type,
            image=image
        )

        messages.success(request, "Product added successfully")
        return redirect('company_home')

    return render(request, 'company_add.html')



def company_spare(request, vehicle_id):
    company_id = request.session.get('company_id')

    if not company_id:
        messages.error(request, "Please log in first")
        return redirect('company_login')

    try:
        company = Company.objects.get(company_id=company_id)
        vehicle = Vehicle.objects.get(Vehicle_id=vehicle_id, company=company)
    except (Company.DoesNotExist, Vehicle.DoesNotExist):
        messages.error(request, "Invalid request")
        return redirect('company_home')

    if request.method == "POST":
        spare_ids = request.POST.getlist('spare_id[]')
        spare_names = request.POST.getlist('spare_name[]')
        type = request.POST.getlist('typ[]')
        prices = request.POST.getlist('price[]')
        descriptions = request.POST.getlist('description[]')
        image = request.FILES.getlist('spare_image[]')

        for i in range(len(spare_ids)):
            SPARE.objects.create(
                spare_id=spare_ids[i],
                vehicle=vehicle,
                company=company,
                spare_name=spare_names[i],
                typ=type[i],
                price=prices[i],
                description=descriptions[i],
                image=image[i] if i < len(image) else None
            )

        messages.success(request, "Spare parts added successfully!")
        return redirect('company_home')

    return render(request, 'company_spare.html', {'vehicle': vehicle})


def add_stock(request, spare_id):
    spare = get_object_or_404(SPARE, pk=spare_id)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 0))
            if quantity > 0:
                spare.stock += quantity
                spare.save()
                messages.success(request, f"Successfully added {quantity} units to stock.")
                return redirect('individual_spare', vehicle_id=spare.vehicle.Vehicle_id)
            else:
                messages.error(request, "Please enter a positive number.")
        except (ValueError, TypeError):
            messages.error(request, "Invalid input. Please enter a number.")

    return render(request, 'add_stock.html', {'spare': spare})
    
def individual_spare(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    spares = SPARE.objects.filter(vehicle=vehicle)
    return render(request, 'individual_spare.html', {'vehicle': vehicle, 'spares': spares})

def delete_spare(request, spare_id):
    spare = get_object_or_404(SPARE, pk=spare_id)
    vehicle_id = spare.vehicle  
    if request.method == 'POST':
        spare.delete()
    return redirect('individual_spare', vehicle_id=vehicle_id)






#Vehicle
def bike(request):
    dict_bkview={
        'vehicle': Vehicle.objects.all()
    }
    return render(request,"bike.html",dict_bkview)
def car(request):
    dict_bkview={
        'vehicle': Vehicle.objects.all()
    }
    return render(request,"car.html",dict_bkview)
def company_sep(request):
    if request.method == "POST":
        comp_id = request.POST.get("comp_id")  
        vehicles = Vehicle.objects.filter(company_id=comp_id)  
        return render(request, "company_sep.html", {"vehicles": vehicles, "comp_id": comp_id})
    
    return render(request, "company_sep.html", {"vehicles": []})


def spareview(request):
    if request.method == 'POST':
        veh=request.POST.get('id')
        spr = SPARE.objects.filter(vehicle=veh)
        return render(request,"spareview.html", {'spr': spr})
    return render(request,"spareview.html", {'spr': []})



#buying








def payment_cancel(request):
    return render(request, 'payment_cancel.html')

from django.http import HttpResponse

@login_required(login_url='log')
def cod_payment(request, spare_id):
    print(f"COD Payment View Reached with spare_id: {spare_id}")  

    
    spare = get_object_or_404(SPARE, spare_id=spare_id)

    if request.method == "GET":
        print("GET request - Showing COD confirmation page")

       
        temp_order = {
            "total_price": spare.price,
            "payment_method": "COD",
        }

        return render(request, "cod_payment.html", {"spare": spare, "order": temp_order})

    if request.method == "POST":
        print("POST request received - Creating COD Order")

        
        order = Order.objects.create(
            user=request.user,
            product=spare,
            total_price=spare.price,
            payment_method="COD",
            status="Pending"
        )
        order.save()
        print(f"Order {order.order_id} Created Successfully!")

        return redirect("order_success")


    return render(request, "cod_payment.html", {"spare": spare})

def order_success(request):
    return render(request, "order_success.html")


def log(request):
    spare_id = request.GET.get("spare_id")  

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        spare_id = request.POST.get("spare_id")  

        user = authenticate(request, email=email, password=password)  

        if user is not None:
            login(request, user)  
            messages.success(request, "Login successful!")

            if spare_id:
                return redirect("create_order", spare_id=spare_id)  

            return redirect("spare")
        else:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, "logiin.html", {"spare_id": spare_id})

def add_cart1(request, spare_id):
    if request.method == "POST":
        email = request.POST.get("email")
        print(f"Received Email: {email}")  
        fname = request.POST.get("fname")

        if not email:
            print("Email missing!")
            messages.error(request, "Email is required.")
            return render(request, "add_cart1.html", {"spare_id": spare_id})

        user = RegistrationForm.objects.filter(email=email).first()
        print(f"User Found: {user}")  

        if not user:
            print("User not found!")
            messages.error(request, "Email not found. Please register first.")
            return render(request, "add_cart1.html", {"spare_id": spare_id})

        spare = get_object_or_404(SPARE, spare_id=spare_id)
        print(f"Spare Found: {spare}")  

        if Cart.objects.filter(user=user, spare=spare).exists():
            print("Item already in cart!")
            messages.warning(request, "This item is already in your cart.")
            return redirect("cart_view")

        cart_item = Cart(spare=spare, user=user)
        cart_item.save()
        print("Item added successfully!")
        
        request.session["user_email"] = email

        messages.success(request, "Item added to cart successfully!")
        return redirect("cart_view")

    return render(request, "add_cart1.html", {"spare_id": spare_id})

def cart_view(request):
    
    user_email = request.session.get("user_email")

    if not user_email:
        messages.error(request, "User email not found! Please add an item to the cart first.")
        return redirect('add_cart1', spare_id="default_spare_id")

    user = RegistrationForm.objects.filter(email=user_email).first()
    if not user:
        messages.error(request, "User not found!")
        return redirect('add_cart1', spare_id="default_spare_id")

    cart_items = Cart.objects.filter(user=user)

    if not cart_items:
        messages.info(request, "Your cart is empty! 🛒")

    return render(request, "cart_view.html", {"cart_items": cart_items})

def cart_viewprofile(request):
    email = request.session.get("email")  

    if not email:
        messages.error(request, "Please log in first")
        return redirect("signin")

    try:
        user = RegistrationForm.objects.get(email=email) 
        cart_items = Cart.objects.filter(user=user)  
    except RegistrationForm.DoesNotExist:
        messages.error(request, "User does not exist")
        return redirect("signin")

    return render(request, "cart_viewprofile.html", {"cart_items": cart_items, "user": user})


def remove_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, cart_id=cart_id)
    cart_item.delete()
    messages.success(request, "Item removed from cart successfully!")
    return redirect("cart_view")

def orders(request):
    email = request.session.get("email")  

    if not email:
        messages.error(request, "Please log in first")
        return redirect("signin")

    try:
        user = RegistrationForm.objects.get(email=email)  
        order_items = Order.objects.filter(user=user)  
    except RegistrationForm.DoesNotExist:
        messages.error(request, "User does not exist")
        return redirect("signin")

    return render(request, "orders.html", {"order_items": order_items, "user": user})

def rate_product(request, order_id):
    if request.method == "POST":
        email = request.session.get("email")
        if not email:
            messages.error(request, "Please log in to rate a product.")
            return redirect("signin")

        user = RegistrationForm.objects.get(email=email)
        order = Order.objects.get(order_id=order_id)

        rating = int(request.POST.get("rating", 0))
        review = request.POST.get("review", "").strip()

        if rating < 1 or rating > 5:
            messages.error(request, "Rating must be between 1 and 5.")
            return redirect("orders")

        ProductRating.objects.update_or_create(
            user=user,
            product=order.product,
            order=order,
            defaults={"rating": rating, "review": review}
        )

        messages.success(request, "Thank you for rating the product!")
        return redirect("orders")


def view_reviews(request, spare_id):
    product = get_object_or_404(SPARE, spare_id=spare_id)
    reviews = ProductRating.objects.filter(product=product)

    return render(request, 'view_reviews.html', {
        'product': product,
        'reviews': reviews
    })



from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='signin')
def create_bulk_order(request):
    user = request.user  

    
    cart_items = Cart.objects.filter(user=user)

    if not cart_items:
        messages.info(request, "Your cart is empty!")
        return redirect("cart_view")

   
    total_price = sum(item.spare.price for item in cart_items)

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }

    return render(request, "create_bulk_order.html", context)







from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def payment_success_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            
            name = data.get("name")
            email = data.get("email")
            contact = data.get("contact")
            amount = data.get("amount")
            razorpay_payment_id = data.get("razorpay_payment_id")
            spare_name= data.get("spare_name")
            
            
            
            spare = SPARE.objects.filter(spare_name=spare_name).first()
            if not spare:
                return JsonResponse({"status": "error", "message": "Spare part not found"}, status=404)

           
            if spare.stock is not None and spare.stock > 0:
                spare.stock -= 1
                spare.save()
            else:
                return JsonResponse({"status": "error", "message": "Out of stock"}, status=400)



            
            request.session['payment_info'] = {
                "name": name,
                "email": email,
                "contact": contact,
                "amount": amount,
                "razorpay_payment_id": razorpay_payment_id,
                "spare_name": spare_name

            }

            return JsonResponse({"status": "success"})
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "invalid request"}, status=405)




import io
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
import os

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths for xhtml2pdf.
    """
    if uri.startswith('/static/'):
        path = os.path.join(settings.BASE_DIR, uri[1:])  # removes leading "/"
    else:
        path = os.path.join(settings.STATIC_ROOT, uri)
    
    if not os.path.isfile(path):
        raise Exception(f"File not found: {path}")
    return path

def generate_pdf(payment_info):
    template = get_template('payment_pdf.html')
    html = template.render({'payment_info': payment_info})
    pdf_io = BytesIO()

    pisa_status = pisa.CreatePDF(
        html, dest=pdf_io, link_callback=link_callback
    )

    if pisa_status.err:
        raise Exception("Error generating PDF.")

    pdf_io.seek(0)
    return pdf_io

def send_payment_confirmation_email(payment_info, user_email):
    subject = "Payment Confirmation"
    message = "Thank you for your purchase. Please find the attached invoice."

    
    pdf_io = generate_pdf(payment_info)

    
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[user_email],  
    )

    
    print(pdf_io.getvalue())  

    
    email.attach('payment_invoice.pdf', pdf_io.read(), 'application/pdf')

    
    try:
        email.send()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def payment_success_page(request):
    payment_info = request.session.get('payment_info', {})
    
    
    user_email = payment_info.get('email')
    if user_email:
        send_payment_confirmation_email(payment_info, user_email)
    
    return render(request, 'payment_success_page.html', {"payment_info": payment_info})
