import tkinter as tk
from tkinter import simpledialog, messagebox

class DragAndDropApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Grid of Boxes")
        self.root.geometry("800x600")

        self.drag_data = {"x": 0, "y": 0, "item": None}  # Store drag data

        # Prompt user for number of blue boxes
        self.num_boxes = self.prompt_num_boxes()
        if self.num_boxes is None:
            return  # Exit if user cancels the input

        self.create_grid()

        # Dictionary to store grey box occupancy
        self.grey_box_occupancy = {}

        # Create a frame to display grey box occupancy
        self.occupancy_frame = tk.Frame(self.root, bg="white", width=200, height=600)
        self.occupancy_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.occupancy_label = tk.Label(self.occupancy_frame, text="Grey Box Occupancy", font=("Helvetica", 16))
        self.occupancy_label.pack(pady=10)

        self.occupancy_text = tk.Text(self.occupancy_frame, wrap=tk.WORD, font=("Helvetica", 12))
        self.occupancy_text.pack(fill=tk.BOTH, expand=True)

    def prompt_num_boxes(self):
        # Prompt user to enter number of blue boxes
        return simpledialog.askinteger("Number of Blue Boxes", "Enter the number of blue boxes:")

    def create_grid(self):
        rows, cols = 10, 4
        cell_width, cell_height = 50, 50
        row_spacing = 10  # Space between rows

        # Adjust canvas size to accommodate the grid and border
        canvas_width = cols * (cell_width + 50) + 50
        canvas_height = rows * (cell_height + row_spacing) + 10

        self.canvas = tk.Canvas(self.root, bg="white", width=canvas_width, height=canvas_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Draw border rectangle around the grid
        self.canvas.create_rectangle(5, 5, canvas_width - 5, canvas_height - 5, outline="black")

        # Create a green box outside the border
        green_box_size = 60
        green_box_x1 = canvas_width + 10
        green_box_y1 = 10
        green_box_x2 = green_box_x1 + green_box_size
        green_box_y2 = green_box_y1 + green_box_size
        self.canvas.create_rectangle(green_box_x1, green_box_y1, green_box_x2, green_box_y2, fill="green")

        # Calculate positions for blue boxes dynamically based on number of boxes
        blue_box_size = 30
        blue_box_margin = 10
        self.blue_boxes = []  # Initialize as an instance variable to store blue box IDs and info

        for i in range(self.num_boxes):
            blue_box_x1 = green_box_x1 + (green_box_size - blue_box_size) / 2
            blue_box_y1 = green_box_y1 + (green_box_size - blue_box_size) / 2 + i * (blue_box_size + blue_box_margin)
            blue_box_x2 = blue_box_x1 + blue_box_size
            blue_box_y2 = blue_box_y1 + blue_box_size
            blue_box_id = self.canvas.create_rectangle(blue_box_x1, blue_box_y1, blue_box_x2, blue_box_y2, fill="blue",
                                                       tags=("draggable", f"blue_box_{i}"))
            self.blue_boxes.append({
                'id': blue_box_id,
                'number': i + 1  # Unique number for each blue box
            })

        self.rectangles = []  # To store rectangle IDs
        self.labels = []  # To store label IDs

        for r in range(rows):
            for c in range(cols):
                x1 = c * (cell_width + 50) + 50  # Adjusted to leave space for labels
                y1 = r * (cell_height + row_spacing) + 10
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgrey", outline="black",
                                                       tags=("box", f"box_{r}_{c}"))
                label_text = f"{r * cols + c}"
                label_id = self.canvas.create_text(x1 - 25, y1 + cell_height / 2, text=label_text, anchor="e")
                self.rectangles.append(rect_id)
                self.labels.append(label_id)

        # Bind events for draggable items (blue boxes)
        self.canvas.tag_bind("draggable", "<ButtonPress-1>", self.on_drag_start)
        self.canvas.tag_bind("draggable", "<B1-Motion>", self.on_drag_motion)
        self.canvas.tag_bind("draggable", "<ButtonRelease-1>", self.on_drag_stop)

    def on_drag_start(self, event):
        '''Beginning drag of a blue box'''
        # Raise the draggable item to the top
        self.canvas.tag_raise("draggable")

        # record the item and its location
        self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_drag_motion(self, event):
        '''Handle dragging of a blue box'''
        # compute how much the mouse has moved
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]

        # move the blue box the appropriate amount
        self.canvas.move(self.drag_data["item"], delta_x, delta_y)

        # record the new position
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_drag_stop(self, event):
        '''End drag of a blue box'''
        if not self.drag_data["item"]:
            return  # Ensure drag data is set

        # Check if the drop position is within the grid area
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        border_width = 5

        if event.x < border_width or event.x > canvas_width - border_width or \
                event.y < border_width or event.y > canvas_height - border_width:
            # If dropped outside the border, snap back to the green box position based on item
            for blue_box in self.blue_boxes:
                if self.drag_data["item"] == blue_box['id']:
                    self.canvas.coords(self.drag_data["item"], blue_box['x1'], blue_box['y1'], blue_box['x2'],
                                       blue_box['y2'])
                    break
        else:
            # Find the closest rectangle
            nearest_item = self.canvas.find_closest(event.x, event.y)[0]

            # Check if the nearest item is a grey box
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
                # Check if the grey box already contains a blue box
                occupied_tags = self.canvas.gettags(nearest_rect)
                if "occupied" in occupied_tags:
                    # Check if the blue box being moved is already in this grey box
                    current_blue_box = self.canvas.find_withtag("occupied")[0]
                    if current_blue_box == self.drag_data["item"]:
                        # If dragging the same blue box onto itself, do nothing
                        return

                    # If already occupied by another blue box, show a message and snap back to the original position
                    messagebox.showinfo("Occupied Box", "The grey box is already occupied.")
                    for blue_box in self.blue_boxes:
                        if self.drag_data["item"] == blue_box['id']:
                            self.canvas.coords(self.drag_data["item"], blue_box['x1'], blue_box['y1'], blue_box['x2'],
                                               blue_box['y2'])
                            break
                else:
                    # Remove "occupied" tag from the previously occupied grey box, if any
                    for item in self.canvas.find_withtag("occupied"):
                        self.canvas.dtag(item, "occupied")

                    # Move the blue box to the grey box position and mark it as occupied
                    x1, y1, x2, y2 = self.canvas.coords(nearest_rect)
                    self.canvas.coords(self.drag_data["item"], x1, y1, x2, y2)
                    self.canvas.addtag_withtag(f"occupied", nearest_rect)

                    # Update grey box occupancy dictionary
                    grey_box_number = self.canvas.itemcget(self.labels[self.rectangles.index(nearest_rect)], "text")
                    blue_box_number = None
                    for blue_box in self.blue_boxes:
                        if self.drag_data["item"] == blue_box['id']:
                            blue_box_number = blue_box['number']
                            break
                    self.grey_box_occupancy[int(grey_box_number)] = blue_box_number

                    # Update occupancy display
                    self.update_occupancy_display()

                    messagebox.showinfo("Box Placement",
                                        f"The blue box {blue_box_number} was placed into grey box {grey_box_number}.")

        # reset the drag data
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def update_occupancy_display(self):
        # Clear previous text
        self.occupancy_text.delete(1.0, tk.END)

        # Write updated occupancy information
        for grey_box_number, blue_box_number in self.grey_box_occupancy.items():
            self.occupancy_text.insert(tk.END, f"Grey Box {grey_box_number}: Blue Box {blue_box_number}\n")
        self.occupancy_text.insert(tk.END, "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = DragAndDropApp(root)
    root.mainloop()
