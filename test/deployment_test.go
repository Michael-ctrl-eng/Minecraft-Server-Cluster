package test  

import (  
  "testing"  
  "github.com/gruntwork-io/terratest/modules/k8s"  
)  

func TestMinecraftDeployment(t *testing.T) {  
  kubectlOptions := k8s.NewKubectlOptions("", "", "minecraft")  
  k8s.WaitUntilDeploymentAvailable(t, kubectlOptions, "minecraft", 10, 5*time.Second)  
}  
