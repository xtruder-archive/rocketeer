PIPA STREAM 3rd GENERATION
==========================

Description
-----------
This app let's you start your streams remotely.
It is actually very smart process launcher, specialized for starting
processes that provide statuses(like ffmpeg). Currently it has only
ability to parse statuses of ffmpeg processes, but it's very easy to extend.
It has xml-rpc interface, so you can create/start/stop stream remotely and set its parameters.

Installation
-----------
**Current stable version is in branch pipa_stream3_0.5**

This app works with python2.7, i didn't test with other python versions.

- Install newest stable ffmpeg from git with whatever support you want.
- Install liblirc if you want to control streams with your remote.
- python setup.py install
- if you want to start on system startup there are init script avalible in init
  folder and sample config in config folder.
- Copy init scripts to /etc/init.d/
- Copy config files to /etc/pstream/

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

First you should create streamer from list of avalible streamers. You can get list of avalible streamers with **GetStreamers**. 
Then you can create streamer using **CreateStreamer** and it will return instance id of newly created streamer. 
You can get all streamer instances using **GetStreamerInstances**. 
You can destroy instance using **DestroyInstance** or to destroy all instances, call **DestroyInstances**.

If you want to know more open server.py.

You can access any instance you created on uri "http://host:port/instance_id/".
You can get streamer status using **GetStreamerStatus**, which returns list of status vars, like fps, time,... 
You can get streamer run status you can call **GetStreamerRunStatus**, which returns 0 for stopped, 1 for running, 2 for error, 3 for ended and 4 for unknown. 
Of course you can start streamer using **StartStreamer** and stop using **StopStreamer**. 
To get streamer value call **GetStreamerValue** and to set one call **SetStreamerValue**. 
The only usefull value right now is auto_restart set to one. 
This values gets also passed to templates.

if you want to know more open streamer.py

How to create new streamer template:
------------------------------------
Go to templates folder and you can see sample_template.py and sample_template.tpl. In your py file you define what varibales get passed to template, and in tpl file is template. It is based on mustache templating engine. You must remember that __init__ function of template gets values you set using SetStreamerValue as key value.

You must also register your newly created streamer in server.py, using RegisterStreamer.

TODO:
-----
- Add documentation
- Add logging

License:
--------
Pipa_stream3 is Copyright (C) 2011 kiberpipa.

Pipa_stream3 is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License version 2 as published by the Free Software Foundation.

Pipa_stream3 is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
