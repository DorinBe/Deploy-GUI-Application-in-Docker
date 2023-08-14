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



## Requierments
1. a file supported by 'pyshark' library


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
