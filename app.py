import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Load the dataset
data = pd.read_csv("advertising_sales.csv")
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', 1000)  # Adjust console width

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

# Correlation heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Correlation Heatmap")
plt.show()

# Average sales contribution by channel
print("\nAverage Sales Contribution by Channel:")
print("TV:", data['TV Ad Budget ($)'].mean())
print("Radio:", data['Radio Ad Budget ($)'].mean())
print("Newspaper:", data['Newspaper Ad Budget ($)'].mean())

# Average ad spend
avg_spend = data[['TV Ad Budget ($)', 'Radio Ad Budget ($)', 'Newspaper Ad Budget ($)']].mean()
avg_spend.plot(kind='bar', figsize=(8, 6))
plt.title("Average Advertising Spend by Channel")
plt.ylabel("Average Spend ($)")
plt.show()
