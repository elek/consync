package consync

import (
	"regexp"
	"github.com/elek/envtoconf/app"
	"strings"
	"fmt"
	"github.com/pelletier/go-toml"
)

type TransformPlugin struct {
	configuration *toml.TomlTree
}

func (TransformPlugin) collectResources(resources []Resource) ([]Resource, error) {
	return resources, nil;

}

func (TransformPlugin) read(resource *Resource) error {
	return nil
}

func (plugin TransformPlugin) transformContent(resources *[]Resource, resource *Resource) error {
	if (plugin.configuration.Get("format") != nil) {
		for _, format := range plugin.configuration.Get("format").(*toml.TomlTree).Keys() {
			pattern := plugin.configuration.Get("format." + format).(string)
			matched, error := regexp.MatchString(pattern, resource.name)
			if (error != nil) {
				return error
			}
			if (matched) {
				transformed, err := app.TransformToString(parseContent(resource.name, resource.content), format)
				if err == nil {
					resource.content = transformed
				} else {
					resource.content = "Error on transformation: " + err.Error()
				}
			}
		}
	}
	return nil
}
func parseContent(name string, content string) map[string]string {
	results := make(map[string]string)
	for _, line := range strings.Split(content, "\n") {
		line = strings.TrimSpace(line)
		if len(line) > 0 && line[0] != '#' {
			parts := strings.SplitN(line, ":", 2)
			if (len(parts) != 2) {
				fmt.Println("Error in line (" + name + "): " + line)
			} else {
				results[parts[0]] = strings.TrimSpace(parts[1])
			}
		}
	}
	return results
}