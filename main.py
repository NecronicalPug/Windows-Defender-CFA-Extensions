import configparser
import hashlib
import winreg
import pandas as pd

# Setup basic config. 

try:  # Reading old snapshot.
    old_allowed_applications = pd.read_csv("allowed_applications.csv", header=0)
except FileNotFoundError:
    old_allowed_applications = None

allowed_applications = []  # Creating list and opening key in advance
allowed_applications_key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows Defender\Windows Defender Exploit Guard\Controlled Folder Access\AllowedApplications")
invalid_applications = []
count = 0  # Counter for enum.

while True:
    try:
        temp = list(winreg.EnumValue(allowed_applications_key, count))  # Add each entry under the open key to the list.
    except OSError:
        break
    try:
        with open(temp[0], "rb") as f:
            digest = hashlib.file_digest(f, "sha512").hexdigest()  # Hashing and storing content in hexadecimal
    except FileNotFoundError:
        invalid_applications.append(temp[0])
        count += 1
        continue
    temp.append(digest)
    allowed_applications.append(temp)
    count += 1

allowed_applications_key.Close()  # Close the key once the data collection is done.

print(invalid_applications)  # Finish up deleting invalid apps from controlled folder access.


new_allowed_applications = pd.DataFrame(allowed_applications, columns=("Directory", "Object holding data", "Type of data", "Checksum"))
new_allowed_applications.to_csv("allowed_applications.csv", index=False)  # Store data until next cycle.

modified_applications = []
for i in range(len(old_allowed_applications)):
    old_row = old_allowed_applications.iloc[[i]]
    directory = old_row.Directory.values[0]  # Directly accessing directory value.
    new_row = new_allowed_applications.loc[new_allowed_applications.Directory == directory]
    if old_row.Checksum.values[0] == new_row.Checksum.values[0]:
        pass
    else:
        modified_applications.append(new_row.Directory.values[0])

#  Finish up warning the user about modified applications

