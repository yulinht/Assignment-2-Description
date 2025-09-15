from mmu import MMU
from mmu import Page
import random
class RandMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for RandMMU
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
        # load_page_into_Memory: is accessed, and if no page can be found, disk is accessed, and the data are swapped
        if self.debug_mode:
            print(f"Reading page {page_number}")

        self.load_page_into_memory(page_number)
        if self.debug_mode:
            print(f" Loaded page {page_number} into memory")
            print(f"Total page faults so far: {self.page_faults}")
            print(f"Total disk reads so far: {self.disk_reads}")
            print(f"Total disk writes so far: {self.disk_writes}\n")

        return

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        # load_page_into_Memory: is accessed, and if no page can be found, disk is accessed, and the data are swapped

        # Only writes are required to make the currently accessed page dirty
        if self.debug_mode:
            print(f"Writing page {page_number}")  

        self.load_page_into_memory(page_number) 
        
        # write operation makes the page dirty
        for page in self.memory_frames:
            if page.page_number == page_number:
                page.dirty = True    

        if self.debug_mode:
            print(f" Loaded page {page_number} into memory")
            print(f"Total page faults so far: {self.page_faults}")
            print(f"Total disk reads so far: {self.disk_reads}")
            print(f"Total disk writes so far: {self.disk_writes}\n")
       
        
        return

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.disk_reads

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.page_faults

    def load_page_into_memory(self, page_number):
    
         
        #if not found in memory frames
        self.page_faults += 1
        self.disk_reads += 1
        #page fault occurs
        if self.debug_mode:
            print(f" Page fault on page {page_number}")

        #There are two cases:
        #1.Not found it, frame not full ：The page is read from disk and placed in the next available frame
        for i in range(self.frames):
            if self.memory_frames[i].page_number == -1: 
                self.placement(page_number, i)
                return
            
        
        #2.Not found it, frame full：The page is read from disk and placed in a randomly selected frame, 
        # which is written back to disk if it is dirty  
        self.replace(page_number)
        

        #Found it in memory frames(hit), finish function
        for page in self.memory_frames:
            if page.page_number == page_number:
                if self.debug_mode:
                    print(f"  Hit: Page {page_number} found in memory")
                return
    
        return
       

       

    def placement(self, page_number, frame_index):
        # Place the page in the specified frame index
        self.memory_frames[frame_index].page_number = page_number
        self.memory_frames[frame_index].dirty = False
        return
    
    def replace(self, page_number):
        # Random algorithm: Randomly select a page from the frame and replace. 
        # If the replaced page is dirty: it is written back to disk once
        replace_index = random.randrange(0, self.frames)
        replace_number = self.memory_frames[replace_index].page_number

        if self.memory_frames[replace_index].dirty:
            # If the replaced page is dirty: it is written back to disk once
            self.disk_writes += 1

        if self.debug_mode:
            if self.memory_frames[replace_index].dirty:
                print(f" Dirty page {replace_number} with page {page_number} in frame {replace_index}")
            else:
                print(f" Discaard page {replace_number} with page {page_number} in frame {replace_index}")
        
        self.memory_frames[replace_index].page_number = page_number
        self.memory_frames[replace_index].dirty = False
        return
        