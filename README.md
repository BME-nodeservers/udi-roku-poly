
# Roku media devices

A node server for [Roku](http://www.roku.com/) media devices. 

This is node server is for [Polyglot V3](https://github.com/UniversalDevices/pg3/) running on a 
[Polisy](https://www.universal-devices.com/product/polisy/)
from 
[Universal Devices Inc.](https://www.universal-devices.com/)


With this node server you can launch applications and send remote command to anyRoku device on your network.

## Installation

1. Backup Your ISY in case of problems!
   * Really, do the backup, please
2. Go to the Polyglot Store and purchase/install the Roku node server.
3. After installation, restart the Admin Console.

The node server will automatically start, scan your network for Roku
devices, and then add a node to the ISY for each Roku found.  This process
can take 10-15 seconds.

Once running, it will poll each device at the shortPoll interval to 
determine what application is runnning on that device.  This keeps the
device status in the ISY up-to-date.  The node server will also re-scan
the network every longPoll interval looking for new devices and for 
changes in the applications installed on each device. 

The ROKU firmware has a bug where it fails to update it's reported IP address
if the IP address changes while it is running (I.E. set via dhcp). When this 
happens, the node server will attempt to connect using this wrong IP address
and fail.  Re-booting the Roku device resolves the issue.

### Node substituion variables
 * sys.node.[address].ST   - Roku device status (True (active), False inactive)
 * sys.node.[address].GV1  - Current running application name
 * sys.node.[address].GV2  - Current running application ID


### Node Settings
The settings for this node are:

#### Short Poll
   * How often to poll each device for status (default 5 seconds)
#### Long Poll
   * How often to scan the network for device changes (default 60 seconds)

## Requirements
1. Polyglot V3.
2. ISY firmware 5.3.x or later
3. One or more Roku devices


# Release Notes
- 2.0.1 05/10/2022
   - node address need to be lower case.  Some devices now have uppercase letters in serial number
- 2.0.0 08/13/2021
   - Re-write for PG3
- 0.0.6 03/28/2020
   - Enable polling to get current status of Roku device.
- 0.0.5 03/27/2020
   - Strip '&' from application names.
- 0.0.4 12/22/2019
   - Fix requirements.txt file to have the right requirements.
- 0.0.3 03/20/2019
   - Fix online status going false after query.
- 0.0.2 01/11/2019
   - Initial working version published to github
- 0.0.1 01/07/2019
   - Initial template published to github
