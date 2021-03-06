import sys
from sys import argv
import datetime
from logging import basicConfig, getLogger, FileHandler, StreamHandler, DEBUG, INFO, ERROR, Formatter
import time
import asyncio
import raidnearby
import findfort
import crop
import os
import concurrent.futures

LOG = getLogger('')

no_findfort = False
if len(argv) >= 2:
    if str(argv[1]) == 'NO_FINDFORT':
        no_findfort = True
        LOG.info('No findfort option selected.')
        LOG.info('Run findfort.py separately to identify new unknown gyms')

cpu_count = os.cpu_count()
LOG.info('{} cpu cores found'.format(cpu_count))

def exception_handler(loop, context):
    loop.default_exception_handler(context)
    exception = context.get('exception')
    if isinstance(exception, Exception):
        LOG.error("Found unhandeled exception. Stoping...")
        loop.stop()

if __name__ == '__main__':
    raid_nearby = raidnearby.RaidNearby()
    if no_findfort == False:
        find_fort = findfort.FindFort()
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(exception_handler)
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count)
    loop.set_default_executor(executor)
    loop.create_task(raid_nearby.main())
    if no_findfort == False:    
        loop.create_task(find_fort.findfort_main())
    loop.create_task(crop.crop_task())
    loop.run_forever()
    loop.close()
