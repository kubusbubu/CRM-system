# yourapp/management/commands/update_lead_scores.py

from django.core.management.base import BaseCommand
import pandas as pd
from joblib import load
from leads.models import Lead

class Command(BaseCommand):
    help = 'Update lead scores based on predictions'

    def handle(self, *args, **kwargs):
        model = load('leads/classification/model.joblib')

        # Fetch unscored leads
        leads_to_score = Lead.objects.filter(score__isnull=True)

        for lead in leads_to_score:
            # Extracting features as per the model training script
            lead_data = {
                'Prospect ID': lead.prospect_id,
                'Lead Number': lead.lead_number,
                'Lead Origin': lead.lead_origin,
                'Lead Source': lead.lead_source,
                'Do Not Email': lead.do_not_email,
                'Do Not Call': lead.do_not_call,
                'TotalVisits': lead.total_visits,
                'Total Time Spent on Website': lead.total_time_spent_on_website,
                'Page Views Per Visit': lead.page_views_per_visit,
                'Last Activity': lead.last_activity,
                'Country': lead.country,
                'Specialization': lead.specialization,
                'How did you hear about X Education': lead.how_did_you_hear_about_x_education,
                'What is your current occupation': lead.what_is_your_current_occupation,
                'What matters most to you in choosing a course': lead.what_matters_most_to_you_in_choosing_a_course,
                'Search': lead.search,
                'Magazine': lead.magazine,
                'Newspaper Article': lead.newspaper_article,
                'X Education Forums': lead.x_education_forums,
                'Newspaper': lead.newspaper,
                'Digital Advertisement': lead.digital_advertisement,
                'Through Recommendations': lead.through_recommendations,
                'Receive More Updates About Our Courses': lead.receive_more_updates_about_our_courses,
                'Tags': lead.tags,
                'Lead Quality': lead.lead_quality,
                'Update me on Supply Chain Content': lead.update_me_on_supply_chain_content,
                'Get updates on DM Content': lead.get_updates_on_dm_content,
                'Lead Profile': lead.lead_profile,
                'City': lead.city,
                'Asymmetrique Activity Index': lead.asymmetrique_activity_index,
                'Asymmetrique Profile Index': lead.asymmetrique_profile_index,
                'Asymmetrique Activity Score': lead.asymmetrique_activity_score,
                'Asymmetrique Profile Score': lead.asymmetrique_profile_score,
                'I agree to pay the amount through cheque': lead.i_agree_to_pay_the_amount_through_cheque,
                'A free copy of Mastering The Interview': lead.a_free_copy_of_mastering_the_interview,
                'Last Notable Activity': lead.last_notable_activity
            }

            # Convert the lead data to DataFrame
            lead_df = pd.DataFrame([lead_data])

            # Predict score
            probability = model.predict_proba(lead_df)[:, 1]
            lead.score = probability[0] * 100
            lead.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated lead scores'))
