from django.urls import path
from.views import *

urlpatterns = [
    path("order/<str:id>" , Orderdeliver.as_view(), name="order"),
    path("signup", AccountSignupApiView.as_view(), name="account-signup"),
    path("login", AccountLoginApiView.as_view(), name="account-login"),
    path("logout", handlelogout, name="logout"),
    path("", CustomerHomepage.as_view(), name= "custom-home"),
    path("list-order", Orderlist.as_view(), name="order/list"),
    path("seller/add-book", addbook.as_view(), name="add-book"),
    path("sellerhome", sellerhome.as_view(), name="seller-home"),
    path("delete/<str:id>", deletebook.as_view(), name="delete-book"),
    path("update/<str:id>", update.as_view(), name="update-book1"),
    path("sellerorderlist",sellerorderlist, name="seller-order-list" )
]