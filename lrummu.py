from mmu import MMU
from mmu import Page
class LruMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for LruMMU
        self.frames = frames
        self.debug_mode = False
        self.memory_frames= [Page() for _ in range(self.frames)]
        
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        return
        

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        self.debug_mode = True
        return

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        self.debug_mode = False
        return

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        return

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        return

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return -1

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return -1

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return -1
