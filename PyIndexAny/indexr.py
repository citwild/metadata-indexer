#!/usr/bin/env python
__author__ = 'Wei Wang'

import os
import sys
import time

sys.path.append(os.getcwd())
from util import myutil
from data import stream
from data import db

MIN_PATH_CHECK_LEVEL = 0
ESTIMATED_TOTAL_FILE_NUM = 65000


def disk_root():
    # return "C:\\Users\\Fida\\Desktop\\BCResearchers"
    return "F:\BeamCoffer dataset\Thumbnails"


def not_interested_path(root, path):
    # returns true for paths that we do not care
    if myutil.rel_level(root, path) < MIN_PATH_CHECK_LEVEL:
        return True
    if myutil.is_hidden(path):
        return True
    if myutil.contain_hidden_dir(path):
        return True
    if not myutil.match_type(path, ["mp4", "jpg", "wav", "mts", "lrv"]):
        return True
    return False


def get_parsed_file(full_file_path):
    s_file = stream.StreamFile(full_file_path)
    s_file.parse()
    return s_file


def scan_file(root, full_file_path):
    if not_interested_path(root, full_file_path):
        return False
    s_file = get_parsed_file(full_file_path)
    #db.insert_stream(s_file)
    return True


def scan_disk(root, file_begin, file_limit=1000000):
    if not os.path.exists(root):
        print (root, "not exist. Nothing to scan.")
        return
    start_time = time.time()
    file_count = 0
    inserted_count = 0
    file_end = file_begin + file_limit
    last_time = time.time()
    prof_round = 20  # check time for each round
    #db.connect_db()
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
            if file_count < file_begin:
                continue
            if file_count > file_end:
                break
            full_file_path = os.path.join(dir_, file_name)
            if not scan_file(root, full_file_path):
                continue
            inserted_count += 1
        if file_count > file_end:
            break

    end_time = time.time()
    #db.close_db()
    print ("Scanned", file_count - 1, "files in", \
        end_time - start_time, "seconds. Inserted:", \
        inserted_count, "db records.")


def run_main():
    #db.prepare_db()
    scan_disk(disk_root(), 0)


def run_test():
    test_file = "/Volumes/NO NAME/2014-02-18/WB wall/162GOPRO/G0022975.JPG"
    stream.StreamFile.Debug = True
    s_file = get_parsed_file(test_file)
    print (s_file)
    stream.StreamFile.Debug = False

run_main()
# run_test()

print ("[Program ended.]")

