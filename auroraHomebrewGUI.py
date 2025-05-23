import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import tkinter.font as tkFont
import xml.etree.ElementTree as ET

# Function to add spells. Should probably break this up to make it less of a monolithic mess.
def save_spell():
    spell_path = output_path.get() + "\\spells.xml"
    temp_directory = output_path.get() + "\\temp.txt"
    import os
    if os.path.exists(spell_path):
        header_line1 = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n"
        header_line2 = "<elements>\n"
        with open(spell_path, 'r', encoding="utf-8") as file:
            first_line = file.readline()
            second_line = file.readline()
            remaining_lines = file.readlines()
        if first_line != header_line1 and second_line != header_line2:
            lines = [header_line1, header_line2] + remaining_lines
            with open(spell_path, 'w', encoding="utf-8") as file:
                file.writelines(lines)
        elif first_line != header_line1 and second_line == header_line2:
            lines = header_line1 + remaining_lines
            with open(spell_path, 'w', encoding="utf-8") as file:
                file.writelines(lines)
        footer_exists = "</elements>"
        with open(spell_path, 'r', encoding="utf-8") as file:
            lines = file.readlines()
        if lines and lines[-1].strip() == footer_exists:
            with open(temp_directory, 'w') as temp_file:
                temp_file.writelines(lines[:-1])
            os.replace(temp_directory, spell_path)
    else:
        with open(f"{output_path.get()}\\spells.xml", "a") as file:
            file.write("<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n")
            file.write("<elements>\n")
    spellAuthor_sanitized, spellSource_sanitized, spellName_sanitized = spell_id_sanitizer()
    spellDescription_sanitized = spellDescription_entry.get('1.0', 'end-1c')
    spellDescription_sanitized = spellDescription_sanitized.replace("\n", "</p>\n\t\t\t<p>")
    with open(f"{output_path.get()}\\spells.xml", "a", encoding="utf-8") as file:
        classes_list = []
        for class_name, class_var in class_checkboxes:
            if class_var.get():
                classes_list.append(class_name)
        file.write(f"\t<element name=\"{spellName_entry.get()}\" type=\"Spell\" source=\"{spellSource_entry.get()}\" id=\"ID_{spellAuthor_sanitized}{spellSource_sanitized}_SPELL_{spellName_sanitized}\">\n")
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

# Function to sanitize spell author, source, and name
def spell_id_sanitizer():
    spellSource_sanitized = spellSource_entry.get()
    spellSource_sanitized = spellSource_sanitized.replace(" ", "_")
    spellSource_sanitized = spellSource_sanitized.replace("\'", "")
    spellSource_sanitized = spellSource_sanitized.upper()
    spellName_sanitized = spellName_entry.get()
    spellName_sanitized = spellName_sanitized.replace(" ", "_")
    spellName_sanitized = spellName_sanitized.replace("\'", "")
    spellName_sanitized = spellName_sanitized.upper()
    spellAuthor_sanitized = spellAuthor_entry.get()
    if spellAuthor_sanitized != "":
        spellAuthor_sanitized = spellAuthor_sanitized + "_"
        spellAuthor_sanitized = spellAuthor_sanitized.replace(" ", "_")
        spellAuthor_sanitized = spellAuthor_sanitized.replace("\'", "")
        spellAuthor_sanitized = spellAuthor_sanitized.upper()
    return spellAuthor_sanitized, spellSource_sanitized, spellName_sanitized

# Function to enable/disable "add spell" button
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

# Function to enable/disable material component entry
def update_materialSpell_entry_state():
    material_component_entry_state = "normal" if material.get() else "disabled"
    material_component_entry.config(state=material_component_entry_state)
    update_saveSpell_button_state()

# Function to add the online source header info
def insert_header():
    with open(f"spells.xml", "a", encoding="utf-8") as file:
        file.write("<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n")
        file.write("<elements>\n")
        file.write("\t<info>\n")
        file.write("\t\t<name>Spells</name>\n")
        file.write(f"\t\t<update version=\"{source_version_entry.get()}\">\n")
        file.write(f"\t\t\t<file name=\"spells.xml\" url=\"{source_url_entry.get()}\" />\n")
        file.write("\t\t</update>\n")
        file.write("\t</info>\n")

# Function to allow online source info entry
def update_spellSource_entry_state():
    source_url_entry_state = "normal" if source_exists.get() else "disabled"
    source_url_entry.config(state=source_url_entry_state)
    source_version_entry_state = "normal" if source_exists.get() else "disabled"
    source_version_entry.config(state=source_version_entry_state)
    update_header_button_state()

# Function to update the "add header" button
def update_header_button_state():
    header_required_fields = [source_version_entry.get()]
    if all(header_required_fields) and (not source_exists.get() or source_url_entry.get()):
        header_button.config(state="normal")
    else:
        header_button.config(state="disabled")

# Folder selection function
def select_folder():
    global output_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_path.set(folder_path)
    folder_path_label.config(text=output_path)
    update_saveSpell_button_state()

