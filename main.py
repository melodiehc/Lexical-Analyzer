from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

# Initialize the main application window
compiler = Tk()
compiler.title('Lexical Analyzer')
file_path = ''


def set_file_path(path):
    global file_path
    file_path = path


def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    if path:  # Check if a file was selected
        with open(path, 'r') as file:
            code = file.read()
            editor.delete('1.0', END)
            editor.insert('1.0', code)
            set_file_path(path)


def save_as():
    global file_path
    path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    if path:  # Check if a file path was provided
        with open(path, 'w') as file:
            code = editor.get('1.0', END)
            file.write(code)
            set_file_path(path)


def run():
    global file_path
    if file_path == '':
        save_prompt = Toplevel()
        save_prompt.title("Save Required")
        text = Label(save_prompt, text='Please save your code before running.')
        text.pack()
        return
    try:
        command = f'python "{file_path}"'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()

        # Clear previous output
        code_output.delete('1.0', END)

        # Insert new output
        code_output.insert('1.0', output.decode())
        code_output.insert('1.0', error.decode())
    except Exception as e:
        code_output.delete('1.0', END)
        code_output.insert('1.0', f"Error: {str(e)}")


# Create menu bar
menu_bar = Menu(compiler)

# File menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=compiler.quit)
menu_bar.add_cascade(label='File', menu=file_menu)

# Run menu
run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)

# Configure the menu
compiler.config(menu=menu_bar)

# Editor for code input
editor = Text()
editor.pack(fill=BOTH, expand=True)

# Output display
code_output = Text(height=10)
code_output.pack(fill=BOTH, expand=True)

# Start the Tkinter main loop
compiler.mainloop()
