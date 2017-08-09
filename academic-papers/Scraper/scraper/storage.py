import os
import re

def actual_storage_available(path):
    filesystem_stats = os.statvfs(path)
    block_size = filesystem_stats.f_frsize
    blocks_available = filesystem_stats.f_bavail
    return block_size * blocks_available

def _get_part_files(directory):
    filenames = os.listdir(directory)
    app_filename_pattern = re.compile(r'part_\d\d\d\d')
    app_filenames = list(filter(app_filename_pattern.match, filenames))
    return app_filenames


class LocalStorage:

    def __init__(self, root_directory, storage_measure=actual_storage_available, capacity_percent=0.85):
        self._root_directory = root_directory
        self._storage_measure = storage_measure
        self._capacity_percent = capacity_percent
        app_filenames = _get_part_files(self._root_directory)
        if len(app_filenames) == 0:
            self._filenum = 0
        else:
            self._filenum = max(map(lambda filename: int(filename[len('part_'):]), app_filenames))

    def available_storage(self):
        return int(self._storage_measure(self._root_directory) * self._capacity_percent)

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
        with open(filepath, 'wb') as f:
            f.write(data)

    def log_resumption(self, token):
        with open(os.path.join(self._root_directory, 'resumption'), 'a') as f:
            f.write(token)
            f.write('\n')

class MockStorage:

    def __init__(self, capacity_bytes):
        self._capacity_bytes = capacity_bytes
        self._bytes_used = 0

    def has_space(self, data):
        """See if storage has enough space.
        data - must by bytes
        """
        return self._bytes_used + len(data) <= self._capacity_bytes

    def store(self, data):
        """Store data in data store.
        data - must be bytes
        """
        if self._bytes_used + len(data) > self._capacity_bytes:
            raise RuntimeError('Not enough space remaining to store data.')
        self._bytes_used += len(data)
    
    def log_resumption(self, token):
        pass
