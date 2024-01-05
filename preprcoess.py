import os
from os.path import basename, splitext, join, exists
import sys
import glob
import re


def get_output_filename(input_path_name, process_type):

    #依規定組裝檔案名
    #BPS_OVERDUE-TEL-11212-1.001 -> DBPS_OVERDUE_TEL_11212_1.001.par

    source_filename= basename(input_path_name)
    filename, extension = splitext(source_filename)
    output_filename = process_type + filename.replace("-", "_") + extension + ".par"

    return output_filename

def preprocess(input_path_name, output_filepath, delimeter, process_type):

    #取得輸出檔案名稱
    output_filename = get_output_filename(input_path_name, process_type)

    #組裝輸出路徑
    output_path_name = join(output_filepath, output_filename)



    if exists(output_path_name):
        print(f"remove:{output_path_name}")
        os.remove(output_path_name)

    try:
        with open(input_path_name,'r') as file:
            outf = open(output_path_name,'a',newline='')
            for line in file:
                line = line.strip()


                prefix_col = []
                suffix_col = []

                prefix_col.append(line[0:4].strip())
                prefix_col.append(line[4:16].strip())
                prefix_col.append(line[16:21].strip().lstrip('0'))
                prefix_col.append(line[21:23].strip())
                prefix_col.append(line[23:27].strip())
                prefix_col.append(line[27:39].strip())
                prefix_col.append(line[39:41].strip())

                prefix_result = delimeter.join([item for item in prefix_col])

                if process_type == 'D':

                    suffix = line[54:]
                    for i in range(0, len(suffix), 13):
                        suffix_col.append(suffix[i:i+13])

                    for index,item in enumerate(suffix_col):
                        suffix_without_space = re.sub(r'\s+', delimeter, item)
                        result = delimeter.join([prefix_result, suffix_without_space, str(index+1)]) + '\r\n'

                        outf.write(result)

                elif process_type == 'M' :

                    suffix_col.append(line[41:54].strip()[:-3])
                    suffix_col.append(line[41:54].strip()[-3:])

                    result = delimeter.join([prefix_result, suffix_col[0], suffix_col[1]])+ '\r\n'

                    outf.write(result)

    except Exception as e :
        print(e)
        sys.exit(1)
    finally:
        print("complete")
        outf.close()

if __name__ == '__main__':

    source_filepath = sys.argv[1]
    file_pattern = sys.argv[1]
    output_filepath_m = sys.argv[1]
    output_filepath_d = sys.argv[1]


    matching_files = glob.glob(join(source_filepath, file_pattern))
    print(matching_files)

    #執行ladoing_d處理
    for input_path_name in matching_files:
        preprocess(input_path_name, output_filepath=output_filepath_d, delimeter='\u0006', process_type='D')

    #執行ladoing_m處理
    for input_path_name in matching_files:
        preprocess(input_path_name, output_filepath=output_filepath_m, delimeter='\u0006', process_type='M')