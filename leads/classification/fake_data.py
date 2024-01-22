import pandas as pd
from faker import Faker

fake = Faker()

# Load the actual leads data
leads_actual = pd.read_csv('leads/classification/leads_actual.csv')

# Add fake data for the new fields
leads_actual['first_name'] = [fake.first_name() for _ in range(len(leads_actual))]
leads_actual['last_name'] = [fake.last_name() for _ in range(len(leads_actual))]
leads_actual['email'] = [fake.email() for _ in range(len(leads_actual))]
leads_actual['phone_number'] = [fake.phone_number() for _ in range(len(leads_actual))]
leads_actual['address'] = [fake.street_address() for _ in range(len(leads_actual))]
leads_actual['state'] = [fake.state() for _ in range(len(leads_actual))]
leads_actual['postal_code'] = [fake.postcode() for _ in range(len(leads_actual))]
leads_actual['age'] = [fake.random_int(min=18, max=75) for _ in range(len(leads_actual))]

# Save the modified CSV
leads_actual.to_csv('leads/classification/leads_actual_with_fake_data.csv', index=False)

