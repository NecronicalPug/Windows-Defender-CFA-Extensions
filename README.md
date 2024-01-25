# Windows Defender Controlled Folder Access Extension
Light Python script made to work alongside Windows Defender.
Created as a fun little side project.

## Allowed Applications Checker
Used alongside Controlled Folder Access, it issues a notification when an application with access to protected folders has either been modified or deleted since the last time the script has been ran. 

The script requires admin access to read the allowed applications Windows Registry values and it will create multiple .csv files for allowed/invalid/modified applications as well as a .bat file to remove all invalid applications every time it's ran.

In the case that invalid/modified applications are found, the user can access the .csv file or look at the notification in the Action Centre in order to get the details of the applications in question. They can then run the bat file to remove the invalid applications from the registry.

The script itself does not modify the Windows Registry and instead relies on the user to make the changes whenever a warning is issued.

The purpose of this script is to enhance the functionality of the Controlled Folder Access feature as it in its current form, it's unable to block access to protected folders by compromised allowed applications. This script of course is only effective if it's ran fairly often so I'd recommend creating a task to have the script run every day/every time the computer is turned on. 

### Note about the .bat file.
Administrators only have read access to the Allowed Applications registry key, therefore if you'd like to use the .bat file (to save time when you have a lot of invalid applications to get rid of and/or you hate the UI) you'll have to go into Safe Mode, take ownership of the registry key and assign your user account Full Control permissions to make changes outside of Defender's UI.


I don't recommend making any permanent changes to the permissions, instead take ownership, grant yourself permissions, make the registry changes and give back ownership/permissions.


Registry key below for reference: "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows Defender\Windows Defender Exploit Guard\Controlled Folder Access\AllowedApplications"


**Example Notification:**

![image](https://github.com/NecronicalPug/Windows-Defender-CFA-Extensions/assets/46400065/ef78ee7a-a26c-46f4-b8a7-1001ab55490c)
