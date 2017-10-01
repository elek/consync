package consync

import (
	"github.com/pelletier/go-toml"
	"path/filepath"
	"strings"
	"path"
	"os"
	"io/ioutil"
	"fmt"
)

type ProfilePlugin struct {
	rootdir       string
	configuration *toml.TomlTree
	profiles      []string
}

func (plugin ProfilePlugin) collectResources(resources []Resource) ([]Resource, error) {
	if len(plugin.profiles) == 0 {
		return resources, nil
	}
	result := resources
	resourcesByPath := make(map[string]*Resource)
	for _, resource := range resources {
		resourcesByPath[resource.name] = &resource
	}
	for _, profile := range (plugin.profiles) {
		configdir := path.Join(plugin.rootdir, (plugin.configuration.GetDefault("profiles.dir", "profiles")).(string), profile)

		err := filepath.Walk(configdir, func(path string, file os.FileInfo, err error) error {
			if (!file.IsDir()) {
				relpath, _ := filepath.Rel(configdir, path)
				if (!strings.HasPrefix(relpath, ".")) {
					if _, ok := resourcesByPath[relpath]; ok {
						resourcesByPath[relpath].sources = append(resourcesByPath[relpath].sources, path)
					} else {
						resource := Resource{relpath, path, "", []string{relpath}, 0}
						result = append(result, resource)
					}
				}
			}
			return nil
		})

		if (err != nil) {
			return result, err
		}
	}
	return result, nil
}

func (plugin ProfilePlugin) read(resource *Resource) error {
	for _, profile := range (plugin.profiles) {
		path := path.Join(plugin.rootdir, (plugin.configuration.GetDefault("profiles.dir", "profiles")).(string), profile, resource.name)
		if _, err := os.Stat(path); !os.IsNotExist(err) {
			content, err := ioutil.ReadFile(path)
			if (err != nil) {
				return err
			}
			resource.content = fmt.Sprintf("%s\n%s", resource.content, string(content))
		}
	}
	return nil
}

func (plugin ProfilePlugin) transformContent(resources *[]Resource, resource *Resource) error {
	return nil
}
