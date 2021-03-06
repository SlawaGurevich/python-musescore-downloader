from configparser import ConfigParser

class OptionHandler():
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.ini')
        if not self.config.has_section("options"):
            self.config.add_section("options")
            with open('config.ini', 'w') as f:
                self.config.write(f)

    def get(self, key):
        return self.config.get("options", key)

    def set(self, key, value):
        self.config.set("options", key, value)
        with open('config.ini', 'w') as f:
            self.config.write(f)

    def delete(self, key):
        self.config.remove_option(key)
        with open('config.ini', 'w') as f:
            self.config.write(f)

    def has(self, key):
        return self.config.has_option("options", key)
