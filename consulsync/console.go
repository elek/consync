package consync

import "fmt"

type ConsolAdapter struct {

}

func (ConsolAdapter) write(resource Resource) error {
	fmt.Println("===================")
	fmt.Println(resource.path)
	fmt.Println(resource.sources)
	fmt.Println("-------------------")
	fmt.Println(resource.content)
	fmt.Println("-------------------")

	return nil
}


