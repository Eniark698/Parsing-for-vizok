from data_gather import gather
from main2 import main as main2
from data_overload import overload
from pr_br import prx

import os
import time
from traceback import format_exc


import logging
from logging.handlers import TimedRotatingFileHandler
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file = '/logs/GoogleShop/GoogleShop_all.log'
#log_file = './google_shop/log_GoogleShop_all.log'
handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=30)
handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.ERROR)
import warnings
warnings.filterwarnings("ignore") 






def main() -> None:
    try:
        try:
            os.remove('./google_shop/file_temp.xls')
        except:
            pass


        


        
        start=time.time()
        prx_l=prx()
        gather()
        main2(prx_l)
        overload()



        
    except:
        logger.setLevel(logging.ERROR)
        logger.error('{}'.format(format_exc()))
        logger.error('\n not completed\n')
        logger.error('\n exec time: ' + str(time.time()-start))
    else:
        logger.setLevel(logging.ERROR)
        logger.error('successfull completed\n')
        logger.error('\n exec time: ' + str(time.time()-start))
        logger.setLevel(logging.ERROR)


if __name__=='__main__':
    main()


