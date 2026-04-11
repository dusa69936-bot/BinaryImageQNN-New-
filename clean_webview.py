import os
import shutil

path = r'c:\Users\91817\OneDrive\Documents\Desktop\BinaryImageQNN\WebViewApp'
folders_to_delete = ['app', 'app_backup', 'components', 'hooks', 'constants', 'scripts', '.expo', '.vscode', 'app_backup']

for folder in folders_to_delete:
    full_path = os.path.join(path, folder)
    if os.path.exists(full_path):
        try:
            shutil.rmtree(full_path)
            print(f"Deleted: {folder}")
        except Exception as e:
            print(f"Failed to delete {folder}: {e}")

files_to_delete = ['expo-env.d.ts', 'tsconfig.json']
for file in files_to_delete:
    full_path = os.path.join(path, file)
    if os.path.exists(full_path):
        try:
            os.remove(full_path)
            print(f"Deleted file: {file}")
        except Exception as e:
            print(f"Failed to delete file {file}: {e}")
