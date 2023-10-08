import tkinter as tk
from tkinter import ttk
import os
import tkinter.font as tkFont
from tkinter import filedialog

def save_spell():
    spell_path = output_path.get() + "\\spells.xml"
    import os
    if os.path.exists(spell_path):
        footer_exists = "</elements>"
        with open('spells.xml', 'r', encoding="utf-8") as file:
            lines = file.readlines()
        if lines and lines[-1].strip() == footer_exists:
            with open('temp.txt', 'w') as temp_file:
                temp_file.writelines(lines[:-1])
            os.replace('temp.txt', 'spells.xml')
    else:
        with open(f"{output_path.get()}\\spells.xml", "a") as file:
            file.write("<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n")
            file.write("<elements>\n")
    spellSource_sanitized = spellSource_entry.get()
    spellSource_sanitized = spellSource_sanitized.replace(" ", "_")
    spellSource_sanitized = spellSource_sanitized.replace("\'", "")
    spellName_sanitized = spellName_entry.get()
    spellName_sanitized = spellName_sanitized.replace(" ", "_")
    spellName_sanitized = spellName_sanitized.replace("\'", "")
    spellDescription_sanitized = spellDescription_entry.get('1.0', 'end-1c')
    spellDescription_sanitized = spellDescription_sanitized.replace("\n", "</p>\n\t\t\t<p>")
    with open(f"{output_path.get()}\\spells.xml", "a", encoding="utf-8") as file:
        classes_list = []
        for class_name, class_var in class_checkboxes:
            if class_var.get():
                classes_list.append(class_name)
        file.write(f"\t<element name=\"{spellName_entry.get()}\" type=\"Spell\" source=\"{spellSource_entry.get()}\" id=\"id_{spellSource_sanitized}_{spellName_sanitized}\">\n")
        file.write("\t\t<supports>" + ", ".join(classes_list) + "</supports>\n")
        file.write("\t\t<description>\n")
        file.write(f"\t\t\t<p>{spellDescription_sanitized}</p>\n")
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
        file.write("</elements>")

def update_saveSpell_button_state():
    required_fields = [spellName_entry.get(), spellSource_entry.get(), spellDescription_entry.get("1.0", "end-1c"), school_combobox.get(), casting_time_entry.get(), duration_entry.get(), range_entry.get()]
    if all(required_fields) and (not material.get() or material_component_entry.get()):
        if artificer.get() == 1 or bard.get() == 1 or cleric.get() == 1 or druid.get() == 1 or paladin.get() == 1 or ranger.get() == 1 or sorcerer.get() == 1 or warlock.get == 1 or wizard.get() == 1:
            if output_path.get():
                save_button.config(state="normal")
            else:
                save_button.config(state="disabled")
        else:
            save_button.config(state="disabled")
    else:
        save_button.config(state="disabled")

def update_materialSpell_entry_state():
    material_component_entry_state = "normal" if material.get() else "disabled"
    material_component_entry.config(state=material_component_entry_state)
    update_saveSpell_button_state()

def insert_header():
    with open(f"spells.xml", "a", encoding="utf-8") as file:
        file.write("<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n")
        file.write("<elements>\n")
        file.write("\t<info>\n")
        file.write("\t\t<name>Spells</name>\n")
        file.write(f"\t\t<update version=\"{source_version_entry.get()}\">\n")
        file.write(f"\t\t\t<file name=\"spells.xml\" url=\"{source_url_entry.get()}\" />\n")
        file.write("\t\t</update>\n")
        file.write("\t<\info>\n")

def update_spellSource_entry_state():
    source_url_entry_state = "normal" if source_exists.get() else "disabled"
    source_url_entry.config(state=source_url_entry_state)
    source_version_entry_state = "normal" if source_exists.get() else "disabled"
    source_version_entry.config(state=source_version_entry_state)
    update_header_button_state()

