import redis
import time
r = redis.Redis(host='localhost', port=6379)
def setMsg(): 
    r.set('MSG','eric')
    print r.get('MSG')
    
def pipeline():
    r.set('k1','foo')
    pipe = r.pipeline()
    pipe.set('foo', 'bar')
    pipe.get('bing')
    
    pipe.execute()

def pipewatch():
    '''
    watch is necessary to ensure an atomic increment.  Exception is raised if it changes during the sequence.
    '''
    pipe = r.pipeline()
    while 1:
        try:
            pipe.watch('OUR-SEQUENCE-KEY')
            current_value = pipe.get('OUR-SEQUENCE-KEY')
            next_value = int(current_value) + 1
            pipe.multi()
            pipe.set('OUR-SEQUENCE-KEY', next_value)
            pipe.execute()
            break
        except redis.WatchError:
            continue
        finally:
            pipe.reset()
          
            
    
def pubsub():
    p = r.pubsub()
    p.subscribe('channel1', 'channel2', 'channel3')
    # or p.psubscribe('channel*')
    while 1:
        msg = p.get_message()
        if msg is not None:
            print msg
def my_handler(message):
    print "my_handler: ",message['data']
    
    
def pubsub2():
    ''' Wait for message '''
    p = r.pubsub()
    p.subscribe(**{'my-channel': my_handler})
    p.get_message()
    for msg in p.listen():
        print msg  
                  
def pubsub3():
    ''' Polling '''
    p = r.pubsub()
    p.subscribe(**{'my-channel': my_handler})
    p.get_message()
    while 1:
        msg = p.get_message()
        if msg is not None:
            print msg    
            

def pubsub4():
    ''' In thread'''
    p = r.pubsub()
    p.subscribe(**{'my-channel': my_handler})
    thread = p.run_in_thread(sleep_time=0.001)
    time.sleep(10)
       
#setMsg()
#pipeline()
#pipewatch()
pubsub4()