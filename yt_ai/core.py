from yt_ai.utils.configreader import Config


class Core:
    def __init__(self, config_file):
        self.config = Config(config_file)
        