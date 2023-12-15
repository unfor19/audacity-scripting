
""""
Source - https://github.com/unfor19/audacity-scripting

Instructions:
1. Start Audacity
2. Enable mod-script-pipe - https://manual.audacityteam.org/man/scripting.html
3. Restart Audacity
4. (Windows) Install pywin32 - `pip install pywin32`
4. (Windows) Download "pipelist" - https://learn.microsoft.com/en-us/sysinternals/downloads/pipelist
5. (Windows) Run "pipelist" to make sure Audacity's pipes are available - "FromSrvPipe" and "ToSrvPipe"
6. Run this script to send a command to Audacity and get the response

Usage:
   python audacity_pipetest.py
"""

import time
import sys
import os

if sys.platform == 'win32':
    import win32pipe
    import win32file
else:
    # No need to import anything for macOS or Linux
    pass


def send_command(TOFILE, EOL, command):
    """Send a single command."""
    time.sleep(0.5)
    full_command = command + EOL
    print(f"Send: >>> '{full_command}'")
    TOFILE.write(full_command)
    print("TOFILE Written")
    TOFILE.flush()
    print("TOFILE Flushed")


def get_response(FROMFILE):
    """Return the command response."""
    result = ''
    line = ''
    while True:
        result += line
        line = FROMFILE.readline()
        if line == '\n' and len(result) > 0:
            break
    print(f"Result: {result}")
    return result


def main():
    # Initialize variables for Windows and macOS/Linux
    # Pipe names and EOL is set according to - https://manual.audacityteam.org/man/scripting.html
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
    else:
        # macOS or Linux
        pipe_name_send = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
        pipe_name_from = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
        EOL = '\n'
    print(f"Trying to access pipe {pipe_send}")
    try:
        # Set command to send to Audacity
        # According to -
        CMD = f'GetInfo: Preferences'  # Sample command

        # Open file buffer in write according to the platform
        print(f"Accessing send pipe - '{pipe_name_send}' ...")
        with open(pipe_name_send, 'w') as fp:
            print("Accessed send pipe")
            # Send command to Audacity using the write pipe
            send_command(fp, EOL, CMD)

        print(f"Accessing from pipe - '{pipe_name_from}' ...")
        # Open file buffer in text mode - must set encoding as Windows uses cp1252 by default
        with open(pipe_name_from, 'rt', encoding='utf-8') as fp:
            print("Accessed from pipe")
            # Get response from Audacity using the read pipe
            response = get_response(fp)
            print(f"Response:\n{response}")
    except Exception as e:
        raise e
    finally:
        if sys.platform == 'win32':
            win32file.CloseHandle(pipe_send)


if __name__ == '__main__':
    main()
