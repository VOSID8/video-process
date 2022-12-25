import pandas as pd
import random
import csv

df = pd.read_csv('data.csv')


#df1 = pd.DataFrame([[1, 2, 3],[5,6,7]], columns=['count','name','type'])
#result = pd.concat([df, df1], ignore_index=True, sort=False)
#print(result)
#df = df.append(pd.Series(new, index=df.columns[:len(new)]), ignore_index=True)

num_rows = df.shape[0]
c = num_rows

for i in range(num_rows):
    count = df['count'][i]
    row = df.loc[i]
    high_val = df.iloc[i, 3+(2*count)]
    flag = 0
    flag2=0
    if(high_val > 1000):
        while flag<3:
            while flag2 == 0:
                randn = random.randint(1, count)
                x = random.randint(1, count - randn + 1)

                list = [c, df.iloc[i, 1], f'{i}' + '_' + f'{flag}' + df.iloc[i, 2], x]
                start = df.iloc[i, 2 * randn + 1]
                end = df.iloc[i, 2 * randn + 2 * x]
                for jj in range(1, 2 * x + 1):
                    list.append(df.iloc[i, 2 * randn + jj])
                if (int(end) - int(start) > 64):
                    c += 1
                    flag += 1
                    flag2 = 1
                    with open('data.csv', 'a', newline='') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(list)
                else:
                    continue
            flag2=0
    elif(high_val > 500 and high_val < 1000):
        while flag<2:
            while flag2 == 0:
                randn = random.randint(1, count)
                x = random.randint(1, count - randn + 1)

                list = [c, df.iloc[i, 1], f'{i}' + '_' + f'{flag}' + df.iloc[i, 2], x]
                start = df.iloc[i, 2 * randn + 1]
                end = df.iloc[i, 2 * randn + 2 * x]
                for jj in range(1, 2 * x + 1):
                    list.append(df.iloc[i, 2 * randn + jj])
                if (int(end) - int(start) > 64):
                    c += 1
                    flag += 1
                    flag2 = 1
                    with open('data.csv', 'a', newline='') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(list)
                else:
                    continue
            flag2=0
    else:
        while flag2 == 0:
            randn = random.randint(1, count)
            x = random.randint(1, count - randn + 1)

            list = [c, df.iloc[i, 1], f'{i}' + '_' + f'{flag}' + df.iloc[i, 2], x]
            start = df.iloc[i, 2 * randn +1]
            end = df.iloc[i, 2 * randn + 2 * x]
            for jj in range(1,2*x+1):
                list.append(df.iloc[i, 2 * randn + jj])
            if (int(end) - int(start) > 64):
                c += 1
                flag2 = 1
                with open('data.csv', 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(list)
            else:
                continue






