from django.shortcuts import render
from django.views import View
from .models import User, Book, Order

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
import uuid

# Create your views here.
class AccountSignupApiView(View):
    def get(self, request):
        return render(request, "account/signup.html")

    def post(self,request):
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        address=request.POST['address']
        usertype=request.POST['usertype']
        countery=request.POST['country']
        state=request.POST['state']
        zip=request.POST['zip']
        try:
            user = User.objects.filter(email=email).exists()
            if pass1 != pass2:
                messages.error(request, 'Password do no match')
                return redirect('account-signup')
            myuser = User.objects.create_user(username, email, pass1, is_staff=True)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.email=email
            myuser.address=address
            myuser.pincode=zip
            myuser.state=state
            myuser.country=countery
            myuser.user_type=usertype
            myuser.save()
            return redirect('account-login')
        except :
            messages.error(request, "Email is already exits")
            return redirect('account-signup')



class AccountLoginApiView(View):
    def get(self,request):
        return render(request, "account/login.html")

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = authenticate(email=email, password=password)
            login(request, user)
            if user.is_authenticated and user.user_type=="SELLER":
                return redirect("seller-home")
            if user.is_authenticated and user.user_type=="CUSTOMER":
                return redirect("custom-home")

        except:
            messages.success(request, "Invaild  Credentials, Please try again")
            return redirect("account-login")


def handlelogout(request):
    logout(request)
    messages.success(request,"Successfuly Logged  out" )
    return redirect('account-login')


@method_decorator(login_required(login_url='/login'), name='dispatch')
class CustomerHomepage(ListView):
    model = Book
    template_name = "list-blog.html"
    def get(self, request):
        user=request.user
        if user.user_type=="CUSTOMER":
            if "search" in request.GET:
                search=request.GET['search']
                blog=self.model.objects.all().filter(title=search)
                return render(request, self.template_name, {"object_list": blog})
            Blog=self.model.objects.all()
            return render(request, self.template_name, {"object_list": Blog})
        else:
            return redirect("account-login")

class Orderdeliver(View):
    def get (self, request, id):
        try:
            user=request.user
            if request.user.is_authenticated and request.user.user_type=="CUSTOMER":
                print(id)
                order=Order(user=user, book=Book(id=id), address=user.address, country=user.country,
                              state=user.state, pincode=user.pincode)
                order.save()
                messages.success(request, "Successfuly Order deliver in you address")
                return redirect("order/list")
        except:
            return redirect("account-login")

class Orderlist(View):
   def get(self, request):
        if request.user.is_authenticated and request.user.user_type == "CUSTOMER":
            user=request.user
            orders=user.order.all()

            return render(request, "order.html", {"orders":orders})
        return redirect("account-login")

@method_decorator(login_required(login_url='/login'), name='dispatch')
class sellerhome(View):
    def get(self, request):
        if request.user.user_type=="SELLER" and request.user.is_authenticated :
            user=request.user
            book=user.book.all()
            return render(request, "account/seller-home.html", {"object_list": book})
        else:
            return redirect("account-login")

class addbook(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.user_type == "SELLER":
            return render(request, "add-book.html")
        else:
            return redirect("account-login")
    def post(self,request):
        try:
            if request.user.is_authenticated and request.user.user_type == "SELLER" :
                name = request.POST['name']
                title = request.POST['title']
                description = request.POST['description']
                price = request.POST['price']
                image = request.FILES['image']
                book=Book(name=name, title=title, descriptions=description, prize=price, image=image, user=request.user)
                book.save()
                return redirect("seller-home")

        except:
            return redirect("account-login")

class deletebook(View):
    def get(self,request, id):
        try:
            if request.user.is_authenticated \
                    and request.user.user_type == "SELLER" \
                    and Book.objects.filter(id=id, user=request.user).count()>0:
                book=Book.objects.filter(id=id, user=request.user)
                book.delete()
                return redirect("seller-home")
        except:
            return redirect("account-login")



class update(View):
    def get(self, request, id):
        if request.user.is_authenticated \
                    and request.user.user_type == "SELLER" \
                    and Book.objects.filter(id=id, user=request.user).count() >0:
                book = Book.objects.filter(id=id, user=request.user)
                return render(request, "updatebook.html" , {"booklist":book})
        return redirect("account-login")


    def post(self, request, id):
        if request.user.is_authenticated \
                    and request.user.user_type == "SELLER" \
                and Book.objects.filter(id=id, user=request.user).count() > 0:
            name=request.POST['name']
            title = request.POST['title']
            description = request.POST['description']
            price = request.POST['price']
            Book.objects.filter(id=id, user=request.user).update(name=name, title=title, descriptions=description,
                                                                 prize=price, user=request.user)
            return redirect("seller-home")
        else:
            return redirect("account-login")

def sellerorderlist(request):
    if request.user.is_authenticated and request.user.user_type == "SELLER":
        order=Order.objects.all()
        print(order)
        return render(request, "orderlist.html", {"orders": order})

    else:
        return  redirect("account-login")










