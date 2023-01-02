import pandas as pd
import random
import cv2
import os
import multiprocessing as mp
from icecream import ic
from tqdm import tqdm

random.seed(0)
df = pd.read_csv("train.csv")
num_rows = df.shape[0]

updated_csv = []
ffmpeg_task_list = []
input_video_path = "/mnt/workspace/UMD/CMSC733/CMSC733_project/LLSP/train"
output_trimmed_video_path = "/mnt/workspace/UMD/CMSC733/CMSC733_project/LLSP/trimmed_train"  # This folder will contain only the cropped videos and will require merging the current video with the trimmed videos
os.makedirs(output_trimmed_video_path, exist_ok=True)


def trim_video(input_video_path, starting_frame, duration, output_video_path):
    video = cv2.VideoCapture(input_video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    video_size = (
        int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    )
    out_video = cv2.VideoWriter(
        output_video_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, video_size
    )
    count = 0
    while video.isOpened():
        ret, frame = video.read()
        if ret:
            if count < starting_frame:
                count += 1
                continue
            if count >= starting_frame + duration:
                break
            count += 1
            out_video.write(frame)
    out_video.release()


def frame_no_to_time(frame_no, fps):
    seconds = frame_no / fps
    minutes = seconds // 60
    seconds = seconds % 60
    return [int(minutes), int(seconds)]


def crop_current_row(row, number_of_new_videos):
    count = 0
    updated_video_rows = []
    ffmpeg_command_params = []
    no_luck = 0
    while count < number_of_new_videos:
        ## Generate a random number between 1 and repetition count in column ['count'], idx = 3
        new_video_rep_count = random.randint(1, int(row[3]))
        ## Generate random starting index to start clipping between 0 and repetition count - new_video_rep_count
        ## This index starts after column 4.
        starting_index = random.randint(0, int(row[3]) - new_video_rep_count) * 2
        end_index = starting_index + new_video_rep_count * 2
        start_frame = int(row[starting_index + 4])
        try:
            time_part_of_row = [
                int(i) - start_frame for i in row[starting_index + 4 : end_index + 4]
            ]
        except:
            ic(
                "Error in row",
                row[2],
                start_frame,
                row[:50],
                new_video_rep_count,
                starting_index,
                end_index,
            )
        if time_part_of_row[-1] - time_part_of_row[0] < 64:
            no_luck += 1
            if no_luck == 5:
                ic("No luck, skipping this video", row[2])
                break
            continue

        starting_time = start_frame  # / fps
        duration = time_part_of_row[-1]  # / fps
        ## Subtract the first element from all elements to make it start from 0
        new_row = [
            row[1],
            row[2].replace(".mp4", "_{}.mp4".format(count)),
            new_video_rep_count,
        ] + time_part_of_row
        updated_video_rows.append(new_row)
        ffmpeg_command_params.append(
            (
                os.path.join(input_video_path, row[2]),
                starting_time,
                duration,
                os.path.join(
                    output_trimmed_video_path,
                    row[2].replace(".mp4", "_{}.mp4".format(count)),
                ),
            )
        )
        count += 1
    return updated_video_rows, ffmpeg_command_params


def write_list_to_csv(list_of_rows, output_csv_path):
    pd.DataFrame(list_of_rows).to_csv(output_csv_path, index=True)


if __name__ == "__main__":
    for i in tqdm(range(num_rows)):
        count = df["count"][i]
        row = df.loc[i].values.tolist()
        updated_csv += [row[1:]]
        cap = cv2.VideoCapture(os.path.join(input_video_path, row[2]))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_number_of_frames_video = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if total_number_of_frames_video > 1000:
            updated_csv_rows, ffmpeg_commands = crop_current_row(row, 5)
            updated_csv += updated_csv_rows
            ffmpeg_task_list += ffmpeg_commands

        elif total_number_of_frames_video > 500 and total_number_of_frames_video < 1000:
            updated_csv_rows, ffmpeg_commands = crop_current_row(row, 3)
            updated_csv += updated_csv_rows
            ffmpeg_task_list += ffmpeg_commands

        elif total_number_of_frames_video > 200 and total_number_of_frames_video < 500:
            updated_csv_rows, ffmpeg_commands = crop_current_row(row, 2)
            updated_csv += updated_csv_rows
            ffmpeg_task_list += ffmpeg_commands
        elif total_number_of_frames_video < 200 and total_number_of_frames_video > 100:
            updated_csv_rows, ffmpeg_commands = crop_current_row(row, 1)
            updated_csv += updated_csv_rows
            ffmpeg_task_list += ffmpeg_commands
    write_list_to_csv(updated_csv, "updated_train.csv")
    ic("wrote updated csv, starting ffmpeg tasks")
    # for i in ffmpeg_task_list:
    #     trim_video(*i)
    pool = mp.Pool(mp.cpu_count())
    pool.starmap(trim_video, ffmpeg_task_list)
    pool.close()
    pool.join()
