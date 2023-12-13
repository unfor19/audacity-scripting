from unittest import TestCase
from audacity_scripting.bridge.pipe import do_command
from src.audacity_scripting.bridge.wrappers import remove_spaces_between_clips, open_project_copy
from pathlib import Path
from time import sleep
import filecmp

test_file_relative_path = 'tests/data/1.aup3'
expected_file_path = 'tests/data/expected/1.expected.aup3'


class WrappersTestCase(TestCase):
    gaps = dict()

    def test_1_openproject(self):
        test_file_path = Path.cwd().joinpath(test_file_relative_path)
        new_file_path = open_project_copy(test_file_path)
        sleep(1.5)  # To wait for timestamp to be different
        self.assertTrue(new_file_path)

    def test_2_remove_spaces_between_clips(self):
        test_file_path = Path.cwd().joinpath(test_file_relative_path)
        new_file_path = open_project_copy(test_file_path)
        result = remove_spaces_between_clips()
        self.assertTrue(new_file_path and result and len(self.gaps) == 0 and filecmp.cmp(
            expected_file_path, new_file_path, shallow=False))

    def test_3_raw_command(self):
        result = do_command("Select: Start=0.0 End=1.0 Track=0.0")
        self.assertTrue("BatchCommand finished: OK" in result)
