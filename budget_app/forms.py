from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Income, Expense, IncomeCategory, ExpenseCategory, Goal


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
    def available_mail(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Enter username',
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Enter password',
        })
    )

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'description', 'category', 'date']
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
    new_category = forms.CharField(
    max_length=100,
    required=False,
    label="New category",
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields["category"].queryset.count() == 0:
            self.fields["category"].widget = forms.HiddenInput()
            self.fields["category"].required = False
        else:
            self.fields["category"].required = False

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'category', 'date']
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
    new_category = forms.CharField(
    max_length=100, 
    required=False, 
    label="New category",
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields["category"].queryset.count() == 0:
            self.fields["category"].widget = forms.HiddenInput()
            self.fields["category"].required = False
        else:
            self.fields["category"].required = False

class IncomeCategoryForm(forms.ModelForm):
    class Meta:
        model = IncomeCategory
        fields = ['name']
        
class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name']

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description', 'target_amount']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }