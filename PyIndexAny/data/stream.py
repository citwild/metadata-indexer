__author__ = 'Wei Wang'

import os
import re
from pymediainfo import MediaInfo
from util import myutil
from pprint import pprint


class StreamFile():
    Debug = False

    def __init__(self, path):
        self.file_path = path
        self.nominal_date = "Unknown"
        self.location = "Unknown"
        self.is_compressed = "Unknown"
        self.equipment = "Unknown"
        self.begin_time = "Unknown"
        self.end_time = "Unknown"
        self.media_type = "Unknown"
        self.mtime_begin = -1  # time_t format
        self.mtime_end = -1
        self.video_width = -1
        self.video_height = -1
        self.duration = -1
        self.ext = os.path.splitext(path)[1].lower()

    def __str__(self):
        return self.file_path + ",nominal_date:" + str(self.nominal_date) + ",location:" \
               + str(self.location) + ",is_compressed:" + str(self.is_compressed) \
               + ",equipment:" + str(self.equipment) + ",file_extension:" + str(self.ext) + \
               ",width:" + str(self.video_width) + ",height:" + str(self.video_height) + \
               ",media_type:" + str(self.media_type) + ",duration:" + str(self.duration)

    def calc_mtime_begin(self):
        if self.duration is None:
            self.mtime_begin = -1
        else:
            self.mtime_begin = self.mtime_end - (self.duration/1000)

    def parse_media(self):
        self.mtime_end = os.path.getmtime(self.file_path)
        if myutil.match_type(self.file_path, ["jpg"]):
            self.media_type = "Thumbnail"
        elif myutil.match_type(self.file_path, ["mp4", "mts", "lrv"]):
            self.media_type = "Video"
        elif myutil.match_type(self.file_path, ["wav"]):
            self.media_type = "Audio"
        media_info = MediaInfo.parse(self.file_path)
        for track in media_info.tracks:
            if StreamFile.Debug:
                pprint(track.to_data())
            if track.track_type == "Video":     # some jpg has a video track
                self.video_width = track.width
                self.video_height = track.height
                if track.duration is None:
                    self.duration = -1
                else:
                    self.duration = track.duration
                break
            elif track.track_type == "Audio":
                self.duration = track.duration
                break
            elif track.track_type == "Thumbnail":
                self.video_width = track.width
                self.video_height = track.height
                self.duration = -1
                break
        self.calc_mtime_begin()

    def parse_name(self):
        path_parts = self.file_path.split(os.sep)
        date_pat = re.compile("^[\d]{4}-[\d]{2}-[\d]{2}$")
        loc_pat = re.compile("(PS [A-Z]|Huddle)")
        #comp_pat = re.compile("Compressed")
        equip_pat1 = re.compile("gopro|([\d]+gopro)", re.IGNORECASE)
        equip_pat2 = re.compile("zoom", re.IGNORECASE)
        for part in path_parts:
            if date_pat.match(part):
                self.nominal_date = part
            elif loc_pat.match(part):
                self.location = part
            elif comp_pat.match(part):
                self.is_compressed = True
            elif equip_pat1.match(part):
                self.equipment = "gopro"
            elif equip_pat2.match(part):
                self.equipment = "zoom"

    def parse(self):
        self.parse_name()
        self.parse_media()
