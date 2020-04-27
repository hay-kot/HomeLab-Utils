## HomeLab-Utils
A place for all my scripts that I use for various homelab tasks.

## Backup Checker
The Backup checker is used to scan a back-up folder for a specific file type and check it against parameters in the config file. You can configure as many of these as you'd like. Each should start with [Backup Name] and include all the data below. Currently no fields are optional.

**Example:**
```
[Home Assistant]
directory = \\path\to\data\backups
secret = xxxx-123123123123123-123123123123-123123123123-123123123123
channel = #mychannel
file_type = .mrbak
days = 7
```
- directory = Directory to check
- secret    = Your Slack API Key
- channel   = Your slack channel, inclucde #
- file_type = File type to be checked. Currently only supports 1 file type.
- days      = This means in your folder the newest backup must be newer than 7 days

In this case, if the backup is OLDER than 7 days a slack message will be generated with an error emoji alterting you that the backup ran incorrectly and how old the current newest backup is. If the backup is within 7 days a green checkmark and message saying the backup ran successfully will be sent to the slack channel. 

**Example Notification:**

![Slack Notification](https://raw.githubusercontent.com/hay-kot/HomeLab-Utils/master/Backup%20Checker/Slack%20Notification%20Example.jpg)

## Move, Archive, with Config
A simple script to take a file/directory and copy it to another and zip the files.

**Use Cases**
- Pull settings files from applications for backup (I use it for Windows Terminal and Sublime)
- Pull Backups from Home Assistant via SMB Share

**Example:**
```
[Exampe] # Remove me!
source = \\some file server\backup
destination = \\path\to\data\new name
all_files   = False
clean_up    = True
keep        = 1
```
- source      = Source folder 
- destination = Destination Folder
- all_files   = False will only take the newest file from the source, True will take all the files/folders in the directory
- clean_up    = True will only keep the "keep" number in the destination folder. False will keep all files in the destination.
- keep        = The number of backups to keep. 

