## HomeLab-Utils
A place for all my scripts that I use for various homelab tasks.

### Backup Checker
The Backup checker is used to scan a back-up folder for a specific file type and check it against parameters in the config file. You can configure as many of these as you'd like. Each should start with [Backup Name] and include all the data below. Currently no fields are optional.

**Example:**
```
[Home Assistant]
directory = \\path\to\data\backups
secret = xxxx-123123123123123-123123123123-123123123123-123123123123  **- Replace with your Key**
channel = #mychannel **- Your slack channel, inclucde #**
file_type = .mrbak **- File type to be checked. Currently only supports 1 file type.**
days = 7 **- This means in your folder the newest backup must be newer than 7 days**
```

In this case, if the backup is OLDER than 7 days a slack message will be generated with an error emoji alterting you that the backup ran incorrectly and how old the current newest backup is. If the backup is within 7 days a green checkmark and message saying the backup ran successfully will be sent to the slack channel. 
