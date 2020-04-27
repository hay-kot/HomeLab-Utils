import os
import glob
import shutil
import time
import configparser
from tqdm import tqdm


def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


timestr = time.strftime("%Y.%m.%d")
config = configparser.ConfigParser()
config.read("config.ini")

config_list = config.sections()

for set_configs in tqdm(config_list):
    name = set_configs
    source = config.get(set_configs, "source")
    destination = config.get(set_configs, "destination")
    all_files = config.get(set_configs, "all_files")
    clean_up = config.get(set_configs, "clean_up")
    keep_num = config.getint(set_configs, "keep")
    os.chdir(destination)

    # This deal with what files are going to be copied:  All/Newest
    if all_files == "True":
        new_name = f"{timestr}_{name}"
        copyanything(source, new_name)
        target = os.path.join(destination, new_name)
    elif all_files == "False":
        list_of_files = glob.glob(source + "/*")
        latest_file = max(list_of_files, key=os.path.getctime, default=0)
        filename, extension = os.path.splitext(latest_file)
        new_name = f"{timestr}_{name}{extension}"
        copyanything(latest_file, new_name)
        target = os.path.join(destination, new_name)

    # This deals with clean-up of the destination directory
    backup = shutil.make_archive(new_name, "zip", destination, target)
    if os.path.isdir(target):
        shutil.rmtree(target)
    elif os.path.isfile(target):
        os.remove(target)

    # This deals with processing the clean_up/keep aspects of the file back-up
    list_of_files = glob.glob(destination + "/*")
    clean_list = []
    for files in list_of_files:
        # print(files)
        filename = os.path.basename(files)
        if name in filename:
            clean_list.append(files)
    clean_list.sort(key=os.path.getctime, reverse=True)
    for files in clean_list[keep_num:]:
        if os.path.isfile(files):
            os.remove(files)
