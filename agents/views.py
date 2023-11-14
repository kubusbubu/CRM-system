from django.views import generic
from django.shortcuts import reverse
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin


class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
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
        agent = form.save(commit=False)
        agent.organization = self.request.user.userprofile
        agent.save()
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
    

class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
    
class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agents:agent-list") 

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
    

