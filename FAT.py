import tkinter as tk
from tkinter import messagebox

class FAT:
    def __init__(self, size):
        self.size = size
        self.table = [-1] * size
        self.free_blocks = list(range(size))
        self.files = {}

    def create_file(self, file_name, num_blocks):
        if len(self.free_blocks) < num_blocks:
            return None
        
        allocated_blocks = []
        for _ in range(num_blocks):
            block = self.free_blocks.pop(0)
            allocated_blocks.append(block)
        
        for i in range(num_blocks - 1):
            self.table[allocated_blocks[i]] = allocated_blocks[i + 1]
        self.table[allocated_blocks[-1]] = -1
        
        self.files[file_name] = (allocated_blocks[0], allocated_blocks[-1])
        return allocated_blocks

    def delete_file(self, file_name):
        if file_name not in self.files:
            return False

        start_block = self.files[file_name][0]
        current_block = start_block

        while current_block != -1:
            next_block = self.table[current_block]
            self.free_blocks.append(current_block)
            self.table[current_block] = -1
            current_block = next_block

        self.free_blocks.sort()
        del self.files[file_name]
        return True

    def get_table(self):
        return self.table

    def get_files(self):
        return self.files

class FATApp:
    def __init__(self, root, fat):
        self.root = root
        self.fat = fat
        self.root.title("File Allocation Table Game")

        self.blocks_frame = tk.Frame(self.root)
        self.blocks_frame.pack(padx=10, pady=10)

        self.create_file_frame = tk.Frame(self.root)
        self.create_file_frame.pack(padx=10, pady=10)

        self.create_file_label = tk.Label(self.create_file_frame, text="File Name:")
        self.create_file_label.pack(side=tk.LEFT)
        
        self.file_name_entry = tk.Entry(self.create_file_frame)
        self.file_name_entry.pack(side=tk.LEFT)

        self.num_blocks_label = tk.Label(self.create_file_frame, text="Number of Blocks:")
        self.num_blocks_label.pack(side=tk.LEFT)
        
        self.num_blocks_entry = tk.Entry(self.create_file_frame)
        self.num_blocks_entry.pack(side=tk.LEFT)

        self.create_file_button = tk.Button(self.create_file_frame, text="Create File", command=self.create_file)
        self.create_file_button.pack(side=tk.LEFT)

        self.delete_file_frame = tk.Frame(self.root)
        self.delete_file_frame.pack(padx=10, pady=10)

        self.delete_file_label = tk.Label(self.delete_file_frame, text="File Name to Delete:")
        self.delete_file_label.pack(side=tk.LEFT)
        
        self.delete_file_name_entry = tk.Entry(self.delete_file_frame)
        self.delete_file_name_entry.pack(side=tk.LEFT)

        self.delete_file_button = tk.Button(self.delete_file_frame, text="Delete File", command=self.delete_file)
        self.delete_file_button.pack(side=tk.LEFT)

        self.files_frame = tk.Frame(self.root)
        self.files_frame.pack(padx=10, pady=10)

        self.update_blocks()
        self.update_files()

    def update_blocks(self):
        for widget in self.blocks_frame.winfo_children():
            widget.destroy()

        table = self.fat.get_table()
        for i, next_block in enumerate(table):
            block_label = tk.Label(self.blocks_frame, text=f"Block {i}: {next_block}")
            block_label.pack()

    def update_files(self):
        for widget in self.files_frame.winfo_children():
            widget.destroy()

        files = self.fat.get_files()
        for file_name, (start_block, end_block) in files.items():
            file_label = tk.Label(self.files_frame, text=f"File '{file_name}': Start Block = {start_block}, End Block = {end_block}")
            file_label.pack()

    def create_file(self):
        file_name = self.file_name_entry.get().strip()
        try:
            num_blocks = int(self.num_blocks_entry.get())
            if num_blocks <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number of blocks.")
            return

        if not file_name:
            messagebox.showerror("Invalid input", "Please enter a valid file name.")
            return

        allocated_blocks = self.fat.create_file(file_name, num_blocks)
        if allocated_blocks is None:
            messagebox.showerror("Error", "Not enough free blocks available.")
        else:
            messagebox.showinfo("Success", f"File '{file_name}' created with blocks: {allocated_blocks}")
        
        self.update_blocks()
        self.update_files()

    def delete_file(self):
        file_name = self.delete_file_name_entry.get().strip()
        if not file_name:
            messagebox.showerror("Invalid input", "Please enter a valid file name.")
            return

        success = self.fat.delete_file(file_name)
        if success:
            messagebox.showinfo("Success", f"File '{file_name}' deleted.")
        else:
            messagebox.showerror("Error", f"File '{file_name}' not found.")
        
        self.update_blocks()
        self.update_files()

if __name__ == "__main__":
    root = tk.Tk()
    fat = FAT(size=10)  # Size of the FAT (number of blocks)
    app = FATApp(root, fat)
    root.mainloop()
