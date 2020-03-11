import logging

class StarterKitLogging:
    def __init__(self,logpath,logfile,title):
        self.logpath=logpath
        self.logfile=logfile
        self.title=title
    def startLogging(self):
        logging.basicConfig(
            filename='{0}{1}'.format(self.logpath,self.logfile),
            filemode = 'a',
            format='%(asctime)s ----- %(levelname)s ::::: %(message)s ..... (%(name)s)',
            datefmt='%Y-%m-%d %H:%M:%S %Z %z',
            level=logging.DEBUG
        )
        logging.info('Start {0}'.format(self.title))
    def endLogging(self):
        logging.info('End {0}'.format(self.title))
