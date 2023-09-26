# All code contained herewithin was written by ERROR_CODE 509, with assistance from ChatGPT.

import tkinter as tk
from tkinter import ttk

def save_spell():
    source_sanitized = source_entry.get()
    source_sanitized = source_sanitized.replace(" ", "_")
    source_sanitized = source_sanitized.replace("\'", "")
    name_sanitized = name_entry.get()
    name_sanitized = name_sanitized.replace(" ", "_")
    name_sanitized = name_sanitized.replace("\'", "")
    description_sanitized = description_entry.get('1.0', 'end-1c')
    description_sanitized = description_sanitized.replace("\n", "</p>\n\t\t\t<p>")
    with open(f"spells.xml", "a") as file:
        classes_list = []
        for class_name, class_var in class_checkboxes:
            if class_var.get():
                classes_list.append(class_name)
        file.write(f"\t<element name=\"{name_entry.get()}\" type=\"Spell\" source=\"{source_entry.get()}\" id=\"id_{source_sanitized}_{name_sanitized}\">\n")
        file.write("\t\t<supports>" + ", ".join(classes_list) + "</supports>\n")
        file.write("\t\t<description>\n")
        file.write(f"\t\t\t<p>{description_sanitized}</p>\n")
        file.write("\t\t</description>\n")
        file.write("\t\t<setters>\n")
        file.write(f"\t\t\t<set name=\"level\">{level.get()}</set>\n")
        file.write(f"\t\t\t<set name=\"school\">{school_combobox.get()}</set>\n")
        file.write(f"\t\t\t<set name=\"time\">{casting_time_entry.get()}</set>\n")
        file.write(f"\t\t\t<set name=\"duration\">{duration_entry.get()}</set>\n")
        file.write(f"\t\t\t<set name=\"range\">{range_entry.get()}</set>\n")
        file.write(f"\t\t\t<set name=\"hasVerbalComponent\">{'true' if verbal.get() == 1 else 'false'}</set>\n")
        file.write(f"\t\t\t<set name=\"hasSomaticComponent\">{'true' if somatic.get() == 1 else 'false'}</set>\n")
        file.write(f"\t\t\t<set name=\"hasMaterialComponent\">{'true' if material.get() == 1 else 'false'}</set>\n")
        if material.get() == 1:
            file.write(f"\t\t\t<set name=\"materialComponent\">{material_component_entry.get()}</set>\n")
        else:
            file.write("\t\t\t<set name=\"materialComponent\" />\n")
        file.write(f"\t\t\t<set name=\"isConcentration\">{'true' if concentration.get() == 1 else 'false'}</set>\n")
        file.write(f"\t\t\t<set name=\"isRitual\">{'true' if ritual.get() == 1 else 'false'}</set>\n")
        file.write("\t\t</setters>\n")
        file.write("\t</element>\n")

def update_save_button_state():
    required_fields = [name_entry.get(), source_entry.get(), description_entry.get("1.0", "end-1c"), school_combobox.get(), casting_time_entry.get(), duration_entry.get(), range_entry.get()]
    if all(required_fields) and (not material.get() or material_component_entry.get()):
        save_button.config(state="normal")
    else:
        save_button.config(state="disabled")

def update_material_entry_state():
    material_component_entry_state = "normal" if material.get() else "disabled"
    material_component_entry.config(state=material_component_entry_state)
    update_save_button_state()

def insert_header():
    with open(f"spells.xml", "a") as file:
        file.write("<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n")
        file.write("<elements>\n")
        file.write("\t<info>\n")
        file.write("\t\t<name>Spells</name>\n")
        file.write(f"\t\t<update version=\"{version_entry.get()}\">\n")
        if source_exists.get() == 1:
            file.write(f"\t\t\t<file name=\"spells.xml\" url=\"{source_url_entry.get()}\" />\n")
        else:
            file.write(f"\t\t\t<file name=\"spells.xml\" url=\"127.0.0.1\" />\n")
        file.write("\t\t</update>\n")
        file.write("\t<\info>\n")

