package consync

import (
	"bytes"
	"html/template"
	"os"
)

type TemplatePlugin struct {
	configuration Configuration
}

func (TemplatePlugin) collectResources(resources []Resource) ([]Resource, error) {
	return resources, nil;

}

func (TemplatePlugin) read(resource *Resource) error {
	return nil
}
func service(name string) string {
	if gateway, defined := os.LookupEnv("GATEWAY_HOST"); defined {
		return gateway
	} else {
		return name
	}
}
func (TemplatePlugin) transformContent(resources *[]Resource, resource *Resource) error {
	var err error
	funcmap := template.FuncMap{
		"service": service,
	}
	tmpl := template.New(resource.name)
	tmpl = tmpl.Funcs(funcmap)
	tmpl, err = tmpl.Parse(resource.content)
	if err != nil {
		return err
	}

	for _, rsc := range *resources {

		tmpl = tmpl.New(rsc.name)
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
