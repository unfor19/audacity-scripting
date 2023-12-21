from copy import deepcopy
from ..utils.logger import logger
from .pipe import do_command
from .clip import Clip
from .project import open_project, save_project, save_project_as
from time import sleep
import os
import shutil


def open_project_copy(file_path, file_extra_label="", sleep_seconds=0.5):
    file_name, file_extension = os.path.splitext(file_path)
    new_file_path = f"{file_name}.output.{file_extension}"
    if len(file_extra_label) > 0:
        new_file_path = f"{file_name}.output.{file_extra_label}{file_extension}"
    shutil.copyfile(file_path, new_file_path)
    sleep(sleep_seconds)
    if os.path.exists(new_file_path):
        open_project(new_file_path)
        sleep(sleep_seconds)
        return new_file_path
    return False


def calculate_clips_gaps(clips_info):
    logger.info("Started calculating gaps between clips ...")

    if not clips_info:
        clips_info = Clip.get_clips()
    gaps = {}
    for i in range(len(clips_info) - 1):
        current_clip: Clip = clips_info[i]
        next_clip: Clip = clips_info[i + 1]

        # Check if the next clip is in the same track
        if current_clip.track == next_clip.track \
                and current_clip.end != next_clip.start:
            if current_clip.track not in gaps:
                gaps[current_clip.track] = []
            gap = {
                "start": current_clip.end,
                "end": next_clip.start
            }
            gaps[current_clip.track].append(gap)
    logger.info("Completed calculating gaps between clips")
    logger.info(f"Gaps - {gaps}")
    return gaps


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


def calculate_new_positions(clips_objects: [Clip]) -> [object]:
    # Organize clips by track
    logger.info("Calculating new positions for clips ...")
    tracks = {}
    clips_old_positions = deepcopy(clips_objects)
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
    logger.info("Completed calculating new positions for clips")
    return clips_new_positions


def remove_spaces_between_clips(new_file_path="", sleep_seconds=0.01):
    logger.info("Started removing spaces between clips ...")
    Clip.get_clips()  # Fetch clips for the first time
    all_tracks_gaps = deepcopy(calculate_clips_gaps(Clip.to_objects())).items()
    tracks_with_gaps = [track for track, gaps in all_tracks_gaps]
    clips_objects = Clip.to_objects()
    clips_new_positions = calculate_new_positions(clips_objects)
    num_of_tracks = Clip.get_num_tracks()

    if all_tracks_gaps:
        for track_index in range(num_of_tracks):
            # Filter clips_new_positions for the current track
            current_track_new_positions = [
                clip for clip in clips_new_positions if clip.track == track_index]

            track_clips = [
                clip for clip in clips_objects if clip.track == track_index]
            target_track_index = track_index + num_of_tracks
            logger.info(
                f"Moving clips from track {track_index} to {target_track_index} ...")
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
        for track_index in all_tracks_gaps:
            logger.info(f"Removing track {track_index} with gaps ...")
            select_track(track_index)  # Select the track with gaps
            remove_tracks()  # Remove the selected track
            # Give some time for the command to complete
            sleep(sleep_seconds)

        # Verify that all gaps between clips were removed
        Clip.get_clips()  # Fetch clips after cleanup
        all_tracks_gaps_after = deepcopy(
            calculate_clips_gaps(Clip.to_objects())).items()
        if all_tracks_gaps_after:
            logger.error(
                f"Failed to clean all gaps between clips - Gaps - {all_tracks_gaps_after}")
            return False
        else:
            logger.info("Completed removing spaces between clips")

        if new_file_path:
            logger.info(f"Saving project ...")
            save_project_as(new_file_path)
            sleep(sleep_seconds)
            logger.info("Completed saving project")
    return True
