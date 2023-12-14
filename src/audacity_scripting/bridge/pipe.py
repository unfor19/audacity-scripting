from io import TextIOWrapper
import json
import os
import sys
from time import sleep
from ..utils.logger import logger

if sys.platform == 'win32':
    import win32file
    import pywintypes

    def is_named_pipe_open(pipe_name):
        try:
            # Attempt to open the named pipe
            handle = win32file.CreateFile(
                pipe_name,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            # Close the handle if successful
            win32file.CloseHandle(handle)
            return True
        except pywintypes.error as e:
            # Check the specific error
            if e.args[0] == 2:  # ERROR_FILE_NOT_FOUND
                return False
            elif e.args[0] == 231:  # ERROR_PIPE_BUSY
                return True
            else:
                raise


def send_command(TOFILE: TextIOWrapper, EOL, command, close, flush):
    """Send a single command."""
    full_command = command + EOL
    logger.debug(f"Send: >>> '{full_command}'")
    TOFILE.write(full_command)
    if flush:
        TOFILE.flush()
    if close:
        TOFILE.close()


def get_response(FROMFILE: TextIOWrapper, EOL, close, flush):
    """Return the command response."""
    result = ''
    line = ''
    while True:
        result += line
        line = FROMFILE.readline()
        if line == '\n' and len(result) > 0:
            break
    logger.debug(f"Result: {result}")
    if close:
        FROMFILE.close()
    if flush:
        FROMFILE.flush()
    return result


def do_command(command, retry_max_count=100):
    TONAME = ''
    FROMNAME = ''
    EOL = ''
    WRITE_MODE = ''
    READ_MODE = ''
    CLOSE_READ = True
    CLOSE_WRITE = True
    SLEEP_SECONDS = 0.01
    FLUSH_READ = False
    FLUSH_WRITE = False
    """Send one command, and return the response."""
    # Based on the official pipe_test.py - https://github.com/audacity/audacity/blob/master/scripts/piped-work/pipe_test.py
    if sys.platform == 'win32':
        logger.debug("pipe-test.py, running on windows")
        TONAME = '\\\\.\\pipe\\ToSrvPipe'
        FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
        EOL = '\r\n\0'
        READ_MODE = 'rt'
        WRITE_MODE = 'w'
        CLOSE_READ = False
        CLOSE_WRITE = False
        SLEEP_SECONDS = 0.1
        FLUSH_READ = True
    else:
        logger.debug("pipe-test.py, running on linux or mac")
        TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
        FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
        EOL = '\n'
        READ_MODE = 'rt'
        WRITE_MODE = 'w'
    logger.debug(
        f'EOL:{json.dumps(EOL)}, TONAME:{TONAME}, FROMNAME:{FROMNAME}')
    logger.debug("Read from \"" + FROMNAME + "\"")
    logger.debug("Write to \"" + TONAME + "\"")
    retry_count = 0
    while retry_count < retry_max_count:
        retry_count += 1
        try:
            if sys.platform == 'win32':
                # if not is_named_pipe_open(TONAME):
                if not os.path.exists(TONAME):
                    if retry_count == retry_max_count:
                        logger.error(
                            "Failed to connect to Audacity with pipes")
                        sys.exit(1)
                # if not is_named_pipe_open(FROMNAME):
                if not os.path.exists(FROMNAME):
                    if retry_count == retry_max_count:
                        logger.error(
                            "Failed to connect to Audacity with pipes")
                        sys.exit(1)
            else:
                if not os.path.exists(TONAME):
                    if retry_count == retry_max_count:
                        logger.error(
                            "Failed to connect to Audacity with pipes")
                        sys.exit(1)
                if not os.path.exists(FROMNAME):
                    if retry_count == retry_max_count:
                        logger.error(
                            "Failed to connect to Audacity with pipes")
                        sys.exit(1)
                break
        except Exception as e:
            logger.debug(
                f"'{e}. Ensure Audacity is running with mod-script-pipe.")
        sleep(SLEEP_SECONDS)

    logger.debug("-- Both pipes exist.  Good.")
    TOFILE = open(TONAME, WRITE_MODE)
    logger.debug("-- File to write to has been opened")
    FROMFILE = open(FROMNAME, READ_MODE)
    logger.debug("-- File to read from has now been opened too\r\n")
    sleep(SLEEP_SECONDS)
    send_command(TOFILE, EOL, command, close=CLOSE_WRITE, flush=FLUSH_WRITE)
    sleep(SLEEP_SECONDS)
    response = get_response(
        FROMFILE, EOL=EOL, close=CLOSE_READ, flush=FLUSH_READ)
    sleep(SLEEP_SECONDS)
    return response
