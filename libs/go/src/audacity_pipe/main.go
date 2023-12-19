package audacity_pipe

import (
	"audacity_pipe/core"
	"fmt"
	"os"
	"os/signal"
	"syscall"
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
	c := make(chan os.Signal)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-c
		os.Exit(1)
	}()
	return core.Api(command)
}
