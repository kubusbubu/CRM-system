from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.dispatch import receiver
from PIL import Image
import os
import uuid


class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False) 


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/profile_pics/', default='default_pic/default.png', null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # Check if the user already has a profile picture
        try:
            existing_user_profile = UserProfile.objects.get(user=self.user)
            old_profile_picture = existing_user_profile.profile_picture
            # If a new profile picture is uploaded, delete the old one
            if self.profile_picture and old_profile_picture and self.profile_picture != old_profile_picture:
                old_picture_path = os.path.join(settings.MEDIA_ROOT, str(old_profile_picture))
                if os.path.exists(old_picture_path):
                    os.remove(old_picture_path)
        except UserProfile.DoesNotExist:
            pass

        super().save(*args, **kwargs)
        if self.profile_picture:
            img = Image.open(self.profile_picture.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)


class Lead(models.Model):
    # Fields from the leads dataset
    prospect_id = models.CharField(max_length=100, unique=True, blank=True)
    lead_number = models.CharField(max_length=100, blank=True, null=True)
    lead_origin = models.CharField(max_length=100, blank=True, null=True)
    lead_source = models.CharField(max_length=100, blank=True, null=True)
    do_not_email = models.BooleanField(default=False)
    do_not_call = models.BooleanField(default=False)
    total_visits = models.FloatField(null=True, blank=True)
    total_time_spent_on_website = models.IntegerField(null=True, blank=True)
    page_views_per_visit = models.FloatField(null=True, blank=True)
    last_activity = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    how_did_you_hear_about_x_education = models.CharField(max_length=100, blank=True, null=True)
    what_is_your_current_occupation = models.CharField(max_length=100, blank=True, null=True)
    what_matters_most_to_you_in_choosing_a_course = models.CharField(max_length=100, blank=True, null=True)
    search = models.BooleanField(default=False)
    magazine = models.BooleanField(default=False)
    newspaper_article = models.BooleanField(default=False)
    x_education_forums = models.BooleanField(default=False)
    newspaper = models.BooleanField(default=False)
    digital_advertisement = models.BooleanField(default=False)
    through_recommendations = models.BooleanField(default=False)
    receive_more_updates_about_our_courses = models.BooleanField(default=False)
    tags = models.CharField(max_length=100, blank=True, null=True)
    lead_quality = models.CharField(max_length=100, blank=True, null=True)
    update_me_on_supply_chain_content = models.BooleanField(default=False)
    get_updates_on_dm_content = models.BooleanField(default=False)
    lead_profile = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    asymmetrique_activity_index = models.CharField(max_length=100, blank=True, null=True)
    asymmetrique_profile_index = models.CharField(max_length=100, blank=True, null=True)
    asymmetrique_activity_score = models.FloatField(null=True, blank=True)
    asymmetrique_profile_score = models.FloatField(null=True, blank=True)
    i_agree_to_pay_the_amount_through_cheque = models.BooleanField(default=False)
    a_free_copy_of_mastering_the_interview = models.BooleanField(default=False)
    last_notable_activity = models.CharField(max_length=100, blank=True, null=True)

    # Fake generated fields
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(default=0)

    score = models.FloatField(null=True, blank=True)
    
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.prospect_id:
            # Generate a unique ID if prospect_id is not provided
            self.prospect_id = uuid.uuid4().hex[:10]
        super().save(*args, **kwargs)  


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Category(models.Model):
    name = models.CharField(max_length=30)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @staticmethod
    def handle_category_deletion(category):
        unassigned_category, created = Category.objects.get_or_create(
            name="Unassigned", defaults={'organization': category.organization}
        )
        Lead.objects.filter(category=category).update(category=unassigned_category)

@receiver(pre_delete, sender=Category)
def pre_delete_category(sender, instance, **kwargs):
    Category.handle_category_deletion(instance)


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)