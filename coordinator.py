import customtkinter as ctk
from tkinter import messagebox
from db_config import get_connection
from tkcalendar import DateEntry
import datetime
import tkinter.ttk as ttk
import tkinter as tk

def view_volunteer_details():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Username, Email, contact_no, Category, Address, NGOID FROM volunteers")
        rows = cursor.fetchall()

        if not rows:
            messagebox.showinfo("No Volunteers", "There are no volunteer records.")
            return

        # Create window
        win = ctk.CTkToplevel()
        win.title("Volunteer Details")
        win.geometry("900x500")
        win.configure(bg="white")

        # Green banner header
        header = ctk.CTkFrame(win, fg_color="#5CAD8A")
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text="Volunteer Details",
            font=("Arial", 18, "bold"),
            text_color="white"
        ).pack(pady=12)

        # Frame for Treeview + Scrollbars
        frame = ctk.CTkFrame(win)
        frame.pack(padx=10, pady=10, expand=True, fill="both")

        columns = ("Username", "Email", "contact_no", "Category", "Address", "NGO ID")

        # Scrollbars
        y_scroll = ttk.Scrollbar(frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = ttk.Scrollbar(frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        # Treeview
        tree = ttk.Treeview(frame, columns=columns, show="headings",
                            yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor="center")

        # Insert rows with alternating tag styles
        for index, row in enumerate(rows):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            tree.insert("", "end", values=row, tags=(tag,))

        tree.pack(fill="both", expand=True)
        y_scroll.config(command=tree.yview)
        x_scroll.config(command=tree.xview)

        # Style for Treeview
        style = ttk.Style()
        style.theme_use("default")

        # Column heading style
        style.configure("Treeview.Heading",
                        font=('Arial', 12, 'bold'),
                        background="black",
                        foreground="white",
                        relief="raised")

        # Main Treeview style
        style.configure("Treeview",
                        rowheight=30,
                        font=('Arial', 11),
                        bordercolor="black",
                        borderwidth=1)

        # Row color tags
        tree.tag_configure('evenrow', background="#f0f0f0")  # light gray
        tree.tag_configure('oddrow', background="white")

        win.protocol("WM_DELETE_WINDOW", lambda: [cursor.close(), conn.close(), win.destroy()])

    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch volunteers.\n{str(e)}")
def view_beneficiaries():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT ID, Name, Age, Gender, Contact FROM beneficiaries")
        rows = cursor.fetchall()

        if not rows:
            messagebox.showinfo("No Beneficiaries", "No beneficiary records found.")
            return

        # Create window
        win = ctk.CTkToplevel()
        win.title("Beneficiaries")
        win.geometry("700x400")
        win.configure(bg="white")

        # Green header banner for title
        header = ctk.CTkFrame(win, fg_color="#5CAD8A")  # Custom green background
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text="Beneficiaries",
            font=("Arial", 18, "bold"),
            text_color="white"
        ).pack(pady=12)

        # Frame for Treeview + Scrollbars
        frame = ctk.CTkFrame(win)
        frame.pack(padx=10, pady=10, expand=True, fill="both")

        columns = ("ID", "Name", "Age", "Gender", "Contact")

        # Scrollbars
        y_scroll = ttk.Scrollbar(frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = ttk.Scrollbar(frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        # Treeview
        tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")

        # Insert rows with alternating colors
        for index, row in enumerate(rows):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            tree.insert("", "end", values=row, tags=(tag,))

        tree.pack(expand=True, fill="both")
        y_scroll.config(command=tree.yview)
        x_scroll.config(command=tree.xview)

        # Treeview Style
        style = ttk.Style()
        style.theme_use("default")

        # Column heading style
        style.configure("Treeview.Heading",
                        font=('Arial', 12, 'bold'),
                        background="black",  # Column heading background black
                        foreground="white",
                        relief="raised")

        # Main Treeview style (for rows)
        style.configure("Treeview",
                        rowheight=30,
                        font=('Arial', 11),
                        bordercolor="black",
                        borderwidth=1)

        # Row color tags
        tree.tag_configure('evenrow', background="#f0f0f0")  # light gray for even rows
        tree.tag_configure('oddrow', background="white")  # white for odd rows

        win.protocol("WM_DELETE_WINDOW", lambda: [cursor.close(), conn.close(), win.destroy()])

    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch beneficiaries.\n{str(e)}")

def assign_task_to_volunteer():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        assign_win = ctk.CTkToplevel()
        assign_win.title("Assign Task")
        assign_win.geometry("600x500")
        assign_win.configure(fg_color="white")

        # Header
        header_frame = ctk.CTkFrame(assign_win, fg_color="white")
        header_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(header_frame, text="Task Assignment", font=("Arial", 20, "bold"), text_color="#333").pack(anchor="w", padx=30)
        ctk.CTkLabel(header_frame, text="Create and assign a new task", font=("Arial", 12), text_color="#888").pack(anchor="w", padx=30)

        form_frame = ctk.CTkFrame(assign_win, fg_color="white")
        form_frame.pack(padx=40, pady=10, fill="both", expand=True)

        # Title
        ctk.CTkLabel(form_frame, text="Title", anchor="w", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 2))
        task_desc_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter task title")
        task_desc_entry.pack(fill="x", pady=5)

        # Description (optional, but removed as per code logic — if needed, add back)
        # ctk.CTkLabel(form_frame, text="Description", anchor="w").pack(anchor="w", pady=(10, 2))
        # task_description_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter task description")
        # task_description_entry.pack(fill="x", pady=5)

        # Due Date
                # Deadline Label
        ctk.CTkLabel(form_frame, text="Deadline", anchor="w", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 2))

        deadline_container = ctk.CTkFrame(form_frame, fg_color="white")
        deadline_container.pack(fill="x", pady=5)

        # Entry to show selected date
        deadline_entry = ctk.CTkEntry(deadline_container, placeholder_text="YYYY-MM-DD")
        deadline_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        def open_calendar():
            # Temporary top-level window for calendar
            top = tk.Toplevel(assign_win)
            top.title("Select Date")
            top.geometry("250x220")
            top.transient(assign_win)  # Attach to parent window
            top.grab_set()             # Make it modal so it grabs all focus


            cal = DateEntry(top, width=12, background='darkblue',
                            foreground='white', borderwidth=2, year=2025, date_pattern='yyyy-mm-dd')
            cal.pack(pady=20)

            def select_date():
                deadline_entry.delete(0, tk.END)
                deadline_entry.insert(0, cal.get_date().strftime("%Y-%m-%d"))
                top.destroy()

            ttk.Button(top, text="Select", command=select_date).pack(pady=10)

                # Calendar Button
        calendar_button = ctk.CTkButton(deadline_container, text="📅", width=40, command=open_calendar)
        calendar_button.pack(side="right")


        # Assign To
        ctk.CTkLabel(form_frame, text="Assign To", anchor="w", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 2))
        volunteer_id_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter volunteer username")
        volunteer_id_entry.pack(fill="x", pady=5)

        # Optional Event ID
        ctk.CTkLabel(form_frame, text="Event ID (optional)", anchor="w", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 2))
        event_id_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter Event ID (if any)")
        event_id_entry.pack(fill="x", pady=5)

        # Button Frame
        button_frame = ctk.CTkFrame(form_frame, fg_color="white")
        button_frame.pack(pady=20)

        def submit_task():
            try:
                vid = volunteer_id_entry.get()
                task_name = task_desc_entry.get()
                deadline = deadline_entry.get()
                eid = event_id_entry.get() if event_id_entry.get().isdigit() else None

                if not vid or not task_name or not deadline:
                    messagebox.showerror("Invalid Input", "Fill all required fields correctly.")
                    return

                cursor.execute("""
                    INSERT INTO tasks (Name, Deadline, EventsID)
                    VALUES (%s, %s, %s)
                """, (task_name, deadline, eid))
                task_id = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO volunteer_tasks (VolunteerUsername, TaskID, task_name)
                    VALUES (%s, %s, %s)
                """, (vid, task_id, task_name))

                conn.commit()
                messagebox.showinfo("Success", f"Task '{task_name}' assigned to Volunteer '{vid}' successfully!")
                assign_win.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Task assignment failed.\n{str(e)}")
            finally:
                cursor.close()
                conn.close()

        # Buttons
        ctk.CTkButton(button_frame, text="Cancel", fg_color="lightgray", text_color="black", hover_color="#ddd", command=assign_win.destroy).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Create Task", fg_color="#5CAD8A", hover_color="green", command=submit_task).pack(side="left", padx=10)

        assign_win.protocol("WM_DELETE_WINDOW", lambda: [cursor.close(), conn.close(), assign_win.destroy()])

    except Exception as e:
        messagebox.showerror("Connection Error", str(e))
        # Calendar Button
        calendar_button = ctk.CTkButton(deadline_container, text="📅", width=40, command=open_calendar)
        calendar_button.pack(side="right")


        # Assign To
        ctk.CTkLabel(form_frame, text="Assign To", anchor="w", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 2))
        volunteer_id_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter volunteer username")
        volunteer_id_entry.pack(fill="x", pady=5)

        # Optional Event ID
        ctk.CTkLabel(form_frame, text="Event ID (optional)", anchor="w", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 2))
        event_id_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter Event ID (if any)")
        event_id_entry.pack(fill="x", pady=5)

        # Button Frame
        button_frame = ctk.CTkFrame(form_frame, fg_color="white")
        button_frame.pack(pady=20)

        def submit_task():
            try:
                vid = volunteer_id_entry.get()
                task_name = task_desc_entry.get()
                deadline = deadline_entry.get()
                eid = event_id_entry.get() if event_id_entry.get().isdigit() else None

                if not vid or not task_name or not deadline:
                    messagebox.showerror("Invalid Input", "Fill all required fields correctly.")
                    return

                cursor.execute("""
                    INSERT INTO tasks (Name, Deadline, EventsID)
                    VALUES (%s, %s, %s)
                """, (task_name, deadline, eid))
                task_id = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO volunteer_tasks (VolunteerUsername, TaskID, task_name)
                    VALUES (%s, %s, %s)
                """, (vid, task_id, task_name))

                conn.commit()
                messagebox.showinfo("Success", f"Task '{task_name}' assigned to Volunteer '{vid}' successfully!")
                assign_win.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Task assignment failed.\n{str(e)}")
            finally:
                cursor.close()
                conn.close()

        # Buttons
        ctk.CTkButton(button_frame, text="Cancel", fg_color="lightgray", text_color="black", hover_color="#ddd", command=assign_win.destroy).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Create Task", fg_color="#5CAD8A", hover_color="green", command=submit_task).pack(side="left", padx=10)

        assign_win.protocol("WM_DELETE_WINDOW", lambda: [cursor.close(), conn.close(), assign_win.destroy()])

    except Exception as e:
        messagebox.showerror("Connection Error", str(e))

