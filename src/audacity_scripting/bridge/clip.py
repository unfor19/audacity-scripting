from ..utils.logger import logger
import json
from .pipe import do_command


class Clip:
    _registry = []
    _tracks = set()  # Use a set for faster lookups

    def __init__(self, raw_clip):
        self.start = max(round(raw_clip['start'], 5), 0.0)
        self.end = round(raw_clip['end'], 5)
        self.duration = round(self.end - self.start, 5)
        self.end = round(self.start + self.duration, 5)  # Is this necessary?
        self.track = raw_clip['track']
        self.color = raw_clip['color']

    def copy(self):
        """
        Create a shallow copy of the Clip instance.
        """
        copied_clip_data = {
            'start': self.start,
            'end': self.end,
            'duration': self.duration,
            'track': self.track,
            'color': self.color
        }
        return Clip(copied_clip_data)

    @classmethod
    def to_json(cls):
        return [json.dumps(clip.__dict__) for clip in cls._registry]

    @classmethod
    def to_objects(cls):
        return cls._registry

    @classmethod
    def get_num_tracks(cls):
        return len(cls._tracks)

    @classmethod
    def get_clips(cls):
        clips_raw = do_command('GetInfo: Type=Clips')
        success_message = "BatchCommand finished: OK"
        if success_message not in clips_raw:
            return []

        # Extracting clips data
        clips_json = clips_raw.split(success_message)[0].strip()
        clips_data = json.loads(clips_json)

        # Sorting and filtering clips
        valid_clips = [c for c in clips_data if c['start']
                       >= 0.0 and c['end'] > 0.0]
        sorted_clips = sorted(
            valid_clips, key=lambda x: (x['track'], x['start']))

        # Creating Clip objects and updating class attributes
        cls._registry = [Clip(clip) for clip in sorted_clips]
        cls._tracks.update(clip.track for clip in cls._registry)
        return cls._registry

    def __str__(self):
        return json.dumps(self.__dict__)
