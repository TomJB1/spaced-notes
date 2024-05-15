'''
box-order.csv holds the "boxes" - lists of names of notes and which box they are in
notes array {name: Note} in subfolder
Note: path, localpath
the boxes are loaded into an array [[str, ...], ...]
a session is created [str, ...]
'''

from dataclasses import dataclass
import os, random, csv
import matplotlib.pyplot as plt

NOTES_PATH = r'C:\Users\tomjb\Documents\Obsidian\Notes\School'
SAVE_FILE =   'save.csv'
NOTES_PER_BOX = [20, 10, 3, 2, 1]
STARTING_BOX = 1

@dataclass
class Note:
    path: str
    localpath: str


def get_notes_values(file) -> dict:
    if not os.path.isfile(file):
        with open(file, "w") as csvfile:
            csvfile.write("name,value")
        print("WARNING: made a new blank save file")
    notes_values = {}
    with open(file, "r") as csvfile:
        for row in csv.DictReader(csvfile):
            notes_values.update({row["name"]: row["value"]})
    return notes_values

def print_folders() -> None:
    global NOTES_PATH
    for contents in os.scandir(NOTES_PATH):
        if contents.is_dir():
            print(contents.name)

def get_notes() -> dict: 
    notes = {}
    for (root, dirs, files) in os.walk(folder):
        for file in files:
            if '.md' in file:
                notes.update({file.replace('.md', ''): Note(root+ "\\" + file, (root+ "\\" + file).replace(NOTES_PATH, ""))})
    return notes

def sort_notes(notes:dict, notes_values:dict) -> list[list[list], dict]:
    sorted_notes = [[], [], [], [], []]
    for name in notes.keys():
        try:
            value = notes_values[name]
        except KeyError:
            # adding new
            value = STARTING_BOX
            notes_values[name] = STARTING_BOX
        try:
            sorted_notes[int(value)].append(name)
        except IndexError:
            # skipping
            pass
    return sorted_notes, notes_values # returns the notes values so that new notes can be added as 0

def create_session(notes_per_box:list[str], sorted_notes:list[list]) -> list[str]:
    session_notes = []
    for n in range(0,5):
        for _ in range(notes_per_box[n]):
            if len(sorted_notes[n]) != 0:
                random.shuffle(sorted_notes[n])
                session_notes.append(sorted_notes[n].pop())
    random.shuffle(session_notes)
    return session_notes

def check_note(content) -> bool:
    if (content.find("#index")!=-1 or content.find("#archive")!=-1 or content.find("#stub")!=-1):
        if content.find("#index/has-info")==-1:
            return False
    return True

def save_notes_values(file, notes_values:dict) -> None:
    with open(file, "w+") as csvfile:
        writer = csv.DictWriter(csvfile, ["name","value"], lineterminator="\n")
        writer.writeheader()
        for note, value in notes_values.items():
            writer.writerow({"name": note, "value": value})
    return 

def get_outcome(notes_values:dict, name)->dict:
    try:
        print("\n0: incorrect   1: partially correct    2: correct")
        response = int(input())
    except ValueError:
            return None
    note_value = int(notes_values[name])
    match(response):
        case 0:
            notes_values[name] = 0
        case 1:
            pass
        case 2:
            if note_value < 4:
                notes_values[name] = note_value+1
        case -1:
            notes_values[name] = 10
        case _:
            return None
    return notes_values
            
if __name__ == "__main__":

################### main variables ##########################
    notes = {} # {note_name: Note, ...}
    notes_values = {} # {name: value, ...}
    sorted_notes = [[], [], [], [], []] # [[str, ...], ...]
    session_notes = [] # [str, ...]
#############################################################

    # select subfolder
    print_folders()
    folder = NOTES_PATH+"\\"+input("enter a subfolder: ")
    ## load names of notes in subfolder
    notes = get_notes()
    ## get values of all tracked notes
    notes_values = get_notes_values(SAVE_FILE)
    ## sort notes into 'boxes' based on value
    sorted_notes, notes_values = sort_notes(notes, notes_values)
    ## print number of notes in each box
    i=0
    for box in sorted_notes:
        print(f"{i}: {len(box)}")
        i+=1
    ##
    input()
    ## create list of notes for session
    session_notes = create_session(NOTES_PER_BOX, sorted_notes)

    completed = 0

    for name in session_notes:
        path = notes[name].path
        localpath = notes[name].localpath
        if (name).find(".excalidraw"):
            next
        with open(path) as f:
            content = f.read()
        if check_note(content):
            os.system('cls')
            ## print title and header
            print(localpath)
            print("#"*(completed+1), "~"*(len(session_notes)-completed+1), sep="")
            print(f"{completed+1}/{len(session_notes)}")
            print(name)
            if input()=="x":
                break
            ## print content
            print("obsidian://open?vault=Notes&file="+localpath.replace(" ", "%20"))
            print("------------\n"+content+"\n------------")
            ## if needed open matplot for LaTeX
            if(content.find("$")!=-1):
                plt.plot()
                plt.axis('off')
                plt.text(-0.07, 0,'%s'%content.replace("$$", "$"), size=10)
                plt.show()
            ## get outcome
            temp_notes_values=None
            while not temp_notes_values:
                temp_notes_values = get_outcome(notes_values, name)
            notes_values = temp_notes_values
            ## 
            completed+=1
        else:
            # not a valid note
            notes_values[name] = 10 # 10 denotes a non-revision note (ie #index)

    save_notes_values(SAVE_FILE, notes_values)
    os.system('cls')
    input("session saved, press enter to exit")