# def show_volunteer_tasks():
#     # Connect to MySQL
#     conn = get_connection()
#     cursor = conn.cursor()
#     # Execute query
#     cursor.execute("SELECT * FROM volunteer_tasks")
#     rows = cursor.fetchall()
#     columns = [desc[0] for desc in cursor.description]

#     # Create new window
#     new_window = tk.Toplevel()
#     new_window.title("Volunteer Tasks")

#     # Create Treeview
#     tree = ttk.Treeview(new_window, columns=columns, show='headings')

#     # Define columns
#     for col in columns:
#         tree.heading(col, text=col)
#         tree.column(col, width=150, anchor=tk.CENTER)

#     # Insert data
#     for row in rows:
#         tree.insert('', tk.END, values=row)

#     # Add scrollbar
#     scrollbar = ttk.Scrollbar(new_window, orient=tk.VERTICAL, command=tree.yview)
#     tree.configure(yscroll=scrollbar.set)

#     # Layout
#     tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#     # Close connection
#     cursor.close()
#     conn.close()
def show_volunteer_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    new_window = tk.Toplevel()
    new_window.title("Volunteer Tasks")
    new_window.geometry("700x500")

    # --- Category Filter Section ---
    filter_frame = tk.Frame(new_window)
    filter_frame.pack(pady=10)

    tk.Label(filter_frame, text="Category:").pack(side=tk.LEFT, padx=5)
    category_entry = tk.Entry(filter_frame)
    category_entry.pack(side=tk.LEFT, padx=5)

    tk.Label(filter_frame, text="New Task:").pack(side=tk.LEFT, padx=5)
    task_entry = tk.Entry(filter_frame, width=30)
    task_entry.pack(side=tk.LEFT, padx=5)

    def apply_update():
        category = category_entry.get()
        new_task = task_entry.get()

        if not category or not new_task:
            messagebox.showerror("Missing Data", "Please enter both category and task.")
            return

        try:
            update_query = """
                UPDATE volunteer_tasks vt
                JOIN volunteers v ON vt.VolunteerUsername = v.Username
                SET vt.task_name = %s
                WHERE v.Category = %s
            """
            cursor.execute(update_query, (new_task, category))
            conn.commit()
            messagebox.showinfo("Success", "Task updated for all volunteers in category: " + category)
            refresh_treeview()  # Reload tree data
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(filter_frame, text="Update Task", bg="#5CAD8A", fg="black", command=apply_update).pack(side=tk.LEFT, padx=10)


    # --- Treeview Section ---
    tree = ttk.Treeview(new_window, show='headings')
    tree.pack(fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(tree, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh_treeview():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("""
            SELECT vt.VolunteerUsername, vt.TaskID, vt.task_name, v.Category
            FROM volunteer_tasks vt
            JOIN volunteers v ON vt.VolunteerUsername = v.Username
        """)
        rows = cursor.fetchall()
        columns = ["VolunteerUsername", "TaskID", "task_name", "Category"]
        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor=tk.CENTER)
        for row in rows:
            tree.insert('', tk.END, values=row)

    refresh_treeview()

    new_window.protocol("WM_DELETE_WINDOW", lambda: [cursor.close(), conn.close(), new_window.destroy()])


def show_all_events_with_status():
    conn = get_connection()
    cursor = conn.cursor()

    # Step 1: Update the statuses first
    update_query = """
        UPDATE events e
        JOIN (
            SELECT EventsID, SUM(Amount) as total_amt
            FROM sponsors
            GROUP BY EventsID
        ) s ON e.ID = s.EventsID
        SET e.status = 'successful'
        WHERE s.total_amt >= e.amt_required;
    """
    cursor.execute(update_query)
    conn.commit()

    # Step 2: Get all event data with current status
    cursor.execute("""
        SELECT ID, Name, Location, Date, amt_required, status 
        FROM events
    """)
    all_events = cursor.fetchall()

    # Create the window
    event_win = tk.Toplevel()
    event_win.title("All Events with Status")
    event_win.geometry("800x500")

    # Header with green background
    header = tk.Frame(event_win, bg="#4CAF50")
    header.pack(fill="x")

    label = tk.Label(header, text="All Events with Status", font=("Arial", 16, "bold"), bg="#4CAF50", fg="white")
    label.pack(pady=10)

    # Style configuration
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#D3D3D3")
    style.configure("Treeview", rowheight=25, font=("Arial", 11))

    # Treeview container
    tree_frame = tk.Frame(event_win)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree_scroll = tk.Scrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Location", "Date", "Amount Required", "Status"),
                        show="headings", yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=tree.yview)

    # Define columns
    headings = ["ID", "Name", "Location", "Date", "Amount Required", "Status"]
    for col in headings:
        tree.heading(col, text=col)

    tree.column("ID", width=60, anchor='center')
    tree.column("Name", width=150)
    tree.column("Location", width=130)
    tree.column("Date", width=100, anchor='center')
    tree.column("Amount Required", width=130, anchor='e')
    tree.column("Status", width=100, anchor='center')

    # Tag styles for status
    tree.tag_configure('successful', background="#e6ffe6")  # Light green
    tree.tag_configure('pending', background="#ffe6e6")      # Light red

    # Insert rows
    for row in all_events:
        tag = 'successful' if row[5].lower() == 'successful' else 'pending'
        tree.insert("", tk.END, values=row, tags=(tag,))

    tree.pack(fill="both", expand=True)

    cursor.close()
    conn.close()

