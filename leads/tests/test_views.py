from django.test import TestCase
from django.shortcuts import reverse
from leads.models import Lead, User, Agent


class LeadListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser', password='12345', email='test@test'
        )

        self.client.login(username='testuser', password='12345')

        # Create two leads
        self.lead1 = Lead.objects.create(
            prospect_id="1" , first_name='John', last_name='Doe', email='john@example.com',
            organization=self.user.userprofile,
        )
        self.lead2 = Lead.objects.create(
            prospect_id="2", first_name='Jane', last_name='Doe', email='jane@example.com',
            organization=self.user.userprofile, 
        )

        # Create an agent
        self.agent = Agent.objects.create(
            user=self.user,
            organization=self.user.userprofile
            # Add any other required fields for the agent
        )
        # Assign the agent to one of the leads
        self.lead1.agent = self.agent
        self.lead1.save()


    def test_unassigned_lead_list_authenticated_user(self):
        response = self.client.get(reverse("leads:lead-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "leads/lead_list.html")
        context = response.context
        self.assertTrue('leads' in context)
        leads = context['unassigned_leads']
        self.assertEqual(len(leads), 1)
    
    def test_assigned_lead_list_authenticated_user(self):
        response = self.client.get(reverse("leads:lead-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "leads/lead_list.html")
        context = response.context
        self.assertTrue('leads' in context)
        leads = context['leads']
        self.assertEqual(len(leads), 1)
    
    def test_lead_detail_page_access(self):
        response = self.client.get(reverse("leads:lead-detail", args=[self.lead1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "leads/lead_detail.html")

    def test_lead_update_page_access(self):
        response = self.client.get(reverse("leads:lead-update", args=[self.lead1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "leads/lead_update.html")
    
    def test_lead_deletion(self):
        lead = Lead.objects.create(
            prospect_id="3", first_name='John', last_name='Doe', email='john@example.com',
            organization=self.user.userprofile,
        )
        response = self.client.post(reverse("leads:lead-delete", args=[lead.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Lead.objects.filter(id=lead.id).exists())
        
    def test_lead_assignment_view(self):
        response = self.client.post(reverse("leads:assign-agent", args=[self.lead2.id]), {'agent': self.agent.id})
        self.assertEqual(response.status_code, 302)
        self.lead2.refresh_from_db()
        self.assertEqual(self.lead2.agent, self.agent)

    def test_lead_create_page_access(self):
        response = self.client.get(reverse("leads:lead-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "leads/lead_create.html")

