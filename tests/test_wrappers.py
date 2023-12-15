import hashlib
from unittest import TestCase
from audacity_scripting.bridge.clip import Clip
from audacity_scripting.bridge.pipe import do_command
from audacity_scripting.bridge.project import open_project, save_project, save_project_as
from src.audacity_scripting.bridge.wrappers import remove_spaces_between_clips, open_project_copy
from pathlib import Path

test_file_relative_path = 'tests/data/input/1.aup3'


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class WrappersTestCase(TestCase):
    def test_1_remove_spaces_between_clips(self):
        test_file_path = Path.cwd().joinpath(test_file_relative_path)
        expected_file_path = Path.cwd().joinpath(
            'tests/data/expected/1.expected.remove_spaces_between_clips.aup3')
        new_file_path = open_project_copy(
            test_file_path, 'remove_spaces_between_clips')
        result = remove_spaces_between_clips(new_file_path)
        new_clips_info = Clip.get_clips()
        open_project_copy(expected_file_path)
        expected_clips_info = Clip.get_clips()
        self.assertTrue(new_clips_info, expected_clips_info)

    def test_2_raw_command(self):
        result = do_command("Select: Start=0.0 Track=0.0")
        self.assertTrue("BatchCommand finished: OK" in result)
