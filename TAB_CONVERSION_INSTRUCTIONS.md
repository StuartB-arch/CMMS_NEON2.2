# Tkinter to PyQt5 Tab Conversion Instructions

## Table of Contents
1. [Equipment Management Tab](#equipment-management-tab)
2. [PM Scheduling Tab](#pm-scheduling-tab)
3. [PM Completion Tab](#pm-completion-tab)
4. [Corrective Maintenance Tab](#corrective-maintenance-tab)
5. [General Conversion Patterns](#general-conversion-patterns)
6. [Widget Mapping Reference](#widget-mapping-reference)
7. [Layout Manager Conversion](#layout-manager-conversion)
8. [Dialog Conversion Patterns](#dialog-conversion-patterns)

---

## Equipment Management Tab

### Original Tkinter Code Pattern
```python
def create_equipment_tab(self):
    """Equipment management and data import tab"""
    self.equipment_frame = ttk.Frame(self.notebook)
    self.notebook.add(self.equipment_frame, text="Equipment Management")

    # Controls frame
    controls_frame = ttk.LabelFrame(self.equipment_frame, text="Equipment Controls", padding=10)
    controls_frame.pack(fill='x', padx=10, pady=5)

    # Buttons
    ttk.Button(controls_frame, text="Import Equipment CSV",
              command=self.import_equipment_csv).pack(side='left', padx=5)
    ttk.Button(controls_frame, text="Add Equipment",
              command=self.add_equipment_dialog).pack(side='left', padx=5)

    # Search frame
    search_frame = ttk.Frame(self.equipment_frame)
    search_frame.pack(fill='x', padx=10, pady=5)

    ttk.Label(search_frame, text="Search Equipment:").pack(side='left', padx=5)
    self.equipment_search_var = tk.StringVar()
    self.equipment_search_entry = ttk.Entry(search_frame, textvariable=self.equipment_search_var, width=30)
    self.equipment_search_entry.pack(side='left', padx=5)
    self.equipment_search_entry.bind('<KeyRelease>', self.filter_equipment_list)

    # Location filter
    self.equipment_location_var = tk.StringVar(value="All Locations")
    self.equipment_location_combo = ttk.Combobox(search_frame, textvariable=self.equipment_location_var,
                                                 width=25, state='readonly')
    self.equipment_location_combo.pack(side='left', padx=5)
    self.equipment_location_combo.bind('<<ComboboxSelected>>', self.filter_equipment_list)

    # Treeview with scrollbars
    list_frame = ttk.Frame(self.equipment_frame)
    list_frame.pack(fill='both', expand=True, padx=10, pady=5)

    self.equipment_tree = ttk.Treeview(list_frame,
                                     columns=('SAP', 'BFM', 'Description', 'Location', 'LIN',
                                             'Monthly', 'Six Month', 'Annual', 'Status'),
                                     show='headings')
    self.equipment_tree.configure(selectmode='extended')

    columns_config = {
        'SAP': ('SAP Material No.', 120),
        'BFM': ('BFM Equipment No.', 130),
        'Description': ('Description', 300),
        'Location': ('Location', 100),
        'LIN': ('Master LIN', 80),
        'Monthly': ('Monthly PM', 80),
        'Six Month': ('6-Month PM', 80),
        'Annual': ('Annual PM', 80),
        'Status': ('Status', 80)
    }

    for col, (heading, width) in columns_config.items():
        self.equipment_tree.heading(col, text=heading)
        self.equipment_tree.column(col, width=width)

    v_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.equipment_tree.yview)
    h_scrollbar = ttk.Scrollbar(list_frame, orient='horizontal', command=self.equipment_tree.xview)
    self.equipment_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    self.equipment_tree.grid(row=0, column=0, sticky='nsew')
    v_scrollbar.grid(row=0, column=1, sticky='ns')
    h_scrollbar.grid(row=1, column=0, sticky='ew')

    list_frame.grid_rowconfigure(0, weight=1)
    list_frame.grid_columnconfigure(0, weight=1)
```

### PyQt5 Conversion
```python
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                            QPushButton, QLabel, QLineEdit, QComboBox,
                            QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt

def create_equipment_tab(self):
    """Equipment management and data import tab - PyQt5 version"""
    # Create main widget for the tab
    self.equipment_widget = QWidget()

    # Main vertical layout
    main_layout = QVBoxLayout(self.equipment_widget)
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(5)

    # Controls frame (GroupBox replaces LabelFrame)
    controls_group = QGroupBox("Equipment Controls")
    controls_layout = QHBoxLayout()
    controls_layout.setSpacing(5)

    # Buttons (QPushButton replaces ttk.Button)
    import_btn = QPushButton("Import Equipment CSV")
    import_btn.clicked.connect(self.import_equipment_csv)  # .connect() replaces command=
    controls_layout.addWidget(import_btn)

    add_btn = QPushButton("Add Equipment")
    add_btn.clicked.connect(self.add_equipment_dialog)
    controls_layout.addWidget(add_btn)

    edit_btn = QPushButton("Edit Equipment")
    edit_btn.clicked.connect(self.edit_equipment_dialog)
    controls_layout.addWidget(edit_btn)

    refresh_btn = QPushButton("Refresh List")
    refresh_btn.clicked.connect(self.refresh_equipment_list)
    controls_layout.addWidget(refresh_btn)

    export_btn = QPushButton("Export Equipment")
    export_btn.clicked.connect(self.export_equipment_list)
    controls_layout.addWidget(export_btn)

    bulk_edit_btn = QPushButton("Bulk Edit PM Cycles")
    bulk_edit_btn.clicked.connect(self.bulk_edit_pm_cycles)
    controls_layout.addWidget(bulk_edit_btn)

    controls_layout.addStretch()  # Push buttons to left
    controls_group.setLayout(controls_layout)
    main_layout.addWidget(controls_group)

    # Statistics frame
    stats_group = QGroupBox("Equipment Statistics")
    stats_layout = QHBoxLayout()

    # Statistics labels
    self.stats_total_label = QLabel("Total Assets: 0")
    self.stats_total_label.setStyleSheet("font-weight: bold; font-size: 10pt;")
    stats_layout.addWidget(self.stats_total_label)

    self.stats_cf_label = QLabel("Cannot Find: 0")
    self.stats_cf_label.setStyleSheet("font-weight: bold; font-size: 10pt; color: red;")
    stats_layout.addWidget(self.stats_cf_label)

    self.stats_rtf_label = QLabel("Run to Failure: 0")
    self.stats_rtf_label.setStyleSheet("font-weight: bold; font-size: 10pt; color: orange;")
    stats_layout.addWidget(self.stats_rtf_label)

    self.stats_active_label = QLabel("Active Assets: 0")
    self.stats_active_label.setStyleSheet("font-weight: bold; font-size: 10pt; color: green;")
    stats_layout.addWidget(self.stats_active_label)

    stats_layout.addStretch()

    refresh_stats_btn = QPushButton("Refresh Stats")
    refresh_stats_btn.clicked.connect(self.update_equipment_statistics)
    stats_layout.addWidget(refresh_stats_btn)

    stats_group.setLayout(stats_layout)
    main_layout.addWidget(stats_group)

    # Search frame
    search_widget = QWidget()
    search_layout = QHBoxLayout(search_widget)
    search_layout.setContentsMargins(0, 0, 0, 0)

    search_layout.addWidget(QLabel("Search Equipment:"))

    # QLineEdit replaces ttk.Entry (no need for StringVar)
    self.equipment_search_entry = QLineEdit()
    self.equipment_search_entry.setFixedWidth(300)
    # textChanged signal replaces '<KeyRelease>' binding
    self.equipment_search_entry.textChanged.connect(self.filter_equipment_list)
    search_layout.addWidget(self.equipment_search_entry)

    search_layout.addWidget(QLabel("Filter by Location:"))

    # QComboBox replaces ttk.Combobox
    self.equipment_location_combo = QComboBox()
    self.equipment_location_combo.setFixedWidth(250)
    self.equipment_location_combo.addItem("All Locations")
    # currentIndexChanged signal replaces '<<ComboboxSelected>>' binding
    self.equipment_location_combo.currentIndexChanged.connect(self.filter_equipment_list)
    search_layout.addWidget(self.equipment_location_combo)

    clear_btn = QPushButton("Clear Filters")
    clear_btn.clicked.connect(self.clear_equipment_filters)
    search_layout.addWidget(clear_btn)

    search_layout.addStretch()
    main_layout.addWidget(search_widget)

    # Equipment list - QTableWidget replaces ttk.Treeview
    self.equipment_table = QTableWidget()
    self.equipment_table.setColumnCount(9)
    self.equipment_table.setHorizontalHeaderLabels([
        'SAP Material No.', 'BFM Equipment No.', 'Description',
        'Location', 'Master LIN', 'Monthly PM', '6-Month PM',
        'Annual PM', 'Status'
    ])

    # Set column widths
    header = self.equipment_table.horizontalHeader()
    header.resizeSection(0, 120)  # SAP
    header.resizeSection(1, 130)  # BFM
    header.resizeSection(2, 300)  # Description
    header.resizeSection(3, 100)  # Location
    header.resizeSection(4, 80)   # LIN
    header.resizeSection(5, 80)   # Monthly
    header.resizeSection(6, 80)   # Six Month
    header.resizeSection(7, 80)   # Annual
    header.resizeSection(8, 80)   # Status

    # Enable sorting
    self.equipment_table.setSortingEnabled(True)

    # Enable multi-selection (replaces selectmode='extended')
    self.equipment_table.setSelectionBehavior(QTableWidget.SelectRows)
    self.equipment_table.setSelectionMode(QTableWidget.ExtendedSelection)

    # Scrollbars are automatic in QTableWidget
    main_layout.addWidget(self.equipment_table, stretch=1)  # stretch=1 makes it expand

    # Add tab to notebook
    self.tab_widget.addTab(self.equipment_widget, "Equipment Management")

    # Initialize data
    self.refresh_equipment_list()
```

### Key Helper Methods Conversion

#### Populating Table Data
```python
# Tkinter version
def refresh_equipment_list(self):
    self.equipment_tree.delete(*self.equipment_tree.get_children())
    cursor = self.conn.cursor()
    cursor.execute('SELECT * FROM equipment ORDER BY bfm_equipment_no')
    for row in cursor.fetchall():
        self.equipment_tree.insert('', 'end', values=row)

# PyQt5 version
def refresh_equipment_list(self):
    self.equipment_table.setRowCount(0)  # Clear all rows
    cursor = self.conn.cursor()
    cursor.execute('SELECT * FROM equipment ORDER BY bfm_equipment_no')

    rows = cursor.fetchall()
    self.equipment_table.setRowCount(len(rows))

    for row_idx, row_data in enumerate(rows):
        for col_idx, cell_data in enumerate(row_data):
            item = QTableWidgetItem(str(cell_data))
            self.equipment_table.setItem(row_idx, col_idx, item)
```

#### Getting Selected Items
```python
# Tkinter version
selected = self.equipment_tree.selection()
if selected:
    item = self.equipment_tree.item(selected[0])
    bfm_no = item['values'][1]

# PyQt5 version
selected_rows = self.equipment_table.selectedItems()
if selected_rows:
    row = selected_rows[0].row()
    bfm_no = self.equipment_table.item(row, 1).text()
```

---

## PM Scheduling Tab

### Original Tkinter Code Pattern
```python
def create_pm_scheduling_tab(self):
    """PM Scheduling and assignment tab"""
    self.pm_schedule_frame = ttk.Frame(self.notebook)
    self.notebook.add(self.pm_schedule_frame, text="PM Scheduling")

    # Controls
    controls_frame = ttk.LabelFrame(self.pm_schedule_frame, text="PM Scheduling Controls", padding=10)
    controls_frame.pack(fill='x', padx=10, pady=5)

    # Week selection with dropdown
    ttk.Label(controls_frame, text="Week Starting:").grid(row=0, column=0, sticky='w', padx=5)
    self.week_start_var = tk.StringVar(value=self.current_week_start.strftime('%Y-%m-%d'))

    self.week_combo = ttk.Combobox(controls_frame, textvariable=self.week_start_var, width=12)
    self.week_combo.grid(row=0, column=1, padx=5)
    self.week_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_technician_schedules())

    # Technician exclusion listbox
    exclusion_frame = ttk.LabelFrame(self.pm_schedule_frame, text="Exclude Technicians", padding=10)
    exclusion_frame.pack(fill='x', padx=10, pady=5)

    self.excluded_technicians_listbox = tk.Listbox(exclusion_frame, selectmode='multiple',
                                                   height=6, exportselection=False)
    self.excluded_technicians_listbox.pack(side='left', fill='both', expand=True)

    # Nested notebook for technicians
    self.technician_notebook = ttk.Notebook(schedule_frame)
    self.technician_notebook.pack(fill='both', expand=True)

    self.technician_trees = {}
    for tech in self.technicians:
        tech_frame = ttk.Frame(self.technician_notebook)
        self.technician_notebook.add(tech_frame, text=tech)

        tech_tree = ttk.Treeview(tech_frame,
                               columns=('BFM', 'Description', 'PM Type', 'Due Date', 'Status'),
                               show='headings')
        tech_tree.pack(fill='both', expand=True)
        self.technician_trees[tech] = tech_tree
```

### PyQt5 Conversion
```python
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QGroupBox, QPushButton, QLabel, QComboBox,
                            QListWidget, QTabWidget, QTableWidget, QAbstractItemView)

def create_pm_scheduling_tab(self):
    """PM Scheduling and assignment tab - PyQt5 version"""
    self.pm_schedule_widget = QWidget()
    main_layout = QVBoxLayout(self.pm_schedule_widget)
    main_layout.setContentsMargins(10, 10, 10, 10)

    # Controls frame with grid layout
    controls_group = QGroupBox("PM Scheduling Controls")
    controls_grid = QGridLayout()

    # Week selection
    controls_grid.addWidget(QLabel("Week Starting:"), 0, 0, Qt.AlignLeft)

    self.week_combo = QComboBox()
    self.week_combo.setFixedWidth(120)
    self.week_combo.addItem(self.current_week_start.strftime('%Y-%m-%d'))
    # Signal connection for combo box selection
    self.week_combo.currentIndexChanged.connect(self.refresh_technician_schedules)
    controls_grid.addWidget(self.week_combo, 0, 1)

    # Buttons
    generate_btn = QPushButton("Generate Weekly Schedule")
    generate_btn.clicked.connect(self.generate_weekly_assignments)
    controls_grid.addWidget(generate_btn, 0, 2)

    print_btn = QPushButton("Print PM Forms")
    print_btn.clicked.connect(self.print_weekly_pm_forms)
    controls_grid.addWidget(print_btn, 0, 3)

    export_btn = QPushButton("Export Schedule")
    export_btn.clicked.connect(self.export_weekly_schedule)
    controls_grid.addWidget(export_btn, 0, 4)

    controls_group.setLayout(controls_grid)
    main_layout.addWidget(controls_group)

    # Technician exclusion frame
    exclusion_group = QGroupBox("Exclude Technicians from This Week's Schedule")
    exclusion_layout = QVBoxLayout()

    exclusion_layout.addWidget(QLabel("Select technicians to exclude (e.g., vacation, out sick):"))

    # QListWidget replaces tk.Listbox
    self.excluded_technicians_listbox = QListWidget()
    self.excluded_technicians_listbox.setSelectionMode(QAbstractItemView.MultiSelection)
    self.excluded_technicians_listbox.setMaximumHeight(150)
    exclusion_layout.addWidget(self.excluded_technicians_listbox)

    # Clear exclusions button
    clear_exclusions_btn = QPushButton("Clear All Exclusions")
    clear_exclusions_btn.clicked.connect(self.clear_all_exclusions)
    exclusion_layout.addWidget(clear_exclusions_btn)

    exclusion_group.setLayout(exclusion_layout)
    main_layout.addWidget(exclusion_group)

    # Schedule display with nested tabs
    schedule_group = QGroupBox("Weekly PM Schedule")
    schedule_layout = QVBoxLayout()

    # QTabWidget replaces ttk.Notebook
    self.technician_tab_widget = QTabWidget()

    # Create tabs for each technician
    self.technician_tables = {}
    for tech in self.technicians:
        tech_table = QTableWidget()
        tech_table.setColumnCount(5)
        tech_table.setHorizontalHeaderLabels([
            'BFM Equipment No.', 'Description', 'PM Type', 'Due Date', 'Status'
        ])

        # Set column widths
        header = tech_table.horizontalHeader()
        for i in range(5):
            header.resizeSection(i, 150)

        tech_table.setSortingEnabled(True)
        tech_table.setSelectionBehavior(QTableWidget.SelectRows)

        # Add tab for this technician
        self.technician_tab_widget.addTab(tech_table, tech)
        self.technician_tables[tech] = tech_table

    schedule_layout.addWidget(self.technician_tab_widget)
    schedule_group.setLayout(schedule_layout)
    main_layout.addWidget(schedule_group, stretch=1)

    # Add to main tab widget
    self.tab_widget.addTab(self.pm_schedule_widget, "PM Scheduling")

    # Load data
    self.populate_week_selector()
    self.load_latest_weekly_schedule()
```

### Listbox Operations Conversion
```python
# Tkinter - Adding items to Listbox
for tech in technicians:
    self.excluded_technicians_listbox.insert('end', tech)

# PyQt5 - Adding items to QListWidget
for tech in technicians:
    self.excluded_technicians_listbox.addItem(tech)

# Tkinter - Getting selected items
selected_indices = self.excluded_technicians_listbox.curselection()
selected_items = [self.excluded_technicians_listbox.get(i) for i in selected_indices]

# PyQt5 - Getting selected items
selected_items = [item.text() for item in self.excluded_technicians_listbox.selectedItems()]

# Tkinter - Clearing listbox
self.excluded_technicians_listbox.delete(0, 'end')

# PyQt5 - Clearing listbox
self.excluded_technicians_listbox.clear()
```

---

## PM Completion Tab

### Original Tkinter Code Pattern
```python
def create_pm_completion_tab(self):
    """PM Completion entry tab"""
    self.pm_completion_frame = ttk.Frame(self.notebook)
    self.notebook.add(self.pm_completion_frame, text="PM Completion")

    # Completion form
    form_frame = ttk.LabelFrame(self.pm_completion_frame, text="PM Completion Entry", padding=15)
    form_frame.pack(fill='x', padx=10, pady=5)

    row = 0

    # Equipment selection
    ttk.Label(form_frame, text="BFM Equipment Number:").grid(row=row, column=0, sticky='w', pady=5)
    self.completion_bfm_var = tk.StringVar()
    bfm_combo = ttk.Combobox(form_frame, textvariable=self.completion_bfm_var, width=20)
    bfm_combo.grid(row=row, column=1, sticky='w', padx=5, pady=5)
    bfm_combo.bind('<KeyRelease>', self.update_equipment_suggestions)
    row += 1

    # PM Type
    ttk.Label(form_frame, text="PM Type:").grid(row=row, column=0, sticky='w', pady=5)
    self.pm_type_var = tk.StringVar()
    pm_type_combo = ttk.Combobox(form_frame, textvariable=self.pm_type_var,
                               values=['Monthly', 'Six Month', 'Annual'], width=20)
    pm_type_combo.bind('<<ComboboxSelected>>', lambda e: self.update_pm_completion_form())
    pm_type_combo.grid(row=row, column=1, sticky='w', padx=5, pady=5)
    row += 1

    # Labor time with multiple entries
    ttk.Label(form_frame, text="Labor Time:").grid(row=row, column=0, sticky='w', pady=5)
    time_frame = ttk.Frame(form_frame)
    time_frame.grid(row=row, column=1, sticky='w', padx=5, pady=5)

    self.labor_hours_var = tk.StringVar(value="0")
    ttk.Entry(time_frame, textvariable=self.labor_hours_var, width=5).pack(side='left')
    ttk.Label(time_frame, text="hours").pack(side='left', padx=5)

    self.labor_minutes_var = tk.StringVar(value="0")
    ttk.Entry(time_frame, textvariable=self.labor_minutes_var, width=5).pack(side='left')
    ttk.Label(time_frame, text="minutes").pack(side='left', padx=5)
    row += 1

    # Notes with Text widget
    ttk.Label(form_frame, text="Notes from Technician:").grid(row=row, column=0, sticky='nw', pady=5)
    self.notes_text = tk.Text(form_frame, width=50, height=4)
    self.notes_text.grid(row=row, column=1, sticky='w', padx=5, pady=5)
    row += 1

    # Recent completions treeview with double-click binding
    self.recent_completions_tree = ttk.Treeview(recent_frame,
                                              columns=('Date', 'BFM', 'PM Type', 'Technician', 'Hours'),
                                              show='headings')
    self.recent_completions_tree.pack(fill='both', expand=True)
    self.recent_completions_tree.bind('<Double-1>', self.on_completion_double_click)
```

### PyQt5 Conversion
```python
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QGroupBox, QPushButton, QLabel, QLineEdit,
                            QComboBox, QTextEdit, QTableWidget, QSpinBox)

def create_pm_completion_tab(self):
    """PM Completion entry tab - PyQt5 version"""
    self.pm_completion_widget = QWidget()
    main_layout = QVBoxLayout(self.pm_completion_widget)
    main_layout.setContentsMargins(10, 10, 10, 10)

    # Completion form with grid layout
    form_group = QGroupBox("PM Completion Entry")
    form_grid = QGridLayout()
    form_grid.setVerticalSpacing(5)
    form_grid.setHorizontalSpacing(10)

    row = 0

    # Equipment selection
    form_grid.addWidget(QLabel("BFM Equipment Number:"), row, 0, Qt.AlignLeft)

    self.completion_bfm_combo = QComboBox()
    self.completion_bfm_combo.setEditable(True)  # Makes it searchable/editable
    self.completion_bfm_combo.setFixedWidth(200)
    # textChanged signal for the editable combo box
    self.completion_bfm_combo.lineEdit().textChanged.connect(self.update_equipment_suggestions)
    form_grid.addWidget(self.completion_bfm_combo, row, 1, Qt.AlignLeft)
    row += 1

    # PM Type
    form_grid.addWidget(QLabel("PM Type:"), row, 0, Qt.AlignLeft)

    self.pm_type_combo = QComboBox()
    self.pm_type_combo.addItems(['Monthly', 'Six Month', 'Annual', 'CANNOT FIND', 'Run to Failure'])
    self.pm_type_combo.setFixedWidth(200)
    self.pm_type_combo.currentIndexChanged.connect(self.update_pm_completion_form_with_template)
    form_grid.addWidget(self.pm_type_combo, row, 1, Qt.AlignLeft)
    row += 1

    # Technician
    form_grid.addWidget(QLabel("Maintenance Technician:"), row, 0, Qt.AlignLeft)

    self.completion_tech_combo = QComboBox()
    self.completion_tech_combo.addItems(self.technicians)
    self.completion_tech_combo.setFixedWidth(200)
    form_grid.addWidget(self.completion_tech_combo, row, 1, Qt.AlignLeft)
    row += 1

    # Labor time - horizontal layout with spinboxes
    form_grid.addWidget(QLabel("Labor Time:"), row, 0, Qt.AlignLeft)

    time_widget = QWidget()
    time_layout = QHBoxLayout(time_widget)
    time_layout.setContentsMargins(0, 0, 0, 0)

    # QSpinBox is better than QLineEdit for numeric input
    self.labor_hours_spinbox = QSpinBox()
    self.labor_hours_spinbox.setRange(0, 24)
    self.labor_hours_spinbox.setValue(0)
    self.labor_hours_spinbox.setFixedWidth(50)
    time_layout.addWidget(self.labor_hours_spinbox)
    time_layout.addWidget(QLabel("hours"))

    self.labor_minutes_spinbox = QSpinBox()
    self.labor_minutes_spinbox.setRange(0, 59)
    self.labor_minutes_spinbox.setValue(0)
    self.labor_minutes_spinbox.setFixedWidth(50)
    time_layout.addWidget(self.labor_minutes_spinbox)
    time_layout.addWidget(QLabel("minutes"))
    time_layout.addStretch()

    form_grid.addWidget(time_widget, row, 1, Qt.AlignLeft)
    row += 1

    # PM Due Date
    form_grid.addWidget(QLabel("PM Due Date:"), row, 0, Qt.AlignLeft)

    self.pm_due_date_entry = QLineEdit()
    self.pm_due_date_entry.setFixedWidth(200)
    self.pm_due_date_entry.setPlaceholderText("YYYY-MM-DD")
    form_grid.addWidget(self.pm_due_date_entry, row, 1, Qt.AlignLeft)
    row += 1

    # Special Equipment
    form_grid.addWidget(QLabel("Special Equipment Used:"), row, 0, Qt.AlignLeft)

    self.special_equipment_entry = QLineEdit()
    self.special_equipment_entry.setFixedWidth(400)
    form_grid.addWidget(self.special_equipment_entry, row, 1, Qt.AlignLeft)
    row += 1

    # Notes - QTextEdit replaces tk.Text
    form_grid.addWidget(QLabel("Notes from Technician:"), row, 0, Qt.AlignTop | Qt.AlignLeft)

    self.notes_text_edit = QTextEdit()
    self.notes_text_edit.setFixedHeight(80)
    self.notes_text_edit.setFixedWidth(500)
    form_grid.addWidget(self.notes_text_edit, row, 1, Qt.AlignLeft)
    row += 1

    # Next Annual PM Date
    form_grid.addWidget(QLabel("Next Annual PM Date:"), row, 0, Qt.AlignLeft)

    self.next_annual_pm_entry = QLineEdit()
    self.next_annual_pm_entry.setFixedWidth(200)
    self.next_annual_pm_entry.setPlaceholderText("YYYY-MM-DD")
    form_grid.addWidget(self.next_annual_pm_entry, row, 1, Qt.AlignLeft)
    row += 1

    # Buttons
    button_widget = QWidget()
    button_layout = QHBoxLayout(button_widget)
    button_layout.setContentsMargins(0, 10, 0, 0)

    summary_btn = QPushButton("Monthly Summary Report")
    summary_btn.clicked.connect(self.show_monthly_summary)
    button_layout.addWidget(summary_btn)

    history_btn = QPushButton("Show Equipment PM History")
    history_btn.clicked.connect(self.show_equipment_pm_history_dialog)
    button_layout.addWidget(history_btn)

    submit_btn = QPushButton("Submit PM Completion")
    submit_btn.clicked.connect(self.submit_pm_completion)
    button_layout.addWidget(submit_btn)

    refresh_btn = QPushButton("Refresh List")
    refresh_btn.clicked.connect(self.load_recent_completions)
    button_layout.addWidget(refresh_btn)

    schedule_btn = QPushButton("Check Equipment Schedule")
    schedule_btn.clicked.connect(self.create_pm_schedule_lookup_dialog)
    button_layout.addWidget(schedule_btn)

    cm_btn = QPushButton("Create CM from PM")
    cm_btn.clicked.connect(self.create_cm_from_pm_dialog)
    button_layout.addWidget(cm_btn)

    button_layout.addStretch()

    form_grid.addWidget(button_widget, row, 0, 1, 2)

    form_group.setLayout(form_grid)
    main_layout.addWidget(form_group)

    # Recent completions table
    recent_group = QGroupBox("Recent PM Completions")
    recent_layout = QVBoxLayout()

    self.recent_completions_table = QTableWidget()
    self.recent_completions_table.setColumnCount(5)
    self.recent_completions_table.setHorizontalHeaderLabels([
        'Date', 'BFM', 'PM Type', 'Technician', 'Hours'
    ])

    header = self.recent_completions_table.horizontalHeader()
    for i in range(5):
        header.resizeSection(i, 120)

    self.recent_completions_table.setSortingEnabled(True)
    self.recent_completions_table.setSelectionBehavior(QTableWidget.SelectRows)

    # Double-click event handling
    self.recent_completions_table.cellDoubleClicked.connect(self.on_completion_double_click)
    # Selection changed event
    self.recent_completions_table.itemSelectionChanged.connect(self.on_completion_select)

    recent_layout.addWidget(self.recent_completions_table)
    recent_group.setLayout(recent_layout)
    main_layout.addWidget(recent_group, stretch=1)

    # Add to main tab widget
    self.tab_widget.addTab(self.pm_completion_widget, "PM Completion")

    # Load data
    self.load_recent_completions()
```

### Text Widget Conversion
```python
# Tkinter - Get text from Text widget
notes = self.notes_text.get('1.0', 'end-1c')

# PyQt5 - Get text from QTextEdit
notes = self.notes_text_edit.toPlainText()

# Tkinter - Set text in Text widget
self.notes_text.delete('1.0', 'end')
self.notes_text.insert('1.0', "New text here")

# PyQt5 - Set text in QTextEdit
self.notes_text_edit.setPlainText("New text here")

# Tkinter - Clear text
self.notes_text.delete('1.0', 'end')

# PyQt5 - Clear text
self.notes_text_edit.clear()
```

---

## Corrective Maintenance Tab

### Original Tkinter Code Pattern
```python
def create_cm_management_tab(self):
    """Corrective Maintenance management tab"""
    self.cm_frame = ttk.Frame(self.notebook)
    self.notebook.add(self.cm_frame, text="Corrective Maintenance")

    # CM controls
    controls_frame = ttk.LabelFrame(self.cm_frame, text="CM Controls", padding=10)
    controls_frame.pack(fill='x', padx=10, pady=5)

    # Filter controls
    filter_frame = ttk.Frame(controls_frame)
    filter_frame.pack(fill='x')

    ttk.Label(filter_frame, text="Filter by Status:").pack(side='left', padx=(0, 5))

    self.cm_filter_var = tk.StringVar(value="All")
    self.cm_filter_dropdown = ttk.Combobox(filter_frame, textvariable=self.cm_filter_var,
                                        values=["All", "Open", "Closed"],
                                        state="readonly", width=15)
    self.cm_filter_dropdown.pack(side='left', padx=5)
    self.cm_filter_dropdown.bind('<<ComboboxSelected>>', self.filter_cm_list)

    # CM list treeview
    cm_list_frame = ttk.LabelFrame(self.cm_frame, text="Corrective Maintenance List", padding=10)
    cm_list_frame.pack(fill='both', expand=False, padx=10, pady=5)

    self.cm_tree = ttk.Treeview(cm_list_frame,
                            columns=('CM Number', 'BFM', 'Description', 'Priority',
                                   'Assigned', 'Status', 'Created', 'Source'),
                            show='headings', height=8)

    # Grid layout with scrollbars
    self.cm_tree.grid(row=0, column=0, sticky='nsew')
    cm_v_scrollbar.grid(row=0, column=1, sticky='ns')
    cm_h_scrollbar.grid(row=1, column=0, sticky='ew')

    # Separator
    separator = ttk.Separator(self.cm_frame, orient='horizontal')
    separator.pack(fill='x', padx=10, pady=10)

    # Equipment Missing Parts list - SEPARATE
    emp_list_frame = ttk.LabelFrame(self.cm_frame, text="⚠️ EQUIPMENT WITH MISSING PARTS", padding=10)
    emp_list_frame.pack(fill='both', expand=True, padx=10, pady=5)

    self.emp_tree = ttk.Treeview(emp_tree_container,
                            columns=('EMP Number', 'BFM', 'Description', 'Priority',
                                   'Assigned', 'Status', 'Reported Date', 'Missing Parts'),
                            show='headings', height=10)
```

### PyQt5 Conversion
```python
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                            QPushButton, QLabel, QComboBox, QTableWidget,
                            QFrame, QSplitter)
from PyQt5.QtCore import Qt

def create_cm_management_tab(self):
    """Corrective Maintenance management tab - PyQt5 version"""
    self.cm_widget = QWidget()
    main_layout = QVBoxLayout(self.cm_widget)
    main_layout.setContentsMargins(10, 10, 10, 10)

    # CM controls
    controls_group = QGroupBox("CM Controls")
    controls_main_layout = QVBoxLayout()

    # First row of controls
    controls_row1 = QWidget()
    row1_layout = QHBoxLayout(controls_row1)
    row1_layout.setContentsMargins(0, 0, 0, 0)

    create_btn = QPushButton("Create New CM")
    create_btn.clicked.connect(self.create_cm_dialog)
    row1_layout.addWidget(create_btn)

    edit_btn = QPushButton("Edit CM")
    edit_btn.clicked.connect(self.edit_cm_dialog)
    row1_layout.addWidget(edit_btn)

    complete_btn = QPushButton("Complete CM")
    complete_btn.clicked.connect(self.complete_cm_dialog)
    row1_layout.addWidget(complete_btn)

    refresh_btn = QPushButton("Refresh CM List")
    refresh_btn.clicked.connect(self.load_corrective_maintenance_with_filter)
    row1_layout.addWidget(refresh_btn)

    row1_layout.addStretch()
    controls_main_layout.addWidget(controls_row1)

    # Filter controls
    filter_widget = QWidget()
    filter_layout = QHBoxLayout(filter_widget)
    filter_layout.setContentsMargins(0, 5, 0, 0)

    filter_layout.addWidget(QLabel("Filter by Status:"))

    self.cm_filter_combo = QComboBox()
    self.cm_filter_combo.addItems(["All", "Open", "Closed"])
    self.cm_filter_combo.setFixedWidth(150)
    self.cm_filter_combo.currentIndexChanged.connect(self.filter_cm_list)
    filter_layout.addWidget(self.cm_filter_combo)

    clear_filter_btn = QPushButton("Clear Filter")
    clear_filter_btn.clicked.connect(self.clear_cm_filter)
    filter_layout.addWidget(clear_filter_btn)

    filter_layout.addStretch()
    controls_main_layout.addWidget(filter_widget)

    # Second row - Missing Parts controls
    controls_row2 = QWidget()
    row2_layout = QHBoxLayout(controls_row2)
    row2_layout.setContentsMargins(0, 5, 0, 0)

    row2_layout.addWidget(QLabel("Equipment Missing Parts:"))

    report_parts_btn = QPushButton("Report Missing Parts")
    report_parts_btn.clicked.connect(self.create_missing_parts_dialog)
    row2_layout.addWidget(report_parts_btn)

    edit_parts_btn = QPushButton("Edit Missing Parts Entry")
    edit_parts_btn.clicked.connect(self.edit_missing_parts_dialog)
    row2_layout.addWidget(edit_parts_btn)

    close_parts_btn = QPushButton("Close Missing Parts Entry")
    close_parts_btn.clicked.connect(self.close_missing_parts_dialog)
    row2_layout.addWidget(close_parts_btn)

    row2_layout.addStretch()
    controls_main_layout.addWidget(controls_row2)

    controls_group.setLayout(controls_main_layout)
    main_layout.addWidget(controls_group)

    # CM list table
    cm_list_group = QGroupBox("Corrective Maintenance List")
    cm_list_layout = QVBoxLayout()

    self.cm_table = QTableWidget()
    self.cm_table.setColumnCount(8)
    self.cm_table.setHorizontalHeaderLabels([
        'CM Number', 'BFM', 'Description', 'Priority',
        'Assigned', 'Status', 'Created', 'Source'
    ])

    # Set column widths
    header = self.cm_table.horizontalHeader()
    widths = [120, 120, 250, 80, 120, 80, 100, 80]
    for i, width in enumerate(widths):
        header.resizeSection(i, width)

    # Fixed height to ensure missing parts list is visible
    self.cm_table.setMaximumHeight(300)
    self.cm_table.setSortingEnabled(True)
    self.cm_table.setSelectionBehavior(QTableWidget.SelectRows)

    cm_list_layout.addWidget(self.cm_table)
    cm_list_group.setLayout(cm_list_layout)
    main_layout.addWidget(cm_list_group)

    # Separator - QFrame with horizontal line
    separator = QFrame()
    separator.setFrameShape(QFrame.HLine)
    separator.setFrameShadow(QFrame.Sunken)
    main_layout.addWidget(separator)

    # Equipment Missing Parts list - SEPARATE section
    emp_list_group = QGroupBox("⚠️ EQUIPMENT WITH MISSING PARTS - SEPARATE LIST ⚠️")
    emp_list_layout = QVBoxLayout()

    # Controls for missing parts
    emp_controls = QWidget()
    emp_controls_layout = QHBoxLayout(emp_controls)
    emp_controls_layout.setContentsMargins(0, 0, 0, 5)

    refresh_emp_btn = QPushButton("🔄 Refresh Missing Parts List")
    refresh_emp_btn.clicked.connect(self.load_missing_parts_list)
    emp_controls_layout.addWidget(refresh_emp_btn)

    info_label = QLabel("This is a SEPARATE list from CM items above - entries you create will appear here")
    info_label.setStyleSheet("color: blue; font-style: italic; font-size: 9pt;")
    emp_controls_layout.addWidget(info_label)
    emp_controls_layout.addStretch()

    emp_list_layout.addWidget(emp_controls)

    # Missing parts table
    self.emp_table = QTableWidget()
    self.emp_table.setColumnCount(8)
    self.emp_table.setHorizontalHeaderLabels([
        'EMP Number', 'BFM', 'Description', 'Priority',
        'Assigned', 'Status', 'Reported Date', 'Missing Parts'
    ])

    # Set column widths
    header = self.emp_table.horizontalHeader()
    emp_widths = [120, 120, 200, 80, 120, 80, 100, 300]
    for i, width in enumerate(emp_widths):
        header.resizeSection(i, width)

    self.emp_table.setSortingEnabled(True)
    self.emp_table.setSelectionBehavior(QTableWidget.SelectRows)

    emp_list_layout.addWidget(self.emp_table)
    emp_list_group.setLayout(emp_list_layout)
    main_layout.addWidget(emp_list_group, stretch=1)

    # Add to main tab widget
    self.tab_widget.addTab(self.cm_widget, "Corrective Maintenance")

    # Initialize data
    self.cm_original_data = []
    self.load_corrective_maintenance_with_filter()
    self.load_missing_parts_list()
```

### Alternative: Using QSplitter for Resizable Sections
```python
# Instead of fixed heights, use QSplitter for user-resizable sections
def create_cm_management_tab_with_splitter(self):
    """CM tab with resizable sections"""
    self.cm_widget = QWidget()
    main_layout = QVBoxLayout(self.cm_widget)

    # Controls at top (fixed)
    # ... (controls code same as above)

    # Create splitter for resizable table sections
    splitter = QSplitter(Qt.Vertical)

    # CM list in top section
    cm_list_group = QGroupBox("Corrective Maintenance List")
    cm_list_layout = QVBoxLayout()
    self.cm_table = QTableWidget()
    # ... (table setup)
    cm_list_layout.addWidget(self.cm_table)
    cm_list_group.setLayout(cm_list_layout)
    splitter.addWidget(cm_list_group)

    # Missing parts in bottom section
    emp_list_group = QGroupBox("⚠️ EQUIPMENT WITH MISSING PARTS")
    emp_list_layout = QVBoxLayout()
    self.emp_table = QTableWidget()
    # ... (table setup)
    emp_list_layout.addWidget(self.emp_table)
    emp_list_group.setLayout(emp_list_layout)
    splitter.addWidget(emp_list_group)

    # Set initial sizes (30% top, 70% bottom)
    splitter.setSizes([300, 700])

    main_layout.addWidget(splitter, stretch=1)
    self.tab_widget.addTab(self.cm_widget, "Corrective Maintenance")
```

---

## General Conversion Patterns

### 1. Widget Hierarchy and Initialization

#### Tkinter Pattern
```python
class CMMS_App:
    def __init__(self, root):
        self.root = root
        self.root.title("CMMS Application")

        # Create notebook (tab widget)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.create_equipment_tab()
        self.create_pm_scheduling_tab()
```

#### PyQt5 Pattern
```python
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget
from PyQt5.QtCore import Qt

class CMMS_App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CMMS Application")

        # Create central widget (required for QMainWindow)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Create tabs
        self.create_equipment_tab()
        self.create_pm_scheduling_tab()

        # Set window size
        self.resize(1200, 800)
```

### 2. Variable Management

#### Tkinter - StringVar, IntVar, BooleanVar
```python
# Tkinter uses special variable objects
self.search_var = tk.StringVar()
self.entry = ttk.Entry(self.frame, textvariable=self.search_var)

# Get value
value = self.search_var.get()

# Set value
self.search_var.set("New value")

# Trace changes
self.search_var.trace('w', lambda *args: self.on_search_changed())
```

#### PyQt5 - Direct Widget Values
```python
# PyQt5 widgets store values directly
self.entry = QLineEdit()

# Get value
value = self.entry.text()

# Set value
self.entry.setText("New value")

# Connect to changes
self.entry.textChanged.connect(self.on_search_changed)
```

### 3. Event Binding

#### Tkinter Event Binding
```python
# Keyboard events
widget.bind('<KeyRelease>', self.on_key_release)
widget.bind('<Return>', self.on_enter_pressed)
widget.bind('<Escape>', self.on_escape_pressed)

# Mouse events
widget.bind('<Button-1>', self.on_left_click)
widget.bind('<Double-1>', self.on_double_click)
widget.bind('<Button-3>', self.on_right_click)

# Widget events
combobox.bind('<<ComboboxSelected>>', self.on_combo_selected)
tree.bind('<<TreeviewSelect>>', self.on_tree_select)
```

#### PyQt5 Signal-Slot Connections
```python
# Text input events
widget.textChanged.connect(self.on_text_changed)
widget.returnPressed.connect(self.on_enter_pressed)
# Note: Escape requires keyPressEvent override

# Mouse events on tables
table.cellClicked.connect(self.on_cell_clicked)
table.cellDoubleClicked.connect(self.on_double_click)
# Right-click requires contextMenuEvent override or customContextMenuRequested

# Widget events
combobox.currentIndexChanged.connect(self.on_combo_selected)
table.itemSelectionChanged.connect(self.on_selection_changed)
```

### 4. Key Press Events (Advanced)

```python
# PyQt5 - Override keyPressEvent for special keys
from PyQt5.QtCore import Qt

def keyPressEvent(self, event):
    """Handle keyboard events"""
    if event.key() == Qt.Key_Escape:
        self.on_escape_pressed()
    elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
        self.on_enter_pressed()
    elif event.key() == Qt.Key_Delete:
        self.on_delete_pressed()
    else:
        super().keyPressEvent(event)  # Pass to parent
```

---

## Widget Mapping Reference

### Complete Widget Conversion Table

| Tkinter Widget | PyQt5 Widget | Notes |
|----------------|--------------|-------|
| `tk.Frame` / `ttk.Frame` | `QWidget` or `QFrame` | Use `QFrame` for borders |
| `ttk.LabelFrame` | `QGroupBox` | GroupBox has built-in title |
| `ttk.Label` | `QLabel` | Similar functionality |
| `ttk.Button` | `QPushButton` | Use `.clicked.connect()` instead of `command=` |
| `ttk.Entry` | `QLineEdit` | No need for StringVar |
| `tk.Text` | `QTextEdit` | Multi-line text widget |
| `ttk.Combobox` | `QComboBox` | Set editable with `.setEditable(True)` |
| `ttk.Checkbutton` | `QCheckBox` | Use `.isChecked()` instead of BooleanVar |
| `ttk.Radiobutton` | `QRadioButton` | Group with `QButtonGroup` |
| `ttk.Notebook` | `QTabWidget` | `.addTab()` instead of `.add()` |
| `ttk.Treeview` | `QTableWidget` or `QTreeWidget` | Use `QTableWidget` for table data |
| `ttk.Scrollbar` | Built-in | Most widgets have automatic scrollbars |
| `tk.Listbox` | `QListWidget` | Similar functionality |
| `ttk.Separator` | `QFrame` with `setFrameShape(QFrame.HLine)` | Horizontal or vertical line |
| `ttk.Progressbar` | `QProgressBar` | Similar functionality |
| `tk.Menu` / `ttk.Menu` | `QMenu` / `QMenuBar` | Attached to QMainWindow |
| `tk.Spinbox` | `QSpinBox` or `QDoubleSpinBox` | Integer or double values |
| `tk.Scale` | `QSlider` | Horizontal or vertical slider |
| `messagebox` | `QMessageBox` | Static methods: `information()`, `warning()`, etc. |
| `filedialog` | `QFileDialog` | Static methods: `getOpenFileName()`, etc. |
| `simpledialog` | `QInputDialog` | Static methods: `getText()`, `getInt()`, etc. |

### Detailed Widget Conversions

#### Labels with Styling
```python
# Tkinter
label = ttk.Label(frame, text="Status:", font=('Arial', 12, 'bold'),
                 foreground='red', background='yellow')

# PyQt5
label = QLabel("Status:")
label.setStyleSheet("""
    QLabel {
        font-family: Arial;
        font-size: 12pt;
        font-weight: bold;
        color: red;
        background-color: yellow;
    }
""")
```

#### Buttons
```python
# Tkinter
button = ttk.Button(frame, text="Click Me", command=self.on_click, width=20)
button.config(state='disabled')

# PyQt5
button = QPushButton("Click Me")
button.setFixedWidth(150)  # Width in pixels
button.clicked.connect(self.on_click)
button.setEnabled(False)  # Disable button
```

#### Entry Fields
```python
# Tkinter
var = tk.StringVar(value="default")
entry = ttk.Entry(frame, textvariable=var, width=30)
value = var.get()
var.set("new value")

# PyQt5
entry = QLineEdit("default")
entry.setFixedWidth(300)
value = entry.text()
entry.setText("new value")

# Placeholder text
entry.setPlaceholderText("Enter text here...")
```

#### Checkboxes
```python
# Tkinter
var = tk.BooleanVar(value=True)
checkbox = ttk.Checkbutton(frame, text="Enable feature", variable=var)
is_checked = var.get()

# PyQt5
checkbox = QCheckBox("Enable feature")
checkbox.setChecked(True)
is_checked = checkbox.isChecked()
```

#### Radio Buttons
```python
# Tkinter
var = tk.StringVar(value="option1")
radio1 = ttk.Radiobutton(frame, text="Option 1", variable=var, value="option1")
radio2 = ttk.Radiobutton(frame, text="Option 2", variable=var, value="option2")
selected = var.get()

# PyQt5
from PyQt5.QtWidgets import QRadioButton, QButtonGroup

# Create button group to manage exclusivity
button_group = QButtonGroup()

radio1 = QRadioButton("Option 1")
radio1.setChecked(True)
button_group.addButton(radio1, 1)

radio2 = QRadioButton("Option 2")
button_group.addButton(radio2, 2)

# Get selected
selected_id = button_group.checkedId()
```

---

## Layout Manager Conversion

### Pack Layout

#### Tkinter pack()
```python
# Vertical stacking (default)
label1.pack()
label2.pack()
label3.pack()

# Horizontal arrangement
button1.pack(side='left')
button2.pack(side='left')
button3.pack(side='left')

# With spacing and fill
frame.pack(fill='both', expand=True, padx=10, pady=5)
widget.pack(fill='x', padx=5)
```

#### PyQt5 QVBoxLayout and QHBoxLayout
```python
# Vertical stacking
layout = QVBoxLayout()
layout.addWidget(label1)
layout.addWidget(label2)
layout.addWidget(label3)

# Horizontal arrangement
layout = QHBoxLayout()
layout.addWidget(button1)
layout.addWidget(button2)
layout.addWidget(button3)

# With spacing and stretch
layout.setContentsMargins(10, 5, 10, 5)  # left, top, right, bottom (like padx/pady)
layout.setSpacing(5)  # spacing between widgets
layout.addWidget(widget, stretch=1)  # stretch factor (like expand=True)

# Add spacer to push widgets
layout.addStretch()  # Adds expanding space
```

### Grid Layout

#### Tkinter grid()
```python
# Simple grid
label.grid(row=0, column=0)
entry.grid(row=0, column=1)
button.grid(row=1, column=0, columnspan=2)

# With sticky (alignment)
label.grid(row=0, column=0, sticky='w')  # Align west (left)
entry.grid(row=0, column=1, sticky='ew')  # Stretch east-west

# With padding
widget.grid(row=0, column=0, padx=10, pady=5)

# Configure row/column weights
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
```

#### PyQt5 QGridLayout
```python
# Simple grid
layout = QGridLayout()
layout.addWidget(label, 0, 0)  # row, column
layout.addWidget(entry, 0, 1)
layout.addWidget(button, 1, 0, 1, 2)  # row, col, rowspan, colspan

# With alignment (replaces sticky)
from PyQt5.QtCore import Qt
layout.addWidget(label, 0, 0, Qt.AlignLeft)  # Align left
layout.addWidget(entry, 0, 1, Qt.AlignLeft | Qt.AlignTop)  # Multiple alignments

# With spacing
layout.setHorizontalSpacing(10)
layout.setVerticalSpacing(5)
layout.setContentsMargins(10, 10, 10, 10)

# Configure row/column stretch (replaces weight)
layout.setRowStretch(0, 1)
layout.setColumnStretch(0, 1)
```

### Layout Comparison Table

| Tkinter | PyQt5 | Description |
|---------|-------|-------------|
| `pack(side='top')` | `QVBoxLayout().addWidget()` | Stack vertically |
| `pack(side='left')` | `QHBoxLayout().addWidget()` | Arrange horizontally |
| `pack(fill='both', expand=True)` | `layout.addWidget(w, stretch=1)` | Expand to fill space |
| `pack(padx=10, pady=5)` | `layout.setContentsMargins(10,5,10,5)` | Outer padding |
| `grid(row=0, column=1)` | `layout.addWidget(w, 0, 1)` | Grid positioning |
| `grid(sticky='nsew')` | `Qt.AlignLeft | Qt.AlignTop` | Alignment |
| `grid(columnspan=2)` | `layout.addWidget(w, r, c, 1, 2)` | Column span |
| `grid_rowconfigure(0, weight=1)` | `layout.setRowStretch(0, 1)` | Row expansion |

---

## Dialog Conversion Patterns

### Simple Input Dialog

#### Tkinter Dialog
```python
def add_equipment_dialog(self):
    """Dialog to add new equipment"""
    dialog = tk.Toplevel(self.root)
    dialog.title("Add New Equipment")
    dialog.geometry("500x400")
    dialog.transient(self.root)  # Make modal
    dialog.grab_set()  # Capture all events

    # Form fields
    ttk.Label(dialog, text="SAP Material No:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
    sap_var = tk.StringVar()
    ttk.Entry(dialog, textvariable=sap_var, width=30).grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(dialog, text="BFM Equipment No:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
    bfm_var = tk.StringVar()
    ttk.Entry(dialog, textvariable=bfm_var, width=30).grid(row=1, column=1, padx=10, pady=5)

    def save():
        sap = sap_var.get()
        bfm = bfm_var.get()
        # Save to database
        dialog.destroy()

    # Buttons
    button_frame = ttk.Frame(dialog)
    button_frame.grid(row=2, column=0, columnspan=2, pady=10)
    ttk.Button(button_frame, text="Save", command=save).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side='left', padx=5)
```

#### PyQt5 Dialog
```python
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

def add_equipment_dialog(self):
    """Dialog to add new equipment - PyQt5 version"""
    dialog = QDialog(self)
    dialog.setWindowTitle("Add New Equipment")
    dialog.setFixedSize(500, 400)
    dialog.setModal(True)  # Replaces transient + grab_set

    # Main layout
    main_layout = QVBoxLayout(dialog)

    # Form layout
    form_layout = QGridLayout()

    # SAP Material No
    form_layout.addWidget(QLabel("SAP Material No:"), 0, 0, Qt.AlignLeft)
    sap_entry = QLineEdit()
    sap_entry.setFixedWidth(300)
    form_layout.addWidget(sap_entry, 0, 1, Qt.AlignLeft)

    # BFM Equipment No
    form_layout.addWidget(QLabel("BFM Equipment No:"), 1, 0, Qt.AlignLeft)
    bfm_entry = QLineEdit()
    bfm_entry.setFixedWidth(300)
    form_layout.addWidget(bfm_entry, 1, 1, Qt.AlignLeft)

    main_layout.addLayout(form_layout)
    main_layout.addStretch()

    # Buttons
    button_layout = QHBoxLayout()

    save_btn = QPushButton("Save")
    def save():
        sap = sap_entry.text()
        bfm = bfm_entry.text()
        # Save to database
        dialog.accept()  # Close with success
    save_btn.clicked.connect(save)
    button_layout.addWidget(save_btn)

    cancel_btn = QPushButton("Cancel")
    cancel_btn.clicked.connect(dialog.reject)  # Close without saving
    button_layout.addWidget(cancel_btn)

    button_layout.addStretch()
    main_layout.addLayout(button_layout)

    # Show dialog and wait for result
    result = dialog.exec_()  # Blocks until dialog closes
    if result == QDialog.Accepted:
        # User clicked Save
        pass
```

### Custom Dialog with Calendar Picker

#### Tkinter with tkcalendar
```python
def create_cm_dialog(self):
    """Create CM with calendar picker"""
    dialog = tk.Toplevel(self.root)
    dialog.title("Create New CM")

    # Date entry with calendar button
    ttk.Label(dialog, text="CM Date:").grid(row=0, column=0)

    date_frame = ttk.Frame(dialog)
    date_frame.grid(row=0, column=1)

    cm_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
    date_entry = ttk.Entry(date_frame, textvariable=cm_date_var, width=15)
    date_entry.pack(side='left', padx=(0, 5))

    def open_calendar():
        from tkcalendar import Calendar
        cal_dialog = tk.Toplevel(dialog)
        cal_dialog.title("Select Date")

        cal = Calendar(cal_dialog, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(pady=20)

        def select_date():
            cm_date_var.set(cal.get_date())
            cal_dialog.destroy()

        ttk.Button(cal_dialog, text="Select", command=select_date).pack()

    ttk.Button(date_frame, text="Pick Date", command=open_calendar).pack(side='left')
```

#### PyQt5 with QDateEdit
```python
from PyQt5.QtWidgets import QDateEdit, QCalendarWidget
from PyQt5.QtCore import QDate

def create_cm_dialog(self):
    """Create CM with date picker - PyQt5 version"""
    dialog = QDialog(self)
    dialog.setWindowTitle("Create New CM")

    layout = QGridLayout(dialog)

    # Date entry with built-in calendar popup
    layout.addWidget(QLabel("CM Date:"), 0, 0)

    date_edit = QDateEdit()
    date_edit.setCalendarPopup(True)  # Enables calendar dropdown
    date_edit.setDate(QDate.currentDate())  # Set to today
    date_edit.setDisplayFormat("yyyy-MM-dd")
    layout.addWidget(date_edit, 0, 1)

    # Get selected date
    selected_date = date_edit.date()
    date_string = selected_date.toString("yyyy-MM-dd")
```

### Message Boxes

#### Tkinter messagebox
```python
from tkinter import messagebox

# Info message
messagebox.showinfo("Success", "Equipment added successfully!")

# Warning
messagebox.showwarning("Warning", "Please select equipment to edit")

# Error
messagebox.showerror("Error", f"Failed to add equipment: {str(e)}")

# Yes/No question
response = messagebox.askyesno("Confirm", "Are you sure you want to delete?")
if response:
    # User clicked Yes
    pass
```

#### PyQt5 QMessageBox
```python
from PyQt5.QtWidgets import QMessageBox

# Info message
QMessageBox.information(self, "Success", "Equipment added successfully!")

# Warning
QMessageBox.warning(self, "Warning", "Please select equipment to edit")

# Error
QMessageBox.critical(self, "Error", f"Failed to add equipment: {str(e)}")

# Yes/No question
response = QMessageBox.question(self, "Confirm", "Are you sure you want to delete?",
                               QMessageBox.Yes | QMessageBox.No)
if response == QMessageBox.Yes:
    # User clicked Yes
    pass

# Custom buttons and detailed text
msg = QMessageBox(self)
msg.setIcon(QMessageBox.Warning)
msg.setWindowTitle("WARNING: Potential Duplicate PM Detected")
msg.setText("A similar PM was recently submitted.")
msg.setDetailedText(f"Equipment: {bfm_no}\nPM Type: {pm_type}")
msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
result = msg.exec_()
```

### File Dialogs

#### Tkinter filedialog
```python
from tkinter import filedialog

# Open file
filename = filedialog.askopenfilename(
    title="Select CSV file",
    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
)

# Save file
filename = filedialog.asksaveasfilename(
    title="Export to CSV",
    defaultextension=".csv",
    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
)

# Select directory
directory = filedialog.askdirectory(title="Select folder")
```

#### PyQt5 QFileDialog
```python
from PyQt5.QtWidgets import QFileDialog

# Open file
filename, _ = QFileDialog.getOpenFileName(
    self,
    "Select CSV file",
    "",  # Starting directory (empty = current)
    "CSV files (*.csv);;All files (*.*)"
)

# Save file
filename, _ = QFileDialog.getSaveFileName(
    self,
    "Export to CSV",
    "export.csv",  # Default filename
    "CSV files (*.csv);;All files (*.*)"
)

# Select directory
directory = QFileDialog.getExistingDirectory(
    self,
    "Select folder",
    ""  # Starting directory
)

# Check if user cancelled
if filename:
    # User selected a file
    with open(filename, 'r') as f:
        pass
```

---

## Complete Example: Tab Method Conversion

### Equipment Tab - Side by Side Comparison

#### Tkinter Version (Original)
```python
def create_equipment_tab(self):
    self.equipment_frame = ttk.Frame(self.notebook)
    self.notebook.add(self.equipment_frame, text="Equipment Management")

    controls_frame = ttk.LabelFrame(self.equipment_frame, text="Equipment Controls", padding=10)
    controls_frame.pack(fill='x', padx=10, pady=5)

    ttk.Button(controls_frame, text="Add Equipment",
              command=self.add_equipment_dialog).pack(side='left', padx=5)

    self.equipment_tree = ttk.Treeview(self.equipment_frame,
                                     columns=('SAP', 'BFM', 'Description'),
                                     show='headings')
    self.equipment_tree.pack(fill='both', expand=True, padx=10, pady=5)
```

#### PyQt5 Version (Converted)
```python
def create_equipment_tab(self):
    self.equipment_widget = QWidget()

    main_layout = QVBoxLayout(self.equipment_widget)
    main_layout.setContentsMargins(10, 5, 10, 5)

    controls_group = QGroupBox("Equipment Controls")
    controls_layout = QHBoxLayout()

    add_btn = QPushButton("Add Equipment")
    add_btn.clicked.connect(self.add_equipment_dialog)
    controls_layout.addWidget(add_btn)
    controls_layout.addStretch()

    controls_group.setLayout(controls_layout)
    main_layout.addWidget(controls_group)

    self.equipment_table = QTableWidget()
    self.equipment_table.setColumnCount(3)
    self.equipment_table.setHorizontalHeaderLabels(['SAP', 'BFM', 'Description'])
    main_layout.addWidget(self.equipment_table, stretch=1)

    self.tab_widget.addTab(self.equipment_widget, "Equipment Management")
```

---

## Summary Checklist

When converting a tab from Tkinter to PyQt5:

- [ ] Replace `ttk.Frame` with `QWidget`
- [ ] Replace `ttk.LabelFrame` with `QGroupBox`
- [ ] Replace `.pack()` with `QVBoxLayout/QHBoxLayout`
- [ ] Replace `.grid()` with `QGridLayout`
- [ ] Replace `ttk.Button` with `QPushButton`
- [ ] Replace `command=method` with `.clicked.connect(method)`
- [ ] Replace `ttk.Entry` + `StringVar` with `QLineEdit`
- [ ] Replace `ttk.Combobox` with `QComboBox`
- [ ] Replace `ttk.Treeview` with `QTableWidget`
- [ ] Replace `tk.Text` with `QTextEdit`
- [ ] Replace `tk.Listbox` with `QListWidget`
- [ ] Replace `.bind()` with `.connect()` signals
- [ ] Replace `messagebox` with `QMessageBox`
- [ ] Replace `filedialog` with `QFileDialog`
- [ ] Replace `tk.Toplevel` dialogs with `QDialog`
- [ ] Remove all `StringVar`, `IntVar`, `BooleanVar` - use widget methods instead
- [ ] Update all event handlers to use PyQt5 signal signatures
- [ ] Test all button clicks, form submissions, and data loading

---

## Additional Resources

### PyQt5 Signal Reference
- `textChanged` - Text changed in QLineEdit or QTextEdit
- `clicked` - Button or checkbox clicked
- `currentIndexChanged` - ComboBox selection changed
- `itemSelectionChanged` - Table/List selection changed
- `cellClicked(row, col)` - Table cell clicked
- `cellDoubleClicked(row, col)` - Table cell double-clicked
- `valueChanged` - SpinBox or Slider value changed

### Common PyQt5 Methods
- `setText(str)` / `text()` - QLineEdit, QLabel
- `setPlainText(str)` / `toPlainText()` - QTextEdit
- `addItem(str)` / `addItems(list)` - QComboBox, QListWidget
- `setRowCount(int)` / `rowCount()` - QTableWidget
- `setItem(row, col, item)` / `item(row, col)` - QTableWidget
- `setEnabled(bool)` / `isEnabled()` - Any widget
- `setVisible(bool)` / `isVisible()` - Any widget
- `setStyleSheet(css)` - Apply CSS-like styling

### Debugging Tips
1. Use `print()` statements in signal handlers to verify connections
2. Check that all `.connect()` calls use methods without parentheses
3. Verify widget parent-child relationships (all widgets need a parent)
4. Use Qt Designer to prototype layouts visually
5. Enable PyQt5 exceptions: `sys.excepthook = lambda *args: print(args)`

---

End of Conversion Instructions
