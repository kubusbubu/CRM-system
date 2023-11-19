from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from joblib import load
import pandas as pd


leads_data = pd.read_csv('leads/classification/Leads.csv')
# Load the model from the file
model = load('leads/classification/model.joblib')

# Load X_test and y_test using joblib
X_test = load('leads/classification/X_test.joblib')
y_test = load('leads/classification/y_test.joblib')

y_pred = model.predict(X_test)

# Evaluating the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Printing the evaluation results
print("Accuracy:", accuracy)
print("Classification Report:\n", report)
print("Confusion Matrix:\n", conf_matrix)

# Selecting a single lead from the test dataset
# For example, selecting the first row from the X_test set
single_lead = X_test.iloc[0:1]

# Making a prediction on this single lead
single_lead_prediction = model.predict(single_lead)

# Retrieving the actual class for this lead from y_test
actual_class = y_test.iloc[0]

# Output the prediction and the actual class
print("Predicted Class for the Lead:", 'Converted' if single_lead_prediction[0] == 1 else 'Not Converted')
print("Actual Class for the Lead:", 'Converted' if actual_class == 1 else 'Not Converted')

# Predicting probabilities for each lead
# The second column ([1]) of predict_proba gives the probability of the class being '1' (converted)
probabilities = model.predict_proba(leads_data.drop('Converted', axis=1))[:, 1]

# Converting probabilities to scores (0 to 100 scale)
scores = probabilities * 100

# Adding the scores to the leads_data dataframe
leads_data['Score'] = scores

# Sorting the leads by their score
sorted_leads = leads_data.sort_values(by='Score', ascending=False)

# Display the sorted leads with their scores
print(sorted_leads[['Prospect ID', 'Converted', 'Score']])

sorted_leads.to_csv('leads/classification/sorted_leads.csv', index=False)
