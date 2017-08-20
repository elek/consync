package consync

import (
	"fmt"
	"strconv"
)

type ConsolAdapter struct {

}

func (ConsolAdapter) write(resource Resource) error {
	fmt.Println("===================")
	fmt.Println(resource.path + "(" + strconv.Itoa(resource.flag) + ")")
	fmt.Println(resource.sources)
	fmt.Println("-------------------")
	fmt.Println(resource.content)
	fmt.Println("-------------------")

	return nil
}