def update_source_url_entry_state():
    source_url_entry_state = "normal" if source_exists.get() else "disabled"
    source_url_entry.config(state=source_url_entry_state)
    update_header_button_state()

def update_header_button_state():
    header_required_fields = [version_entry.get()]
    if all(header_required_fields) and (not source_exists.get() or source_url_entry.get()):
        header_button.config(state="normal")
    else:
        header_button.config(state="disabled")

def finish_close():
    with open(f"spells.xml", "a") as file:
        file.write("</elements>")
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Aurora Homebrew GUI v1.0")

# Create variables for checkboxes
artificer = tk.IntVar()
bard = tk.IntVar()
cleric = tk.IntVar()
druid = tk.IntVar()
paladin = tk.IntVar()
ranger = tk.IntVar()
sorcerer = tk.IntVar()
warlock = tk.IntVar()
wizard = tk.IntVar()

# Create variables for checkboxes and text entry
concentration = tk.IntVar()
ritual = tk.IntVar()
material = tk.IntVar()
verbal = tk.IntVar()
somatic = tk.IntVar()
source_exists = tk.IntVar()

# Create a variable for the level
level = tk.IntVar()
level.set(0)

# Create the main frame
main_frame = ttk.Frame(root)
main_frame.pack(padx=20, pady=20)

# Name Entry
name_label = ttk.Label(main_frame, text="Name")
name_label.grid(row=0, column=0, sticky="w")
name_entry = ttk.Entry(main_frame)
name_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="w")
name_entry.bind("<KeyRelease>", lambda event: update_save_button_state())

# Source Entry
source_label = ttk.Label(main_frame, text="Source")
source_label.grid(row=1, column=0, sticky="w")
source_entry = ttk.Entry(main_frame)
source_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="w")
source_entry.bind("<KeyRelease>", lambda event: update_save_button_state())

# Checkboxes for Classes
classes_label = ttk.Label(main_frame, text="Classes")
classes_label.grid(row=2, column=0, sticky="w")

# Predefined width for checkboxes
checkbox_width = 12

class_checkboxes = [
    ("Artificer", artificer),
    ("Bard", bard),
    ("Cleric", cleric),
    ("Druid", druid),
    ("Paladin", paladin),
    ("Ranger", ranger),
    ("Sorcerer", sorcerer),
    ("Warlock", warlock),
    ("Wizard", wizard)
]
for i, (class_name, class_var) in enumerate(class_checkboxes):
    checkbox = tk.Checkbutton(main_frame, text=class_name, variable=class_var, width=checkbox_width)
    checkbox.grid(row=2, column=i + 1, sticky="w")
    checkbox.bind("<ButtonRelease-1>", lambda event: update_save_button_state())

# Description Text Entry
description_label = ttk.Label(main_frame, text="Description")
description_label.grid(row=3, column=0, sticky="w")
description_entry = tk.Text(main_frame, height=5, width=40)
description_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="w")
description_entry.bind("<KeyRelease>", lambda event: update_save_button_state())

# Level Slider
level_label = tk.Label(main_frame, text="Level")
level_label.grid(row=4, column=0, sticky="w")
level_slider = tk.Scale(main_frame, from_=0, to=9, orient="horizontal", variable=level)
level_slider.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky="w")

# School Dropdown
school_label = ttk.Label(main_frame, text="School")
school_label.grid(row=5, column=0, sticky="w")
school_options = ["Abjuration", "Conjuration", "Divination", "Enchantment", "Evocation", "Illusion", "Necromancy", "Transmutation"]
school_combobox = ttk.Combobox(main_frame, state="readonly", values=school_options)
school_combobox.grid(row=5, column=1, columnspan=2, padx=10, pady=5, sticky="w")
school_combobox.bind("<<ComboboxSelected>>", lambda event: update_save_button_state())

# Casting Time Entry
casting_time_label = ttk.Label(main_frame, text="Casting Time")
casting_time_label.grid(row=6, column=0, sticky="w")
casting_time_entry = ttk.Entry(main_frame)
casting_time_entry.grid(row=6, column=1, columnspan=2, padx=10, pady=5, sticky="w")
casting_time_entry.bind("<KeyRelease>", lambda event: update_save_button_state())

