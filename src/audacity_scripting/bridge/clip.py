from ..utils.logger import logger
import json
from .pipe import do_command


class Clip(object):
    def __init__(self, raw_clip):
        self.start = raw_clip['start']
        self.end = raw_clip['end']
        self.track = raw_clip['track']
        self.color = raw_clip['color']

    @staticmethod
    def get_clips() -> list[dict]:
        """
        Gets current clips in the project
        Returns: list of clips objects
        """
        clips_raw = do_command('GetInfo: Type=Clips')

        # Last line is the result of the command
        clips_raw_result = clips_raw.split("\n")[:-1]

        # TODO: Use ENUMs instead of hardcoded text
        success_message = "BatchCommand finished: OK"

        if success_message in clips_raw_result:
            clips_only = clips_raw.replace(success_message, "")
            clips_clean = clips_only.replace("\n", "").replace(" ", "").strip()
            clips_ready = clips_clean[clips_clean.find(
                "["):clips_clean.find("]")+1]
            logger.debug(f"clips_ready: {clips_ready}")
            clips_obj = json.loads(clips_ready)

            # Sorting the data by track and then by start time to ensure correct ordering
            clips_sorted = sorted(
                clips_obj, key=lambda x: (x['track'], x['start']))
            return clips_sorted

        return clips_raw_result
