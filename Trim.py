import pandas as pd
import random

# Read the CSV file
df = pd.read_csv('data.csv')

# Print the dataframe
num_rows = df.shape[0]

for i in range(num_rows):
    count = df['count'][i]
    row = df.loc[i]
    high_val = df.iloc[i, 3+(2*count)]
    flag = 0
    if(high_val > 1000):
        while flag<3:
            randn = random.randint(1, 2*count)
            x = random.randint(1, 2*count - randn)
            start = df.iloc[i, randn]
            end = df.iloc[i, randn + x]
            if(end - start > 64):
                df.iloc[i, randn] = start + 32
                df.iloc[i, randn + x] = end - 32
                flag += 1
            else:
                continue
    elif(high_val > 500 and high_val < 1000):
        while flag<2:
            randn = random.randint(1, count)
            x = random.randint(1, count - randn)
    else:
        randn = random.randint(1, count)
        x = random.randint(1, count - randn)









