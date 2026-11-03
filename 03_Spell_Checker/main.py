import tkinter as tk
from tkinter import messagebox
import re

# A small built-in starter vocabulary. Add more words to this set as needed.
WORDS = set("""
a about above accept across act action actually add after again against age ago air all
allow almost alone along already also always am an and animal another answer any appear
are around as ask at away back be because become been before begin best better between big
book both boy bring build but by call came can change check child city class close code come
computer could country course create day decide different do document down each early easy
education end enough even every example eye face fact family far fast feel few find first
follow food for form from full game get give go good great group grow had hand happen happy
has have he head help her here high him his home house how idea if important in include into
is it its just keep kind know language large last later learn leave left let life like line
list little live long look made make man many may me mean more most move much must my name
need never new next night no not now number of off often old on once one only open or other
our out over own part people place play point problem program project public put question
read real right run said same say school science see seem set she should show small so some
something sound spell start state still story study such take tell text than that the their
them then there these they thing think this those through time to together too try turn two
under understand up use user very want was way we well were what when where which while who
why will with word work world would write year you your python file handling data structure
snake ladder contact spell checker student grade management system analytics dictionary
algorithm function variable loop condition string integer list tuple set dictionary class
object method exception error input output search sort save delete update phone email address
student marks subject average grade roll random dice player board winner spelling mistake
correct suggestion frequency distance text passage word count character line
""".split())

def levenshtein(a, b):
    """Return the minimum edits needed to change word a into word b."""
    previous = list(range(len(b) + 1))
    for i, char_a in enumerate(a, start=1):
        current = [i]
        for j, char_b in enumerate(b, start=1):
            insert_cost = current[j - 1] + 1
            delete_cost = previous[j] + 1
            replace_cost = previous[j - 1] + (char_a != char_b)
            current.append(min(insert_cost, delete_cost, replace_cost))
        previous = current
    return previous[-1]

def check_text():
    text = input_box.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Empty text", "Enter or paste some text first.")
        return
    tokens = re.findall(r"[A-Za-z']+", text)
    unknown = []
    for word in tokens:
        if word.lower() not in WORDS and word.lower() not in [x.lower() for x in unknown]:
            unknown.append(word)
    output.delete("1.0", tk.END)
    if not unknown:
        output.insert(tk.END, "No possible spelling mistakes found in the built-in vocabulary.")
        return
    output.insert(tk.END, f"Possible spelling mistakes ({len(unknown)}):\n\n")
    for word in unknown:
        lower = word.lower()
        candidates = sorted(WORDS, key=lambda candidate: levenshtein(lower, candidate))
        best = [candidate for candidate in candidates
                if levenshtein(lower, candidate) <= 2][:3]
        suggestion = ", ".join(best) if best else "No close suggestion found"
        output.insert(tk.END, f"• {word}  →  {suggestion}\n")

def clear_all():
    input_box.delete("1.0", tk.END)
    output.delete("1.0", tk.END)

root = tk.Tk()
root.title("Spell Checker")
root.geometry("760x620")
root.configure(bg="#f4f0ff")

tk.Label(root, text="Spell Checker App", font=("Arial", 22, "bold"),
         bg="#f4f0ff", fg="#51427c").pack(pady=12)
tk.Label(root, text="Enter a passage. The app checks words against its built-in vocabulary.",
         bg="#f4f0ff").pack()
input_box = tk.Text(root, height=9, width=82, font=("Arial", 11), wrap="word")
input_box.pack(padx=15, pady=12)
buttons = tk.Frame(root, bg="#f4f0ff")
buttons.pack()
tk.Button(buttons, text="Check Spelling", command=check_text, bg="#8875c7",
          fg="white", padx=15, pady=7).pack(side="left", padx=6)
tk.Button(buttons, text="Clear", command=clear_all, padx=15, pady=7).pack(side="left", padx=6)
tk.Label(root, text="Results and suggestions", font=("Arial", 12, "bold"),
         bg="#f4f0ff").pack(pady=(14, 4))
output = tk.Text(root, height=13, width=82, font=("Arial", 10), wrap="word")
output.pack(padx=15, pady=5)
root.mainloop()
