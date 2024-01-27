import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from joblib import dump

# Load the historical dataset
leads_hist = pd.read_csv('leads/classification/leads_hist.csv')

# Selecting features and target variable
X_hist = leads_hist.drop('Converted', axis=1)
y_hist = leads_hist['Converted']

# Identifying numerical and categorical columns
numerical_cols = X_hist.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = X_hist.select_dtypes(include=['object', 'bool']).columns

# Preprocessing for numerical data
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())])

# Preprocessing for categorical data
cat_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

# Combining preprocessing for both types of data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numerical_cols),
        ('cat', cat_transformer, categorical_cols)])

# Create the final pipeline with preprocessing and the model
model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('classifier', RandomForestClassifier(random_state=42))])

# Splitting data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_hist, y_hist, test_size=0.2, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Evaluate the model using cross-validation
cv_scores = cross_val_score(model, X_train, y_train, cv=5)

# Print cross-validation scores
print(f"Cross-validation scores: {cv_scores}")
print(f"Average cross-validation score: {cv_scores.mean()}")

# Save the trained model
dump(model, 'leads/classification/model.joblib')
