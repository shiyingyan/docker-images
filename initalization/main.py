import glob
import os
import datetime
import pyinotify
import logging

log = pyinotify.log
# log.setLevel(logging.DEBUG)
log.setLevel(logging.INFO)


@DeprecationWarning
class MyEventHandler1(pyinotify.ProcessEvent):
    log.info("Starting monitor...")

    # def my_init(self, wm: pyinotify.WatchManager):
    def my_init(self, **kwargs):
        self.wm = kwargs['wm']

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
        log.info(f"process_IN_CREATE event : {event}")

        exclude_path_prefixes = ['prometheus', 'forward', 'promdump',
                                 'node-exporter', 'cadvisor', 'scada_exporter',
                                 'voice', 'telegraf', 'chronograf', ]
        in_exclude = [d for d in exclude_path_prefixes if
                      str(event.pathname).startswith(f'/data/{d}') or str(event.pathname).startswith(f'/logs/{d}')]
        if in_exclude:
            return

        watched_files = [w.path for wd, w in self.wm.watches.items()]
        log.debug(f'create file, watched_files:{watched_files}')

        if os.path.exists(event.pathname):
            os.system(f'chown -R 3188:3166 {event.pathname}')

            if event.pathname not in watched_files:
                os.system(f'chown -R 3188:3166 {event.pathname}')
                self.wm.add_watch(event.pathname,
                                  pyinotify.IN_ATTRIB | pyinotify.IN_CREATE | pyinotify.IN_IGNORED,
                                  rec=True)
            else:
                fstat = os.stat(event.pathname)
                user_id = fstat.st_uid
                group_id = fstat.st_gid
                if user_id != 3188 or group_id != 3166:
                    os.system(f'chown 3188:3166 {event.pathname}')

    def process_IN_ATTRIB(self, event):
        log.info(f"process_IN_ATTRIB event : {event}")

        if not str(event.pathname).startswith('/data') and not str(event.pathname).startswith('/logs'):
            return

        if os.path.exists(event.pathname):
            fstat = os.stat(event.pathname)
            user_id = fstat.st_uid
            group_id = fstat.st_gid
            if user_id != 3188 or group_id != 3166:
                os.system(f'chown 3188:3166 {event.pathname}')

    def process_IN_IGNORED(self, event):
        log.info(f"process_IN_IGNORE event : {event}")
        self.delete_file(event)

    def process_IN_DELETE(self, event):
        log.info(f"process_IN_DELETE event : {event}")
        self.delete_file(event)

    def delete_file(self, event):
        log.debug(f'delete file, watched_files:{[w.path for w in self.wm.watches.values()]}')

        if hasattr(event, 'wd') and event.wd > 0 and event.wd in self.wm.watches:
            self.wm.rm_watch(event.wd, rec=True)
            return

        wd = [wd for wd, watch in self.wm.watches.items() if watch.path == event.pathname]
        if wd:
            self.wm.rm_watch(wd[0], rec=True)


class MyEventHandler(pyinotify.ProcessEvent):
    log.info("Starting monitor...")

    # def my_init(self, wm: pyinotify.WatchManager):
    def my_init(self, **kwargs):
        self.wm = kwargs['wm']

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
        log.info(f"process_IN_CREATE event : {event}")

        exclude_path_prefixes = ['prometheus', 'forward', 'promdump',
                                 'node-exporter', 'cadvisor', 'scada_exporter',
                                 'voice', 'telegraf', 'chronograf', ]
        in_exclude = [d for d in exclude_path_prefixes if
                      str(event.pathname).startswith(f'/data/{d}') or str(event.pathname).startswith(f'/logs/{d}')]
        if in_exclude:
            return

        if log.level <= logging.DEBUG:
            watched_files = [w.path for wd, w in self.wm.watches.items()]
            log.debug(f'create file, watched_files:{watched_files}')

        self.modify_access(event)

    def process_IN_ATTRIB(self, event):
        log.info(f"process_IN_ATTRIB event : {event}")

        if not str(event.pathname).startswith('/data') and not str(event.pathname).startswith('/logs'):
            return

        self.modify_access(event)

    def modify_access(self, event):
        if os.path.exists(event.pathname):
            fstat = os.stat(event.pathname)
            user_id = fstat.st_uid
            group_id = fstat.st_gid
            if user_id != 3188 or group_id != 3166:
                os.system(f'chown 3188:3166 {event.pathname}')

    def process_IN_IGNORED(self, event):
        log.debug(f"process_IN_IGNORED event : {event}")

        if log.level <= logging.DEBUG:
            watched_files = [w.path for wd, w in self.wm.watches.items()]
            log.debug(f'create file, watched_files:{watched_files}')


def pre_handler(event):
    log.debug(f'preHandler:{event}')


def main():
    # watch manager
    wm = pyinotify.WatchManager()
    wm.add_watch('/data', pyinotify.IN_ATTRIB | pyinotify.IN_CREATE, rec=True, auto_add=True)
    wm.add_watch('/logs', pyinotify.IN_ATTRIB | pyinotify.IN_CREATE, rec=True, auto_add=True)
    # /tmp是可以自己修改的监控的目录
    # event handler
    eh = MyEventHandler(pevent=pre_handler, wm=wm)

    # notifier
    notifier = pyinotify.Notifier(wm, eh)

    # bug-fix: loop之前，再做一次额外的权限修改。防止未监听之前新创建的文件权限问题
    os.system(''' find /logs \\( \\! -uid 3188 -o \\! -gid 3166 \\) -exec chown 3188:3166 {} \\; ''')
    os.system(''' find /data \\( \\! -uid 3188 -o \\! -gid 3166 \\) -exec chown 3188:3166 {} \\; ''')

    notifier.loop()


if __name__ == '__main__':
    main()
