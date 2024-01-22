import random
from django.core.mail import send_mail
from django.views import generic
from django.shortcuts import reverse, redirect
from leads.models import Agent
from .forms import AgentModelForm, UserProfileUpdateForm
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


class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user.userprofile

        # Add the profile picture update form
        context['profile_picture_form'] = UserProfileUpdateForm(instance=context['user_profile'])

        return context
    
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserProfileUpdateForm

class UserProfileUpdateView(View):
    template_name = "path_to_template.html"  # Update with your actual template path

    def get(self, request, *args, **kwargs):
        form = UserProfileUpdateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to the database
            form.save()
            return redirect('profile_success')  # Redirect to a success page
        return render(request, self.template_name, {'form': form})


def update_profile_picture(request, pk):
    agent = Agent.objects.get(pk=pk)
    user_profile = agent.user.userprofile
    print('Here in update')
    if request.method == 'POST':
        profile_picture_form = UserProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        print('Post was sent')
        if profile_picture_form.is_valid():
            profile_picture_form.save()

    return redirect('agents:agent-detail', pk=pk)

    

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
    

