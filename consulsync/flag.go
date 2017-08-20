package consync

import (
	"github.com/pelletier/go-toml"
	"regexp"
	"strconv"
	"github.com/pkg/errors"
)

type FlagPlugin struct {
	configuration *toml.TomlTree
}

func (FlagPlugin) collectResources(resources []Resource) ([]Resource, error) {
	return resources, nil;

}

func (FlagPlugin) read(resource *Resource) error {
	return nil
}

func (plugin FlagPlugin) transformContent(resources *[]Resource, resource *Resource) error {
	if (plugin.configuration.Get("flags") != nil) {
		for _, flag := range plugin.configuration.Get("flags").(*toml.TomlTree).Keys() {
			pattern := plugin.configuration.Get("flags." + flag).(string)
			matched, error := regexp.MatchString(pattern, resource.name)
			if (error != nil) {
				return error
			}
			if matched {
				flagInt, err := strconv.Atoi(flag)
				if err != nil {
					return errors.New("flag property name should be in instead of " + flag)
				}
				resource.flag += flagInt
			}
		}
	}

	return nil

}
