from unittest import TestCase
from audacity_scripting.bridge.clip import Clip
from audacity_scripting.bridge.pipe import do_command
from src.audacity_scripting.bridge.wrappers import add_labels_to_clips, remove_spaces_between_clips, open_project_copy
from pathlib import Path
from src.audacity_scripting.utils.logger import logger
from src.audacity_scripting.utils.enums import AudacityCommandStatus

test_file_relative_path = 'tests/data/input/1.aup3'
test_file_path = Path.cwd().joinpath(test_file_relative_path)


class WrappersTestCase(TestCase):

    @staticmethod
    def run_test_and_compare(file_extra_label, operation_func, *args, **kwargs):
        expected_file_path = Path.cwd().joinpath(
            f'tests/data/expected/1.expected{file_extra_label}.aup3')
        new_file_path = open_project_copy(
            test_file_path, file_extra_label=file_extra_label)

        result = operation_func(new_file_path, *args, **kwargs)
        logger.info(f"result: {result}")

        Clip.refresh_clips()
        new_clips_info_json = Clip.to_json()
        logger.info(f"new_clips_info: {new_clips_info_json}")

        open_project_copy(expected_file_path)
        Clip.refresh_clips()
        expected_clips_info = Clip.to_json()
        logger.info(f"expected_clips_info: {expected_clips_info}")
        return result and new_clips_info_json == expected_clips_info

    def test_1_remove_spaces_between_clips(self):
        self.assertTrue(self.run_test_and_compare(
            '.remove_spaces_between_clips',
            remove_spaces_between_clips
        ))

    def test_2_good_raw_command(self):
        result = do_command("Select: Start=0.0 Track=0.0")
        logger.info(f"test_2_good_raw_command result: {result}")
        self.assertTrue(AudacityCommandStatus.SUCCESS.value in result)

    def test_3_bad_raw_command(self):
        result = do_command("Corrupt: Start=0.0 Track=0.0")
        logger.info(f"test_3_bad_raw_command result: {result}")
        self.assertTrue(AudacityCommandStatus.FAIL.value in result)

    def test_4_add_labels_to_clips(self):
        self.assertTrue(self.run_test_and_compare(
            '.add_labels_to_clips',
            add_labels_to_clips,
            start_label_iterator=40
        ))

    def test_5_remove_labels(self):
        pass
