import turtle
import random
import tkinter as tk
from tkinter import ttk, messagebox

"""
    The Python code simulates a turtle race game where players place bets on turtle colors and the
    program determines the winner, updating player balances accordingly.
    
    :param player_name: player_name is a variable that stores the name of a player participating in a
    turtle racing game
    :param available_colors: The `available_colors` variable is a list that contains the colors
    available for the players to choose from in the turtle race game. Initially, it includes all the
    colors in English ("red", "green", "blue", "orange", "purple"). As players place their bets on
    specific colors, those
    :return: The code provided is a Python program that simulates a turtle race game where players can
    place bets on different colored turtles. The program initializes player balances, allows players to
    place bets on turtle colors, creates a race track with turtle graphics, moves the turtles randomly,
    determines the winner turtle, updates player balances based on the race outcome, and displays the
    results.
    """


class TurtleRaceGUI:
    def __init__(self):
        # Configuración inicial
        self.root = tk.Tk()
        self.root.title("¡Carrera de Tortugas Ninja!")
        self.root.geometry("600x700")

        # Centrar la ventana en la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 700) // 2
        self.root.geometry(f"600x700+{x}+{y}")

        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure(
            "TFrame", background="#2E8B57"
        )  # Verde oscuro para el fondo
        self.style.configure(
            "TLabel",
            background="#2E8B57",
            font=("Comic Sans MS", 12),
            foreground="white",
        )
        self.style.configure("TButton", font=("Comic Sans MS", 11), padding=10)
        self.style.configure(
            "Title.TLabel",
            font=("Comic Sans MS", 18, "bold"),
            foreground="#FFD700",  # Dorado para el título
            padding=20,
            background="#2E8B57",
        )

        # Configurar colores
        self.root.configure(bg="#2E8B57")

        self.color_mapping = {
            "Leonardo (Azul)": "#0000CD",  # Azul
            "Raphael (Rojo)": "#FF0000",  # Rojo
            "Michelangelo (Naranja)": "#FFA500",  # Naranja
            "Donatello (Morado)": "#800080",  # Morado
            "Splinter (Marrón)": "#8B4513",  # Marrón
        }

        self.players = {}
        self.available_colors = list(self.color_mapping.values())

        # Crear el frame principal con padding y borde
        self.main_frame = ttk.Frame(self.root, padding="20", style="TFrame")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        self.setup_initial_screen()

    def setup_initial_screen(self):
        """Configurar la pantalla inicial para número de jugadores"""
        # Título
        title_label = ttk.Label(
            self.main_frame,
            text="¡Cowabunga! Carrera de Tortugas Ninja",
            style="Title.TLabel",
        )
        title_label.grid(row=0, column=0, pady=20)

        # Instrucciones
        ttk.Label(
            self.main_frame,
            text="¿Cuántos ninjas participarán en la carrera?",
            wraplength=400,
            justify="center",
        ).grid(row=1, column=0, pady=10)

        # Frame para entrada y botón
        entry_frame = ttk.Frame(self.main_frame)
        entry_frame.grid(row=2, column=0, pady=20)

        self.num_players_var = tk.StringVar()
        num_players_entry = ttk.Entry(
            entry_frame, textvariable=self.num_players_var, width=10, justify="center"
        )
        num_players_entry.grid(row=0, column=0, padx=10)

        start_button = ttk.Button(
            entry_frame, text="Comenzar", command=self.start_player_registration
        )
        start_button.grid(row=0, column=1, padx=10)

    def start_player_registration(self):
        """Iniciar el registro de jugadores"""
        try:
            num_players = int(self.num_players_var.get())
            if num_players < 1 or num_players > 5:
                messagebox.showerror(
                    "Error", "El número de jugadores debe estar entre 1 y 5"
                )
                return

            # Limpiar la pantalla
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            self.current_player = 0
            self.num_players = num_players
            self.register_next_player()

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número válido")

    def register_next_player(self):
        """Registrar el siguiente jugador"""
        if self.current_player < self.num_players:
            # Título
            ttk.Label(
                self.main_frame,
                text=f"Registro del Ninja {self.current_player + 1}",
                style="Title.TLabel",
            ).grid(row=0, column=0, pady=20)

            # Frame para el formulario
            form_frame = ttk.Frame(self.main_frame)
            form_frame.grid(row=1, column=0, pady=20)

            # Nombre
            ttk.Label(form_frame, text="Nombre del Ninja:").grid(
                row=0, column=0, pady=5, padx=5
            )
            name_var = tk.StringVar()
            name_entry = ttk.Entry(form_frame, textvariable=name_var, width=20)
            name_entry.grid(row=0, column=1, pady=5, padx=5)

            # Color
            ttk.Label(form_frame, text="Elige tu Tortuga:").grid(
                row=1, column=0, pady=5, padx=5
            )
            color_var = tk.StringVar()
            color_combo = ttk.Combobox(
                form_frame, textvariable=color_var, width=17, state="readonly"
            )
            color_combo["values"] = [
                k for k, v in self.color_mapping.items() if v in self.available_colors
            ]
            color_combo.grid(row=1, column=1, pady=5, padx=5)

            # Apuesta
            ttk.Label(form_frame, text="Cantidad a apostar:").grid(
                row=2, column=0, pady=5, padx=5
            )
            bet_var = tk.StringVar()
            bet_entry = ttk.Entry(form_frame, textvariable=bet_var, width=20)
            bet_entry.grid(row=2, column=1, pady=5, padx=5)

            # Mostrar balance inicial
            ttk.Label(
                form_frame, text="Balance inicial: 500 monedas", foreground="#FFD700"
            ).grid(row=3, column=0, columnspan=2, pady=10)

            ttk.Button(
                self.main_frame,
                text="¡Unirse a la carrera!",
                command=lambda: self.register_player(
                    name_var.get(), color_var.get(), bet_var.get()
                ),
            ).grid(row=2, column=0, pady=20)
        else:
            self.start_race()

    def register_player(self, name, color_esp, bet_amount):
        """Registrar un jugador"""
        if not name or not color_esp or not bet_amount:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return

        try:
            bet = int(bet_amount)
            if bet <= 0:
                messagebox.showerror("Error", "La apuesta debe ser mayor a 0")
                return
            if bet > 500:
                messagebox.showerror(
                    "Error", "La apuesta no puede superar tu balance inicial de 500"
                )
                return
        except ValueError:
            messagebox.showerror("Error", "La apuesta debe ser un número válido")
            return

        color = self.color_mapping[color_esp]
        if color not in self.available_colors:
            messagebox.showerror("Error", "Tortuga no disponible")
            return

        self.players[name] = {"balance": 500, "bet": color, "bet_amount": bet}
        self.available_colors.remove(color)
        self.current_player += 1

        # Limpiar la pantalla y continuar con el siguiente jugador
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.register_next_player()

    def start_race(self):
        """Iniciar la carrera de tortugas"""
        self.root.withdraw()

        # Configurar pantalla de turtle
        screen = turtle.Screen()
        screen.title("¡Carrera de Tortugas Ninja!")
        screen.bgcolor("#2E8B57")  # Fondo verde

        # Dibujar línea de meta
        finish_line = turtle.Turtle()
        finish_line.hideturtle()
        finish_line.penup()
        finish_line.goto(screen.window_width() / 2 - 20, 150)
        finish_line.pendown()
        finish_line.right(90)
        finish_line.pensize(3)
        finish_line.color("white")
        finish_line.forward(300)

        # Obtener solo las tortugas seleccionadas por los jugadores
        selected_colors = set(
            player_info["bet"] for player_info in self.players.values()
        )

        # Crear las tortugas seleccionadas
        turtles = []
        starting_pos = -screen.window_width() / 2 + 20
        spacing = 300 / (
            len(selected_colors) + 1
        )  # Distribuir el espacio equitativamente

        for i, color in enumerate(selected_colors):
            new_turtle = turtle.Turtle(shape="turtle")
            new_turtle.color(color)
            new_turtle.shapesize(2, 2)  # Hacer las tortugas más grandes
            new_turtle.penup()
            # Ajustar la posición vertical según el número de tortugas
            y_pos = 100 - (i * spacing)
            new_turtle.goto(starting_pos, y_pos)
            turtles.append(new_turtle)

        # Carrera
        winner = None
        while winner is None:
            for t in turtles:
                t.forward(random.randint(1, 10))
                if t.xcor() >= screen.window_width() / 2 - 20:
                    winner = t.color()[0]
                    break

        # Mostrar resultados
        results = "Resultados de la Carrera:\n\n"
        for player_name, player_info in self.players.items():
            if player_info["bet"] == winner:
                winnings = player_info["bet_amount"] * 3
                player_info["balance"] += winnings
                results += f"¡{player_name} ha ganado {winnings} monedas!\n"
                results += f"Balance final: {player_info['balance']} monedas\n\n"
            else:
                player_info["balance"] -= player_info["bet_amount"]
                results += (
                    f"{player_name} ha perdido {player_info['bet_amount']} monedas\n"
                )
                results += f"Balance final: {player_info['balance']} monedas\n\n"

        messagebox.showinfo("¡Fin de la Carrera!", results)
        screen.bye()
        self.root.quit()


def main():
    app = TurtleRaceGUI()
    app.root.mainloop()


if __name__ == "__main__":
    main()
