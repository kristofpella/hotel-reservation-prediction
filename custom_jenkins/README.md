# Jenkins Docker-in-Docker Setup

This directory contains the custom Jenkins setup with Docker support.

## Problem

When running `docker build` commands in Jenkins pipelines, you may encounter:
```
ERROR: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

This happens because the Jenkins container has Docker CLI installed but cannot access a Docker daemon.

## Solution: Mount Host Docker Socket (Recommended)

The simplest and most common solution is to mount the host's Docker socket into the Jenkins container.

### Using Docker Compose (Recommended)

```bash
cd custom_jenkins
docker-compose up -d
```

This will:
- Build the custom Jenkins image
- Mount the host Docker socket (`/var/run/docker.sock`)
- Set proper permissions
- Start Jenkins on port 8080

### Using Docker Run

```bash
docker build -t custom-jenkins .
docker run -d \
  --name jenkins \
  --privileged \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e DOCKER_HOST=unix:///var/run/docker.sock \
  custom-jenkins
```

## Alternative: True Docker-in-Docker (DinD)

If you need true isolation (not recommended for most cases), you can use a DinD sidecar:

```yaml
version: '3.8'
services:
  docker-dind:
    image: docker:dind
    privileged: true
    volumes:
      - docker-certs-ca:/certs/ca
      - docker-certs-client:/certs/client
    environment:
      DOCKER_TLS_CERTDIR: /certs

  jenkins:
    build:
      context: .
      dockerfile: Dockerfile
    depends_on:
      - docker-dind
    environment:
      DOCKER_HOST: tcp://docker-dind:2376
      DOCKER_TLS_CERTDIR: /certs
      DOCKER_CERT_PATH: /certs/client
      DOCKER_TLS_VERIFY: 1
    volumes:
      - jenkins_home:/var/jenkins_home
      - docker-certs-ca:/certs/ca:ro
      - docker-certs-client:/certs/client:ro
```

## Security Note

⚠️ **Warning**: Mounting the Docker socket gives the Jenkins container full access to the host's Docker daemon. This is a security consideration but is the standard approach for CI/CD pipelines.

## Verification

After starting Jenkins, verify Docker access:

1. Access Jenkins at `http://localhost:8080`
2. Create a test pipeline or run in Jenkins script console:
   ```groovy
   sh 'docker ps'
   ```

If this works, your Docker setup is correct!

