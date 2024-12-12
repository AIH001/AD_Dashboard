import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
#This model is deprecated and not fit!!!!!

# Load the dataset
data = pd.read_csv("advertising_sales.csv")

# Features (X) and Target (y)
X = data[['TV Ad Budget ($)', 'Radio Ad Budget ($)', 'Newspaper Ad Budget ($)']]
y = data['Sales ($)']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Linear Regression Model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the Model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print results
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"R-squared (R²): {r2:.2f}")
print("Intercept (b0):", model.intercept_)
print("Coefficients (b1, b2, b3):", model.coef_)

# Save results
coeff_df = pd.DataFrame(model.coef_, X.columns, columns=['Coefficient'])
with open("model_results.txt", "w") as file:
    file.write(f"Mean Squared Error (MSE): {mse:.2f}\n")
    file.write(f"R-squared (R²): {r2:.2f}\n")
    file.write("\nIntercept and Coefficients:\n")
    file.write(f"Intercept: {model.intercept_}\n")
    file.write(coeff_df.to_string())
