from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from .models import CustomUser,Income, Expense, IncomeCategory, ExpenseCategory, Goal
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .forms import RegisterForm, LoginForm, IncomeForm, ExpenseForm, GoalForm
from django.db.models import Sum
from django.contrib import messages
import json
from django.core.serializers.json import DjangoJSONEncoder



class SignUpView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('budget_app:index')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)
       
class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    redirect_authenticated_user = True 
    def get_success_url(self):
        redirect_to = self.request.POST.get('next') or self.request.GET.get('next')
        if redirect_to:
            return redirect_to
        return reverse_lazy('budget_app:index')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('budget_app:index')

def password_change_view(request):
    message = ''
    form = None

    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            user = None
            message = 'User not found'

        if user:
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('budget_app:login')
    else:
        form = None

    return render(request, 'password_change.html', {'form': form, 'message': message})

def incomes_view(request):
    categories = IncomeCategory.objects.filter(user=request.user)
    message = ''

    if request.method == 'POST':
        form = IncomeForm(request.POST)

        if form.is_valid():
            selected_category = form.cleaned_data.get("category")
            new_category_name = form.cleaned_data.get("new_category")

            if new_category_name:
                selected_category, created = IncomeCategory.objects.get_or_create(name=new_category_name,user=request.user)

            income = form.save(commit=False)
            income.category = selected_category
            income.user = request.user
            income.save()

            messages.success(request, "Income added successfully!")
            return redirect("budget_app:incomes")

    else:
        form = IncomeForm()

    incomes = Income.objects.filter(user=request.user).order_by("-date")
    return render(request, 'incomes.html', {
        'form': form,
        "incomes": incomes,
        "categories": categories,
    })


def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id)
    income.delete()
    messages.success(request, "Income deleted!")
    return redirect('budget_app:incomes')


def expenses_view(request):
    categories = ExpenseCategory.objects.filter(user=request.user)
    message = ''

    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            selected_category = form.cleaned_data.get("category")
            new_category_name = form.cleaned_data.get("new_category")

            if new_category_name:
                selected_category, created = ExpenseCategory.objects.get_or_create(name=new_category_name, user=request.user)

            expense = form.save(commit=False)
            expense.category = selected_category
            expense.user = request.user
            expense.save()

            messages.success(request, "Expense added successfully!")
            return redirect("budget_app:expenses")

    else:
        form = ExpenseForm()

    
    expenses = Expense.objects.filter(user=request.user).order_by("-date")
    return render(request, 'expenses.html', {
        'form': form,
        "expenses": expenses,
        "categories": categories,
    })


def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    messages.success(request, "Expense deleted!")
    return redirect('budget_app:expenses')


@login_required
def HomepageView(request):

    income_categories = IncomeCategory.objects.filter(user=request.user)
    expense_categories = ExpenseCategory.objects.filter(user=request.user)

    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)


    total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0
    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0
    
    income_progress = []
    for category in income_categories:
        category_sum = incomes.filter(category=category).aggregate(total=Sum('amount'))['total'] or 0
        percent = (category_sum / total_income * 100) if total_income else 0
        income_progress.append({
            'category': category.name,
            'percent': round(percent, 2),
            'sum': category_sum
        })

    

    expense_progress = []
    for category in expense_categories:
        category_sum = expenses.filter(category=category).aggregate(total=Sum('amount'))['total'] or 0
        percent = (category_sum / total_expense * 100) if total_expense else 0
        expense_progress.append({
            'category': category.name,
            'percent': round(percent, 2),
            'sum': category_sum
        })
        
    goals = Goal.objects.filter(user=request.user)
    goals_data = []
    for goal in goals:
        current_amount = Income.objects.aggregate(total=Sum('amount'))['total'] or 0
        progress_percent = min(round(current_amount / goal.target_amount * 100, 2), 100)
        remaining_percent = 100 - progress_percent
        goals_data.append({
            "id": goal.id,
            "title": goal.title,
            "description": goal.description,
            "target": goal.target_amount,
            "current": current_amount,
            "progress_percent": progress_percent,
            "remaining_percent": remaining_percent,
            
        })

    context = {
        "income_categories": income_categories,
        "expense_categories": expense_categories,
        "income_progress": income_progress,
        "expense_progress": expense_progress,
        "total_income": total_income,
        "total_expense": total_expense,
        "goals_data": goals_data,
    }

    return render(request, "index.html", context)

def goals_view(request):
    goals = Goal.objects.filter(user=request.user).order_by('id')

    if request.method == "POST":
        if "add_goal" in request.POST:
            form = GoalForm(request.POST)
            if form.is_valid():
                goal = form.save(commit=False)
                goal.user = request.user
                goal.save()
                messages.success(request, "Goal added successfully!")
                return redirect('budget_app:goals')
        elif "complete_goal" in request.POST:
            goal_id = request.POST.get("goal_id")
            goal = get_object_or_404(Goal, id=goal_id)
            goal.delete()
            messages.success(request, "Goal completed and removed!")
            return redirect('budget_app:goals')
    else:
        form = GoalForm()

    return render(request, "goals.html", {
        "form": form,
        "goals": goals
    })

def complete_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    goal.delete()
    messages.success(request, "Goal completed and removed!")
    return redirect('budget_app:goals')

def revenue_view(request):
    incomes_qs = Income.objects.filter(user=request.user).order_by('date')
    expenses_qs = Expense.objects.filter(user=request.user).order_by('date')

    incomes = list(incomes_qs.values('date', 'amount'))
    expenses = list(expenses_qs.values('date', 'amount'))

    context = {
        'incomes': json.dumps(incomes, cls=DjangoJSONEncoder),
        'expenses': json.dumps(expenses, cls=DjangoJSONEncoder),
    }
    return render(request, 'revenue.html', context)

def calculator_view(request):
    return render(request, 'calculator.html')