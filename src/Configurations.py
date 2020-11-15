import os


class Configurations:
    """Object holding configurations for the project. Encapsulates reading configs from a fil"""

    def __init__(self, config_file_path="./extra/config.txt"):
        with open(config_file_path, mode="r", encoding="utf-8") as config_file:
            self.__config_dict = dict(arg.rstrip("\n").split("=") for arg in config_file.readlines())

    def __getitem__(self, item):
        return self.__config_dict[item]
