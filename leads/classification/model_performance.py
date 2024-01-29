import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
# from joblib import dump
import time
import matplotlib.pyplot as plt

"""This file is for measuring performence of different models"""

# Wczytywanie danych
w = 'leads/classification/Leads.csv'
x1 = pd.read_csv(w)

# Wyodrębnienie etykiet
x2 = x1.drop('Converted', axis=1)
y = x1['Converted']

# Identyfikacja kolumn numerycznych i tekstowych
n1 = x2.select_dtypes(include=['int64', 'float64']).columns
t1 = x2.select_dtypes(include=['object', 'bool']).columns

# Preprocessing dla dancyh numerycznych
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())])

# Preprocessing dla danych tekstowych
cat_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

# Zestawienie transformat w jeden preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, n1),
        ('cat', cat_transformer, t1)])

# Create the final pipelines with preprocessing and the models
model_rf = Pipeline(steps=[('preprocessor', preprocessor),
                            ('classifier', RandomForestClassifier())])

model_lr = Pipeline(steps=[('preprocessor', preprocessor),
                            ('classifier', LogisticRegression(max_iter=1000))])


model_dt = Pipeline(steps=[('preprocessor', preprocessor),
                            ('classifier', DecisionTreeClassifier())])

# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(x2, y, test_size=0.2)

# Trenowanie modeli
start_time_rf = time.time()
model_rf.fit(X_train, y_train)
end_time_rf = time.time()
training_time_rf = end_time_rf - start_time_rf

start_time_lr = time.time()
model_lr.fit(X_train, y_train)
end_time_lr = time.time()
training_time_lr = end_time_lr - start_time_lr

start_time_dt = time.time()
model_dt.fit(X_train, y_train)
end_time_dt = time.time()
training_time_dt = end_time_dt - start_time_dt

print(f"Random Forest Training Time: {round(training_time_rf,)} seconds")
print(f"Logistic Regression Training Time: {round(training_time_lr, 1)} seconds")
print(f"Decision Tree Training Time: {round(training_time_dt, 1)} seconds")

# Predykcja modeli przy użyciu walidacji krzyżowej
y_pred_rf = cross_val_predict(model_rf, X_test, y_test, cv=5)
y_pred_lr = cross_val_predict(model_lr, X_test, y_test, cv=5)
y_pred_dt = cross_val_predict(model_dt, X_test, y_test, cv=5)

# Function to print indicators for each model
def print_indicators(model_name, y_true, y_pred):
    # Calculate and print confusion matrix
    conf_matrix = confusion_matrix(y_true, y_pred)
    print(f"\n{model_name} Confusion Matrix:")
    print(conf_matrix)

    # Plot confusion matrix
    plt.figure(figsize=(4, 3))
    plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
    # plt.title(f'{model_name} Confusion Matrix')
    plt.colorbar()
    tick_marks = [0, 1]
    plt.xticks(tick_marks, ["Pozytyw", "Negatyw"])
    plt.yticks(tick_marks, ["Pozytyw", "Negatyw"])
    plt.xlabel('Aktualne wartości')
    plt.ylabel('Predykowane wartości')

    # Add labels to each cell
    for i in range(conf_matrix.shape[0]):
        for j in range(conf_matrix.shape[1]):
            plt.text(j, i, str(conf_matrix[i, j]), horizontalalignment="center", color="white" if conf_matrix[i, j] > conf_matrix.max() / 2 else "black")

    plt.tight_layout()
    plt.show()

    # Calculate and print first-level indicators
    tp, fp, fn, tn = conf_matrix.ravel()
    print(f"{model_name} First Level Indicators:")
    print(f"{tp}")
    print(f"{fp}")
    print(f"{fn}")
    print(f"{tn}")

    # Calculate and print second-level indicators
    accuracy = round(accuracy_score(y_true, y_pred)*100, 1)
    precision = round(precision_score(y_true, y_pred)*100, 1)
    recall = round(recall_score(y_true, y_pred)*100, 1)
    f1 = round(f1_score(y_true, y_pred)*100, 1)

    print(f"{model_name} Second Level Indicators:")
    print(f"{accuracy}")
    print(f"{precision}")
    print(f"{recall}")
    print(f"{f1}")

# Print indicators for each model
print_indicators("Random Forest", y_test, y_pred_rf)
print_indicators("Logistic Regression", y_test, y_pred_lr)
print_indicators("Decision Tree", y_test, y_pred_dt)

# Save the trained models
# dump(model_rf, 'leads/classification/model_rf.joblib')
# dump(model_lr, 'leads/classification/model_lr.joblib')
# dump(model_dt, 'leads/classification/model_dt.joblib')
