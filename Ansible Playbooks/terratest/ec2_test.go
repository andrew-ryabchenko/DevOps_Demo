package terratest

import (
	"encoding/pem"
	"fmt"
	"io/ioutil"
	"log"
	"testing"
	"time"

	"github.com/gruntwork-io/terratest/modules/retry"
	"github.com/gruntwork-io/terratest/modules/ssh"
	"github.com/gruntwork-io/terratest/modules/terraform"
)

func CheckSsh(t *testing.T, hosts *[]map[string]string, len int) (string, error) {
	fileContent, err := ioutil.ReadFile("../andrew.pem")
	if err != nil {
		log.Fatal(err)
	}
	pemBlock, _ := pem.Decode(fileContent)

	privateKey := string(pemBlock.Bytes)
	fmt.Println(privateKey)

	keyPair := ssh.KeyPair{
		PrivateKey: privateKey,
	}

	for i := 0; i < len; i++ {
		host := ssh.Host{
			Hostname:    (*hosts)[i]["host"],
			SshUserName: (*hosts)[i]["uname"],
			SshKeyPair:  &keyPair,
			SshAgent:    true,
		}

		err := ssh.CheckSshConnectionE(t, host)
		if err != nil {
			return "", err
		}
	}
	return "", nil
}
func TestEc2(t *testing.T) {

	var options *terraform.Options = &terraform.Options{
		// Set the path to the Terraform code that will be tested.
		TerraformDir: "../tf_infrastructure",
	}

	options = terraform.WithDefaultRetryableErrors(t, options)

	defer terraform.Destroy(t, options)

	terraform.InitAndApply(t, options)

	var output []map[string]string
	rawOutput := terraform.OutputListOfObjects(t, options, "host_ips")
	for _, item := range rawOutput {
		stringMap := make(map[string]string)
		for key, value := range item {
			stringMap[key] = value.(string)
		}
		output = append(output, stringMap)
	}

	closure := func() (string, error) {
		return CheckSsh(t, &output, 3)
	}

	var retryInterval time.Duration = 6e10

	retry.DoWithRetry(t, "Check SSH connection", 2, retryInterval, closure)
}
