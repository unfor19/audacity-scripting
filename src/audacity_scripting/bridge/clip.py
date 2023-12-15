from ..utils.logger import logger
import json
from .pipe import do_command


class Clip(object):
    _registry = []
    _tracks = []

    def __init__(self, raw_clip):
        self.start = round(raw_clip['start'], 5)
        self.end = round(raw_clip['end'], 5)
        if self.start <= 0.0:
            self.start = 0.0
        self.duration = round(self.end - self.start, 5)
        self.end = round(self.start + self.duration, 5)
        self.track = raw_clip['track']
        self.color = raw_clip['color']

    @classmethod
    def to_json(cls):
        json_list = [clip.__str__() for clip in cls._registry]
        return json_list

    @classmethod
    def to_objects(self):
        return self._registry

    def __str__(self):
        return json.dumps({
            "start": self.start,
            "end": self.end,
            "duration": self.duration,
            "track": self.track,
            "color": self.color
        })

    @classmethod
    def get_num_tracks(cls):
        return len(cls._tracks)

    @staticmethod
    def get_clips() -> [object]:
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
            clips_final = []
            for raw_clip in clips_sorted:
                if raw_clip['start'] >= 0.0 and raw_clip['end'] > 0.0:
                    raw_clip['_id'] = "" + \
                        str(raw_clip['track']) + \
                        str(round(raw_clip['start'], 5))
                    clips_final.append(Clip(raw_clip))
                    if raw_clip['track'] not in Clip._tracks:
                        Clip._tracks.append(raw_clip['track'])
            Clip._registry = clips_final
            return clips_final
        return clips_raw_result
