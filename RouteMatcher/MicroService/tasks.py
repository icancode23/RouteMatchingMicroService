from celery.decorators import task
from celery import shared_task
from celery.utils.log import get_task_logger
import time

logger = get_task_logger(__name__)

@shared_task
def rebuild_search_index():
	print "check"
	for i in range(20):
		print i 
    #import time 
    #time.sleep(20) # mimicking a long running process
    print('rebuilt search index')

    return 42