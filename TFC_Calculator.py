import tkinter as tk
from itertools import product

class MetalCombinerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Disable maximize button
        self.resizable(0, 0)

        # Main Layout
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(padx=10, pady=10)

        # Input Section
        self.rich_input = self.create_entry("Rich metal pieces", 0)
        self.normal_input = self.create_entry("Normal metal pieces", 1)
        self.poor_input = self.create_entry("Poor metal pieces", 2)
        self.small_input = self.create_entry("Small metal pieces", 3)

        submit_button = tk.Button(self.main_frame, text="Find Combinations", command=self.show_combinations)
        submit_button.grid(row=4, column=0, pady=10)

        # Output Section
        self.output_frame = tk.Frame(self.main_frame)
        self.output_frame.grid(row=5, column=0)

    def create_entry(self, hint_text, row):
        label = tk.Label(self.main_frame, text=hint_text)
        label.grid(row=row, column=0, sticky="w", pady=5)
        entry = tk.Entry(self.main_frame)
        entry.grid(row=row, column=1, pady=5)
        return entry

    def show_combinations(self):
        rich = int(self.rich_input.get() or 0)
        normal = int(self.normal_input.get() or 0)
        poor = int(self.poor_input.get() or 0)
        small = int(self.small_input.get() or 0)

        combinations = self.find_combinations(rich, normal, poor, small)
        combinations.sort(key=lambda x: sum(x), reverse=True)
        used_combinations = self.use_combinations(rich, normal, poor, small, combinations)

        # Clear previous results
        for widget in self.output_frame.winfo_children():
            widget.destroy()

        # Add table headers
        headers = ['Rich', 'Normal', 'Poor', 'Small']
        for col, header in enumerate(headers):
            label = tk.Label(self.output_frame, text=header, font=("Arial", 10, "bold"))
            label.grid(row=0, column=col)

        # Add combinations to the table
        if used_combinations:
            for row, combo in enumerate(used_combinations, start=1):
                for col, value in enumerate(combo):
                    label = tk.Label(self.output_frame, text=str(value))
                    label.grid(row=row, column=col)
        else:
            additional_pieces = self.recommend_additional_pieces(rich, normal, poor, small)
            if additional_pieces:
                label = tk.Label(self.output_frame, text="Additional pieces needed:")
                label.grid(row=1, column=0, columnspan=4)
                headers = ['Rich', 'Normal', 'Poor', 'Small']
                for col, header in enumerate(headers, start=0):
                    label = tk.Label(self.output_frame, text=header, font=("Arial", 10, "bold"))
                    label.grid(row=2, column=col)
                for col, piece in enumerate(additional_pieces, start=0):
                    label = tk.Label(self.output_frame, text=str(piece))
                    label.grid(row=3, column=col)
            else:
                label = tk.Label(self.output_frame, text="No possible combinations.")
                label.grid(row=1, column=0, columnspan=4)

    def find_combinations(self, rich, normal, poor, small):
        combinations = product(range(25), repeat=4)
        valid_combinations = []

        for combo in combinations:
            r, n, p, s = combo
            total_volume = r*35 + n*25 + p*15 + s*10
            total_pieces = r + n + p + s

            if total_volume % 100 == 0 and total_volume != 0 and total_pieces <= 24:
                valid_combinations.append(combo)

        return valid_combinations

    def use_combinations(self, rich, normal, poor, small, combinations):
        used_combinations = []

        for combo in combinations:
            r, n, p, s = combo
            if r <= rich and n <= normal and p <= poor and s <= small:
                used_combinations.append(combo)
                rich -= r
                normal -= n
                poor -= p
                small -= s

        return used_combinations

    def recommend_additional_pieces(self, rich, normal, poor, small):
        best_combo = None
        min_pieces_needed = float('inf')

        for r in range(25):
            for n in range(25):
                for p in range(25):
                    for s in range(25):
                        total_volume = (rich + r)*35 + (normal + n)*25 + (poor + p)*15 + (small + s)*10
                        total_pieces = r + n + p + s

                        if total_volume % 100 == 0 and total_volume != 0 and total_pieces <= 24 and total_pieces < min_pieces_needed:
                            best_combo = (r, n, p, s)
                            min_pieces_needed = total_pieces

        return best_combo

if __name__ == '__main__':
    app = MetalCombinerApp()
    app.title("Metal Combiner")
    app.mainloop()