# Function to update the spell ID display
def spell_id_update():
    spellAuthor_sanitized, spellSource_sanitized, spellName_sanitized = spell_id_sanitizer()
    spellid = "ID_" + spellAuthor_sanitized + spellSource_sanitized + "_SPELL_" + spellName_sanitized
    if spellSource_sanitized != "" and spellName_sanitized !="":
        iddisplay_label.config(text=spellid)

# Display description help box
def description_help():
    messagebox.showinfo("Description Help", "The description (from what it seems) accepts basic HTML tags, including but not limited to the following:\n\n<i></i>, <em></em> - Italics\n<b></b>, <strong></strong> - Bold\n<p></p> - Line break (the program will do this for you)\n <h1> through <h6> - Supports h1 through h6 HTML tags, for larget/smaller text\n\nIndents can be added by including class=\"indent\" in the <p> tag, though you'll have to add this yourself.\n\nTables can also be added, but I'd suggest using an existing table as a template. The formatting isn't the most intuitive.")

# Create the main window
root = tk.Tk()
root.title("Aurora Homebrew GUI v1.6.1")

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

# Create a StringVar to store the output folder path and spell ID
output_path = tk.StringVar()
spellid = tk.StringVar()

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
spellName_entry.bind("<KeyRelease>", lambda event: [update_saveSpell_button_state(), spell_id_update()])

# Spell ID Display
idexplanation_label = ttk.Label(spellCore, text="Spell ID will be:")
idexplanation_label.grid(row=0, column=3, sticky="w")
spellid = ""
iddisplay_label = ttk.Label(spellCore, textvariable=spellid)
iddisplay_label.grid(row=0, column=4, sticky="w")

# Source Entry
source_label = ttk.Label(spellCore, text="Source")
source_label.grid(row=1, column=0, sticky="w")
spellSource_entry = ttk.Entry(spellCore)
spellSource_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="w")
spellSource_entry.bind("<KeyRelease>", lambda event: [update_saveSpell_button_state(), spell_id_update()])

# Author entry
author_label = ttk.Label(spellCore, text="Author (optional)")
author_label.grid(row=1, column=3, sticky="w")
spellAuthor_entry = ttk.Entry(spellCore)
spellAuthor_entry.grid(row=1, column=4, columnspan=2, padx=10, pady=5, sticky="w")
spellAuthor_entry.bind("<KeyRelease>", lambda event: spell_id_update())

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
    checkbox = ttk.Checkbutton(spellCore, text=class_name, variable=class_var, width=12)
    checkbox.grid(row=2, column=i + 1, sticky="w")
    checkbox.bind("<ButtonRelease-1>", lambda event: update_saveSpell_button_state())


# Description Text Entry
description_label = ttk.Label(spellCore, text="Description")
description_label.grid(row=3, column=0, sticky="w")
spellDescription_entry = tk.Text(spellCore, height=5, width=40)
spellDescription_entry.grid(row=3, column=1, columnspan=3, padx=10, pady=5, sticky="w")
spellDescription_entry.bind("<KeyRelease>", lambda event: update_saveSpell_button_state())

# Description help dialogue
descriptionhelp_button = ttk.Button(spellCore, text="?", command=description_help, width=3)
descriptionhelp_button.grid(row=3, column=4, pady=10)

# Level Slider
level_label = ttk.Label(spellCore, text="Level")
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
casting_label = ttk.Label(spellCore, text="Casting")
casting_label.grid(row=7, column=0, sticky="w")
concentration_checkbox = ttk.Checkbutton(spellCore, text="Concentration", variable=concentration)
concentration_checkbox.grid(row=7, column=1, sticky="w")
concentration_checkbox.bind("<ButtonRelease-1>", lambda event: update_saveSpell_button_state())
ritual_checkbox = ttk.Checkbutton(spellCore, text="Ritual", variable=ritual)
ritual_checkbox.grid(row=7, column=2, sticky="w")
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

# Spell component checkboxes
component_label = ttk.Label(spellCore, text="Components")
component_label.grid(row=10, column=0, sticky="w")
verbal_checkbox = ttk.Checkbutton(spellCore, text="Verbal", variable=verbal)
verbal_checkbox.grid(row=10, column=1, sticky="w")
somatic_checkbox = ttk.Checkbutton(spellCore, text="Somatic", variable=somatic)
somatic_checkbox.grid(row=10, column=2, sticky="w")
material_checkbox = ttk.Checkbutton(spellCore, text="Material", variable=material, command=update_materialSpell_entry_state)
material_checkbox.grid(row=10, column=3, sticky="w")

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
source_exists_checkbox = ttk.Checkbutton(spellHeader, text="Has Online Source", variable=source_exists, command=update_spellSource_entry_state)
source_exists_checkbox.grid(row=0, column=3, sticky="w")

# Header Insert Button
header_button = ttk.Button(spellHeader, text="Add Header", command=insert_header, state="disabled")
header_button.grid(row=2, column=0, columnspan=3, pady=10)

# Header warning label and italicized font
default_font = tkFont.nametofont("TkDefaultFont")
italicized_font = default_font.copy()
italicized_font.configure(slant="italic")
header_warning_label = ttk.Label(spellHeader, text="This header is only used for online homebrew!", font=italicized_font, foreground="red")
header_warning_label.grid(row=2, column=3, sticky="w")

# Start the main loop
root.mainloop()
