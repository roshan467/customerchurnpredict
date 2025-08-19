import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pickle

# Absolute path to your dataset CSV file
DATA_PATH = r"C:\Users\Roshan\OneDrive\Desktop\customer-churn-retention\data\WA_Fn-UseC_-Telco-Customer-Churn.csv"

# Path to save trained model
MODEL_DIR = r"C:\Users\Roshan\OneDrive\Desktop\customer-churn-retention\models"
MODEL_PATH = os.path.join(MODEL_DIR, 'model.pkl')

# Create model directory if not exists
os.makedirs(MODEL_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_PATH)

# Drop customerID as it is not useful for prediction
df.drop('customerID', axis=1, inplace=True)

# Convert TotalCharges to numeric and fill missing values
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)

# Map target variable to binary
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

# One-hot encode categorical variables (drop first to avoid dummy trap)
X = pd.get_dummies(df.drop('Churn', axis=1), drop_first=True)
y = df['Churn']

# Split dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42
)

# Train Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate on test set
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model and columns used during training
with open(MODEL_PATH, 'wb') as f:
    pickle.dump({'model': model, 'columns': X.columns.tolist()}, f)

print(f"Model saved successfully at: {MODEL_PATH}")
