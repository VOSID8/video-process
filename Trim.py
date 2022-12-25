import pandas as pd

# Read the CSV file
df = pd.read_csv('data.csv')

# Print the dataframe
num_rows = df.shape[0]

for i in range(num_rows):
    count = df['count'][i]
    row = df.loc[i]
    last_val = df.iloc[i, 3+(2*count)]

    print(last_val)






