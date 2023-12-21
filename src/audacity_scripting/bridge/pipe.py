import time
import sys
import os
from wrapt_timeout_decorator import timeout

from ..utils.logger import logger

if sys.platform == 'win32':
    import win32pipe
    import win32file
else:
    # No need to import anything for macOS or Linux
    pass


def send_command(TOFILE, EOL, command, sleep_seconds=0.001):
    """Send a single command."""
    time.sleep(sleep_seconds)
    full_command = command + EOL
    logger.debug(f"Send: >>> '{full_command}'")
    TOFILE.write(full_command)
    if sys.platform == 'win32':
        logger.debug("TOFILE Written")
        TOFILE.flush()
        logger.debug("TOFILE Flushed")
        time.sleep(sleep_seconds)


def get_response(FROMFILE, sleep_seconds=0.005):
    """Return the command response."""
    time.sleep(sleep_seconds)
    result = ''
    line = ''
    while True:
        result += line
        line = FROMFILE.readline()
        if line == '\n' and len(result) > 0:
            break
    logger.debug(f"Result: {result}")
    return result


@timeout(7)  # Lucky Number Slevin (2006)
def do_command_(CMD='GetInfo: Preferences', sleep_seconds=0.007):
    # Initialize variables for Windows and macOS/Linux
    # Pipe names and EOL is set according to - https://manual.audacityteam.org/man/scripting.html
    time.sleep(sleep_seconds)
    pipe_name_send = ''
    pipe_name_from = ''
    pipe_send = None  # For Windows only
    EOL = ''
    if sys.platform == 'win32':
        pipe_name_send = r'\\.\pipe\ToSrvPipe'
        pipe_name_from = r'\\.\pipe\FromSrvPipe'
        EOL = '\r\n\0'
        pipe_send = win32pipe.CreateNamedPipe(
            pipe_name_send,
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
            1, 65536, 65536,
            0,
            None)
        time.sleep(sleep_seconds)
    else:
        # macOS or Linux
        pipe_name_send = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
        pipe_name_from = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
        EOL = '\n'
    logger.debug(f"Trying to access pipe {pipe_send}")
    try:
        time.sleep(sleep_seconds)
        # Open file buffer in write according to the platform
        logger.debug(f"Accessing send pipe - '{pipe_name_send}' ...")
        with open(pipe_name_send, 'w') as fp:
            time.sleep(sleep_seconds)
            logger.debug("Accessed send pipe")
            # Send command to Audacity using the write pipe
            send_command(fp, EOL, CMD)
        time.sleep(sleep_seconds)
        logger.debug(f"Accessing from pipe - '{pipe_name_from}' ...")
        # Open file buffer in text mode - must set encoding as Windows uses cp1252 by default
        with open(pipe_name_from, 'rt', encoding='utf-8') as fp:
            time.sleep(sleep_seconds)
            logger.debug("Accessed from pipe")
            # Get response from Audacity using the read pipe
            response = get_response(fp)
            time.sleep(sleep_seconds)
            logger.debug(f"Response:\n{response}")
            return response
    except OSError as e:
        logger.warning(f"Waiting for pipe to be ready ...")
        raise e
    except Exception as e:
        raise Exception(f"Unhandled Exception: {e}")
    finally:
        if sys.platform == 'win32':
            win32file.CloseHandle(pipe_send)


def do_command(CMD, retry_count=0, retry_max_count=50, sleep_seconds=0.05):
    while retry_count <= retry_max_count:
        retry_count += 1
        try:
            return do_command_(CMD)
        except OSError as e:
            logger.warning(f"Retrying {retry_count}/{retry_max_count}")
            time.sleep(1)  # Hardcoded 1 second
        except Exception as e:
            logger.error(
                f"Error while executing command. Retrying {retry_count}/{retry_max_count} - {e}")
            time.sleep(sleep_seconds)
        finally:
            if retry_count > retry_max_count:
                raise Exception(f"Failed to execute command: {CMD}")


if __name__ == '__main__':
    do_command()
