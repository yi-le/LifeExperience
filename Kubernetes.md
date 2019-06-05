![ascending logo](https://ascendingdc.com/images/WechatIMG116.jpg) ![apn logo](https://ascendingdc.com/images/aws.png)

# Continuous Deployment on Kubernetes Platform using AWS CodePipeline

In this article:
- Why Kubernetes
- Create Kubernetes Platform in AWS
- Kubectl Tool and Kubernetes API
- Architecture: Continuous Deployment to Kubernetes
- Essential Part: Deploy New Version through Kubernetes API or Kubectl
- Comparision Between CodeBuild and Lambda

## Why Kubernetes

Kubernetes is a portable, extensible open-source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation. Kubernetes uses persistent entities to represent the state of cluster in *.yaml* format. Thus, all of the tasks can be managed in a more consistent way, no matter it’s in on-promise server, cloud computing platform or hybrid cloud environment.

AWS provides Elastic Container Service (Amazon ECS) as a highly scalable, fast, container management service that makes it easy to run, stop, and manage Docker containers on a cluster. ECS components (e.g. services, tasks) can be defined as *.yaml* format within CloudFormation template.

AWS also released Amazon Elastic Container Service for Kubernetes ([AWS EKS](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html)) in 2018. It’s a managed service that makes it easy for users to run Kubernetes on AWS without needing to stand up or maintain their own Kubernetes control plane.

| | ECS | Kubernetest Platform in AWS | EKS |
| --- | --- | --- | --- |
| Application Scalability Constructs | Applications can be defined using task definitions written in YAML. Tasks are instantiations of task definitions and can be scaled up or down manually. | Each application tier is defined as a pod and can be scaled when managed by a deployment, which is specified declaratively, e.g., in YAML. | Each application will be defined and scaled in the level of pods and EC2 instances. |
| High Availability | Deployments allow pods to be distributed among nodes to provide HA, thereby tolerating infrastructure or application failures. | Schedulers place tasks, which are comprised of 1 or more containers, on EC2 container instances. | AWS provides the HA of EKS cluster, while developers can enhance the availability of worker nodes by implementing multi-AZ. | 
| Interoperability | Amazon ECS is tightly integrated with other Amazon services, it relies on other Amazon services, such as Identity and Access Management (IAM), Domain Name System (Route 53), Elastic Load Balancing (ELB), and EC2. | Kubernetes can be either on on-premise servers, AWS or mixed cloud environment. It can be interacted, but not neccessarily, with cloud resources | The EKS cluster relies on AWS (including subnet, security groups and IAM) |
| Rolling Application Upgrades and Rollback | Rolling updates are supported using "minimumHealthyPercent" and "maximumPercent" parameters. | A deployment  supports both "rolling-update" and "recreate" strategies. Rolling updates can specify maximum number of pods. | Same as regular Kubernetest platform |
| Disadvantages | ECS is not publicly available for deployment outside Amazon, which means it can not be implemented in hybrid cloud environment | The installation process is complex (fortunately we have [Kops](https://github.com/kubernetes/kops)) | Easy to use, but not cost-effective |

## Create Kubernetes Platform in AWS

Kops is a tool which can automate the provisioning of Kubernetes clusters in AWS. Users can either create new AWS resources including security group, subnet and SSH key pair or using existing AWS resources. [Kops](https://github.com/kubernetes/kops) is a free, open source tool, and users only pay for AWS resources like EC2 instances, NAT gateway and load balancer. Please refer [this article](https://github.com/kubernetes/kops/blob/master/docs/aws.md) to distribute Kubernetes master and slave servers in AWS, install and configure **kubectl**. Then try

```bash 
kubectl get pods
```
Following result will be returned.

![kube_node](https://s3.amazonaws.com/ascending-devops/ascending-conf/kube_node.png)

A standard Kubernetes Cluster has one master node and at least one worker nodes. Kubernetes master covers controller-manager, API server, scheduler and some other functions, while nodes maintains running pods and provides the Kubernetes runtime environment.

![kube-architecture](https://d33wubrfki0l68.cloudfront.net/e298a92e2454520dddefc3b4df28ad68f9b91c6f/70d52/images/docs/pre-ccm-arch.png)

In AWS, one single EC2 instance can work either as a master or node server.

## Kubectl Tool and Kubernetes API

In Kubernetes, the state of cluster, including the containerized applications running situation, available resources and applications behave policies, upgrades, and fault-tolerance, can be represented by Kubernetes object. 

A Kubernetes object is purpose-oriented, yaml-styled and status-granted concept in Kubernetes system. A typical Kubernetes object can be seen below

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox
    command: ['sh', '-c', 'echo ${DEMO_GREETING} && sleep 3600']
    env:
    - name: DEMO_GREETING
      value: "Hello Kubernetes!"
```

To create, modify or delete Kubernetes objects, users need to interact with Kubernetes cluster via Kubernetes API. Kubernetes tool like kubectl is also optional, in that case, the CLI makes the necessary Kubernetes API calls for you. For example, the command **kubclt describe pods podA** is going to send **GET /api/v1/namespaces/{namespace}/pods/{name}/status** actually.

Users must set up proper credentials before they use kubectl command line or invoke Kubernetes API. In kubectl tool, a set of credentials is stored as Secrets, which is in Kubernetes object format and mounted into pods allowing in-cluster processes to talk to the Kubernetes API.

Kubernetes also supports other methods to authenticate API requests including client certificates, bearer tokens, authenticating proxy or HTTP basic auth.

For example, if the flag **--enable-bootstrap-token-auth** is enabled, then bearer token credentials will be implemented to authenticate requests against the API server. The header **Authorization: Bearer 07401b.f395accd246ae52d** in HTTP request will take effect.

## Continuous Deployment for Kubernetes

In Kubernetes, a Deployment object describes state in a Deployment object, and the Deployment controller changes the actual state to the desired state at a controlled rate. A typical Deployment object can be found below

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
  labels:
    app: myapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp-container
        image: busybox
        command: ['sh', '-c', 'echo ${DEMO_GREETING} && sleep 3600']
        env:
        - name: DEMO_GREETING
          value: "Hello Kubernetes!"
```

The deployment of containerized application in Kubernetes is intrinsically the change from status A to status B in Kubernetes Deployment object. 

Continuous deployment is a software development practice where code changes are automatically deployed to production without explicit approval. A typical continuous deployment process for containerized java application running on Kubernetes can be described in following architecture.

![CICD](https://s3.amazonaws.com/ascending-devops/ascending-conf/CICD.png)

Every time developers push source code (to GitHub or other source code repository), it will go through unit testing (connection to test database), packaging (then store artifacts like war file in S3), image building (then push image to docker repository) and deployment stages. The deployment strategy can be **Rolling, Immutable or Blue/Green**, which grants the application will have zero downtime for users.

## Essential Part: Deploy New Version through Kubernetes API or Kubectl

It's optional that the test, packaging and image building stages can be fulfilled by CodeBuild service. CodeBuild a serverless service that runs a few Linux commands in in docker container based on given image . AWS also provides Lambda function, another serverless service, which invokes a given function in a predefined programming language (e.g. python, Go, java).

In deployment stage, either CodeBuild or Lambda function can be used, which is going to correspond to two interaction methods with Kubernetes cluster, Kubectl tool and Kubernetes API. 

### Demo: Implement CodeBuild in Deployment Stage

In the second part of this article, a new Kubernetes cluster with one slave node server has been created. Create a *yaml* file named **sample_deployment.yaml**, and its content can be found [here](https://github.com/yi-le/LifeExperience/blob/master/sample_deployment.yaml).

Then run following command
```bash
kubectl create -f sample_deployment.yaml
```
Next
```bash
kubectl get pods | grep myapp-deployment
```
Such result will be returned
![PodName](https://ascending-devops.s3.amazonaws.com/ascending-conf/PodName.png)
The pod name can be found in result, then run
```bash
kubectl logs ${POD_NAME}
```
and you will see "Hello Kubernetes!" in the terminal.
After that we can try to update the environment variable DEMO_GREETING, and this behavior can be regarded as a new version deployment.
```bash
kubectl set env deployment/myapp-deployment DEMO_GREETING='Another Hello Kubernetes!'
```
Immediately run
```bash
kubectl get pods | grep myapp-deployment
```
It can be observed that two pods are terminating while two new pods are being launched, copy the new pod name and then
```bash
kubectl logs ${POD_NAME}
```
"Another Hello Kubernetes!" will be returned, which indicates the completion of deployment.

In AWS CloudFormation, this CodeBuild process can be defined in *yaml* format.

```yaml
Deployment:
  Type: AWS::CodeBuild::Project
  Properties:
    Artifacts:
      Type: no_artifacts
    Description: update environment variables
    Environment: 
      ComputeType: BUILD_GENERAL1_SMALL
      Image: aws/codebuild/standard:1.0
      Type: LINUX_CONTAINER
    Name: Deployment
    ServiceRole: !Ref CodeBuildRole
    Source: 
      BuildSpec: |
        version: 0.2
        phases:
          install:
            commands:
              - curl -o kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/linux/amd64/kubectl
              - chmod +x ./kubectl
              - mkdir -p /root/bin
              - cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH
              - curl -o heptio-authenticator-aws https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/linux/amd64/heptio-authenticator-aws
              - chmod +x ./heptio-authenticator-aws
              - cp ./heptio-authenticator-aws $HOME/bin/heptio-authenticator-aws && export PATH=$HOME/bin:$PATH
          pre_build:
            commands:
              - mkdir -p ~/.kube
              # upload the ~/.kube/config file in S3, then retrieve it from S3 and save as ~/.kube/config
              - aws s3 cp s3://example-bucket/config ~/.kube/config
              - export KUBECONFIG=$KUBECONFIG:~/.kube/config
          build:
            commands:
              - kubectl set env deployment/myapp-deployment DEMO_GREETING='Another Hello Kubernetes!' --kubeconfig ~/.kube/config
      GitCloneDepth: 1
      Location: https://github.com/user/example.git
      Type: GITHUB
```

### Demo: Implement Lambda in Deployment Stage

To impement Lambda function in Codepipeline process, a bear token should be retrieved and stored. An HTTP request will be made within Lambda function, and sent to Kubernetes cluster to trigger a new deployment.

Run this command to find the name of secret.
```bash
kubectl get secret
```
Replace $SECRET_NAME with the NAME of secret in result.
```bash
kubectl get secret $SECRET_NAME -o jsonpath='{.data.token}' | base64 --decode
```
Next, store the token in [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html). In this case, the token is named as k8s-bear-token.

![AWS Systems Manager Parameter Store](https://ascending-devops.s3.amazonaws.com/ascending-conf/AWS_Systems_Manager_Parameter_Store.png)

It's essential that a cluster role binding is created to allow cluster API to be invoked. Create following file and named it as **fabric8-rbac.yaml**

```yaml
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: fabric8-rbac
subjects:
  - kind: ServiceAccount
    # Reference to upper's `metadata.name`
    name: default
    # Reference to upper's `metadata.namespace`
    namespace: default
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
```
Then
```bash
kubectl create -f fabric8-rbac.yaml
```

All set, we can edit the lambda function now. In our case, the host site of Kubernetes cluster (http://localhost if run Kubernetes locally) is stored as environment variable

```python 
import requests
import json
import boto3
import os

client = boto3.client('ssm')
response = client.get_parameter(Name='k8s-bear-token')
url = os.environ['k8s_cluster']+'/apis/apps/v1/namespaces/default/deployments/example-deployment'
headers = {'Content-Type':'application/json', 'Authorization':'Bearer '+response['Parameter']['Value']}
body = {
  "apiVersion": "apps/v1",
  "kind": "Deployment",
  "metadata": {
    "name": "example-deployment",
    "labels": {
      "app": "example"
    }
  },
  "spec": {
    "replicas": 2,
    "selector": {
      "matchLabels": {
        "app": "example"
      }
    },
    "template": {
      "metadata": {
        "labels": {
          "app": "example"
        }
      },
      "spec": {
        "containers": [
          {
            "name": "example-container",
            "image": "busybox",
            "command": [
              "sh",
              "-c",
              "echo ${DEMO_GREETING} && sleep 3600"
            ],
            "env": [
              {
                "name": "DEMO_GREETING",
                "value": "Another Hello Kubernetes!"
              }
            ]
          }
        ]
      }
    }
  }
}
body = json.dumps(body)

def lambda_handler(event, context):
  r = requests.put(url, headers=headers,verify=False,data=body)
  return r
```

This lambda can be invoked in deployment stage of codepipeline, with bear token stored in AWS System Patameter and cluster host site stored as environment variable to keep security. Developers are able to define customized parameters in codepipeline event, in case that deployment commands contain a commit hash, time or other variables.

## Comparision Between CodeBuild and Lambda

Both CodeBuild and Lambda function can be implemented in deployment stage, the comparision between them can be seen below

| | CodeBuild | Lambda |
|---|---|---|
|Security|Medium|Strong|
|Difficulty|Easy|Medium|
|Flexibility|Medium|High|
|Effecency|Low|High|
|Overall Score|:star::star::star:|:star::star::star::star::star::star:|

Don't hesitate to contact us if you have any question for our blog and service!