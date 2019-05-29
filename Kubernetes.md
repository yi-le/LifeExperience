![ascending logo](https://ascendingdc.com/images/WechatIMG116.jpg) ![apn logo](https://ascendingdc.com/images/aws.png)

# Continuous Deployment on Kubernetes Platform using AWS CodePipeline

In this article:
- Why Kubernetes
- Create Kubernetes Platform in AWS
- Kubectl Tool and Kubernetes API
- Architecture: Continuous Deployment to Kubernetes
- Essential Part: Updating Pod Command through API
- Conclusion

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

## Essential Part: Updating Pod Command through API or Kubectl

For architecture above, the test, packaging and image building steps can be fulfilled by CodeBuild service. CodeBuild a serverless containerized application that runs a few Linux commands in given docker image. AWS also provides serverless Lambda function, which invokes a given function in predefined runtime (e.g. python, Go, java).

In deployment stage, either CodeBuild or Lambda function can be used, which is going to correspond to two interaction methods with Kubernetes cluster, Kubectl tool and Kubernetes API. 
