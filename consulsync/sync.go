package consync

import (
	"strings"
	"path/filepath"
	"os"
	"io/ioutil"
	"github.com/pelletier/go-toml"
	"path"
	"flag"
)

type Resource struct {
	name    string
	path    string
	content string
	sources []string
	flag    int
}

func (resource *Resource) String() string {
	return resource.path + " " + strings.Join(resource.sources, "")
}

type Adapter interface {
	write(resource Resource) error
}

type Plugin interface {
	collectResources(resources []Resource) ([]Resource, error)

	read(resource *Resource) error

	transformContent(resources *[]Resource, resource *Resource) error
}
type ReadPlugin struct {
	rootdir       string
	configuration *toml.TomlTree
}
type Configuration *toml.TomlTree

func (r ReadPlugin) collectResources(resources []Resource) ([]Resource, error) {
	result := resources

	configdir := path.Join(r.rootdir, (r.configuration.GetDefault("common.sourcedir", "configuration")).(string))
	err := filepath.Walk(configdir, func(path string, file os.FileInfo, err error) error {
		if (!file.IsDir()) {
			relpath, _ := filepath.Rel(configdir, path)
			if (!strings.HasPrefix(relpath, ".")) {
				resource := Resource{relpath, path, "", []string{relpath}, 0}
				result = append(result, resource)
			}
		}
		return nil
	})
	if (err != nil) {
		return result, err
	}
	return result, nil

}

func (r ReadPlugin) read(resource *Resource) error {
	content, err := ioutil.ReadFile(resource.path)
	if (err != nil) {
		return err
	}
	resource.content = string(content)
	return nil
}

func (r ReadPlugin) transformContent(resources *[]Resource, resource *Resource) error {
	return nil
}

func Run() {
	var rootdir = flag.String("dir", ".", "Configuration directory structure")
	var consulHost = flag.String("consul", "", "Host of the consul server")
	var discovery = flag.String("discovery", "static", "Service discovery type (static,dns,consul)")
	var profilesstr = flag.String("profiles", "", "Activated profiles (from the profiles directory)")
	flag.Parse()

	var profiles = strings.Split(*profilesstr, ",")

	if len(profiles) == 1 && profiles[0] == "" {
		profiles = []string{}
	}

	config, err := toml.LoadFile(path.Join(*rootdir, "consync.ini"))
	if err != nil {
		panic(err)
	}

	var adapter Adapter
	if (*consulHost != "") {
		adapter, err = ConnectToConsul(*consulHost, "conf")
		if err != nil {
			panic(err)
		}
	} else {
		adapter = ConsolAdapter{}
	}
	plugins := []Plugin{
		ReadPlugin{*rootdir, config},
		ProfilePlugin{*rootdir, config, profiles},
		TemplatePlugin{config, discovery},
		FlagPlugin{config},
		TransformPlugin{config},
	}
	resources := make([]Resource, 0)

	for _, plugin := range plugins {
		resources, err = plugin.collectResources(resources)
		if (err != nil) {
			panic(err)
		}
	}

	for idx, _ := range resources {
		for _, plugin := range plugins {
			plugin.read(&resources[idx])
		}
	}

	for _, plugin := range plugins {
		for idx, _ := range resources {
			err = plugin.transformContent(&resources, &resources[idx])
			if err != nil {
				panic(err)
			}
		}
	}

	for _, resource := range resources {
		err = adapter.write(resource)
		if err != nil {
			panic(err)
		}
	}

}
