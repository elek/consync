package consync

import "testing"
import "github.com/stretchr/testify/assert"

func TestTemplatePluginTransformContent(t *testing.T) {
	plugin := TemplatePlugin{}

	resources := []Resource{
		Resource{"test.txt", "/tmp/test.txt", "{{ template \"test2.txt\"}}f", []string{}},
		Resource{"test2.txt", "/tmp/test2.txt", "bsd", []string{}},
	}
	err := plugin.transformContent(&resources, &resources[0])
	if err != nil {
		t.Fatal(err.Error())
	}
	assert.Equal(t, "bsdf", resources[0].content)
}