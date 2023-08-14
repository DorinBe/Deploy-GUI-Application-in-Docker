
# <img src="https://i.ibb.co/ZSbWvNw/icon.png" width="30px" height="30px" /> PySurfs
A simple and fun program in Python, made to express knowledge in the usage of wireshark, python, ini files, tkinter, pandas and ssh.
You provide it with a record of wireshark program of interent traffic and the port to listen on, and it provides you with an Hgraph of which webs were visited and in what frequecy.
### A year passed sice I've first uploaded this GUI app, and I decided that I want to try to dockerize it.
But things quickly escalated (which is typical in SWE), so I decided to write this tutorial about how to deploy GUI applications to docker.<br>
why?<br>
I wanted to gain some knowledge and have hands-on practice with dockers.
I've spent some time learning new subjects, programs and libraries that in the end achieved the result. <br>
IVE DEPLOYED A GUI APP TO DOCKER

## Table Of Contents
- [Things I've Learned](#things-ive-learned)
- [Requierments](#requierments)
- [Deploy GUI App to Docker](#deploy-gui-app-to-docker)
	- [The KeyError: 'DISPLAY' Error](#the-keyerror-display-error)
 	- [LocalHost Display](#localhost-display)
 	- [Remote Display Within Network](#remote-display-within-network)
  	- [Remote Display Outside Network](#remote-display-outside-network)
- [The GUI](#the-gui)

## Things I've Learned[](#things-ive-learned)
1. Containers are headless and don't have a monitor to display the GUI, which is very contradicting to the GUI thing (laughting emoji), but can be usefull for testing.
hence, the container needs to be provided with capability to have a monitor interface. This capability is provided by X Servers. 
2. The architecutre of X Servers is very simple server-client like framework where the X Server reciecves signals from the clients' keyboard and mouse, and than sends the signals via network to a remote monitor.
3. Throughtout my expedition I saw toturials that introduce the concept between X-Server and containers, but I didn't like some security gaps that were provided in those toturials. Hence I've learned about secrets, ssh-keygen and ssh (already had some exprence with it, but also achived to sshing from an Ubuntu\Windows to Windows from different networks which felt quite adventorous).
4. RSA is most commonly used by now but it is recomended to use ecdh as rsa is repeteadly being under cracking for years.
5. Pushing and pulling into and outof dockerhub.
6. Deploying to GCP requires *.pub files to be excluded from .dockerfile so at the end I used a simpler and straight-foward way for creating a secure connection, I will be back to it later.

## Requierments[](#requierments)
- Download and install Xming Server (X-Server) [Xming Server](https://sourceforge.net/projects/xming).
- Download and install docker [Docker Desktop](https://www.docker.com/products/docker-desktop).
- You'll need some gui application to test this tutorial, I am not bribed but you can use this one:
  ```docker pull dorincatladish123/pysurfs```

## Deploy GUI APP to Docker[](#deploy-gui-app-to-docker)
- try to run the application with ```docker run --rm -it dorincatladish123/pysurfs```
- ##### The KeyError DISPLAY Error[](#the-keyerror:-'display'-error)
  after running the command above, you will encounter the KeyError: 'DISPLAY'
    ```
    Traceback (most recent call last):
    File "/app/main.py", line 3, in <module>
        from GUI import MainGui
    File "/app/GUI/MainGui.py", line 12, in <module>
        from pyautogui import size
    File "/usr/local/lib/python3.10/site-packages/pyautogui/_init_.py", line 249, in <module>
        import mouseinfo
    File "/usr/local/lib/python3.10/site-packages/mouseinfo/_init_.py", line 223, in <module>
        _display = Display(os.environ['DISPLAY'])
    File "/usr/local/lib/python3.10/os.py", line 680, in _getitem_
        raise KeyError(key) from None
    KeyError: 'DISPLAY'
    ```
   This is where the "containers are headless" comes into consideration. The container doesn't have any display ("screen") to display the GUI. <br> But we will work it on:
- Last Step, brace yourself (:
	- Where is the display (screen) in relation to the network?
		- [LocalHost Display](#localhost-display)
		- [Remote Display Within Network](#remote-display-within-network)
		- [Remote Display Outside Network](#remote-display-outside-network)
			- ### LocalHost Display[](#localhost-display)
     			You can simply run your application without configuring anything. Xming configurations already accept localhost connections because there is no security risk. Just type into the command line:
				```docker run -it --rm -e "DISPLAY=host.docker.internal:0.0" dorincatladish123/pysurfs```
			- ### Remote Display Within Network[](#remote-display-within-network)
			first lets establish a common language: <br>
			host machine - is the machine where the necessary display (screen) is. <br>
			client machine - the machine from which you will be running the GUI application. <br>
			- client machine: open a command line from the client and type 'ipconfig', find the IPV4 (something like 192.168.0.1 or 10.0.0.x), (use the Wireless LAN adapter Wi-Fi if you are connected to wifi, etc..)
			- host machine: navigate to Xming directory, the path is usually "C:\Program Files (x86)\Xming" and open *.hosts file, enter the IPV4 of the client machine to that file.)
			- now restart Xming. It is important to close it from the icon tray and than open it, otherwise, the changes in the .hosts file will not be applied and it will not work. <br>
    			```docker run -it --rm -e "DISPLAY=$(ip_of_host_machine):0.0 dorincatladish123/pysurfs```
			- ### Remote Display Outside Network[](#remote-display-outside-network)
			- create an ssh connection between the host machine and client machine (you will need port fowarding)
			- now you are controlling the host machine from the client machine, repeat all the steps in the mindset of [Remote Display Within Network](#remote-display-within-network).
 
- When should one favour .env files?
	- They can store multiple enviroment variables and configurations.
   	- You can comment out the ev that are not necessary, but keep them in the file.


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
1. Under the Settings button, there are to tabs: 'Sites' and 'SETTINGS', it is more logical to exclude the 'SETTINGS' to its' own button, and disable only 'Sites' before a decipher has been made.