# Concentration and Ritual Checkboxes
concentration_checkbox = tk.Checkbutton(main_frame, text="Concentration", variable=concentration)
concentration_checkbox.grid(row=7, column=0, sticky="w")
concentration_checkbox.bind("<ButtonRelease-1>", lambda event: update_save_button_state())

ritual_checkbox = tk.Checkbutton(main_frame, text="Ritual", variable=ritual)
ritual_checkbox.grid(row=7, column=1, sticky="w")
ritual_checkbox.bind("<ButtonRelease-1>", lambda event: update_save_button_state())

# Duration Entry
duration_label = ttk.Label(main_frame, text="Duration")
duration_label.grid(row=8, column=0, sticky="w")
duration_entry = ttk.Entry(main_frame)
duration_entry.grid(row=8, column=1, columnspan=2, padx=10, pady=5, sticky="w")
duration_entry.bind("<KeyRelease>", lambda event: update_save_button_state())

# Range Entry
range_label = ttk.Label(main_frame, text="Range")
range_label.grid(row=9, column=0, sticky="w")
range_entry = ttk.Entry(main_frame)
range_entry.grid(row=9, column=1, columnspan=2, padx=10, pady=5, sticky="w")
range_entry.bind("<KeyRelease>", lambda event: update_save_button_state())

# Verbal, Somatic, and Material Checkboxes
verbal_checkbox = tk.Checkbutton(main_frame, text="Verbal", variable=verbal)
verbal_checkbox.grid(row=10, column=0, sticky="w")

somatic_checkbox = tk.Checkbutton(main_frame, text="Somatic", variable=somatic)
somatic_checkbox.grid(row=10, column=1, sticky="w")

material_checkbox = tk.Checkbutton(main_frame, text="Material", variable=material, command=update_material_entry_state)
material_checkbox.grid(row=10, column=2, sticky="w")

# Material Component Entry
material_component_label = ttk.Label(main_frame, text="Material Component")
material_component_label.grid(row=11, column=0, sticky="w")
material_component_entry = ttk.Entry(main_frame, state="normal" if material.get() else "disabled")
material_component_entry.grid(row=11, column=1, columnspan=2, padx=10, pady=5, sticky="w")
material_component_entry.bind("<KeyRelease>", lambda event: update_save_button_state())

# Save Button
save_button = ttk.Button(main_frame, text="Save Spell", command=save_spell, state="disabled")
save_button.grid(row=12, column=0, columnspan=3, pady=10)

# Finish Button
finish_button = ttk.Button(main_frame, text="Finish & Close", command=finish_close)
finish_button.grid(row=12, column=1, columnspan=3, pady=10)

# Version Entry
version_label = ttk.Label(main_frame, text="Version")
version_label.grid(row=14, column=0, sticky="w")
version_entry = ttk.Entry(main_frame)
version_entry.grid(row=14, column=1, columnspan=2, padx=10, pady=5, sticky="w")
version_entry.bind("<KeyRelease>", lambda event: update_header_button_state())

# Source URL Entry (if applicable, obviously)
source_url_label = ttk.Label(main_frame, text="Source URL")
source_url_label.grid(row=15, column=0, sticky="w")
source_url_entry = ttk.Entry(main_frame, state="normal" if source_exists.get() else "disabled")
source_url_entry.grid(row=15, column=1, columnspan=2, padx=10, pady=5, sticky="w")
source_url_entry.bind("<KeyRelease>", lambda event: update_header_button_state())
source_exists_checkbox = tk.Checkbutton(main_frame, text="Has Online Source", variable=source_exists, command=update_source_url_entry_state)
source_exists_checkbox.grid(row=15, column=2, sticky="w")

# Header Insert Button
header_button = ttk.Button(main_frame, text="Insert Header", command=insert_header, state="disabled")
header_button.grid(row=16, column=0, columnspan=3, pady=10)

# Start the main loop
root.mainloop()