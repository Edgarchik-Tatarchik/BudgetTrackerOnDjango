from django.urls import path
from .views import (
    HomepageView, SignUpView, CustomLoginView, CustomLogoutView, complete_goal,
    password_change_view,incomes_view, expenses_view,goals_view,revenue_view,
    calculator_view,delete_income,delete_expense
)

app_name = 'budget_app'

urlpatterns = [
    path('', HomepageView, name='index'),
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password_change/', password_change_view, name='password_change'),
    path('incomes/', incomes_view, name='incomes'),
    path('incomes/delete/<int:income_id>/', delete_income, name='delete_income'),
    path('expenses/', expenses_view, name='expenses'),
    path('expenses/delete/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('goals/', goals_view, name='goals'),
    path('goals/complete/<int:goal_id>/', complete_goal, name='complete_goal'),
    path('revenue/', revenue_view, name='revenue'),
    path('calculator/', calculator_view, name='calculator'),
]