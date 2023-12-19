package core

import (
	"bufio"
	"os"
	"strings"
)

func _sendCommand(pipe_send_path string, eol string, command string) {
	toFile, _ := os.OpenFile(pipe_send_path, os.O_WRONLY, os.ModeNamedPipe)
	fullCommand := command + eol
	toFile.WriteString(fullCommand)
	toFile.Sync()
	toFile.Close()
}

func _getResponse(pipe_from_path string) string {
	fromFile, _ := os.OpenFile(pipe_from_path, os.O_RDONLY, os.ModeNamedPipe)
	reader := bufio.NewReader(fromFile)
	var result = ""
	var line = ""
	for {
		result += line
		byte_line, _, err := reader.ReadLine()
		if err != nil {
			// Pipe is broken
			break
		}
		line = string(byte_line)
		if line != "\n" && len(result) > 0 {
			break
		}
	}
	result = strings.Trim(result, "\n")
	return result
}

//export Api
func Api(command string) string {
	eol := "\n" // End of line character based on platform
	const pipe_send_path = "/tmp/audacity_script_pipe.to.501"
	const pipe_from_path = "/tmp/audacity_script_pipe.from.501"
	_sendCommand(pipe_send_path, eol, command)
	response := _getResponse(pipe_from_path)
	return response
}
