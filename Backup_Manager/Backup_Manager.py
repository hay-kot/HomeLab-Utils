import os
import glob
import configparser
from tqdm import tqdm
from slacker import Slacker
import datetime
import time


def slack_notify(text, channel):
    slack.chat.post_message(
        channel=channel,
        text=text,
        username="Python",
        icon_url="http://devarea.com/wp-content/uploads/2017/11/python-300x300.png",
    )


config = configparser.ConfigParser()
config.read("config.ini")

config_list = config.sections()

for set_configs in tqdm(config_list):
    timestr = time.strftime("%Y.%m.%d")
    directory = config.get(set_configs, "directory")
    file_type = config.get(set_configs, "file_type").split()
    file_list = glob.glob(directory + f"/*{file_type}")
    for file in file_list:
        created = datetime.datetime.fromtimestamp(os.path.getctime(file)).strftime("%Y.%m.%d",)
        path, name = os.path.split(file)
        if name == f"{created}_{set_configs}{file_type[0]}":
            print("File Named Correctly!")
        else:
            print("Renaming Files...")
            new_name = f"{path}/{created}_{set_configs}{file_type[0]}"
            os.rename(file, new_name)

for set_configs in tqdm(config_list):
    timestr = datetime.date.today()
    channel = config.get(set_configs, "channel")
    secret = config.get(set_configs, "secret")
    slack = Slacker(secret)
    directory = config.get(set_configs, "directory")
    file_type = config.get(set_configs, "file_type").split()
    x = config.get(set_configs, "days")
    max_delta = datetime.timedelta(days=int(x))
    for extension in file_type:
        files = glob.glob(directory + f"/*{extension}")
    file_dates = []
    for file in files:
        created = os.path.getctime(file)
        modified = os.path.getmtime(file)
        time = datetime.date.fromtimestamp(min(created, modified))
        file_dates.append(time)
    delta = timestr - max(file_dates)
    delta_str = str(delta)
    split = delta_str.split()
    num_days_old = split[0]
    if delta >= max_delta:
        slack_notify(
            f":warning: *{set_configs}* backup failed. The oldest backup is *{num_days_old} days old* :warning:",
            f"{channel}",
        )
    elif delta <= max_delta:
        slack_notify(
            f":heavy_check_mark: *{set_configs}* backup ran successfully. The oldest backup is *{num_days_old} days old*",
            f"{channel}",
        )
