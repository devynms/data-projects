import os
import re
from gevent.os import tp_write


# Might belong in an architecture specific module...
def actual_storage_available(path):
    filesystem_stats = os.statvfs(path)
    block_size = filesystem_stats.f_frsize
    blocks_available = filesystem_stats.f_bavail
    return block_size * blocks_available


# Might belong in an architecture specific module...
def actual_file_writer(path, mode, data):
    with open(path, mode) as f:
        tp_write(f, data)


def _get_part_files(directory):
    filenames = os.listdir(directory)
    app_filename_pattern = re.compile(r'part_\d\d\d\d')
    app_filenames = list(filter(app_filename_pattern.match, filenames))
    return app_filenames


class LocalStorage:

    def __init__(self, root_directory,
                 storage_measure=actual_storage_available,
                 capacity_percent=0.85,
                 write_file=actual_file_writer):
        self._root_directory = root_directory
        self._storage_measure = storage_measure
        self._capacity_percent = capacity_percent
        self._write_file = write_file
        app_filenames = _get_part_files(self._root_directory)
        if len(app_filenames) == 0:
            self._filenum = 0
        else:
            self._filenum = max(
                map(lambda filename: int(filename[len('part_'):]),
                    app_filenames))

    def available_storage(self):
        return int(self._storage_measure(self._root_directory) *
                   self._capacity_percent)

    def has_space(self, data):
        """See if storage has enough space.
        data - must by bytes
        """
        return len(data) <= self.available_storage()

    def store(self, data):
        """Store data in data store.
        data - must be bytes
        """
        if not self.has_space(data):
            raise RuntimeError('Not enough space remaining to store data.')
        self._filenum += 1
        filename = f'part_{self._filenum:04d}'
        filepath = os.path.join(self._root_directory, filename)
        self._write_file(filepath, 'wb', data)

    def log_resumption(self, token):
        path = os.path.join(self._root_directory, 'resumption')
        if token is None:
            data = 'NONE'
        else:
            data = token + '\n'
        self._write_file(path, 'a', data)


class MockStorage:

    def __init__(self, capacity_bytes):
        self._capacity_bytes = capacity_bytes
        self.bytes_used = 0
        self.store_count = 0
        self.log_resumption_count = 0

    def available_storage(self):
        return self._capacity_bytes - self.bytes_used

    def has_space(self, data):
        """See if storage has enough space.
        data - must by bytes
        """
        return self.bytes_used + len(data) <= self._capacity_bytes

    def store(self, data):
        """Store data in data store.
        data - must be bytes
        """
        if self.bytes_used + len(data) > self._capacity_bytes:
            raise RuntimeError('Not enough space remaining to store data.')
        self.bytes_used += len(data)
        self.store_count += 1

    def log_resumption(self, token):
        self.log_resumption_count += 1
