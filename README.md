ROCKETEER - Advanced app launcher and manager
=============================================

Description
-----------
Rocketeer is very smart remote process launcher, watchdog and manager. It has abilty to start user commands from templates, to which you can pass parameters, to controle those processes and parse statuses. The main power is remote xml-rpc interface.

Installation
-----------
This app works with python2.7, i didn't test with other python versions.

- Install newest stable ffmpeg from git with whatever support you want.
- Install liblirc if you want to control streams with your remote.
- python setup.py install

Usage:
------
There are two cli commands(add --help for more info):

- pstream3d - xml-rpc app server.
- pstream3_client - command line client for server.
- pstream3_client_lirc - lirc client for server.

API:
----
Interface is xml-rpc on whatever port and host you set to daemon.

You can access it on url "http://host:port/"

First you should create app from list of avalible apps. You can get list of avalible apps with **GetApps**. 
Then you can create app using **CreateApp** and it will return instance id of newly created app. 
You can get all app instances using **GetAppInstances**. 
You can destroy instance using **DestroyInstance** or to destroy all instances, call **DestroyInstances**.

If you want to know more open server.py.

You can access any instance you created on uri "http://host:port/instance_id/".
You can get app status using **GetAppStatus**, which returns list of status vars, like fps, time,... 
You can get app run status you can call **GetAppRunStatus**, which returns 0 for stopped, 1 for running, 2 for error, 3 for ended and 4 for unknown. 
Of course you can start app using **StartApp** and stop using **StopApp**. 
To get app value call **GetAppValue** and to set one call **SetAppValue**. 
The only usefull value right now is auto_restart set to one. 
This values gets also passed to templates.

if you want to know more open app.py

How to create new app template:
------------------------------------
Go to templates folder and you can see sample_template.py and sample_template.tpl. In your py file you define what varibales get passed to template, and in tpl file is template. It is based on mustache templating engine. You must remember that __init__ function of template gets values you set using SetAppValue as key value.

You must also register your newly created app in server.py, using RegisterApp.

TODO:
-----
- Add documentation
- Add logging

License:
--------
Rocketeer is Copyright (C) 2011 Jaka Hudoklin.

Rocketeer is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License version 2 as published by the Free Software Foundation.

Rocketeer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
