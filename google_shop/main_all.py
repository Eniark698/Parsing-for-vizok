from data_gather_all import gather
from parse_file_all import main as main2
from data_overload_all import overload

import os
import time
from traceback import format_exc


import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/logs/GoogleShop/GoogleShop_all.log"),
        logging.StreamHandler()
    ]
)
import warnings
warnings.filterwarnings("ignore") 


def main() -> None:
    try:
        num_processes = 3

        start = time.time()
        gather(logging)
        main2(logging, num_processes)
        overload(logging)

    except:
        logging.critical('{}'.format(format_exc()))
        logging.critical({'BAD':'NOT COMPLETED'})
   

      

    else:
        logging.info({'SUCCESS':"successfull completed all stages", 'exec time': str(time.time() - start)})


if __name__ == "__main__":
    main()
