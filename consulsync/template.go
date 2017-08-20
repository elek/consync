package consync

import (
	"bytes"
	"text/template"
	"os"
)

type TemplatePlugin struct {
	configuration Configuration
	discovery     *string
}

func (TemplatePlugin) collectResources(resources []Resource) ([]Resource, error) {
	return resources, nil;

}

func (TemplatePlugin) read(resource *Resource) error {
	return nil
}

type DiscoveryFunc func(string) string

func dnsDiscovery(name string) string {
	return name;
}
func staticDiscovery(name string) string {
	if gateway, defined := os.LookupEnv("GATEWAY_HOST"); defined {
		return gateway
	} else {
		return "localhost"
	}
}
func consulDiscovery(name string) string {
	//return "x"
	return "{{ service \"" + name + "\" | hosts \".\"}}"
}
func getDiscoveries() map[string]DiscoveryFunc {
	result := make(map[string]DiscoveryFunc)
	result["dns"] = dnsDiscovery
	result["consul"] = consulDiscovery
	result["static"] = staticDiscovery
	return result
}

func (plugin TemplatePlugin) transformContent(resources *[]Resource, resource *Resource) error {
	var err error

	funcmap := template.FuncMap{
		"service": getDiscoveries()[*plugin.discovery],
	}
	tmpl := template.New(resource.name)
	tmpl = tmpl.Funcs(funcmap)
	tmpl = tmpl.Delims("[[", "]]")
	tmpl, err = tmpl.Parse(resource.content)
	if err != nil {
		return err
	}

	for _, rsc := range *resources {

		tmpl = tmpl.New(rsc.name)
	 	tmpl = tmpl.Delims("[[", "]]")
		tmpl, err = tmpl.Parse(rsc.content)
		if err != nil {
			return err
		}

	}

	if err != nil {
		return err
	}
	buffer := new(bytes.Buffer)
	variables := make(map[string]string)
	err = tmpl.ExecuteTemplate(buffer, resource.name, variables)
	if err != nil {
		return err
	}
	resource.content = buffer.String()
	return nil

}
