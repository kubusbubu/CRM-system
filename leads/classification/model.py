import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from joblib import dump


# Load the dataset
leads_data = pd.read_csv('leads/classification/Leads.csv')

# Selecting features and target variable
X = leads_data.drop('Converted', axis=1)
y = leads_data['Converted']

# Identifying numerical and categorical columns
numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = X.select_dtypes(include=['object', 'bool']).columns

# Preprocessing for numerical data
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())])

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

# Combining preprocessing steps
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)])

def choose_algorithm(algo):
    if algo == "LR":
        # Creating a pipeline that preprocesses the data and applies logistic regression
        model = Pipeline(steps=[('preprocessor', preprocessor),
                                ('classifier', LogisticRegression(max_iter=1000))])
        return model
    elif algo == "RFC":
        # Creating a pipeline that preprocesses the data and then applies Random Forest
        model = Pipeline(steps=[('preprocessor', preprocessor),
                                ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))])
        return model
    elif algo == "GBC":
        # Creating a pipeline with preprocessing and Gradient Boosting classifier
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', GradientBoostingClassifier(n_estimators=100, random_state=42))
        ])
        return model
    else:
        print("Wpisano nie poprawnie nazwę. Spróbuj ponownie")
        give_input()


def give_input():
    answer = input("Choose algorithm to train model from this list: [LR, RFC, GBC]: ")
    model = choose_algorithm(answer)
    print(f"You chose correctly {answer} algorithm")
    return model


model = give_input()

# Splitting data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

dump(X_test, 'leads/classification/X_test.joblib')
dump(y_test, 'leads/classification/y_test.joblib')

# Training the model
model.fit(X_train, y_train)
print("Model is trained. Exporting model to model.joblib file")
# Making predictions on the test set

dump(model, 'leads/classification/model.joblib')