def update_header_button_state():
    header_required_fields = [source_version_entry.get()]
    if all(header_required_fields) and (not source_exists.get() or source_url_entry.get()):
        header_button.config(state="normal")
    else:
        header_button.config(state="disabled")

def select_folder():
    global output_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_path.set(folder_path)
    folder_path_label.config(text=output_path)
    update_saveSpell_button_state()


# Create the main window
root = tk.Tk()
root.title("Aurora Homebrew GUI v1.4.2")

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

# Create a StringVar to store the output folder path
output_path = tk.StringVar()

# Create the Notebook and its frames
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
spellCore = ttk.Frame(notebook)
spellHeader = ttk.Frame(notebook)
notebook.add(spellCore, text="Spell")
notebook.add(spellHeader, text="Source Header")

# Name Entry
name_label = ttk.Label(spellCore, text="Name")
name_label.grid(row=0, column=0, sticky="w")
spellName_entry = ttk.Entry(spellCore)
spellName_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="w")
spellName_entry.bind("<KeyRelease>", lambda event: update_saveSpell_button_state())

# Source Entry
source_label = ttk.Label(spellCore, text="Source")
source_label.grid(row=1, column=0, sticky="w")
spellSource_entry = ttk.Entry(spellCore)
spellSource_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="w")
spellSource_entry.bind("<KeyRelease>", lambda event: update_saveSpell_button_state())

# Checkboxes for Classes
classes_label = ttk.Label(spellCore, text="Classes")
classes_label.grid(row=2, column=0, sticky="w")

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
    checkbox = tk.Checkbutton(spellCore, text=class_name, variable=class_var, width=12)
    checkbox.grid(row=2, column=i + 1, sticky="w")
    checkbox.bind("<ButtonRelease-1>", lambda event: update_saveSpell_button_state())


# Description Text Entry
description_label = ttk.Label(spellCore, text="Description")
description_label.grid(row=3, column=0, sticky="w")
spellDescription_entry = tk.Text(spellCore, height=5, width=40)
spellDescription_entry.grid(row=3, column=1, columnspan=3, padx=10, pady=5, sticky="w")
spellDescription_entry.bind("<KeyRelease>", lambda event: update_saveSpell_button_state())

# Level Slider
level_label = tk.Label(spellCore, text="Level")
level_label.grid(row=4, column=0, sticky="w")
level_slider = tk.Scale(spellCore, from_=0, to=9, orient="horizontal", variable=level)
level_slider.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky="w")

# School Dropdown
school_label = ttk.Label(spellCore, text="School")
school_label.grid(row=5, column=0, sticky="w")
school_options = ["Abjuration", "Conjuration", "Divination", "Enchantment", "Evocation", "Illusion", "Necromancy", "Transmutation"]
school_combobox = ttk.Combobox(spellCore, state="readonly", values=school_options)
school_combobox.grid(row=5, column=1, columnspan=2, padx=10, pady=5, sticky="w")
school_combobox.bind("<<ComboboxSelected>>", lambda event: update_saveSpell_button_state())

# Casting Time Entry
casting_time_label = ttk.Label(spellCore, text="Casting Time")
casting_time_label.grid(row=6, column=0, sticky="w")
casting_time_entry = ttk.Entry(spellCore)
casting_time_entry.grid(row=6, column=1, columnspan=2, padx=10, pady=5, sticky="w")
casting_time_entry.bind("<KeyRelease>", lambda event: update_saveSpell_button_state())

# Concentration and Ritual Checkboxes
concentration_checkbox = tk.Checkbutton(spellCore, text="Concentration", variable=concentration)
concentration_checkbox.grid(row=7, column=0, sticky="w")
concentration_checkbox.bind("<ButtonRelease-1>", lambda event: update_saveSpell_button_state())

ritual_checkbox = tk.Checkbutton(spellCore, text="Ritual", variable=ritual)
ritual_checkbox.grid(row=7, column=1, sticky="w")
ritual_checkbox.bind("<ButtonRelease-1>", lambda event: update_saveSpell_button_state())

