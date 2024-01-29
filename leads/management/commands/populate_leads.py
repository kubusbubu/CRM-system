from django.core.management.base import BaseCommand
import pandas as pd
from itertools import cycle
from leads.models import Lead, Agent, UserProfile, Category

class Command(BaseCommand):
    help = 'Populate database with lead data from CSV'

    def handle(self, *args, **kwargs):
        leads_actual = pd.read_csv('leads/classification/leads_actual_with_fake_data.csv')
        organizations = UserProfile.objects.all()

        if not organizations:
            self.stdout.write(self.style.ERROR('No organizations found in the database.'))
            return

        # Split the DataFrame into equal parts for each organization
        split_size = len(leads_actual) // len(organizations)
        leads_chunks = [leads_actual.iloc[i:i + split_size] for i in range(0, len(leads_actual), split_size)]

        for org, org_leads in zip(organizations, leads_chunks):
            agents = Agent.objects.filter(organization=org)
            if not agents:
                self.stdout.write(self.style.WARNING(f'No agents found for organization: {org}. Skipping these leads.'))
                continue
            agent_cycle = cycle(agents)

            new_category, _ = Category.objects.get_or_create(name='New', organization=org)

        for _, row in org_leads.iterrows():
            Lead.objects.create(
                prospect_id=row['Prospect ID'],
                lead_number=row['Lead Number'],
                lead_origin=row['Lead Origin'],
                lead_source=row['Lead Source'],
                do_not_email=row['Do Not Email'] == 'Yes',
                do_not_call=row['Do Not Call'] == 'Yes',
                total_visits=row['TotalVisits'],
                total_time_spent_on_website=row['Total Time Spent on Website'],
                page_views_per_visit=row['Page Views Per Visit'],
                last_activity=row['Last Activity'],
                country=row['Country'],
                specialization=row['Specialization'],
                how_did_you_hear_about_x_education=row['How did you hear about X Education'],
                what_is_your_current_occupation=row['What is your current occupation'],
                what_matters_most_to_you_in_choosing_a_course=row['What matters most to you in choosing a course'],
                search=row['Search'] == 'Yes',
                magazine=row['Magazine'] == 'Yes',
                newspaper_article=row['Newspaper Article'] == 'Yes',
                x_education_forums=row['X Education Forums'] == 'Yes',
                newspaper=row['Newspaper'] == 'Yes',
                digital_advertisement=row['Digital Advertisement'] == 'Yes',
                through_recommendations=row['Through Recommendations'] == 'Yes',
                receive_more_updates_about_our_courses=row['Receive More Updates About Our Courses'] == 'Yes',
                tags=row['Tags'],
                lead_quality=row['Lead Quality'],
                update_me_on_supply_chain_content=row['Update me on Supply Chain Content'] == 'Yes',
                get_updates_on_dm_content=row['Get updates on DM Content'] == 'Yes',
                lead_profile=row['Lead Profile'],
                city=row['City'],
                asymmetrique_activity_index=row['Asymmetrique Activity Index'],
                asymmetrique_profile_index=row['Asymmetrique Profile Index'],
                asymmetrique_activity_score=row['Asymmetrique Activity Score'],
                asymmetrique_profile_score=row['Asymmetrique Profile Score'],
                i_agree_to_pay_the_amount_through_cheque=row['I agree to pay the amount through cheque'] == 'Yes',
                a_free_copy_of_mastering_the_interview=row['A free copy of Mastering The Interview'] == 'Yes',
                last_notable_activity=row['Last Notable Activity'],
                # Fake generated fields
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                phone_number=row['phone_number'],
                address=row['address'],
                state=row['state'],
                postal_code=row['postal_code'],
                age=row['age'],
                # Round-robin assignment of agents
                agent=next(agent_cycle),
                organization=org,
                category=new_category,  # Assign to 'New' category
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated database with leads from CSV'))
