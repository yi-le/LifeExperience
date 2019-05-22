![ascending logo](https://ascendingdc.com/images/WechatIMG116.jpg) ![apn logo](https://ascendingdc.com/images/aws.png)

# Continuous Deploy to Kubernetes using AWS CodePipeline

In this article:
- Kubernetes Introduction and Comparison with ECS
- Build Kubernetes Cluster with Nodes in AWS via kops
- Kubectl and API, Credentials and Its subcommands
- Architecture: Continuous Deployment to Kubernetes
- Essential Part: Updating Pod Command through API
- Conclusion

## Kubernetes Introduction and Comparison with ECS

Kubernetes is a portable, extensible open-source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation. Kubernetes uses persistent entities to represent the state of cluster in .yaml format. Thus, all of the tasks can be managed in a more consistent way, no matter it’s in on-promise server, cloud computing platform or hybrid cloud environment.

AWS provides Elastic Container Service (Amazon ECS) as a highly scalable, fast, container management service that makes it easy to run, stop, and manage Docker containers on a cluster. ECS components (e.g. services, tasks) can be defined in .yaml format within CloudFormation template, which follows Infrastructure as code process.

AWS also released Amazon Elastic Container Service for Kubernetes ([AWS EKS](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html)) last year. It’s a managed service that makes it easy for users to run Kubernetes on AWS without needing to stand up or maintain their own Kubernetes control plane.

| | Serverless Cluster | Infrastructure as code | Consistency in Hybrid Cloud Environment | Cost |
| --- | --- | --- | --- | --- |
| Customized Kubernetes Platform | No | Kubernetes Object yaml | Yes | $ |
| ECS | Yes | CloudFormation template | No | $$ |
| EKS | Yes | CloudFormation Template for cluster, Kubernetes Object yaml | Yes | $$$ |