from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from itertools import product

class MetalCombinerApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)

        # Input Section
        input_layout = BoxLayout(orientation='vertical', spacing=10)
        self.rich_input = TextInput(hint_text='Rich metal pieces', input_filter='int', multiline=False)
        self.normal_input = TextInput(hint_text='Normal metal pieces', input_filter='int', multiline=False)
        self.poor_input = TextInput(hint_text='Poor metal pieces', input_filter='int', multiline=False)
        self.small_input = TextInput(hint_text='Small metal pieces', input_filter='int', multiline=False)

        # Bind the on_text_validate event to move to the next input
        self.rich_input.bind(on_text_validate=self.focus_next(self.normal_input))
        self.normal_input.bind(on_text_validate=self.focus_next(self.poor_input))
        self.poor_input.bind(on_text_validate=self.focus_next(self.small_input))
        self.small_input.bind(on_text_validate=self.focus_next(self.rich_input))  # Loops back to the first input

        submit_button = Button(text='Find Combinations')
        submit_button.bind(on_press=self.show_combinations)
        input_layout.add_widget(self.rich_input)
        input_layout.add_widget(self.normal_input)
        input_layout.add_widget(self.poor_input)
        input_layout.add_widget(self.small_input)
        input_layout.add_widget(submit_button)

        # Output Section
        self.output_layout = GridLayout(cols=4, spacing=20, size_hint_y=None, row_default_height=40, row_force_default=True)
        self.output_layout.bind(minimum_height=self.output_layout.setter('height'))

        output_container = BoxLayout(orientation='vertical')
        output_container.add_widget(self.output_layout)
        output_container.add_widget(Widget())  # Spacer

        main_layout.add_widget(input_layout)
        main_layout.add_widget(output_container)

        return main_layout

    def focus_next(self, next_widget):
        def _focus_next(instance):
            next_widget.focus = True
        return _focus_next

    def show_combinations(self, instance):
        rich = int(self.rich_input.text or 0)
        normal = int(self.normal_input.text or 0)
        poor = int(self.poor_input.text or 0)
        small = int(self.small_input.text or 0)

        combinations = self.find_combinations(rich, normal, poor, small)
        combinations.sort(key=lambda x: sum(x), reverse=True)
        used_combinations = self.use_combinations(rich, normal, poor, small, combinations)

        # Clear previous results
        self.output_layout.clear_widgets()

        # Add table headers
        headers = ['Rich', 'Normal', 'Poor', 'Small']
        for header in headers:
            self.output_layout.add_widget(Label(text=header, bold=True))

        # Add combinations to the table
        if used_combinations:
            for combo in used_combinations:
                for value in combo:
                    self.output_layout.add_widget(Label(text=str(value)))
        else:
            additional_pieces = self.recommend_additional_pieces(rich, normal, poor, small)
            if additional_pieces:
                self.output_layout.add_widget(Label(text="Additional pieces needed:"))
                for _ in range(3):  # Fill the remaining columns
                    self.output_layout.add_widget(Label(text=""))
                for piece in additional_pieces:
                    self.output_layout.add_widget(Label(text=str(piece)))
            else:
                self.output_layout.add_widget(Label(text="No possible combinations."))
                for _ in range(3):  # Fill the remaining columns
                    self.output_layout.add_widget(Label(text=""))

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
    MetalCombinerApp().run()