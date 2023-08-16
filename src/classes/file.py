import os
import json


class FileOperations:
    def __init__(self) -> None:
        self.path = "./output"

    def save_to_file(self, filename, content):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        with open(os.path.join(self.path, filename), "w") as file:
            json.dump(content, file)
