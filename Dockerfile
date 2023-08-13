# Use Python as parent image, this is actually an image containing linux based python code
FROM python:3.10.11

RUN apt-get update -y
RUN apt-get upgrade -y

# disable option to ask for user input
ENV DEBIAN_FRONTEND=noninteractive

# for analyzing wireshark files
RUN apt-get update && \
    apt-get install -y tshark

# enable option to get input from user
ENV DEBIAN_FRONTEND=dialog

# Install X-Server to make container think it has graphical interface
# -y allow automatic yes for prompts
RUN apt-get install -y libx11-6 libxext-dev libxrender-dev libxinerama-dev libxi-dev libxrandr-dev libxcursor-dev libxtst-dev tk-dev && rm -rf /var/lib/apt/lists/*       

# Install ssh to interact with X-Server
RUN apt-get update && apt-get install -y openssh-server
EXPOSE 22

# Add describtion to image
LABEL describtion="playing with dockers"

# CMD ["/usr/sbin/sshd", "-D"]

# Set the working directory in the container to /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

RUN sh -c 'echo "X11Forwarding yes" >> /etc/ssh/sshd_config'
RUN sh -c 'echo "X11UseLocalhost no" >> /etc/ssh/sshd_config'
RUN mkdir /app/.ssh && ssh-keygen -f "/app/.ssh/id_rsa" -t rsa -b 4096 -N ""
RUN mkdir /app/.ssh/authorized_keys
COPY id_rsa.pub /app/.ssh/authorized_keys

# Run main.py when the container launches
CMD /bin/bash -c "touch /root/.Xauthority && python main.py"