import pandas as pd
import random

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
    if(high_val > 1000):
        while flag<3:
            randn = random.randint(1, 2*count)
            x = random.randint(1, 2*count - randn)
            start = df.iloc[i, randn]
            end = int(df.iloc[i, randn + x]) - start
            if(end - start > 64):
                print(df.iloc[i,1])
                df1 = pd.DataFrame([[c,df.iloc[i,1],f'{i}'+f'{flag}'+df.iloc[i,2],1,0,end]],
                                   columns=['sno','type', 'name', 'count','L1','L2'])
                flag += 1
                c +=1
                df = pd.concat([df, df1], ignore_index=True, sort=False)
            else:
                continue
    elif(high_val > 500 and high_val < 1000):
        while flag<2:
            randn = random.randint(1, count)
            x = random.randint(1, count - randn)
            start = df.iloc[i, randn]
            end = int(df.iloc[i, randn + x]) -start
            df1 = pd.DataFrame([[c,df.iloc[i, 1], f'{i}' + f'{flag}'+df.iloc[i, 2], 1, 0, end]],
                               columns=['sno','type', 'name', 'count', 'L1', 'L2'])
            df = pd.concat([df, df1], ignore_index=True, sort=False)
            flag += 1
            c +=1

    else:
        randn = random.randint(1, count)
        x = random.randint(1, count - randn + 1)
        start = df.iloc[i, randn]
        end = int(df.iloc[i, randn + x]) - start
        df1 = pd.DataFrame([[c ,df.iloc[i, 1], f'{i}' + df.iloc[i, 2], 1, 0, end]],
                           columns=['sno','type', 'name', 'count', 'L1', 'L2'])
        df = pd.concat([df, df1], ignore_index=True, sort=False)
        c += 1

df.to_csv('RESULT.csv', index=False)





