# Windows Defender Controlled Folder Access Extension
Light Python script made to work alongside Windows Defender.
Created as a fun little side project.

## Allowed Applications Checker
Used alongside Controlled Folder Access, it issues the user a warning when an application with access to protected folders has either been modified or deleted since the last time the script has been ran. 

The script requires admin access to read the allowed applications Windows Registry entries and it will create multiple .csv files for allowed/invalid/modified applications every time it's ran. 

In the case that invalid/modified applications are found, the user can access the .csv file or look at the notification in the Action Centre in order to get the details of the applications in question. 

The script itself does not modify the Windows Registry and instead relies on the user to make the changes whenever a warning is issued.

The purpose of this script is to enhance the functionality of the Controlled Folder Access feature as it in its current form, it's unable to block access to protected folders by compromised allowed applications. This script of course is only effective if it's ran fairly often so I'd recommend creating a task to have the script run every day/every time the computer is turned on. 
