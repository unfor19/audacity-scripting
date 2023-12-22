from typing import List
import pyperclip
from ..utils.logger import logger
from .pipe import do_command
from .clip import Clip
from .project import open_project, save_project, save_project_as, save_project_changes
from time import sleep
import os
import shutil


def open_project_copy(file_path, file_extra_label="", sleep_seconds=0.5):
    file_name, file_extension = os.path.splitext(file_path)
    new_file_path = f"{file_name}.output{file_extension}"
    if len(file_extra_label) > 0:
        new_file_path = f"{file_name}.output{file_extra_label}{file_extension}"
    shutil.copyfile(file_path, new_file_path)
    sleep(sleep_seconds)
    if os.path.exists(new_file_path):
        open_project(new_file_path)
        sleep(sleep_seconds)
        return new_file_path
    return False


def select_clip(track_index, start, end):
    return do_command(
        f"Select: Start={start} End={end} Track={track_index}.0")


def cut_clip():
    return do_command('Cut:')


def paste_clip():
    return do_command('Paste:')


def copy_clip():
    return do_command('Copy:')


def select_track(track_index):
    return do_command(
        f"SelectTracks: Track={track_index}.0")


def remove_tracks():
    return do_command("RemoveTracks:")


def move_track_up(track, distance):
    for i in range(distance):
        logger.info(f"Moving track {track} up")
        select_track(track)
        do_command(
            f"TrackMoveUp:")


def move_track_down(track, distance):
    for range in range(distance):
        logger.info(f"Moving track {track} down")
        select_track(track)
        do_command(
            f"TrackMoveDown:")


def move_track(track_index, new_track_index):
    select_track(new_track_index)
    remove_tracks()
    if track_index > new_track_index:
        distance = track_index - new_track_index
        move_track_up(new_track_index, distance)
    else:
        distance = new_track_index - track_index
        move_track_down(new_track_index, distance)
    return True


def copy_and_paste_clip(source_track_index, target_track_index, clip):
    select_clip(source_track_index, clip.start, clip.end)
    copy_clip()
    select_clip(target_track_index, clip.start, clip.end)
    paste_clip()
    return True


def add_label_to_clip(label_iterator, sleep_seconds=0.01):
    do_command('AddLabel:')
    pyperclip.copy(label_iterator)
    do_command('Paste:')
    sleep(sleep_seconds)
    return label_iterator + 1


def clean_up_tracks(original_tracks, sleep_seconds=0.01):
    logger.info("Removing original tracks ...")
    for track_index in original_tracks[::-1]:
        logger.info(f"Removing track {track_index} ...")
        select_track(track_index)
        remove_tracks()
        sleep(sleep_seconds)
    logger.info("Completed removing tracks")
    return True


def calculate_new_positions(clips_objects: [Clip]) -> [Clip]:
    # Organize clips by track
    logger.info("Calculating new positions for clips ...")
    tracks = {}
    clips_old_positions = [clip.copy() for clip in clips_objects]
    for clip in clips_old_positions:
        track = clip.track
        if track not in tracks:
            tracks[track] = []
        tracks[track].append(clip)
    clips_new_positions = []
    for track, track_clips in tracks.items():
        # Sort clips by start time to ensure correct order
        track_clips.sort(key=lambda x: x.start)

        # Initialize the start time for the first clip
        current_start_time = 0.0

        # Adjust start and end times for each clip
        for clip in track_clips:
            clip.start = current_start_time
            clip.end = round(current_start_time + clip.duration, 5)
            current_start_time = clip.end
            clips_new_positions.append(clip)
    logger.info(
        f"Completed calculating new positions for clips")
    return clips_new_positions


def remove_spaces_between_clips(new_file_path="", sleep_seconds=0.01):
    logger.info("Started removing spaces between clips ...")
    Clip.refresh_clips()  # Fetch clips for the first time
    all_tracks_gaps = Clip.get_gaps()
    tracks_with_gaps = Clip.get_tracks_with_gaps()
    clips_objects = Clip.get_clips()
    clips_new_positions = calculate_new_positions(clips_objects)
    num_of_tracks = Clip.get_num_tracks()

    if not all_tracks_gaps:
        return True
    for track_index in range(num_of_tracks):
        # Filter clips_new_positions for the current track
        current_track_new_positions = [
            clip for clip in clips_new_positions if clip.track == track_index]

        track_clips = [
            clip for clip in clips_objects if clip.track == track_index]
        target_track_index = track_index + num_of_tracks
        logger.info(
            f"Copying clips from track {track_index} to {target_track_index} ...")
        for track_clip_index, track_clip in enumerate(track_clips):
            new_clip_position = current_track_new_positions[track_clip_index]
            select_clip(
                track_index,
                track_clip.start,
                track_clip.end
            )
            copy_clip()
            select_clip(
                target_track_index,
                new_clip_position.start,
                new_clip_position.end
            )
            paste_clip()
        sleep(sleep_seconds)
    logger.info(
        f"Removing tracks that contained gaps - {tracks_with_gaps}")
    # Delete tracks that contained gaps
    for track_index in tracks_with_gaps[::-1]:  # Delete from end to start
        logger.info(f"Removing track {track_index} with gaps ...")
        select_track(track_index)  # Select the track with gaps
        remove_tracks()  # Remove the selected track
        # Give some time for the command to complete
        sleep(sleep_seconds)

    # Verify that all gaps between clips were removed
    Clip.refresh_clips()  # Fetch clips after cleanup
    gaps = Clip.get_gaps()
    if gaps:
        raise Exception(
            f"Failed to clean all gaps between clips - Gaps - {gaps}")
    else:
        logger.info("Completed removing spaces between clips")

    save_project_changes(new_file_path, sleep_seconds)
    return True


def add_labels_to_clips(new_file_path="", start_label_iterator=1, sleep_seconds=0.01):
    logger.info("Started adding labels to clips ...")
    Clip.refresh_clips()
    clips_objects = Clip.get_clips()
    num_of_tracks = Clip.get_num_tracks()
    labels_added = 0
    label_iterator = start_label_iterator
    original_tracks = Clip.get_tracks()

    target_track_clips_index = num_of_tracks
    for track_index in range(num_of_tracks):
        track_clips = [
            clip for clip in clips_objects if clip.track == track_index]
        logger.info(
            f"Copying clips from track {track_index} to {target_track_clips_index} ...")
        for track_clip in track_clips:
            copy_and_paste_clip(
                track_index, target_track_clips_index, track_clip)
            label_iterator = add_label_to_clip(label_iterator, sleep_seconds)
            labels_added += 1
        target_track_clips_index += 2
    clean_up_tracks(original_tracks, sleep_seconds)
    logger.info(f"Completed adding labels. Total labels added: {labels_added}")
    save_project_changes(new_file_path, sleep_seconds)
    return labels_added
