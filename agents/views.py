import random
from django.core.mail import send_mail
from django.views import generic
from django.shortcuts import reverse, redirect
from leads.models import Agent
from .forms import AgentModelForm, UserProfileUpdateForm
from .mixins import OrganisorAndLoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from leads.models import Lead, Agent



class AgentStatisticsView(View):
    template_name = 'agents/agent_statistics.html'

    def get(self, request, pk):
        agent = Agent.objects.get(pk=pk)

        categories = agent.organization.category_set.all()

        statistics = {}
        for category in categories:
            count = Lead.objects.filter(agent=agent, category=category).count()
            statistics[category.name] = count

        context = {
            'agent': agent,
            'statistics': statistics,
        }

        return render(request, self.template_name, context)
    

class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
    
class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organization = self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be an agent",
            message="You were added as an agent on KubaCRM. Please come login to start working",
            from_email="admin@test.com",
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organization = self.request.user.agent.organization
        return Agent.objects.filter(organization=organization)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user.agent.organization

        context['profile_picture_form'] = UserProfileUpdateForm(instance=context['user_profile'])

        return context
 

def update_profile_picture(request, pk):
    agent = Agent.objects.get(pk=pk)
    user_profile = agent.user.userprofile
    if request.method == 'POST':
        profile_picture_form = UserProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if profile_picture_form.is_valid():
            profile_picture_form.save()

    return redirect('agents:agent-detail', pk=pk)


class AgentUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        organization = self.request.user.agent.organization
        return Agent.objects.filter(organization=organization)


class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agents:agent-list") 

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
    

