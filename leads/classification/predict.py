import pandas as pd
from joblib import load

"""This is only for testing model"""

leads_actual = pd.read_csv('leads/classification/leads_actual.csv')

model = load('leads/classification/model.joblib')

X_actual = leads_actual.drop('Converted', axis=1) 

probabilities = model.predict_proba(X_actual)[:, 1]

leads_actual['Score'] = probabilities * 100

sorted_leads = leads_actual.sort_values(by='Score', ascending=False)

sorted_leads.to_csv('leads/classification/sorted_leads.csv', index=False)

print(sorted_leads[['Prospect ID', 'Score']])
