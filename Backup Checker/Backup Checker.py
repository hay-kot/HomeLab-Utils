import os
import glob
import configparser
from tqdm import tqdm
import datetime
from slacker import Slacker


def slack_notify(text, channel):
    slack.chat.post_message(
        channel=channel,
        text=text,
        username="Python Test",
        icon_url="http://devarea.com/wp-content/uploads/2017/11/python-300x300.png",
    )


timestr = datetime.date.today()
config = configparser.ConfigParser()
config.read("config.ini")

config_list = config.sections()

for set_configs in tqdm(config_list):
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
