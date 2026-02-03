import os
from utils.enum_path import Path


class FileManager:

    @staticmethod
    def read_txt(path: Path, file_name: str) -> str:
        folder = path.value
        full_path = os.path.join(folder, f"{file_name}.txt")

        with open(full_path, encoding="utf-8") as file:
            return file.read().strip()
