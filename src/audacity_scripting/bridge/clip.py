from ..utils.logger import logger
from ..utils.enums import AudacityCommandStatus, AudacityClipCommands
import json
from .pipe import do_command


class Clip:
    _tracks = []
    _clips = []
    _gaps = dict()
    _tracks_with_gaps = []

    def initialize_clip(self, raw_clip):
        self.start = round(raw_clip['start'], 5)
        self.end = round(raw_clip['end'], 5)
        if self.start <= 0.0:
            self.start = 0.0
        self.duration = round(self.end - self.start, 5)
        self.end = round(self.start + self.duration, 5)
        self.track = raw_clip['track']
        self.color = raw_clip['color']

    def __init__(self, raw_clip):
        self.initialize_clip(raw_clip)

    def __str__(self) -> str:
        return json.dumps({
            "start": self.start,
            "end": self.end,
            "duration": self.duration,
            "track": self.track,
            "color": self.color
        })

    @classmethod
    def get_gaps(cls) -> dict:
        return cls._gaps

    @classmethod
    def get_clips(cls) -> list:
        """
        Gets the clips in the project
        """
        return cls._clips

    @classmethod
    def to_json(cls) -> str:
        if not cls._clips:
            return None
        return json.dumps(cls._clips, default=str)

    @classmethod
    def get_tracks(cls) -> list:
        return cls._tracks

    @classmethod
    def get_tracks_with_gaps(cls) -> list:
        return cls._tracks_with_gaps

    @classmethod
    def get_num_tracks(cls) -> int:
        return len(cls._tracks)

    @staticmethod
    def get_info_clips() -> str:
        return do_command(AudacityClipCommands.GETINFO.value)

    @staticmethod
    def clean_clips_info(clips_raw) -> str:
        """
        Gets the clips info from the raw clips data
        Returns a string of clips info without the command result, ready for json parsing
        :param clips_raw: raw clips data
        """
        logger.debug(f"clips_raw: {clips_raw}")
        clips_lines = clips_raw.split("\n")
        clips_lines = clips_lines[:-1]  # Remove the last empty line

        if AudacityCommandStatus.SUCCESS.value in clips_raw:
            # Last line is the result of the command
            clips_command_result = clips_lines[-1].strip()
            logger.debug(f"clips_command_result: {clips_command_result}")

            if clips_command_result == AudacityCommandStatus.SUCCESS.value:
                # Remove command result
                clips_final = "".join(
                    clips_lines[:-1]).strip().replace("\n", "").replace(" ", "")
                logger.debug(f"clips_final: {clips_final}")
                return clips_final
            else:
                logger.error(
                    f"Failed to compare '{clips_command_result}' to '{AudacityCommandStatus.SUCCESS.value}'")
                return None
        else:
            logger.error(f"Failed to get clips info: {clips_command_result}")
            return None

    @staticmethod
    def sort_clips(clips_list: list) -> list:
        clips_list.sort(key=lambda clip: (clip['track'], clip['start']))

    @staticmethod
    def parse_get_info_clips(clips_cleaned, sort=True) -> [object]:
        clips_list = json.loads(clips_cleaned)
        logger.debug(f"parse_get_info_clips - clips_list: {clips_list}")
        if sort:
            Clip.sort_clips(clips_list)
        return clips_list

    @classmethod
    def calculate_clips_gaps(cls):
        logger.info("Started calculating gaps between clips ...")

        if not cls._clips:
            logger.error("No clips found")
            return None

        # Re-initialize gaps
        cls._gaps = dict()

        # Calculate gaps between clips
        for i in range(len(cls._clips) - 1):
            current_clip: Clip = cls._clips[i]
            next_clip: Clip = cls._clips[i + 1]

            # Check if the next clip is in the same track
            if current_clip.track == next_clip.track \
                    and current_clip.end != next_clip.start:
                if current_clip.track not in cls._gaps:
                    cls._gaps[current_clip.track] = []
                gap = {
                    "start": current_clip.end,
                    "end": next_clip.start
                }
                cls._gaps[current_clip.track].append(gap)
        logger.info("Completed calculating gaps between clips")
        logger.info(f"Gaps - {cls._gaps}")

    @classmethod
    def refresh_clips(cls) -> bool:
        """
        Gets current clips in the project
        Returns: list of clips objects
        """
        # Sorting the data by track and then by start time to ensure correct ordering
        clips_raw = Clip.get_info_clips()
        logger.debug(f"clips_raw: {clips_raw}")
        clips_cleaned = Clip.clean_clips_info(clips_raw)
        logger.debug(f"clips_cleaned: {clips_cleaned}")
        clips_parsed = Clip.parse_get_info_clips(clips_cleaned)
        logger.debug(f"clips_parsed: {clips_parsed}")

        if not clips_parsed or clips_parsed is None:
            return False

        # Re-initialize clips and tracks
        cls._tracks = []
        cls._clips = []

        # Set Class's clips and tracks
        for clip in clips_parsed:
            if clip['start'] >= 0.0 and clip['end'] > 0.0:
                clip['_id'] = "" + \
                    str(clip['track']) + \
                    str(round(clip['start'], 5))
                cls._clips.append(Clip(clip))
                if clip['track'] not in cls._tracks:
                    cls._tracks.append(clip['track'])
        cls.calculate_clips_gaps()
        cls._tracks_with_gaps = [track for track in cls._gaps.keys()]
        return True
