from django.test import TestCase
from django.urls import reverse
from leads.models import Agent, User

class AgentViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.client.login(username='testuser', password='12345')

        self.agent = Agent.objects.create(
            user=self.user,
            organization=self.user.userprofile
        )

    def test_agent_list_view(self):
        response = self.client.get(reverse('agents:agent-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agents/agent_list.html')

    def test_agent_create_view(self):
        response = self.client.post(reverse('agents:agent-create'), {
            'user': self.user,
            'organization': self.user.userprofile
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Agent.objects.filter(user=self.user).exists())

    def test_agent_detail_view(self):
        response = self.client.get(reverse('agents:agent-detail', args=[self.agent.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agents/agent_detail.html')

    def test_agent_update_view(self):
        response = self.client.post(reverse('agents:agent-update', args=[self.agent.id]), {
            'user': self.user,
            'organization': self.user.userprofile
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Agent.objects.filter(user=self.user).exists())

    def test_agent_delete_view(self):
        response = self.client.post(reverse('agents:agent-delete', args=[self.agent.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Agent.objects.filter(user=self.user).exists())

    def test_agent_statistics_view(self):
        response = self.client.get(reverse('agents:agent-statistics', args=[self.agent.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agents/agent_statistics.html')

    def test_update_profile_picture_view(self):
        response = self.client.post(reverse('agents:update-profile-picture', args=[self.agent.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('agents:agent-detail', args=[self.agent.id]))

