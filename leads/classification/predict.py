import pandas as pd
from joblib import load
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Load the actual dataset for prediction
leads_actual = pd.read_csv('leads/classification/leads_actual.csv')

# Load the trained model
model = load('leads/classification/model.joblib')

# Extracting the feature matrix (without the target column 'Converted')
X_actual = leads_actual.drop('Converted', axis=1) # Najlepiej by te dane od razu nie mialy tej kolumny kiedy je tworze

# The model's preprocessor will handle the preprocessing
# We assume that the model pipeline includes the necessary preprocessing steps
probabilities = model.predict_proba(X_actual)[:, 1]

# Converting probabilities to scores (0 to 100 scale)
leads_actual['Score'] = probabilities * 100

# Sorting the leads by their score
sorted_leads = leads_actual.sort_values(by='Score', ascending=False)

# Save the sorted leads with their scores
sorted_leads.to_csv('leads/classification/sorted_leads.csv', index=False)

# Optionally, print or output the sorted leads
print(sorted_leads[['Prospect ID', 'Score']])
