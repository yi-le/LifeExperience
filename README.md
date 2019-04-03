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