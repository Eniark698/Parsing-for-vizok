from data_gather_limit import gather
from parse_file_limit import main as main2
from data_overload_limit import overload

import os
import sys
import time
from traceback import format_exc


import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/logs/GoogleShop/GoogleShop_limit.log"),
        logging.StreamHandler()
    ]
)
import warnings
warnings.filterwarnings("ignore") 


def main() -> None:
    try:
        num_processes=3


        
        start=time.time()
        gather(logging)
        main2(logging,num_processes)
        overload(logging) 
        

        

    except:
        logging.critical('{}'.format(format_exc()))
        logging.critical({'BAD':'NOT COMPLETED'})
   


    else:
        logging.info({'SUCCESS':"successfull completed all stages", 'exec time': str(time.time() - start)})










if __name__=='__main__':
    main()


