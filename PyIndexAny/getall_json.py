import os
import sys
import time
import json
from pprint import pprint
from pymediainfo import MediaInfo

sys.path.append(os.getcwd())

ESTIMATED_TOTAL_FILE_NUM = 65000

def print_frame(text):
    print("+-{}-+".format("-" * len(text)))
    print("| {} |".format(text))
    print("+-{}-+".format("-" * len(text)))

def scan_file(full_file_path):
    media_info = MediaInfo.parse(full_file_path)
    with open('data.json', 'a') as fp:
        fp.write("{\n\t\"file\": \"" + full_file_path + "\",\n")
        fp.write("\t\"tracks\": \n")
        for track in media_info.tracks:
            fp.write("{\n\t\""+(track.track_type)+"\":\n")
            json.dump(track.to_data(), fp, indent=4)
            fp.write("\n},")
        fp.write("},")


def scan_disk(root, file_begin, file_limit=1000000):
    if not os.path.exists(root):
        print (root, "not exist. Nothing to scan.")
        return
    start_time = time.time()
    file_count = 0
    file_end = file_begin + file_limit
    last_time = time.time()
    prof_round = 20  # check time for each round
    with open('data.json', 'a') as fp:
        fp.write("{\n\t\"files\": \n")
    for dir_, dir_names, file_names in os.walk(root):
        for file_name in file_names:
            file_count += 1
            if file_count % prof_round == 0:
                cur_time = time.time()
                round_diff = cur_time - last_time
                last_time = cur_time
                sys.stdout.write(
                    "Scanning %d (at about %f %%) .. Avg speed: %f s/item. Estimated time for 10k items: %f s\r" %
                    (file_count, file_count * 100.0 / ESTIMATED_TOTAL_FILE_NUM,
                     round_diff / prof_round, round_diff / prof_round * 10000.0))
            if file_count > file_end:
                break
            full_file_path = os.path.join(dir_, file_name)
            scan_file(full_file_path)
        if file_count > file_end:
            break

    end_time = time.time()
    with open('data.json', 'a') as fp:
        #filehandle.seek(-1, os.SEEK_END)
        #filehandle.truncate()
        fp.write("\n}")
    print ("Scanned", file_count, "files in", \
        end_time - start_time)


def run_main():
    if len(sys.argv) == 1:
        print("Usage: {} <directory>".format(sys.argv[0]))
        sys.exit(0)
    else:
        scan_disk(sys.argv[1], 0)

run_main()

print ("[Program ended.]")

