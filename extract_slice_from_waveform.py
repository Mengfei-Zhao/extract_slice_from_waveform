# Author: Mengfei Zhao
# Date: 2024.05.25

import csv
import pandas as pd
import numpy as np
import os
import sys


def show_help_info():
    print("\nAuthor: Mengfei Zhao")
    print("Mail: 18037198823@163.com")
    print("Date: 2024.05.25")
    print("Version: v1\n")
    print("This is the help information.")
    print("Syntax: python extract_slice_from_waveform.py filename start end")
    print("Description: filename is the filename you wanna extract; start and end are the start and end time, respectively, eg. 80e-9")


def main(txt_filename, start, end):
    # 解析文件名
    filename_with_extension = os.path.basename(txt_filename)
    filename, file_extension = os.path.splitext(filename_with_extension)

    with open(txt_filename, 'r') as file:
        # 读取文件内容
        content = file.read()
        # 替换制表符为分号
        content_new = content.replace('\t', ';')

    # 如果要写入新文件，使用以下代码
    with open('temp1.txt', 'w') as file:
        file.write(content_new)

    with open("temp1.txt", "r") as f:
        reader = csv.reader(f, delimiter=";")
        data = list(reader)

    # get the name of column
    header = data[0]

    # convert to DataFrame
    df = pd.DataFrame(data[1:], columns=header)
    df["time"] = df["time"].astype(float)
    df["vout"] = df["vout"].astype(float)

    # 提取一段数据
    start_index = 0
    end_index = 0
    delta_time = 0.005e-9
    for index, row in df.iterrows():
        if abs(row["time"] - start) <= delta_time:
            start_index = index
        elif abs(row["time"] - end) <= delta_time:
            end_index = index
    df_sub = df.iloc[start_index:end_index]

    # 将时间轴平移到0，因为alps需要的激励信号必须从0开始
    delay_t = df_sub["time"].iloc[0]
    df_temp = df_sub["time"] - delay_t
    pd.options.mode.chained_assignment = None
    df_sub["time"] = df_temp.copy(deep=True)

    # 将开头的电压都设置为-5mV，如果不需要该功能，注释掉这段即可。
    low_value1 = -5e-3
    for i in range(15):
        df_sub["vout"].iloc[i] = low_value1

    # 保存到文件
    output_filename = filename + ".csv"
    df_sub.to_csv(output_filename, index=False, header=False)

    os.remove("temp1.txt")

    print("\nDone.\n")
    print("The .csv file has been generated.\n")


def run_mode():
    arg_num = len(sys.argv)
    arg1 = sys.argv[1]
    print("\nThere are " + str(arg_num) + " parameters.")

    if arg1 == "-h":
        show_help_info()
    elif arg_num == 2:
        filename = arg1
        start = 80e-9
        end = 90e-9
        main(filename, start, end)
    elif arg_num == 4:
        filename = arg1
        start = float(sys.argv[2])
        end = float(sys.argv[3])
        # print("par: ", filename, start, end)
        main(filename, start, end)
    else:
        print("There are errors in the parameters.")
        sys.exit(1)


def debug_mode():
    # debug用
    main("./inputlink_12Gbps_prbs.txt", 80e-9, 90e-9)


run_mode()
# debug_mode()
