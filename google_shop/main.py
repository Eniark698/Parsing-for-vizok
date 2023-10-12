from nordvpn_switcher import initialize_VPN,rotate_VPN,terminate_VPN

from data_gather_all import gather as gather_all
from data_gather_limit import gather
from parse_file_limit import main as main1
from data_overload import overload
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
logger.addHandler(handler)
logger.setLevel(logging.CRITICAL)
import warnings
warnings.filterwarnings("ignore") 


from urllib.request import urlopen
import re as r
 
def getIP():
    d = str(urlopen('http://checkip.dyndns.com/').read())
 
    return r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)
 



initialize_VPN(save=1,area_input=['ukraine'])
print(getIP())
rotate_VPN(google_check=1)

print(getIP())

terminate_VPN()
quit()
def main() -> None:
    try:
        
        
        part_1_done, part_2_done = False, False
       


        
        start=time.time()
        dict1=gather()
        main1()
        overload() 
        print('part_1_done')
        part_1_done=True

        rotate_VPN()
        terminate_VPN()
        quit()

        dict2=gather_all()
        main2()
        overload_all()  
        print('part_2_done')
        part_2_done=True

        terminate_VPN()

    except:
        logger.critical('{}'.format(format_exc()))
        logger.critical('\n not completed\n')
        logger.critical('\n exec time: ' + str(time.time()-start))
        terminate_VPN()

    else:
        logger.critical('limit part\n', dict1)
        logger.critical('all part\n', dict2)
        logger.critical('successfull completed\n')
        logger.critical('\n exec time: ' + str(time.time()-start))


if __name__=='__main__':
    main()


