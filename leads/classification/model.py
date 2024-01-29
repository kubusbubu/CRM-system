import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from joblib import dump


leads_hist = pd.read_csv('leads/classification/leads_hist.csv')

X_hist = leads_hist.drop('Converted', axis=1)
y_hist = leads_hist['Converted']

numerical_cols = X_hist.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = X_hist.select_dtypes(include=['object', 'bool']).columns

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())])

cat_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numerical_cols),
        ('cat', cat_transformer, categorical_cols)])

model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('classifier', LogisticRegression(max_iter=1000))])

X_train, X_val, y_train, y_val = train_test_split(X_hist, y_hist, test_size=0.2, random_state=42)

model.fit(X_train, y_train)

cv_scores = cross_val_score(model, X_train, y_train, cv=5)

print(f"Cross-validation scores: {cv_scores}")
print(f"Average cross-validation score: {cv_scores.mean()}")

dump(model, 'leads/classification/model.joblib')
