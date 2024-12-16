import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv("advertising_sales.csv")

# Scale the specified columns
columns_to_scale = ['TV Ad Budget ($)', 'Radio Ad Budget ($)', 'Newspaper Ad Budget ($)']
data[columns_to_scale] = data[columns_to_scale] * 1000  # Multiply ad budgets by 1000
data['Sales ($)'] = data['Sales ($)'] * 1_000_000       # Multiply sales by 1,000,000
# Ensure console displays full DataFrame
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', 1000)  # Adjust console width


# Calculate ROI for each channel
data['TV ROI (%)'] = ((data['Sales ($)'] - data['TV Ad Budget ($)']) / data['TV Ad Budget ($)']).replace([float('inf'), -float('inf')], 0) * 100
data['Radio ROI (%)'] = ((data['Sales ($)'] - data['Radio Ad Budget ($)']) / data['Radio Ad Budget ($)']).replace([float('inf'), -float('inf')], 0) * 100
data['Newspaper ROI (%)'] = ((data['Sales ($)'] - data['Newspaper Ad Budget ($)']) / data['Newspaper Ad Budget ($)']).replace([float('inf'), -float('inf')], 0) * 100

# Open file for writing
with open("Advertising_Spend_Report.txt", "w") as file:
    # Write Summary Statistics
    file.write("Advertising Sales Analysis Report\n")
    file.write("="*40 + "\n\n")
    file.write("1. Summary Statistics:\n")
    file.write(data.describe().to_string())  # Convert DataFrame to string for writing
    file.write("\n\n")

    # Write Correlation Matrix
    file.write("2. Correlation Matrix:\n")
    file.write(data.corr().to_string())  # Convert DataFrame to string for writing
    file.write("\n\n")

    # Write Average Sales Contribution
    file.write("3. Average Sales Contribution by Channel:\n")
    file.write(f"   TV: {data['TV Ad Budget ($)'].mean():.2f}\n")
    file.write(f"   Radio: {data['Radio Ad Budget ($)'].mean():.2f}\n")
    file.write(f"   Newspaper: {data['Newspaper Ad Budget ($)'].mean():.2f}\n")
    file.write("\n")

    # Write ROI Analysis
    file.write("4. ROI Analysis (Average ROI by Channel):\n")
    file.write(f"   TV ROI (%): {data['TV ROI (%)'].mean():.2f}\n")
    file.write(f"   Radio ROI (%): {data['Radio ROI (%)'].mean():.2f}\n")
    file.write(f"   Newspaper ROI (%): {data['Newspaper ROI (%)'].mean():.2f}\n")
    file.write("\n")

    # Write Top 10 Ad Campaigns by Sales
    top_sales = data.sort_values(by='Sales ($)', ascending=False).head(10)
    file.write("5. Top 10 Ad Campaigns by Sales:\n")
    file.write(top_sales.to_string(index=False))
    file.write("\n")

# Visualizations

# 1. Plot Distribution of Sales
data['Sales ($)'].hist(bins=20)
plt.title("Distribution of Sales")
plt.xlabel("Sales ($)")
plt.ylabel("Frequency")
plt.savefig("sales_distribution.png")
plt.close()

# 2. Plot Correlation Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Correlation Heatmap")
plt.savefig("correlation_heatmap.png")
plt.close()

# 3. Plot Average Advertising Spend
avg_spend = data[['TV Ad Budget ($)', 'Radio Ad Budget ($)', 'Newspaper Ad Budget ($)']].mean()
avg_spend.plot(kind='bar', figsize=(8, 6))
plt.title("Average Advertising Spend by Channel")
plt.ylabel("Average Spend ($)")
plt.savefig("average_ad_spend.png")
plt.close()

# 4. Plot ROI Comparison
roi_means = {
    'TV ROI (%)': data['TV ROI (%)'].mean(),
    'Radio ROI (%)': data['Radio ROI (%)'].mean(),
    'Newspaper ROI (%)': data['Newspaper ROI (%)'].mean(),
}
pd.Series(roi_means).plot(kind='bar', figsize=(8, 6), color=['blue', 'orange', 'green'])
plt.title("Average ROI by Channel")
plt.ylabel("ROI (%)")
plt.savefig("roi_comparison.png")
plt.close()

print("Analysis complete. Report saved as 'Advertising_Spend_Report.txt'.")
print("Visualizations saved as PNG files.")
