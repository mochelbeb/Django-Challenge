from .forms import ReceiptForm
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Receipt

class ReceiptModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create_user(username='testuser', password='12345')
        user = User.objects.get(id=1)
        Receipt.objects.create(user=user, store_name='Test Store', date_of_purchase='2023-01-01', item_list='Item1, Item2', total_amount=1000.00)

    def test_receipt_content(self):
        receipt = Receipt.objects.get(id=1)
        self.assertEqual(receipt.store_name, 'Test Store')
        self.assertEqual(receipt.user.username, 'testuser')

class ReceiptListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        test_user = User.objects.create_user(username='testuser', password='12345')

        number_of_receipts = 10
        for receipt_num in range(number_of_receipts):
            Receipt.objects.create(user=test_user, store_name=f'Store {receipt_num}', date_of_purchase='2023-01-01', item_list=f'Item {receipt_num}', total_amount=100.00)

    def test_view_url_exists_at_desired_location(self):

        login_successful = self.client.login(username='testuser', password='12345')
        self.assertTrue(login_successful)  # Make 
    
        response = self.client.get('/receipts/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):

        login_successful = self.client.login(username='testuser', password='12345')
        self.assertTrue(login_successful)
    
        response = self.client.get(reverse('receipt-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'receipts/receipt_list.html')

class ReceiptFormTest(TestCase):

    def test_ReceiptForm_valid(self):
        form_data = {'store_name': 'Test Store', 'date_of_purchase': '2023-01-01', 'item_list': 'Item1, Item2', 'total_amount': 100.00}
        form = ReceiptForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_ReceiptForm_invalid(self):
        form_data = {'store_name': '', 'date_of_purchase': '2023-01-01', 'item_list': 'Item1, Item2', 'total_amount': 100.00}
        form = ReceiptForm(data=form_data)
        self.assertFalse(form.is_valid())

