import os

file_path = "my_custom_spreadsheet.csv"

# Check if file exists and is readable
if os.path.exists(file_path) and os.access(file_path, os.R_OK):
    print("File exists and is readable.")
    print(f"File size: {os.path.getsize(file_path)} bytes")
    print(f"Absolute path: {os.path.abspath(file_path)}")
    print(f"Permissions: {oct(os.stat(file_path).st_mode)}")
else:
    print("File does not exist or is not readable.")
