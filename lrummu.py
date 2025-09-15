from mmu import MMU
from mmu import Page

class LruMMU(MMU):
    def __init__(self, frames):
        self.frames = frames
        self.debug_mode = False
        # Suppose Page() defaults to page_number = -1 and dirty = False
        self.memory_frames = [Page() for _ in range(self.frames)]

        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0

    def set_debug(self):
        self.debug_mode = True

    def reset_debug(self):
        self.debug_mode = False

    def read_memory(self, page_number):
        if self.debug_mode:
            print(f"Reading page {page_number}")

        self.load_page_into_memory(page_number)

        if self.debug_mode:
            print(f" Loaded page {page_number} into memory")
            print(f"Total page faults so far: {self.page_faults}")
            print(f"Total disk reads so far: {self.disk_reads}")
            print(f"Total disk writes so far: {self.disk_writes}\n")

    def write_memory(self, page_number):
        if self.debug_mode:
            print(f"Writing page {page_number}")

        self.load_page_into_memory(page_number)

      # Mark the page as dirty
        index = self.find_page_index(page_number)
        if index is not None:
            self.memory_frames[index].dirty = True
            # Move it to the front since it was just visited (MRU)
            used = self.memory_frames.pop(index)
            self.memory_frames.insert(0, used)

        if self.debug_mode:
            print(f"Loaded page {page_number} into memory and marked dirty")
            print(f"Total page faults so far: {self.page_faults}")
            print(f"Total disk reads so far: {self.disk_reads}")
            print(f"Total disk writes so far: {self.disk_writes}\n")

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults

    
    def find_page_index(self, page_number):
        #Returns the index of page_number in memory_frames; None if not found
        for i, p in enumerate(self.memory_frames):
            if p.page_number == page_number:
                return i
        return None

    def load_page_into_memory(self, page_number):
        # Make sure page_number is in memory (read in from disk and replace LRU pages if needed) 
        #  check if it's in memory first (hit)
        hit_index = self.find_page_index(page_number)
        if hit_index is not None:
            # Hit: Move the page to the front (MRU)
            used = self.memory_frames.pop(hit_index)
            self.memory_frames.insert(0, used)
            if self.debug_mode:
                print(f"  Hit: Page {page_number} found in memory (frame {hit_index})")
            return

        # miss -> page fault
        self.page_faults += 1
        self.disk_reads += 1
        if self.debug_mode:
            print(f" Page fault on page {page_number}")

        # Case 1: Empty frame exists (page_number == -1), put it in 
        for i in range(self.frames):
            if self.memory_frames[i].page_number == -1:
                self.placement(page_number, i)
                return

        # Case 2: No empty frame, LRU replacement (least used at the end)
        self.replace(page_number)

    def placement(self, page_number, frame_index):
        # Put page at the specified frame_index and move it to the front (MRU) 
        # Place on the specified frame (the default Page object that overwrites an empty frame)
        self.memory_frames[frame_index].page_number = page_number
        self.memory_frames[frame_index].dirty = False

        # The frame is moved to the front as MRU
        used = self.memory_frames.pop(frame_index)
        self.memory_frames.insert(0, used)

        if self.debug_mode:
            print(f" Placed page {page_number} into empty frame {frame_index} -> moved to MRU")

    def replace(self, page_number):
        # Replace LRU page (end of list), write back to disk if the replaced page is dirty
        replace_index = self.frames - 1  # LRU 在末尾
        replaced_page = self.memory_frames[replace_index]
        replace_number = replaced_page.page_number

        if replaced_page.dirty:
            # Write back to disk
            self.disk_writes += 1
            if self.debug_mode:
                print(f" Dirty page {replace_number} written back to disk before replace")

        if self.debug_mode and not replaced_page.dirty:
            print(f" Discard page {replace_number} (clean) and load page {page_number}")

        # Pop out the oldest page and insert the new one at the top
        self.memory_frames.pop(replace_index)
        new_page = Page()
        new_page.page_number = page_number
        new_page.dirty = False
        self.memory_frames.insert(0, new_page)

        if self.debug_mode:
            print(f" Replaced frame {replace_index} (was page {replace_number}) with page {page_number} at MRU")
