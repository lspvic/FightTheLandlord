import os
import logging
import logging.config

os.chdir(os.path.dirname(__file__))
config_file = os.path.join(os.getcwd(), 'logging.conf')
logging.config.fileConfig(str(config_file))
logger = logging.getLogger('root')
logger.info('config updated.')
