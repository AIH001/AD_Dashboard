import pandas as pd
import matplotlib.pyplot as plt
# Load the dataset
data = pd.read_csv("advertising_sales.csv")

# Display basic info
print("Dataset Information:")
print(data.info())


# Show first few rows
print("\nFirst 5 Rows:")
print(data.head())

# Summary statistics
print("\nSummary Statistics:")
print(data.describe())

data['Sales ($)'].hist(bins=20)
plt.title("Distribution of Sales")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.show()

# Descriptive statistics for each column
print("\nDescriptive Statistics:")
print(data.describe())

# Correlation matrix
print("\nCorrelation Matrix:")
print(data.corr())