def show_tasks_by_event():
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch all event IDs and names
    cursor.execute("SELECT ID, Name FROM events")
    events = cursor.fetchall()

    task_win = tk.Toplevel()
    task_win.title("View Tasks by Event")
    task_win.geometry("800x500")

    # Header section with green background
    header_frame = tk.Frame(task_win, bg="#4CAF50")
    header_frame.pack(fill="x")

    header_label = tk.Label(header_frame, text="Select Event to View Tasks", font=("Arial", 16, "bold"), bg="#4CAF50", fg="white")
    header_label.pack(pady=10)

    # Dropdown to select event
    selection_frame = tk.Frame(task_win)
    selection_frame.pack(pady=10)

    tk.Label(selection_frame, text="Select Event:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

    event_var = tk.StringVar()
    event_dropdown = ttk.Combobox(selection_frame, textvariable=event_var, state="readonly", width=40)
    event_dropdown['values'] = [f"{eid} - {ename}" for eid, ename in events]
    event_dropdown.pack(side=tk.LEFT, padx=5)

    # Treeview table setup
    tree_frame = tk.Frame(task_win)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree_scroll = tk.Scrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(tree_frame, columns=("ID", "Task Name", "Coord ID", "Status", "Deadline"), show='headings', yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=tree.yview)

    # Define headings
    tree.heading("ID", text="Task ID")
    tree.heading("Task Name", text="Task Name")
    tree.heading("Coord ID", text="Coordinator ID")
    tree.heading("Status", text="Status")
    tree.heading("Deadline", text="Deadline")

    # Column widths and alignment
    tree.column("ID", width=70, anchor="center")
    tree.column("Task Name", width=200)
    tree.column("Coord ID", width=100, anchor="center")
    tree.column("Status", width=100, anchor="center")
    tree.column("Deadline", width=120, anchor="center")

    # Treeview style
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    style.configure("Treeview", rowheight=25, font=("Arial", 11))

    tree.pack(fill="both", expand=True)

    # Load tasks when event is selected
    def load_tasks(event):
        tree.delete(*tree.get_children())  # Clear table
        selected = event_var.get()
        if not selected:
            return
        event_id = int(selected.split(' - ')[0])

        cursor.execute("""
            SELECT ID, Name, coordID, Status, Deadline
            FROM tasks
            WHERE EventsID = %s
        """, (event_id,))
        tasks = cursor.fetchall()

        for task in tasks:
            status_text = "Completed" if task[3] else "Pending"
            tree.insert("", tk.END, values=(task[0], task[1], task[2], status_text, task[4]))

    # Bind selection
    event_dropdown.bind("<<ComboboxSelected>>", load_tasks)

    # Close connection on window destroy
    def on_close():
        cursor.close()
        conn.close()
        task_win.destroy()

    task_win.protocol("WM_DELETE_WINDOW", on_close)

def show_unassigned_volunteers():
    conn = get_connection()
    cursor = conn.cursor()

    # Query to get volunteers not in volunteer_tasks
    cursor.execute("""
        SELECT Username, Email, contact_no, Category, address 
        FROM volunteers 
        WHERE Username NOT IN (
            SELECT DISTINCT VolunteerUsername FROM volunteer_tasks
        )
    """)
    unassigned_volunteers = cursor.fetchall()

    # Setup window
    unassigned_win = tk.Toplevel()
    unassigned_win.title("Unassigned Volunteers")
    unassigned_win.geometry("900x500")

    # Green header
    header_frame = tk.Frame(unassigned_win, bg="#4CAF50")
    header_frame.pack(fill="x")

    header_label = tk.Label(
        header_frame,
        text="Volunteers Not Assigned to Any Task",
        font=("Arial", 16, "bold"),
        bg="#4CAF50",
        fg="white"
    )
    header_label.pack(pady=10)

    # Table setup
    tree_frame = tk.Frame(unassigned_win)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree_scroll = tk.Scrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(tree_frame, columns=("Username", "Email", "Contact", "Category", "Address"), show='headings', yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=tree.yview)

    # Define headings
    tree.heading("Username", text="Username")
    tree.heading("Email", text="Email")
    tree.heading("Contact", text="Contact Number")
    tree.heading("Category", text="Category")
    tree.heading("Address", text="Address")

    # Style
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    style.configure("Treeview", font=("Arial", 11), rowheight=25)

    # Column sizing
    tree.column("Username", width=150)
    tree.column("Email", width=200)
    tree.column("Contact", width=120, anchor="center")
    tree.column("Category", width=100, anchor="center")
    tree.column("Address", width=200)

    # Insert data
    for row in unassigned_volunteers:
        tree.insert("", tk.END, values=row)

    tree.pack(fill="both", expand=True)

    # Cleanup
    def on_close():
        cursor.close()
        conn.close()
        unassigned_win.destroy()

    unassigned_win.protocol("WM_DELETE_WINDOW", on_close)

def edit_top_sponsors_vip_inline():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT s.ID, s.Name, SUM(s.Amount) AS amt_contributed, s.VIP
            FROM sponsors s
            GROUP BY s.ID, s.Name, s.VIP
            ORDER BY amt_contributed DESC
            LIMIT 3;
        """
        cursor.execute(query)
        sponsors = cursor.fetchall()

        if not sponsors:
            messagebox.showinfo("Info", "No sponsors found.")
            return

        win = tk.Toplevel()
        win.title("Top 3 Sponsors - Inline VIP Edit")
        win.geometry("800x350")

        header = tk.Frame(win, bg="#4CAF50", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Top 3 Sponsors - Edit VIP Status Inline",
                 font=("Arial", 18, "bold"), bg="#4CAF50", fg="white").pack(pady=15)

        tree_frame = tk.Frame(win)
        tree_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Styling
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=30,
                        fieldbackground="white",
                        bordercolor="gray",
                        borderwidth=1)

        style.configure("Treeview.Heading",
                        font=("Arial", 12, "bold"),
                        background="#E0F2F1",
                        foreground="black")

        style.map("Treeview", background=[("selected", "#AED581")])

        # Alternate row colors
        style.map("Treeview",
                  background=[('selected', '#AED581')])
        tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Total Contribution", "VIP Status"), show="headings")

        tree.tag_configure('oddrow', background="#F5F5F5")
        tree.tag_configure('evenrow', background="white")

        for col in ("ID", "Name", "Total Contribution", "VIP Status"):
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", width=180)

        tree.pack(fill="both", expand=True)

        sponsor_dict = {}
        for idx, row in enumerate(sponsors):
            sponsor_dict[str(row[0])] = row
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            tree.insert("", "end", iid=str(row[0]), values=row, tags=(tag,))

        # Dropdown setup
        vip_options = ["Yes", "No", "Premium"]
        dropdown = ttk.Combobox(tree_frame, values=vip_options, state="readonly")
        dropdown.place_forget()

        def on_tree_click(event):
            selected_item = tree.identify_row(event.y)
            selected_col = tree.identify_column(event.x)

            if selected_item and selected_col == "#4":  # VIP Status column
                bbox = tree.bbox(selected_item, '#4')
                if not bbox:
                    return

                x, y, width, height = bbox
                dropdown.place(x=x, y=y + 5, width=width)
                current_vip = tree.set(selected_item, "VIP Status")
                dropdown.set(current_vip)

                def save_selection(event=None):
                    new_vip = dropdown.get()
                    sponsor_id = selected_item
                    tree.set(sponsor_id, "VIP Status", new_vip)
                    cursor.execute("UPDATE sponsors SET VIP = %s WHERE ID = %s", (new_vip, sponsor_id))
                    conn.commit()
                    dropdown.place_forget()

                dropdown.bind("<<ComboboxSelected>>", save_selection)
                dropdown.focus_set()

        tree.bind("<Button-1>", on_tree_click)

        win.protocol("WM_DELETE_WINDOW", lambda: [cursor.close(), conn.close(), win.destroy()])

    except Exception as e:
        messagebox.showerror("Error", f"Could not load sponsors.\n{str(e)}")