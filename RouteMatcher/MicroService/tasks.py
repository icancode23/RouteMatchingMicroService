@task
def rebuild_search_index():
     time.sleep(500) # mimicking a long running process
     print('rebuilt search index')
     return 42