#from nordvpn_switcher import initialize_VPN,rotate_VPN,terminate_VPN

from data_gather_all import gather as gather_all
from data_gather_limit import gather
from parse_file_limit import main as main1
from data_overload_limit import overload
from parse_file_all import main as main2
from data_overload_all import overload as overload_all

import os
import time
from traceback import format_exc


import logging
from logging.handlers import TimedRotatingFileHandler
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#log_file = '/logs/GoogleShop/GoogleShop_all.log'
log_file = './google_shop/log_GoogleShop_all.log'
handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=30)
handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.propagate = False
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
import warnings
warnings.filterwarnings("ignore") 


def main() -> None:
    try:
        
        
        part_1_done, part_2_done = False, False
       


        
        start=time.time()
        # dict1=gather()
        # main1()
        # overload() 
        # print('part_1_done')
        # part_1_done=True

        

        # dict2=gather_all()
        # main2()
        # overload_all()  
        # print('part_2_done')
        # part_2_done=True

        

    except:
        logger.debug('{}'.format(format_exc()))
        logger.debug('NOT COMPLETED')
        try:
            dict1
            logger.debug('limit part is done')
        except:
            logger.debug('not done limit part')
        try:
            dict2
            logger.debug('all part is done')
        except:
            logger.debug('not done all part')
        logger.debug('exec time: ' + str(time.time()-start))

    else:
        logger.debug('limit part\n', dict1)
        logger.debug('all part\n', dict2)
        logger.debug('successfull completed')
        logger.debug('exec time: ' + str(time.time()-start))


if __name__=='__main__':
    main()


