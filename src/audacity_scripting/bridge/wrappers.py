from ..utils.logger import logger
from .pipe import do_command
from .clip import Clip
from .project import open_project, save_project
from time import sleep, time
import os
import shutil


def open_project_copy(file_path):
    file_name, file_extension = os.path.splitext(file_path)
    timestamp = int(time())
    new_file_path = f"{file_name}.{timestamp}.trimmed{file_extension}"
    shutil.copyfile(file_path, new_file_path)
    if os.path.exists(new_file_path):
        open_project(new_file_path)
        return new_file_path
    return False


def calculate_clips_gaps(clips_info):
    if not clips_info:
        clips_info = Clip.get_clips()
    gaps = {}
    for i in range(len(clips_info) - 1):
        current_clip = clips_info[i]
        next_clip = clips_info[i + 1]

        # Check if the next clip is in the same track
        if current_clip['track'] == next_clip['track'] and current_clip['end'] != next_clip['start']:
            if current_clip['track'] not in gaps:
                gaps[current_clip['track']] = []
            gap = {
                "start": current_clip['end'],
                "end": next_clip['start']
            }
            gaps[current_clip['track']].append(gap)
    return gaps


def delete_segment(track_index, start, end):
    do_command(
        f"Select: Start={start} End={end} Track={track_index}.0")
    do_command('Delete:')


def remove_spaces_between_clips():
    all_tracks_gaps = calculate_clips_gaps(Clip.get_clips())
    while all_tracks_gaps:
        logger.info(f"Gaps - {all_tracks_gaps}")
        for track_index, track_gaps in all_tracks_gaps.items():
            for track_gap in reversed(track_gaps):
                delete_segment(
                    track_index, track_gap['start'], track_gap['end'])
                break
            break
        all_tracks_gaps = calculate_clips_gaps(Clip.get_clips())
    logger.info(f"Removed spaces between clips")
    if save_project():
        logger.info(f"Saved project")
        return True
    return False
