package audacity_pipe

import (
	"audacity_pipe/core"
	"fmt"
)

func main() {}

func TestPrint() {
	const command string = "Select: Start=0.0  End=0.0 Track=0.0"
	var response string = core.Api(command)
	fmt.Println("Received:", response)
}

func TestReturn() string {
	const command string = "Select: Start=0.0  End=0.0 Track=0.0"
	var response string = core.Api(command)
	return response
}

func Api(command string) string {
	return core.Api(command)
}
