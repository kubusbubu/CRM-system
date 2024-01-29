from django.contrib.auth.models import User
from django.test import TestCase
from leads.forms import LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm, CategoryForm
from leads.models import Agent, Category, Lead
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory

User = get_user_model()

class TestLeadForms(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.agent = Agent.objects.create(user=self.user, organization=self.user.userprofile)

    def test_lead_model_form_valid_data(self):
        form = LeadModelForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'agent': self.agent.id,
            'organization': self.user.userprofile,
            'address': '123 Street',
            'what_is_your_current_occupation': 'Engineer',
            'email': 'john@example.com',
            'phone_number': '1234567890'
        })
        self.assertTrue(form.is_valid())

    def test_lead_model_form_invalid_data(self):
        form = LeadModelForm(data={
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_custom_user_creation_form_valid_data(self):
        form = CustomUserCreationForm(data={'username': 'testuser2', 'password1': 'testpassword', 'password2': 'testpassword'})
        self.assertTrue(form.is_valid(), form.errors)


    def test_custom_user_creation_form_invalid_data(self):
        form = CustomUserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_assign_agent_form(self):
        request = RequestFactory().get('/')
        request.user = self.user
        form = AssignAgentForm(data={}, request=request)
        self.assertTrue(form.fields["agent"].queryset.exists())

    def test_lead_category_update_form(self):
        lead = Lead.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            agent=self.agent,
            organization=self.user.userprofile # Provide the organization
        )        
        category = Category.objects.create(name='Test Category', organization=self.user.userprofile)
        form = LeadCategoryUpdateForm(instance=lead, data={'category': category.id})
        self.assertTrue(form.is_valid())

    def test_category_form(self):
        form = CategoryForm(data={'name': 'Test Category'})
        self.assertTrue(form.is_valid())

