from data_gather_limit import gather
from parse_file_limit import main as main2
from data_overload_limit import overload

import os
import sys
import time
from traceback import format_exc


import logging
from logging.handlers import TimedRotatingFileHandler
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file = '/logs/GoogleShop/GoogleShop_limit.log'
#log_file = './google_shop/log_GoogleShop_all.log'
handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=30)
handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.propagate = False
logger.addHandler(handler)
logger.setLevel(logging.CRITICAL)
import warnings
warnings.filterwarnings("ignore") 


def main() -> None:
    try:
        num_processes=3


        
        start=time.time()
        gather(logger)
        main2(logger,num_processes)
        overload(logger) 
        

        

    except:
        logger.critical('{}'.format(format_exc()))
        logger.critical('NOT COMPLETED')
   
        # try:
        #     logger.critical('limit part\n', signal_1)
        #     logger.critical('limit part is done')
        # except:
        #     logger.critical('not done gathering info part')
        # logger.critical('exec time: ' + str(time.time()-start))

    else:
        logger.info('successfull completed all stages')
        logger.info('exec time: ' + str(time.time()-start))










if __name__=='__main__':
    main()


