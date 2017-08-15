package consync

import (
	"github.com/hashicorp/consul/api"
	"path"
	"fmt"
)

type ConsulAdapter struct {
	client *api.Client
	prefix string
}

func ConnectToConsul(host string, prefix string) (ConsulAdapter, error) {
	consul := ConsulAdapter{}
	consul.prefix = prefix
	var err error
	config := api.DefaultConfig()
	config.Address = "http://" + host + ":8500"
	consul.client, err = api.NewClient(config)
	if err != nil {
		return consul, err
	}
	return consul, nil
}

func (consul ConsulAdapter) write(resource Resource) error {
	// Get a handle to the KV API
	kv := consul.client.KV()

	key := path.Join(consul.prefix, resource.name)
	p := &api.KVPair{Key: key, Value: []byte(resource.content)}
	_, err := kv.Put(p, nil)
	if err != nil {
		return err
	}
	fmt.Println("Key has been written to the consul: " + key)
	return nil
}
