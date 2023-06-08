import logging, coloredlogs

# Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s [%(levelname)s] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )

# Get the logger
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', 
                    fmt='%(asctime)s [%(levelname)s] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s')