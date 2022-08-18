from django.urls import path
from userstats import views

urlpatterns=[
    path('expense_category_data',views.ExpenseSummaryStats.as_view(),name='expense-category-summary'),
    path('income_source_data',views.IncomeSourcesStats.as_view(),name='income-source-summary'),

]