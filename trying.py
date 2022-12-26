import pandas as pd
import random
import csv
import cv2
import ffmpeg
df = pd.read_csv('data.csv')
# Create an example DataFrame
#df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
#print(df)
# Add a new row as a list
#df.loc[3] = [7]
#print(df)
#df1 = pd.DataFrame([[1, 2, 3],[5,6,7]])
#result = pd.concat([df, df1], ignore_index=True, sort=False)
#df = df.append([1,2,3], ignore_index=True)
#print(df)

input1 = 'data_dst.mp4'
input_video = ffmpeg.input(input1)
trimmed_video = input_video.trim(start=0, end=10)
ffmpeg.output(trimmed_video, 'hiii.mp4').run()