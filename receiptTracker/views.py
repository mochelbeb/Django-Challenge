from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views import generic
from .models import Receipt
from .forms import ReceiptForm
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url='/login')  # Replace '/login/' with your login route
def home_redirect(request):
    return redirect('receipt-list') 

class ReceiptListView(LoginRequiredMixin, generic.ListView):
    model = Receipt
    context_object_name = 'receipts'
    template_name = 'receipts/receipt_list.html'

    def get_queryset(self):
        return Receipt.objects.filter(user=self.request.user)

class ReceiptDetailView(LoginRequiredMixin, generic.DetailView):
    model = Receipt
    template_name = 'receipts/receipt_detail.html'

class ReceiptCreateView(LoginRequiredMixin, generic.CreateView):
    model = Receipt
    form_class = ReceiptForm
    template_name = 'receipts/receipt_form.html'
    success_url = reverse_lazy('receipt-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReceiptUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Receipt
    form_class = ReceiptForm
    template_name = 'receipts/receipt_form.html'
    success_url = reverse_lazy('receipt-list')  
    
    def form_valid(self, form):
        return super().form_valid(form)
    





@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Please provide both username and password.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'This username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        return Response({'message': 'User created successfully.', 'username': user.username}, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect to a specific page upon successful login
            return redirect('profile')  # Change 'dashboard' to your desired URL name
        else:
            # Handle invalid login (e.g., show error message)
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    else:
        return render(request, 'login.html')
    

@login_required
def profile_view(request):
    # Retrieve user information or any additional profile data
    user = request.user
    context = {
        'user': user,
        # Add any additional profile data you want to display
    }
    return render(request, 'profile.html', context)


def confirm_logout_view(request):
    return render(request, 'logout.html')