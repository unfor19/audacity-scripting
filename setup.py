from os import getcwd, path, getenv
from setuptools import setup

# Change accordingly ----------------------------
PACKAGE_DIR_NAME = "audacity_scripting"
GITHUB_OWNER = "unfor19"
GITHUB_REPOSITORY = "audacity-scripting"
# -----------------------------------------------


# Keep the same structure, should NOT be changed
DEFAULT_PACKAGE_VERSION = '9.9.9rc99'
PACKAGE_VERSION = getenv('PACKAGE_VERSION', DEFAULT_PACKAGE_VERSION)
SOURCE_VERSION_PATH = path.join(getcwd(), 'version')
TARGET_VERSION_PATH = path.join(
    getcwd(),
    'src', PACKAGE_DIR_NAME, 'utils', '__version__.py'
)

if PACKAGE_VERSION == DEFAULT_PACKAGE_VERSION:
    # Attempting to read the version from file
    if path.isfile(SOURCE_VERSION_PATH):
        with open(SOURCE_VERSION_PATH, "r", encoding='utf-8') as fh:
            PACKAGE_VERSION = fh.read().strip()
            if not PACKAGE_VERSION:
                raise ValueError(
                    f"PACKAGE_VERSION is empty in {SOURCE_VERSION_PATH}")

with open(TARGET_VERSION_PATH, "w", encoding='utf-8') as fh:  # noqa: E501
    fh.write(f"package_version = '{PACKAGE_VERSION}'\n")

with open(SOURCE_VERSION_PATH, "w", encoding='utf-8') as fh:  # noqa: E501
    fh.write(PACKAGE_VERSION)


setup(
    version=PACKAGE_VERSION,
    download_url=f'https://github.com/{GITHUB_OWNER}/{GITHUB_REPOSITORY}/archive/{PACKAGE_VERSION}.tar.gz',  # noqa: E501
)
# -----------------------------------------------
