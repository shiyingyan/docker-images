import os
import datetime
import pyinotify
import logging


class MyEventHandler(pyinotify.ProcessEvent):
    logging.info("Starting monitor...")

    def __init__(self, wm: pyinotify.WatchManager):
        self.wm = wm

    def process_IN_CREATE(self, event):
        '''
            The event possible fields are:
              - wd (int): Watch Descriptor.
              - mask (int): Mask.
              - maskname (str): Readable event name.
              - path (str): path of the file or directory being watched.
              - name (str): Basename of the file or directory against which the
                      event was raised in case where the watched directory
                      is the parent directory. None if the event was raised
                      on the watched item itself. This field is always provided
                      even if the string is ''.
              - pathname (str): Concatenation of 'path' and 'name'.
              - src_pathname (str): Only present for IN_MOVED_TO events and only in
                      the case where IN_MOVED_FROM events are watched too. Holds the
                      source pathname from where pathname was moved from.
              - cookie (int): Cookie.
              - dir (bool): True if the event was raised against a directory.
        '''
        logging.info("IN_ATTRIB event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))

        if not os.path.exists(event.pathname):
            # when delete file
            return

        exclude_path_prefixes = ['prometheus', 'forward', 'promdump',
                                 'node-exporter', 'cadvisor', 'scada_exporter',
                                 'voice', 'telegraf', 'chronograf', ]
        in_exclude = [d for d in exclude_path_prefixes if
                      str(event.pathname).startswith(f'/data/{d}') or str(event.pathname).startswith(f'/logs/{d}')]
        if in_exclude:
            return

        os.system(f'chown -R 3188:3166 {event.pathname}')

        watched_files = [w.path for wd, w in self.wm.watches.items()]
        if event.pathname not in watched_files:
            self.wm.add_watch(event.pathname, pyinotify.IN_ATTRIB | pyinotify.IN_CREATE | pyinotify.IN_DELETE, rec=True)

    def process_IN_ATTRIB(self, event):
        logging.info("IN_ATTRIB event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))

        if not os.path.exists(event.pathname):
            # when delete file
            return

        if not str(event.pathname).startswith('/data') and not str(event.pathname).startswith('/logs'):
            return

        fstat = os.stat(event.pathname)
        user_id = fstat.st_uid
        group_id = fstat.st_gid
        if user_id != 3188 or group_id != 3166:
            os.system(f'chown 3188:3166 {event.pathname}')

    def process_IN_ACCESS(self, event):
        pass

    def process_IN_CLOSE_NOWRITE(self, event):
        pass

    def process_IN_CLOSE_WRITE(self, event):
        pass

    def process_IN_DELETE(self, event):
        logging.info("IN_DELETE event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))
        if hasattr(event, 'wd') and event.wd > 0 and event.wd in self.wm.watches:
            self.wm.rm_watch(event.wd, rec=True)
            return

        wd = [wd for wd, watch in self.wm.watches.items() if watch.path == event.pathname]
        if wd:
            self.wm.rm_watch(wd[0], rec=True)

    def process_IN_MODIFY(self, event):
        pass

    def process_IN_OPEN(self, event):
        pass

    def process_IN_Q_VEERFLOW(self, event):
        pass


def config_log():
    from concurrent_log import ConcurrentTimedRotatingFileHandler

    ldir = '/logs/initialization'
    os.makedirs(ldir, exist_ok=True)
    logger_path = os.path.join(ldir, 'main.log')

    log_level = logging.INFO
    log_handler = ConcurrentTimedRotatingFileHandler(filename=logger_path, when='H', interval=24, backupCount=20)
    log_handler.setLevel(log_level)
    log_handler.setFormatter(logging.Formatter('%(levelname)s:%(asctime)s:%(module)s:%(lineno)s:%(message)s'))
    logging.basicConfig(**{'handlers': [log_handler], 'level': log_level})


def main():
    # config_log()
    # watch manager
    wm = pyinotify.WatchManager()
    wm.add_watch('/data', pyinotify.IN_ATTRIB | pyinotify.IN_CREATE, rec=True)
    wm.add_watch('/logs', pyinotify.IN_ATTRIB | pyinotify.IN_CREATE, rec=True)
    # /tmp是可以自己修改的监控的目录
    # event handler
    eh = MyEventHandler(wm)

    # notifier
    notifier = pyinotify.Notifier(wm, eh)

    # bug-fix: loop之前，再做一次额外的权限修改。防止未监听之前新创建的文件权限问题
    os.system(''' find /logs \\( \\! -uid 3188 -o \\! -gid 3166 \\) -exec chown 3188:3166 {} \\; ''')
    os.system(''' find /data \\( \\! -uid 3188 -o \\! -gid 3166 \\) -exec chown 3188:3166 {} \\; ''')

    notifier.loop()


if __name__ == '__main__':
    main()
