import tkinter as tk
from tkinter import simpledialog, messagebox, ttk


class DragAndDropApp:

    def __init__(self, root):
        self.root = root
        self.root.title("OS Game Group 31")
        self.root.geometry("1280x720")

        self.setup_tabs()

        self.show_instructions()

        self.drag_data = {"x": 0, "y": 0, "item": None}  # Store drag data
        self.placement_order = []  # Track order of blue boxes placement
        self.all_boxes_placed = False  # Flag to check if all blue boxes are placed

        self.num_files = self.prompt_num_files()
        if self.num_files is None:
            return
        # Prompt user for number of block boxes

        self.num_boxes = [0] * self.num_files

        for i in range (self.num_files):
            self.num_boxes[i] = self.prompt_num_boxes() + 1
            if self.num_boxes is None:
                return  # Exit if user cancels the input

        self.create_grid()

        # Dictionary to store memory box occupancy
        self.memory_box_occupancy = {}

        # Create a frame to display memory box occupancy
        self.occupancy_frame = tk.Frame(master=self.tab2, bg="white", width=200, height=600)
        self.occupancy_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.occupancy_label = tk.Label(master=self.occupancy_frame, text="Memory Space Occupancy",
                                        font=("Helvetica", 16))
        self.occupancy_label.pack(pady=10)

        self.occupancy_text = tk.Text(self.occupancy_frame, wrap=tk.WORD, font=("Helvetica", 12))
        self.occupancy_text.pack(fill=tk.BOTH, expand=True)

        # Initialize message_shown attribute
        self.message_shown = False

    def show_instructions(self):
        # Create a new top-level window for the instructions

        # Create a frame inside the top-level window
        self.instruction_frame = tk.Frame(master=self.tab3, bg="white", padx=20, pady=20)
        self.instruction_frame.pack(fill=tk.BOTH, expand=True)

        # Create a Text widget for styled instructions
        self.instructions_text = tk.Text(master=self.instruction_frame, wrap=tk.WORD,
                                         font=("Helvetica", 12),
                                         bg="white", fg="black",
                                         padx=10, pady=10)
        self.instructions_text.pack(fill=tk.BOTH, expand=True)

        # Insert styled text into the Text widget
        self.instructions_text.insert(tk.END, "Group 31: Linked Allocation Game\n\n", "welcome")

        self.instructions_text.insert(tk.END,
                                      "The purpose of this game is to help users better understand how disk blocks are allocated for a file "
                                      "using the Linked Allocation Method.\n\n",
                                      "info")

        self.instructions_text.insert(tk.END, "Instructions:\n", "section_header")

        self.instructions_text.insert(tk.END,
                                      "Drag and drop ",
                                      "info")
        self.instructions_text.insert(tk.END,
                                      " blue boxes (Blocks)", "block")
        self.instructions_text.insert(tk.END,
                                      " into the",
                                      "info")
        self.instructions_text.insert(tk.END,
                                      " grey boxes (Memory Spaces)\n", "memory")
        self.instructions_text.insert(tk.END,
                                      "- Each",
                                      "info")
        self.instructions_text.insert(tk.END,
                                      " grey box (Memory Space)", "memory")

        self.instructions_text.insert(tk.END,
                                      " can only contain one",
                                      "info")
        self.instructions_text.insert(tk.END,
                                      " blue box (Block)\n", "block")
        self.instructions_text.insert(tk.END,
                                      "- When a",
                                      "info")
        self.instructions_text.insert(tk.END,
                                      " blue box (Block)", "block")
        self.instructions_text.insert(tk.END,
                                      " is place into a",
                                      "info")
        self.instructions_text.insert(tk.END,
                                      " grey box (Memory Space)", "memory")
        self.instructions_text.insert(tk.END,
                                      ", it will turn",
                                      "info")
        self.instructions_text.insert(tk.END,
                                      " red",
                                      "occupied")
        self.instructions_text.insert(tk.END,
                                      " to signify that the memory space is occupied.\n",
                                      "info")
        self.instructions_text.insert(tk.END,
                                      "- All \n",
                                      "info")
        self.instructions_text.insert(tk.END,
                                      " blue boxes (Blocks)", "block")
        self.instructions_text.insert(tk.END,
                                      " must be placed to complete the game.\n", "info")
        self.instructions_text.insert(tk.END,
                                      "- Once all the ", "info")
        self.instructions_text.insert(tk.END,
                                      " blue boxes (Blocks)", "block")
        self.instructions_text.insert(tk.END,
                                      " are placed,", "info")
        self.instructions_text.insert(tk.END,
                                      " green arrows (Links)", "arrows")
        self.instructions_text.insert(tk.END,
                                      " will appear to signify the order in which the", "info")
        self.instructions_text.insert(tk.END,
                                      " blue boxes (Blocks)", "block")

        self.instructions_text.insert(tk.END,
                                      " will be retrieved.\n", "info")
        self.instructions_text.insert(tk.END,
                                      "- An additional block will be added to your file to signify the end block, which has a value of (-1).\n\n",
                                      "point")

        self.instructions_text.insert(tk.END, "Enjoy the game and have fun learning about linked allocation!", "info")

        self.instructions_text.insert(tk.END,
                                      " blue boxes (Blocks)", "block")
        # Apply tag formatting
        self.instructions_text.tag_configure("welcome", font=("Helvetica", 14, "bold"))
        self.instructions_text.tag_configure("info", font=("Helvetica", 12))
        self.instructions_text.tag_configure("section_header", font=("Helvetica", 12, "bold"))
        self.instructions_text.tag_configure("block", foreground="blue", font=("Helvetica", 12))
        self.instructions_text.tag_configure("file", foreground="purple", font=("Helvetica", 12))
        self.instructions_text.tag_configure("memory", foreground="grey", font=("Helvetica", 12))
        self.instructions_text.tag_configure("arrows", foreground="green", font=("Helvetica", 12))
        self.instructions_text.tag_configure("occupied", foreground="red", font=("Helvetica", 12))

        # Disable text editing
        self.instructions_text.config(state=tk.DISABLED)

        self.legend()

        # Create a frame inside the top-level window
        self.explanation_frame = tk.Frame(master=self.tab4, bg="white", padx=20, pady=20)
        self.explanation_frame.pack(fill=tk.BOTH, expand=True)

        # Create a Text widget
        self.explanation_text = tk.Text(master=self.explanation_frame, wrap=tk.WORD,
                                        font=("Helvetica", 12),
                                        bg="white", fg="black",
                                        padx=10, pady=10)
        self.explanation_text.pack(fill=tk.BOTH, expand=True)

        # Insert styled text into the Text widget
        self.explanation_text.insert(tk.END, "How does Linked Allocation work?\n\n", "header")
        self.explanation_text.insert(tk.END,
                                     "Each file (purple box) comprises a linked list of blocks (blue boxes). These blocks may or may not be scattered on the disk.\n"
                                     "Each block is made up of two parts: data and a pointer. The data stores the physical data, while the pointer stores the address of the next block.\n\n"
                                     "Typically, a block has a size of 512 bytes: 508 bytes for the data and 4 bytes for the pointer.\n\n")

        self.explanation_text.insert(tk.END, "Features:\n\n", "section_header_features")


        # Insert Benefits with green and bold styling
        self.explanation_text.insert(tk.END, "Benefits:\n", "section_header_benefit")
        self.explanation_text.insert(tk.END,
                                     "- No external fragmentation.\n"
                                     "- No need for compaction.\n\n", "info")

        # Insert Drawbacks with red and bold styling
        self.explanation_text.insert(tk.END, "Drawbacks:\n", "section_header_drawback")
        self.explanation_text.insert(tk.END,
                                     "- Due to the scattering of the blocks, it may take more disk seeks to retrieve all the data.\n"
                                     "- Since each block contains a pointer, the overall file size when using Linked Allocation is larger.\n"
                                     "- If a pointer is lost or damaged, the process may or may not be able to retrieve the address of the next block.\n"
                                     "- Low efficiency in random access: To find the ith block of a file, you must start at the beginning of the file.\n\n",
                                     "info")

        # Insert Improvement Techniques with blue styling
        self.explanation_text.insert(tk.END, "Improvement Techniques:\n", "section_header_improvement")
        self.explanation_text.insert(tk.END,
                                     "- Grouping several blocks into a cluster can improve efficiency, but it increases internal fragmentation as more space is wasted for partially full clusters.\n",
                                     "info")

        # Apply tag formatting
        self.explanation_text.tag_configure("header", font=("Helvetica", 14, "bold"))
        self.explanation_text.tag_configure("info", font=("Helvetica", 12))
        self.explanation_text.tag_configure("section_header_features", font=("Helvetica", 12, "bold"))
        self.explanation_text.tag_configure("section_header_benefit", foreground="green", font=("Helvetica", 12, "bold"))
        self.explanation_text.tag_configure("section_header_drawback", foreground="red", font=("Helvetica", 12, "bold"))
        self.explanation_text.tag_configure("section_header_improvement", foreground="blue", font=("Helvetica", 12, "bold"))

        # Disable text editing
        self.explanation_text.config(state=tk.DISABLED)

    def legend(self):
        # Add legend for memory spaces and blocks
        legend_frame = tk.Frame(master=self.instruction_frame, bg="white", pady=10)
        legend_frame.pack(fill=tk.X)

        legend_title = tk.Label(master=legend_frame, text="Legend", font=("Helvetica", 14, "bold"))
        legend_title.pack()

        # Create canvas for legend items
        legend_canvas = tk.Canvas(master=legend_frame, width=300, height=160, bg="white")
        legend_canvas.pack()

        # Draw legend items
        box_size = 20
        box_margin = 10
        text_margin = 5

        # Purple Box (File)
        legend_canvas.create_rectangle(10, 10, 10 + box_size, 10 + box_size, fill="purple")
        legend_canvas.create_text(10 + box_size + text_margin, 10 + box_size / 2, text="Purple Box (File)", anchor=tk.W)

        # Blue Box (Block)
        legend_canvas.create_rectangle(10, 40, 10 + box_size, 40 + box_size, fill="blue")
        legend_canvas.create_text(10 + box_size + text_margin, 40 + box_size / 2, text="Blue Box (Block)", anchor=tk.W)

        # Light Grey Box (Available Memory Space)
        legend_canvas.create_rectangle(10, 70, 10 + box_size, 70 + box_size, fill="lightgrey")
        legend_canvas.create_text(10 + box_size + text_margin, 70 + box_size / 2, text="Light Grey Box (Memory Space)",
                                  anchor=tk.W)

        # Red Box (Occupied Memory Space)
        legend_canvas.create_rectangle(10, 100, 10 + box_size, 100 + box_size, fill="red")
        legend_canvas.create_text(10 + box_size + text_margin, 100 + box_size / 2,
                                  text="Red Box (Occupied Memory Space)",
                                  anchor=tk.W)

        # Green Arrow (Retrieval Order)
        arrow_start = (10, 130)
        arrow_mid = (10 + box_size / 2, 140)
        arrow_end = (10 + box_size, 130)
        legend_canvas.create_line(arrow_start, arrow_mid, arrow_end, width=2, arrow=tk.LAST, fill="green")
        legend_canvas.create_text(10 + box_size + text_margin, 140, text="Green Arrow (Retrieval Order)", anchor=tk.W)

    def setup_tabs(self):
        self.tab_control = ttk.Notebook(self.root)

        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab4 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Game')
        self.tab_control.add(self.tab2, text='Occupancy')
        self.tab_control.add(self.tab3, text='Instructions')
        self.tab_control.add(self.tab4, text='Explanation')

        self.tab_control.pack(expand=1, fill="both")

        self.tab_control.select(self.tab3)

    def prompt_num_files(self):
        return simpledialog.askinteger("Number of files", "Enter the number of files (1-4):", minvalue=1, maxvalue=4)

    def prompt_num_boxes(self):
        # Prompt user to enter number of block boxes within the range of 1 to 9
        return simpledialog.askinteger("Number of blocks", "Enter the number of blocks (1-9):", minvalue=1,
                                       maxvalue=9)

    def create_grid(self):
        rows, cols = 10, 4
        cell_width, cell_height = 50, 50
        row_spacing = 10  # Space between rows

        # Adjust canvas size to accommodate the grid and border
        canvas_width = cols * (cell_width + 50) + 50
        canvas_height = rows * (cell_height + row_spacing) + 10

        self.canvas = tk.Canvas(master=self.tab1, bg="white", width=canvas_width, height=canvas_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Draw border rectangle around the grid
        self.canvas.create_rectangle(5, 5, canvas_width - 5, canvas_height - 5, outline="orange")

        # Create purple boxes outside the border
        purple_box_size = 60
        purple_box_margin = 10  # Space between purple boxes

        # Initial coordinates for the first purple box outside the border
        purple_box_x1 = canvas_width + 20
        purple_box_y1 = 20

        for i in range(self.num_files):
            # Calculate coordinates for each purple box
            purple_box_x2 = purple_box_x1 + purple_box_size
            purple_box_y2 = purple_box_y1 + purple_box_size

            # Create the purple box on the canvas
            self.canvas.create_rectangle(purple_box_x1, purple_box_y1, purple_box_x2, purple_box_y2, fill="purple")

            # Add file label above the purple box
            file_label_text = f"File {i}"
            file_label_x = (purple_box_x1 + purple_box_x2) / 2
            file_label_y = purple_box_y1 - 10  # Adjust the y-coordinate to give more space

            self.canvas.create_text(file_label_x, file_label_y, text=file_label_text, anchor="center")

            # Update coordinates for the next purple box horizontally
            purple_box_x1 += purple_box_size + purple_box_margin

        # Calculate positions for block boxes dynamically based on the number of boxes
        block_box_size = 30
        block_box_margin = 10
        self.block_boxes = []  # Initialize as an instance variable to store block box IDs and info
        self.rectangles = []  # To store rectangle IDs
        self.labels = []  # To store label IDs

        for j in range(self.num_files):
            # Initial coordinates for the first purple box
            purple_box_x1 = canvas_width + 20 + j * (purple_box_size + purple_box_margin)
            purple_box_y1 = 20
            purple_box_x2 = purple_box_x1 + purple_box_size
            purple_box_y2 = purple_box_y1 + purple_box_size

            for i in range(self.num_boxes[j]):
                # Calculate block box coordinates for each iteration
                block_box_x1 = purple_box_x1 + (purple_box_size - block_box_size) / 2
                block_box_y1 = purple_box_y2 + i * (block_box_size + block_box_margin) + block_box_margin
                block_box_x2 = block_box_x1 + block_box_size
                block_box_y2 = block_box_y1 + block_box_size
                block_box_id = self.canvas.create_rectangle(
                    block_box_x1, block_box_y1, block_box_x2, block_box_y2,
                    fill="blue",
                    tags=("draggable", f"block_box_{j}_{i}")
                )

                # Calculate coordinates for the label to the right of the blue box
                block_label_x = block_box_x2 + block_box_margin - 70
                block_label_y = (block_box_y1 + block_box_y2) / 2
                block_label_text = f"{j}_{i}"

                # Add label to the right of the blue box with black text
                block_label_id = self.canvas.create_text(block_label_x, block_label_y, text=block_label_text,
                                                         anchor="w", fill="black",  # Text color set to black
                                                         tags=("draggable", f"block_box_{j}_{i}"))

                # Add label to the blue box
                self.canvas.create_text(block_label_x, block_label_y, text=block_label_text, anchor="center",
                                        fill="white")

                self.block_boxes.append({
                    'id': block_box_id,
                    'number': i,  # Unique number for each block box
                    'file': j,
                    'original_coords': (block_box_x1, block_box_y1, block_box_x2, block_box_y2)
                    # Store original coordinates
                })
                self.placement_order.append(block_box_id)  # Record the order of placement

        for r in range(rows):
            for c in range(cols):
                x1 = c * (cell_width + 50) + 50  # Adjusted to leave space for labels
                y1 = r * (cell_height + row_spacing) + 10
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgrey", outline="black",
                                                       tags=("box", f"box_{r}_{c}"))
                label_text = f"{r * cols + c}"
                label_id = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=label_text, anchor="center")
                self.rectangles.append(rect_id)
                self.labels.append(label_id)

        # Bind events for draggable items (block boxes)
        self.canvas.tag_bind("draggable", "<ButtonPress-1>", self.on_drag_start)
        self.canvas.tag_bind("draggable", "<B1-Motion>", self.on_drag_motion)
        self.canvas.tag_bind("draggable", "<ButtonRelease-1>", self.on_drag_stop)

    def on_drag_start(self, event):
        '''Beginning drag of a block box'''
        # Check if the click is within the canvas area
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        border_width = 5

        if event.x < border_width or event.x > canvas_width - border_width or \
                event.y < border_width or event.y > canvas_height - border_width:
            return

        # Raise the draggable item to the top
        self.canvas.tag_raise("draggable")

        # record the item and its location
        closest_item = self.canvas.find_closest(event.x, event.y)
        if closest_item:
            self.drag_data["item"] = closest_item[0]
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
        else:
            return

    def on_drag_motion(self, event):
        '''Handle dragging of a block box'''
        # compute how much the mouse has moved
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]

        # move the block box the appropriate amount
        self.canvas.move(self.drag_data["item"], delta_x, delta_y)

        # record the new position
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

        # Check if the box is being dragged outside the orange border
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        border_width = 5

        if event.x < border_width or event.x > canvas_width - border_width or \
                event.y < border_width or event.y > canvas_height - border_width:
            self.canvas.coords(self.drag_data["item"], *self.block_boxes[self.drag_data["item"] - 1]['original_coords'])

    def on_drag_stop(self, event):
        '''End drag of a block box'''
        if not self.drag_data["item"]:
            return  # Ensure drag data is set

        # Check if the drop position is within the grid area
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        border_width = 5

        if event.x < border_width or event.x > canvas_width - border_width or \
                event.y < border_width or event.y > canvas_height - border_width:
            # If dropped outside the border, snap back to the purple box position based on item
            for block_box in self.block_boxes:
                if self.drag_data["item"] == block_box['id']:
                    self.canvas.coords(self.drag_data["item"], *block_box['original_coords'])
                    break
        else:
            # Find the closest rectangle
            nearest_item = self.canvas.find_closest(event.x, event.y)[0]

            # Check if the nearest item is a memory box
            tags = self.canvas.gettags(nearest_item)
            if "box" in tags:
                nearest_rect = nearest_item
            else:
                nearest_rect = None
                all_items = self.canvas.find_all()
                smallest_distance = float('inf')
                for item in all_items:
                    item_tags = self.canvas.gettags(item)
                    if "box" in item_tags:
                        x1, y1, x2, y2 = self.canvas.coords(item)
                        cx = (x1 + x2) / 2
                        cy = (y1 + y2) / 2
                        distance = ((event.x - cx) ** 2 + (event.y - cy) ** 2) ** 0.5
                        if distance < smallest_distance:
                            nearest_rect = item
                            smallest_distance = distance

            if nearest_rect:
                # Check if the memory box already contains a block box
                if nearest_rect in self.memory_box_occupancy:
                    # If already occupied by another block box, show a message and snap back to the original position
                    messagebox.showinfo("Occupied Space", "The memory space is already occupied.")
                    for block_box in self.block_boxes:
                        if self.drag_data["item"] == block_box['id']:
                            self.canvas.coords(self.drag_data["item"], *block_box['original_coords'])
                            break
                else:
                    # If the block box was previously placed in another memory box, remove the occupancy
                    for memory_box, block_box in self.memory_box_occupancy.items():
                        if block_box == self.drag_data["item"]:
                            del self.memory_box_occupancy[memory_box]
                            self.canvas.itemconfig(memory_box, fill="lightgrey")
                            break

                    # Move the block box to the memory box position and mark it as occupied
                    x1, y1, x2, y2 = self.canvas.coords(nearest_rect)
                    self.canvas.coords(self.drag_data["item"], x1, y1, x2, y2)
                    self.canvas.addtag_withtag(f"occupied", nearest_rect)

                    # Change the color of the block box to red and unbind drag events
                    self.canvas.itemconfig(self.drag_data["item"], fill="red")
                    self.canvas.dtag(self.drag_data["item"], "draggable")

                    # Update memory box occupancy dictionary
                    memory_box_number = self.canvas.itemcget(self.labels[self.rectangles.index(nearest_rect)], "text")
                    block_box_number = next((block_box_info['number'] for block_box_info in self.block_boxes if
                                             block_box_info['id'] == self.drag_data["item"]), None)
                    block_file_number = next((block_box_info['file'] for block_box_info in self.block_boxes if
                                              block_box_info['id'] == self.drag_data["item"]), None)
                    if block_box_number is not None:
                        self.memory_box_occupancy[nearest_rect] = self.drag_data["item"]

                        # Update occupancy display
                        self.update_occupancy_display()

                        messagebox.showinfo("Memory Allocation",
                                            f"Block {block_box_number} was placed into memory space {memory_box_number} of file {block_file_number}.")

                        # Check if all block boxes are placed
                        if all(self.canvas.itemcget(block_box['id'], "fill") == "red" for block_box in
                               self.block_boxes):
                            self.all_boxes_placed = True

        # # Check if all boxes are placed and draw lines accordingly
        if self.all_boxes_placed:
            self.draw_lines_between_boxes()

        # reset the drag data
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def draw_lines_between_boxes(self):
        # Clear existing lines
        self.canvas.delete("lines")

        # Dictionary to store start and end information for each file
        file_info = {}

        # Iterate through each file
        for file_id in range(self.num_files):
            # Find all block boxes belonging to the current file
            file_block_boxes = [box for box in self.block_boxes if box['file'] == file_id]

            if file_block_boxes:
                # Determine start and end block boxes for the current file
                start_box_id = file_block_boxes[0]['id']
                end_box_id = file_block_boxes[-1]['id']

                # Draw lines between consecutive block boxes based on placement order within the file
                for i in range(len(file_block_boxes) - 1):
                    current_box_id = file_block_boxes[i]['id']
                    next_box_id = file_block_boxes[i + 1]['id']

                    x1, y1, x2, y2 = self.canvas.coords(current_box_id)
                    cx1, cy1 = (x1 + x2) / 2, (y1 + y2) / 2

                    x1, y1, x2, y2 = self.canvas.coords(next_box_id)
                    cx2, cy2 = (x1 + x2) / 2, (y1 + y2) / 2

                    # Draw the line with an arrow pointing towards the next block box
                    arrow_length = 10
                    self.canvas.create_line(cx1, cy1, cx2, cy2, fill="green", tags="lines",
                                            arrow=tk.LAST, arrowshape=(arrow_length, arrow_length, 3))

                # Store start and end information for the current file
                start_memory_box = next(
                    (mem_box for mem_box, block_box in self.memory_box_occupancy.items() if block_box == start_box_id),
                    None)
                end_memory_box = next(
                    (mem_box for mem_box, block_box in self.memory_box_occupancy.items() if block_box == end_box_id),
                    None)

                start_box_label = self.canvas.itemcget(self.labels[self.rectangles.index(start_memory_box)],
                                                       "text") if start_memory_box else "N/A"
                end_box_label = self.canvas.itemcget(self.labels[self.rectangles.index(end_memory_box)],
                                                     "text") if end_memory_box else "N/A"

                total_red_boxes = sum(
                    1 for mem_box, block_box in self.memory_box_occupancy.items() if
                    block_box in [box['id'] for box in file_block_boxes]
                )

                # Store file information for later display
                file_info[file_id] = (start_box_label, end_box_label, total_red_boxes)

        self.display_file_info(file_info)

    def display_file_info(self, file_info):

        for file_id, info in file_info.items():
            start_box_label, end_box_label, total_red_boxes = info
            messagebox.showinfo(
                f"File Information",
                    f"File: {file_id}\n"
                f"Start: {start_box_label}\n"
                f"End: {end_box_label}\n"
                f"Length: {total_red_boxes}"
            )

    def update_occupancy_display(self):
        # Clear previous text
        self.occupancy_text.delete(1.0, tk.END)

        # Write updated occupancy information
        for memory_box, block_box in self.memory_box_occupancy.items():
            memory_box_number = self.canvas.itemcget(self.labels[self.rectangles.index(memory_box)], "text")
            block_box_number = next(
                (block_box_info['number'] for block_box_info in self.block_boxes if block_box_info['id'] == block_box),
                None)
            block_file_number = next(
                (block_box_info['file'] for block_box_info in self.block_boxes if block_box_info['id'] == block_box),
                None)
            if block_box_number is not None:
                self.occupancy_text.insert(tk.END,
                                           f"Memory Space {memory_box_number} occupied by Block {block_box_number} of File {block_file_number}\n")
        self.occupancy_text.insert(tk.END, "\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = DragAndDropApp(root)
    root.mainloop()
