import win32file
import pywintypes


def is_named_pipe_open(pipe_name):
    try:
        # Attempt to open the named pipe
        handle = win32file.CreateFile(
            pipe_name,
            win32file.GENERIC_READ,
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


pipe_name = '\\\\.\\pipe\\FromSrvPipe'
print(is_named_pipe_open(pipe_name))