# Duration Entry
duration_label = ttk.Label(spellCore, text="Duration")
duration_label.grid(row=8, column=0, sticky="w")
duration_entry = ttk.Entry(spellCore)
duration_entry.grid(row=8, column=1, columnspan=2, padx=10, pady=5, sticky="w")
duration_entry.bind("<KeyRelease>", lambda event: update_saveSpell_button_state())

# Range Entry
range_label = ttk.Label(spellCore, text="Range")
range_label.grid(row=9, column=0, sticky="w")
range_entry = ttk.Entry(spellCore)
range_entry.grid(row=9, column=1, columnspan=2, padx=10, pady=5, sticky="w")
range_entry.bind("<KeyRelease>", lambda event: update_saveSpell_button_state())

# Verbal, Somatic, and Material Checkboxes
verbal_checkbox = tk.Checkbutton(spellCore, text="Verbal", variable=verbal)
verbal_checkbox.grid(row=10, column=0, sticky="w")

somatic_checkbox = tk.Checkbutton(spellCore, text="Somatic", variable=somatic)
somatic_checkbox.grid(row=10, column=1, sticky="w")

material_checkbox = tk.Checkbutton(spellCore, text="Material", variable=material, command=update_materialSpell_entry_state)
material_checkbox.grid(row=10, column=2, sticky="w")

# Material Component Entry
material_component_label = ttk.Label(spellCore, text="Material Component")
material_component_label.grid(row=11, column=0, sticky="w")
material_component_entry = ttk.Entry(spellCore, state="normal" if material.get() else "disabled")
material_component_entry.grid(row=11, column=1, columnspan=2, padx=10, pady=5, sticky="w")
material_component_entry.bind("<KeyRelease>", lambda event: update_saveSpell_button_state())

# Save Button
save_button = ttk.Button(spellCore, text="Add Spell", command=save_spell, state="disabled")
save_button.grid(row=12, column=1, pady=10)

# Output selection button and path label
output_button = ttk.Button(spellCore, text="Output Path", command=select_folder)
output_button.grid(row=12, column=2, pady=10)
folder_path_label = ttk.Label(spellCore, textvariable=output_path)
folder_path_label.grid(row=12, column=3, pady=10)

# Version Entry
source_version_label = ttk.Label(spellHeader, text="Version")
source_version_label.grid(row=0, column=0, sticky="w")
source_version_entry = ttk.Entry(spellHeader, state="normal" if source_exists.get() else "disabled")
source_version_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="w")
source_version_entry.bind("<KeyRelease>", lambda event: update_header_button_state())

# Source URL Entry (if applicable, obviously)
source_url_label = ttk.Label(spellHeader, text="Source URL")
source_url_label.grid(row=1, column=0, sticky="w")
source_url_entry = ttk.Entry(spellHeader, state="normal" if source_exists.get() else "disabled")
source_url_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="w")
source_url_entry.bind("<KeyRelease>", lambda event: update_header_button_state())
source_exists_checkbox = tk.Checkbutton(spellHeader, text="Has Online Source", variable=source_exists, command=update_spellSource_entry_state)
source_exists_checkbox.grid(row=0, column=3, sticky="w")

# Header Insert Button
header_button = ttk.Button(spellHeader, text="Add Header", command=insert_header, state="disabled")
header_button.grid(row=2, column=0, columnspan=3, pady=10)

# Header warning label and italicized font
default_font = tkFont.nametofont("TkDefaultFont")
italicized_font = default_font.copy()
italicized_font.configure(slant="italic")
header_warning_label = ttk.Label(spellHeader, text="This header is only for online homebrew!", font=italicized_font, foreground="red")
header_warning_label.grid(row=2, column=3, sticky="w")

# Start the main loop
root.mainloop()
