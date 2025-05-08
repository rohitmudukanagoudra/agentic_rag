import logging
from logging.handlers import TimedRotatingFileHandler
import os


class Logger:
    """
    A class that configures loggers
    """

    def __init__(self, name="RAG", log_level="DEBUG", log_dir="logs"):
        """
        Configures a daily logger
        :param name: logger's name
        :param log_level: logger severity configuration
        :param log_dir: directory where logs are saved
        """

        # 1. Creates a logger using Python's logging facility.
        self.logger = logging.getLogger(name)

        # 2. Prevent duplicate handlers by checking existing handlers
        if not self.logger.hasHandlers():
            # 3. Sets logger's severity threshold.
            self.logger.setLevel(log_level)

            # 4. Creates a daily log file and stores it at log_dir
            log_filename = "rag_app.log"
            fh = TimedRotatingFileHandler(
                os.path.join(log_dir, log_filename), when="midnight", interval=1
            )

            # 5. Configures the log string format
            formatter = logging.Formatter(
                "%(name)-6s %(asctime)s %(levelname)-6s "
                "thread:%(thread)-8d - %(message)s"
            )
            fh.setFormatter(formatter)

            # Adds the handler to the logger
            self.logger.addHandler(fh)

    def get_logger(self):
        """
        Returns logger
        """
        return self.logger


logger = Logger().get_logger()
