# Life Experience
Good good study, day day up

## How to write a README.md

[click me](https://help.github.com/en/articles/basic-writing-and-formatting-syntax)

## Use pyenv to install python on macOS Mojave

```bash
CFLAGS="-I$(xcrun --show-sdk-path)/usr/include" pyenv install -v 3.7.2
```

## SSH Port Forwarding

[click me](https://unix.stackexchange.com/questions/115897/whats-ssh-port-forwarding-and-whats-the-difference-between-ssh-local-and-remot)

## Find Container's Internal IP address

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${CONTAINER_ID}
```

## What should you do if kubectl can't find the cluster

```bash
kubectl config set-cluster demo-cluster --server=http://master.example.com:8080
kubectl config set-context demo-system --cluster=demo-cluster
kubectl config use-context demo-system
kubectl get nodes
```

## Find and restore a deleted file in a Git repository

```bash
git checkout $(git rev-list -n 1 HEAD -- "$file")^ -- "$file"
```

## Set default java version in Mac

```bash
/usr/libexec/java_home -V
```

```bash
export JAVA_HOME=`/usr/libexec/java_home -v 1.8`
```