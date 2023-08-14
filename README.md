# <img src="https://i.ibb.co/ZSbWvNw/icon.png" width="30px" height="30px" /> PySurfs
A simple and fun program in Python, made to express knowledge in the usage of wireshark, python, ini files, tkinter and pandas.
You provide it with a record of wireshark program of interent traffic and the port to listen on, and it provides you with an Hgraph of which webs were visited and in what frequecy.

A year passed sice I've first uploaded this, and I decided that I want to try to dockerize it.
why?
I wanted to gain some knowledge and have hands-on practice in dockers.

Things quickly escalated (which is typical in SWE) as Gui applications are not the best systems to deploy on dockers.
i've spent some time learning new subjects programs and libraries that in the end achieved the result
IVE DEPLOYED A DOCKER BY MY SELF, FIRST APPLICATION

some things i've learned:
1. containers are headless and don't really have a monitor which is very contradicting all the GUI thing (laughting emoji).
hence, the container needs to be provided with capability to have a monitor interface. This capability is provided by X Servers. 
2. The architecutre of X Servers is very simple server-client like framework where the X Server reciecves signals from the clients' keyboard and mouse, and than sends the signals via network to a remote monitor.
3. throughtout my expedition I saw toturials that introduce the concept between X-Server and containers, but I didn't like some security gaps that were provided in those toturials. hence ive learned about secrets, ssh (already had some exprence with it, but also achived to sshing from an Ubuntu to Windows which was quite adventorous and had difficulties. ssh-keygen which was favoured because it didnt envolve secrets or other mechanisms that provide difficulties to non-devops engineers trying to run the application.
4. rsa is most commonly used by now but it is recomended to use ecdh as rsa is repeteadly being under cracking for years.
5. pushing and pulling into and outof dockerhub.

## Instalattion and Usage
1. download and install docker ![link](https://www.docker.com/products/docker-desktop/)
2. open a cmd and write "docker pull dorincatladish123/pysurfs
3. now if you will try to run the container with "docker run dorincatladish123/pysurfs" an error will occur:
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
4. This is where the "containers are headless" comes into consideration. The container doesn't have any display to display on. But we will work it on:
5. download and install Xming Server (X-Server) ![link](https://sourceforge.net/projects/xming/) 
6. do you want your localhost display or a remote display ?
6.1. local host display (the machine you are using right now)
the ip would be: "DISPLAY=host.docker.internal:0.0"
6.2. a remote display within your network
6.3. a remote display outside of your network
i connected another computer to my homes' network
the remote display you want to provision the app from will be called "host"
the machine from where you are running the application (but will not see any GUI) will be called "client"
6.2.1 client machine: open a command line from the client and type 'ipconfig' 
6.2.2 client machine: find the IPV4 (something like 192.168.0.1 or 10.0.0.x), (use the Wireless LAN adapter Wi-Fi if you are connected to wifi, etc..)
6.2.3 host machine: navigate to Xming directory, the path is usually "C:\Program Files (x86)\Xming" and open *.hosts file, enter the IPV4 of the client machine to that file.)
6.2.4 now restart Xming. It is important to close it from the icon tray and than open it, otherwise the changes in the .hosts file will not be applied and it will not work. 
6.3.1 create an ssh connection between the host machine and client machine (you will need port fowarding)
6.3.2 now you are controlling the host machine from the client machine, repeat all the steps in the mindset of a localhost.
7. there are several ways to tell the container the desired ip, you can use secrets, enviroment file, or from the command line.
7.1 to use secrets:
7.2 to use enviroment file: create .env file somewhere in your computer and remember the path
write into the .env file the DISPLAY command from 6.1 or 6.4
then open a command line and execute the line:
"docker run --rm -it --env-file .env dorincatladish123/pysurfs"
7.3 to use from command line:
type into the command line "docker run --rm -it -e "DISPLAY=$(the ip from 6.1 or 6.4) dorincatladish123/pysurfs"

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
