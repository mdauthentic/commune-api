import configparser
from pathlib import Path


def parse_config():
    """Read and convert configuration file to dict"""
    path_own_dir = Path(__file__).resolve().parent
    path_conf = path_own_dir / "config.ini"
    parser = configparser.ConfigParser()
    parser.read(path_conf)

    return {sect: dict(parser.items(sect)) for sect in parser.sections()}
