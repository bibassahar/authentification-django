from django.urls import path
from income import views

urlpatterns=[
    path('',views.IncomeList.as_view(),name='income'),
    path('<int:id>',views.IncomeDetailApiView.as_view(),name='income'),
    # path('login/',views.LoginApiView.as_view(),name='login'),

]