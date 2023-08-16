
# <img src="https://i.ibb.co/ZSbWvNw/icon.png" width="30px" height="30px" /> PySurfs
PySurfs is a simple yet insightful Python GUI application which its purpose is to analyze internet traffic through Wireshark. By providing a record of Wireshark traffic and specifying port to listen on, users are given an H-Bar-Graph displaying the websites visited and their frequency.

After a year from its initial release, the application has been dockerized. <br>
I wanted to gain some knowledge and have hands-on practice with Docker.<br>
But things quickly escalated (which is typical in Software Engineering), so I decided to write this tutorial about how to deploy GUI applications in Docker.<br>

## Table of Contents
- [Things I've Learned](#things-ive-learned)
- [Requirements](#requirements)
- [Deploy a GUI Application to Docker](#deploy-a-gui-application-to-docker)
	- [The KeyError: 'DISPLAY' Error](#the-keyerror-display-error)
	 	- [LocalHost Display](#localhost-display)
	 	- [Remote Display Within Network](#remote-display-within-network)
	  	- [Remote Display Outside Network](#remote-display-outside-network)
  	- [No such file or directory 'Xauthority' Error](#no-such-file-or-directory-xauthority-error)
- [The GUI](#the-gui)

## Things I've Learned[](#things-ive-learned)
1. Containers are headless which means they don't have a screen to display on. Hence, the importance of X Servers is with providing such capability. 
2. The architecture of X Servers is very simple server-client like framework where the X Server receives signals from the clients' keyboard and mouse, and then sends the signals via network to a remote monitor.
3. Throughout my expedition I saw tutorials that introduce the concept between X-Server and containers, but I didn't like some security gaps that were provided in those tutorials. Hence I've learned about secrets, ssh-keygen and ssh and did some testings outside of my private network and between different computers.
4. ECDH over RSA is better security.
5. Pushing and pulling into and out of Dockerhub.
6. WSL simplifies the process by having the .Xauthority.

## Requirements[](#requierments)
- Xming Server: [Download](https://sourceforge.net/projects/xming).
- Docker Desktop [Download](https://www.docker.com/products/docker-desktop).
- Docker image, you can use PySurfs: ```docker pull dorincatladish123/pysurfs```

## Deploy a GUI Application to Docker[](#deploy-a-gui-application-to-docker)
   try to run the application with ```docker run --rm -it dorincatladish123/pysurfs```
- #### The KeyError DISPLAY Error[](#the-keyerror:-'display'-error)
  This error occurs because containers don't have a screen.
    ```
    Traceback (most recent call last):
        import pyatgui
    ...
        _display = Display(os.environ['DISPLAY'])
    File "/usr/local/lib/python3.10/os.py", line 680, in _getitem_
        raise KeyError(key) from None
    KeyError: 'DISPLAY'
    ```    
  	Solutions to different scenarios:
  ---
	- ### LocalHost Display[](#localhost-display)
		Xming configurations already accept localhost connections. Just use the command below: <br>
		```docker run -it --rm -e "DISPLAY=host.docker.internal:0.0" dorincatladish123/pysurfs```
	- ### Remote Display Within Network[](#remote-display-within-network)
		first lets establish a common language: <br>
		host machine - is the machine where the necessary display (screen) is. <br>
		client machine - the machine from which you will be running the GUI application. <br>
		- client machine: open a command line from the client and type 'ipconfig', find the IPV4 (something like 192.168.0.1 or 10.0.0.x), (use the Wireless LAN adapter Wi-Fi if you are connected to wifi, etc..)
		- host machine: navigate to Xming directory, the path is usually "C:\Program Files (x86)\Xming" and open *.hosts file, enter the IPV4 of the client machine to that file.)
		- now restart Xming. It is important to close it from the icon tray and then open it, otherwise, the changes in the .hosts file will not be applied and it will not work. <br>
		```docker run -it --rm -e "DISPLAY=$(ip_of_host_machine):0.0 dorincatladish123/pysurfs```
	- ### Remote Display Outside Network[](#remote-display-outside-network)
		- create an ssh connection between the host machine and client machine (you will need port fowarding)
		- now you are controlling the host machine from the client machine, repeat all the steps in the mindset of [LocalHost Display](#localhost-display).

---
- #### No such file or directory '.Xauthority' Error[](#no-such-file-or-directory-.xauthority-error)
	Another common error when using Xauthority is this traceback:
	```
	Traceback (most recent call last):
	  ...
	    au = xauth.Xauthority()
	  File "/usr/local/lib/python3.10/site-packages/Xlib/xauth.py", line 45, in __init__
	    raise error.XauthError('~/.Xauthority: %s' % err)
	Xlib.error.XauthError: ~/.Xauthority: [Errno 2] No such file or directory: '/root/.Xauthority'
	```
 	 It won't happen to you with the Dockerfile that I provided because I planted an .Xauthority directory with these lines: <br>
   	```# CMD /bin/bash -c "touch /root/.Xauthority && python main.py"```

---
#### The GUI[](#the-gui)
1. Open Default.ini file and insert the correct 'destination port' under [SETTINGS] section. 
2. Open the application, click "load pcap" and choose .pcap file to decipher.
![image](https://user-images.githubusercontent.com/90141260/200125704-7fa1fd28-9274-455e-a866-58873dbf6df0.png)
3. A graph shows the sites that were visited.
![image](https://user-images.githubusercontent.com/90141260/200125726-7c031952-aa24-4d6a-9e40-730ce0680170.png)
4. Clicking on 'settings' button, you can search, select and deselect the sites you wish to conclude in the graph.
![image](https://user-images.githubusercontent.com/90141260/200125768-f4a7ee18-60a1-4de6-ada1-3c3784b460f1.png)
5. Clicking on 'select all' will show all the sites, if more than 20 sites than for visual simplicity a new tab will open for the rest of sites:
![image](https://user-images.githubusercontent.com/90141260/200126462-8d9d6829-d4e1-4276-a843-0fa647ea0423.png)

Known Issues:
1. Under the Settings button, there are two tabs: 'Sites' and 'SETTINGS', it is more logical to exclude the 'SETTINGS' to its own button, and disable only 'Sites' before a decipher has been made.
