# --- connection.py ---
import os

# マウントされたディレクトリ
mount_directory = "/mount"
local_directory = "/local"
file_name = "database.sqlite"

# ダウンロード関数
def download_database():
    try:
        # ファイルのダウンロード
        file_path_in_mount = os.path.join(mount_directory, file_name)
        with open(file_path_in_mount, "rb") as mount_file:
            file_content = mount_file.read()

        # ローカルディレクトリに保存
        file_path_in_local = os.path.join(local_directory, file_name)
        with open(file_path_in_local, "wb") as local_file:
            local_file.write(file_content)

        print(f"Database file downloaded to {file_path_in_local}")

    except Exception as e:
        print(f"Error downloading database file: {e}")

# アップロード関数
def upload_database():
    try:
        # ローカルディレクトリからファイルを読み込み
        file_path_in_local = os.path.join(local_directory, file_name)
        with open(file_path_in_local, "rb") as local_file:
            file_content = local_file.read()

        # ファイルのアップロード
        file_path_in_mount = os.path.join(mount_directory, file_name)
        with open(file_path_in_mount, "wb") as mount_file:
            mount_file.write(file_content)

        print(f"Database file uploaded to {file_path_in_mount}")

    except Exception as e:
        print(f"Error uploading database file: {e}")

