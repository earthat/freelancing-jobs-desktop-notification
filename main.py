import threading
import time
import logging
from win10toast import ToastNotifier
import requests
import notificationClick
import webbrowser


toaster = ToastNotifier()
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class MyThread(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(MyThread,self).__init__(group=group, target=target,name=name)
        self.args = args
        self.kwargs = kwargs
        self._return = None

    def run(self):

        # threading.Timer(12.0, fetchJobs).start()

        storeJobs = {}
        session = requests.get(url, headers=oauth_headers, params=para)

        op = (session.json())
        op1 = op['result']['projects']

        self._return = op1

    def join(self):
        threading.Thread.join(self)
        return self._return

def notification(Jobs):
    for i in range(0, len(Jobs)):
        toaster.show_toast(str(Jobs[i]['title']),
                           str([Jobs[i]['currency']['code'], Jobs[i]['budget']['maximum']]),
                           # str('http://www.freelancer.com'),
                           icon_path=None
                           )
        if notificationClick.checkClickLocation():
            webbrowser.open_new_tab('www.freelancer.com/projects/' + Jobs[i]['seo_url'])

if __name__ == '__main__':

    # credentials for freelancer developer API
    url = "https://www.freelancer.com/api/projects/0.1/projects/active/"
    oauth_headers = {"Freelancer-OAuth-V1": "XXXXXXXXXXXXXXXXXX"}
    para = {
        'query': ['Matlab, python, machine learning'],
        # 'query':'Matlab',
        'sort_field': 'time_updated',
        'limit': 20,
        'or_search_query': True
    }

    # put the API call in threading
    t = MyThread(args=(url,), kwargs={'oauth_headers': oauth_headers, 'para': para})
    t.start()
    Jobs = t.join()
    prevJobs={}
    for i in range(0, len(Jobs)):   # store all jobs as previous which will be compared with new jobs continuously
        prevJobs[i] = [Jobs[i]['title']]

    notification(Jobs) # desktop notification function called

    while True:      # hit the api continuously and display notification if any new job is posted
        storeJobs = {}
        t = MyThread(args=(url,), kwargs={'oauth_headers':oauth_headers, 'para':para})
        t.start()
        op1=t.join()
        if not op1:
            time.sleep(600)
            t.start()
            op1 = t.join()
        print(op1[0]['title'])
        for i in range(0, len(op1)):
            storeJobs[i] = [op1[i]['title']]


        notshared_items = {}
        for (k, jobs) in enumerate(list(storeJobs.values())):
            cnt = 0
            for j in range(len(prevJobs)):
                if storeJobs[k][0] != prevJobs[j][0]:
                    cnt = cnt + 1
            if (cnt + 1) != len(prevJobs):
                notshared_items[k] = jobs

        if list(notshared_items.keys()):
            # showNotification(op1[list(notshared_items.keys())[0]])
            keys=list(notshared_items.keys())
            #op2 = op1[keys[0]:keys[len(keys)-1]+1]
            op2=[op1[x] for x in keys]
            notification(op2)  # desktop notification function called
        prevJobs = storeJobs
