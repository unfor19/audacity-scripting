from ..utils.logger import logger
import os
app_name = os.getenv('AUDACITY_SCRIPTING_APP_NAME', 'audacity-scripting')


def main():
    logger.info("Hello World!")


if __name__ == "__main__":
    main()
