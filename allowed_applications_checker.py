from windows_toasts import Toast, WindowsToaster
import hashlib
import winreg
import pandas as pd

try:  # Reading old snapshot.
    old_allowed_applications = pd.read_csv("allowed_applications.csv", header=0)
except FileNotFoundError:
    old_allowed_applications = None

allowed_applications = []  # Creating list and opening key in advance
allowed_applications_key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows Defender\Windows Defender Exploit Guard\Controlled Folder Access\AllowedApplications")
invalid_applications = []
count = 0

while True:
    try:
        temp = list(winreg.EnumValue(allowed_applications_key, count))  # Add each entry under the open key to the list.
    except OSError:
        break
    try:
        with open(temp[0], "rb") as f:
            digest = hashlib.file_digest(f, "sha512").hexdigest()  # Hashing and storing content in hexadecimal
    except (FileNotFoundError, PermissionError) as e:
        if type(e) is FileNotFoundError:
            invalid_applications.append(temp[0])
            count += 1
            continue
        else:
            count += 1
            continue

    temp.append(digest)
    allowed_applications.append(temp)
    count += 1

allowed_applications_key.Close()  # Close the key once the data collection is done.

new_allowed_applications = pd.DataFrame(allowed_applications, columns=["Directory", "Object holding data", "Type of data", "Checksum"])
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

toaster = WindowsToaster("Windows Defender CFA Allowed Applications")

if len(invalid_applications) > 0:
    ready_string = f"The following applications cannot be found anymore and should have their permissions revoked:\n{invalid_applications}"
    new_toast = Toast()
    new_toast.text_fields = [ready_string]
    toaster.show_toast(new_toast)

if len(modified_applications) > 0:
    ready_string = f"The following applications have been found to have been modified since the last check and may need to have their permissions revoked:\n{modified_applications}"
    new_toast = Toast()
    new_toast.text_fields = [ready_string]
    toaster.show_toast(new_toast)

invalid_applications_df = pd.DataFrame(invalid_applications, columns=["Directory"])
invalid_applications_df.to_csv("invalid_applications.csv", index=False)
modified_applications_df = pd.DataFrame(modified_applications, columns=["Directory"])
modified_applications_df.to_csv("modified_applications.csv", index=False)


