from django.urls import path
from expenses import views

urlpatterns=[
    path('',views.ExpenseList.as_view(),name='expenses'),
    path('<int:id>',views.ExpenseDetailApiView.as_view(),name='expense'),
    # path('login/',views.LoginApiView.as_view(),name='login'),

]