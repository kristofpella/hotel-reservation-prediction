# Use the Jenkins image as the base image
FROM jenkins/jenkins:lts

# Switch to root user to install dependencies
USER root

# Install prerequisites and Docker
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean

# Add Jenkins user to the Docker group
# Create docker group if it doesn't exist, or use existing one
# The GID will be matched at runtime using --group-add flag
RUN (getent group docker || groupadd docker) && \
    usermod -aG docker jenkins

# Install sudo and configure it for jenkins user
RUN apt-get update -y && \
    apt-get install -y sudo && \
    echo "jenkins ALL=(ALL) NOPASSWD: /usr/bin/docker" >> /etc/sudoers && \
    apt-get clean

# Create docker wrapper script that uses sudo if needed
RUN echo '#!/bin/bash\n\
if [ -w /var/run/docker.sock ] 2>/dev/null; then\n\
    exec /usr/bin/docker "$@"\n\
else\n\
    exec sudo /usr/bin/docker "$@"\n\
fi' > /usr/local/bin/docker-wrapper.sh && \
    chmod +x /usr/local/bin/docker-wrapper.sh && \
    chown jenkins:jenkins /usr/local/bin/docker-wrapper.sh

# Create the Docker directory and volume for DinD
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# Switch back to the Jenkins user
USER jenkins