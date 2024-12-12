import numpy as np
import pandas as pd
import statsmodels.api as sm

data = pd.read_csv("advertising_sales.csv")

# Scale ad budgets to millions
data['TV_Budget_Millions'] = data['TV Ad Budget ($)'] / 1000
data['Radio_Budget_Millions'] = data['Radio Ad Budget ($)'] / 1000
data['Newspaper_Budget_Millions'] = data['Newspaper Ad Budget ($)'] / 1000

# Log-transform scaled budgets
data['Log_TV_Budget'] = np.log(data['TV_Budget_Millions'] + 1)
data['Log_Radio_Budget'] = np.log(data['Radio_Budget_Millions'] + 1)
data['Log_Newspaper_Budget'] = np.log(data['Newspaper_Budget_Millions'] + 1)

# Interaction terms with scaled budgets
data['Log_TV_Radio_Interaction'] = data['Log_TV_Budget'] * data['Log_Radio_Budget']
data['Log_TV_Newspaper_Interaction'] = data['Log_TV_Budget'] * data['Log_Newspaper_Budget']
data['Log_Radio_Newspaper_Interaction'] = data['Log_Radio_Budget'] * data['Log_Newspaper_Budget']

# Define predictors and response
X = data[['Log_TV_Budget', 'Log_Radio_Budget', 'Log_Newspaper_Budget',
          'Log_TV_Radio_Interaction', 'Log_TV_Newspaper_Interaction', 'Log_Radio_Newspaper_Interaction']]
X = sm.add_constant(X)
y = data['Sales ($)']  # Sales remain in millions

# Fit the model
scaled_model = sm.OLS(y, X).fit()

# Print summary
print(scaled_model.summary())


