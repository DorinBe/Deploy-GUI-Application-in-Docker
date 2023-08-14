# Use Python as parent image, this is actually an image containing linux based python code 
# so I've adjusted the GUI I wrote in windows OS to work also on Linux OS.
FROM python:3.10.11

# Disable option to ask for input from user
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y tshark \ 
    # X-Server libraries
    libx11-6 libxext-dev libxrender-dev libxinerama-dev libxi-dev libxrandr-dev libxcursor-dev libxtst-dev tk-dev && rm -rf /var/lib/apt/lists/*

# enable option to get input from user
ENV DEBIAN_FRONTEND=dialog      

# Set the working directory in the container to /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

# Update SSH configuration for X11 forwarding
# Only necessary when using SSH.
RUN echo "X11Forwarding yes" >> /etc/ssh/sshd_config && \ 
    echo "X11UseLocalhost no" >> /etc/ssh/sshd_config

# Run main.py when the container launches
# touch the .Xauthority manually to resolve error.
CMD /bin/bash -c "touch /root/.Xauthority && python main.py"