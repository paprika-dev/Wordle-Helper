import tkinter as tk
import os


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('WORDLE')

        # create widgets and variables
        tags = ['wrong letters :', 'right letters :'] + ['possible loc of " " :' for _ in range(3)]
        for index, tag in enumerate(tags):
            setattr(self, f'l{index}', tk.Label(self, text=tag))
            setattr(self, f'e{index}', tk.Entry(self))
            setattr(self, f'var{index}', tk.StringVar())

        self.count = tk.Label(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical")
        self.box = tk.Listbox(self, yscrollcommand=self.scrollbar.set)

        # styling and configuration
        self.labels = [getattr(self, label) for label in ['l0', 'l1', 'l2', 'l3', 'l4']]
        self.entries = [getattr(self, entry) for entry in ['e0', 'e1', 'e2', 'e3', 'e4']]
        self.variables = [getattr(self, variable) for variable in ['var0', 'var1', 'var2', 'var3', 'var4']]

        for index, label in enumerate(self.labels):
            label.grid(row=index, **{'column': 0, 'pady': 5, 'padx': 5, 'sticky': 'w'})

        for index, entry in enumerate(self.entries):
            entry.grid(row=index, column=1)
            entry['textvariable'] = self.variables[index]

        for variable in self.variables:
            variable.trace('w', self.search)

        self.count.grid(row=7, column=2, sticky='wn', pady=5, padx=20)
        self.scrollbar.grid(row=0, column=3, rowspan=7, sticky='ns', pady=5)
        self.box.grid(row=0, column=2, rowspan=7, sticky='ns', pady=5, padx=20)

    def display(self, data, *args):
        self.box.delete(0, 'end')
        self.count['text'] = '# possible words: '
        for item in data:
            self.box.insert('end', item)
        self.count['text'] += str(len(data))

    def update_label(self, rl0, rl1, rl2):
        self.l2['text'] = f'ploc of "{rl0}" :'
        self.l3['text'] = f'ploc of "{rl1}" :'
        self.l4['text'] = f'ploc of "{rl2}" :'

    def search(self, *args):
        wrong_letters = self.var0.get()
        right_letters = self.var1.get()
        ploc_rl0 = self.var2.get()
        ploc_rl1 = self.var3.get()
        ploc_rl2 = self.var4.get()

        rl0 = right_letters[0] if len(right_letters) >= 1 else ' '
        rl1 = right_letters[1] if len(right_letters) >= 2 else ' '
        rl2 = right_letters[2] if len(right_letters) >= 3 else ' '

        self.update_label(rl0, rl1, rl2)

        def check(word):
            # return if the word contains wrong letter
            for wl in wrong_letters:
                if wl in word:
                    return

            def check_loc(rl, ploc):
                if rl == ' ' or ploc == '':
                    return True

                """return word if the word contains rl, and only at possible locations"""
                indices = [str(i) for i, x in enumerate(word) if x == rl]
                if indices != [] and all([index in ploc for index in indices]):
                    return True

            if all([rl in word for rl in right_letters]):
                if check_loc(rl0, ploc_rl0) and check_loc(rl1, ploc_rl1) and check_loc(rl2, ploc_rl2):
                    return word
                return

        if right_letters == '' and wrong_letters == '':
            data = word_list
        else:
            data = []
            for w in word_list:
                poss_word = check(w)
                if poss_word:
                    data.append(poss_word)

        self.display(data)


if __name__ == "__main__":
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, "wordle.txt")
    with open(path, 'r') as f:
        word_list = f.read().split()
    app = App()
    app.display(word_list)

    app.mainloop()
