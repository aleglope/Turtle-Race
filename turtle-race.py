import turtle
import random
import tkinter as tk
from tkinter import ttk, messagebox


class TurtleRaceGUI:
    def __init__(self):
        # Configuración inicial de la ventana principal
        self.root = tk.Tk()
        self.root.title("¡Carrera de Tortugas Ninja!")
        self.root.geometry("600x700")
        # Centrar la ventana en la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 700) // 2
        self.root.geometry(f"600x700+{x}+{y}")

        # Configuración de estilos inspirados en las Tortugas Ninja
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#2E8B57")
        self.style.configure(
            "TLabel",
            background="#2E8B57",
            font=("Comic Sans MS", 12, "bold"),
            foreground="white",
            anchor="center",
            justify="center",
            padding=10,
        )
        self.style.configure("TButton", font=("Comic Sans MS", 11, "bold"), padding=10)
        self.style.configure(
            "Title.TLabel",
            font=("Comic Sans MS", 20, "bold"),
            foreground="#FFD700",  # Dorado
            background="#2E8B57",
            anchor="center",
            justify="center",
            padding=20,
        )

        # Mapeo de tortugas: nombre visible -> código de color
        self.color_mapping = {
            "Leonardo (Azul)": "#0000CD",
            "Raphael (Rojo)": "#FF0000",
            "Michelangelo (Naranja)": "#FFA500",
            "Donatello (Morado)": "#800080",
            "Splinter (Marrón)": "#8B4513",
        }

        # Diccionario para jugadores (persisten a lo largo de las rondas)
        # Cada entrada tendrá: { "balance": int }
        self.players = {}
        self.players_order = []  # Para mantener el orden de registro

        # Variables para las rondas del juego
        self.total_rounds = 0
        self.current_round = 0

        # Frame principal de la interfaz
        self.main_frame = ttk.Frame(self.root, padding="20", style="TFrame")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.setup_initial_screen()

    def setup_initial_screen(self):
        """Pantalla inicial para definir número de jugadores y partidas."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Título grande y centrado
        title_label = ttk.Label(
            self.main_frame,
            text="¡Cowabunga! Carrera de Tortugas Ninja",
            style="Title.TLabel",
        )
        title_label.grid(row=0, column=0, pady=10)

        # Subtítulo ambientado
        subtitle_label = ttk.Label(
            self.main_frame,
            text="¡Prepárate, Ninja! Selecciona tu equipo y demuestra tu valía en la carrera.",
            wraplength=500,
            justify="center",
        )
        subtitle_label.grid(row=1, column=0, pady=10)

        # Preguntar por el número de jugadores
        question_players = ttk.Label(
            self.main_frame,
            text="¿Cuántos ninjas participarán en la carrera?",
            justify="center",
        )
        question_players.grid(row=2, column=0, pady=5)

        self.num_players_var = tk.StringVar()
        num_players_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.num_players_var,
            width=10,
            justify="center",
        )
        num_players_entry.grid(row=3, column=0, pady=5)

        # Preguntar por el número total de partidas (rondas)
        question_rounds = ttk.Label(
            self.main_frame, text="Número total de partidas:", justify="center"
        )
        question_rounds.grid(row=4, column=0, pady=5)

        self.num_rounds_var = tk.StringVar()
        num_rounds_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.num_rounds_var,
            width=10,
            justify="center",
        )
        num_rounds_entry.grid(row=5, column=0, pady=5)

        start_button = ttk.Button(
            self.main_frame,
            text="Comenzar registro",
            command=self.start_player_registration,
        )
        start_button.grid(row=6, column=0, pady=20)

    def start_player_registration(self):
        """Inicia el proceso de registro de jugadores y define el total de partidas."""
        try:
            num_players = int(self.num_players_var.get())
            num_rounds = int(self.num_rounds_var.get())
            if not (1 <= num_players <= 5):
                messagebox.showerror(
                    "Error", "El número de jugadores debe estar entre 1 y 5"
                )
                return
            if num_rounds < 1:
                messagebox.showerror(
                    "Error", "El número de partidas debe ser al menos 1"
                )
                return

            self.total_rounds = num_rounds
            self.num_players = num_players
            self.current_player_registration = 0

            # Limpiar pantalla para comenzar el registro individual de jugadores
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            self.register_next_player()

        except ValueError:
            messagebox.showerror(
                "Error", "Por favor ingrese números válidos para jugadores y partidas"
            )

    def register_next_player(self):
        """Registra a cada jugador (sólo se pide el nombre)."""
        if self.current_player_registration < self.num_players:
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            title_label = ttk.Label(
                self.main_frame,
                text=f"Registro del Ninja {self.current_player_registration + 1}",
                style="Title.TLabel",
            )
            title_label.grid(row=0, column=0, pady=20)

            form_frame = ttk.Frame(self.main_frame, style="TFrame")
            form_frame.grid(row=1, column=0, pady=20)

            ttk.Label(form_frame, text="Nombre del Ninja:").grid(
                row=0, column=0, pady=5, padx=5
            )
            name_var = tk.StringVar()
            name_entry = ttk.Entry(
                form_frame, textvariable=name_var, width=20, justify="center"
            )
            name_entry.grid(row=0, column=1, pady=5, padx=5)

            ttk.Button(
                self.main_frame,
                text="Registrar Ninja",
                command=lambda: self.register_player(name_var.get()),
            ).grid(row=2, column=0, pady=20)
        else:
            # Iniciar el bucle de partidas
            self.start_game_loop()

    def register_player(self, name):
        """Guarda el jugador con un balance inicial de 500 monedas."""
        if not name:
            messagebox.showerror("Error", "El nombre no puede estar vacío")
            return
        if name in self.players:
            messagebox.showerror("Error", "El nombre ya fue registrado")
            return

        self.players[name] = {"balance": 500}
        self.players_order.append(name)
        self.current_player_registration += 1
        self.register_next_player()

    def start_game_loop(self):
        """Inicia el juego en bucle de rondas."""
        self.current_round = 0
        self.play_next_round()

    def play_next_round(self):
        """
        Comprueba si se deben jugar más rondas: se continúa si
          - Quedan rondas por jugar, y
          - Existe al menos un jugador con balance positivo.
        """
        active_players = [
            p for p in self.players_order if self.players[p]["balance"] > 0
        ]
        if self.current_round < self.total_rounds and active_players:
            self.current_round += 1
            messagebox.showinfo(
                "Nueva Ronda",
                f"Comenzando la ronda {self.current_round} de {self.total_rounds}",
            )
            self.setup_round_betting(active_players)
        else:
            self.show_final_results()

    def setup_round_betting(self, active_players):
        """
        Prepara la apuesta para la ronda:
          - Se reinician las tortugas disponibles para la selección.
          - Se recorren los jugadores activos uno a uno para que ingresen su apuesta y elijan su tortuga.
        """
        self.available_turtles_round = list(self.color_mapping.keys())
        self.active_players_round = active_players
        self.round_player_index = 0
        self.current_round_bets = (
            {}
        )  # { jugador: { "bet": tortuga, "bet_amount": int } }
        self.register_next_round_bet()

    def register_next_round_bet(self):
        """Recolecta la apuesta del siguiente jugador activo para esta ronda."""
        if self.round_player_index < len(self.active_players_round):
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            player_name = self.active_players_round[self.round_player_index]
            balance = self.players[player_name]["balance"]

            title_label = ttk.Label(
                self.main_frame,
                text=f"Apuesta del Ninja: {player_name}",
                style="Title.TLabel",
            )
            title_label.grid(row=0, column=0, pady=20)

            info_label = ttk.Label(
                self.main_frame,
                text=f"Balance actual: {balance} monedas",
                justify="center",
            )
            info_label.grid(row=1, column=0, pady=10)

            form_frame = ttk.Frame(self.main_frame, style="TFrame")
            form_frame.grid(row=2, column=0, pady=20)

            # Selección de tortuga (se muestran sólo las disponibles para esta ronda)
            ttk.Label(form_frame, text="Elige tu Tortuga:").grid(
                row=0, column=0, pady=5, padx=5
            )
            turtle_var = tk.StringVar()
            turtle_combo = ttk.Combobox(
                form_frame,
                textvariable=turtle_var,
                width=20,
                state="readonly",
                justify="center",
            )
            turtle_combo["values"] = self.available_turtles_round
            turtle_combo.grid(row=0, column=1, pady=5, padx=5)

            # Monto de la apuesta
            ttk.Label(form_frame, text="Cantidad a apostar:").grid(
                row=1, column=0, pady=5, padx=5
            )
            bet_var = tk.StringVar()
            bet_entry = ttk.Entry(
                form_frame, textvariable=bet_var, width=20, justify="center"
            )
            bet_entry.grid(row=1, column=1, pady=5, padx=5)

            ttk.Button(
                self.main_frame,
                text="Registrar Apuesta",
                command=lambda: self.register_player_bet(
                    player_name, turtle_var.get(), bet_var.get()
                ),
            ).grid(row=3, column=0, pady=20)
        else:
            # Una vez recolectadas todas las apuestas, se inicia la carrera de la ronda
            self.start_round_race()

    def register_player_bet(self, player_name, turtle_choice, bet_amount):
        """Valida y registra la apuesta de un jugador para la ronda actual."""
        if not turtle_choice or not bet_amount:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
        try:
            bet = int(bet_amount)
            if bet <= 0:
                messagebox.showerror("Error", "La apuesta debe ser mayor a 0")
                return
            if bet > self.players[player_name]["balance"]:
                messagebox.showerror(
                    "Error",
                    f"La apuesta no puede superar tu balance actual de {self.players[player_name]['balance']} monedas",
                )
                return
        except ValueError:
            messagebox.showerror("Error", "La apuesta debe ser un número válido")
            return

        if turtle_choice not in self.available_turtles_round:
            messagebox.showerror("Error", "Tortuga no disponible o ya elegida")
            return

        # Se guarda la apuesta del jugador
        self.current_round_bets[player_name] = {"bet": turtle_choice, "bet_amount": bet}
        # Se elimina la tortuga elegida de las disponibles para evitar duplicados en la misma ronda
        self.available_turtles_round.remove(turtle_choice)
        self.round_player_index += 1
        self.register_next_round_bet()

    def start_round_race(self):
        """Ejecuta la carrera de tortugas de la ronda, actualiza balances y muestra los resultados."""
        # Ocultar la ventana principal mientras se ejecuta la carrera con turtle
        self.root.withdraw()

        # Crear (o reutilizar) la pantalla de turtle y limpiarla de dibujos previos
        screen = turtle.Screen()
        screen.clearscreen()  # Limpia la pantalla sin cerrar la ventana
        screen.bgcolor("#2E8B57")
        screen.title(f"Ronda {self.current_round} - Carrera de Tortugas Ninja")
        screen.setup(width=800, height=600)

        # Dibujar la línea de meta
        finish_line = turtle.Turtle()
        finish_line.hideturtle()
        finish_line.penup()
        finish_line.goto(screen.window_width() / 2 - 40, 150)
        finish_line.pendown()
        finish_line.right(90)
        finish_line.pensize(3)
        finish_line.color("white")
        finish_line.forward(300)

        # Crear las tortugas participantes según las apuestas de la ronda
        race_turtles = []
        spacing = 300 / (len(self.current_round_bets) + 1)
        starting_x = -screen.window_width() / 2 + 40
        for i, (player_name, bet_info) in enumerate(self.current_round_bets.items()):
            turtle_name = bet_info["bet"]
            turtle_color = self.color_mapping[turtle_name]
            racer = turtle.Turtle(shape="turtle")
            racer.color(turtle_color)
            racer.shapesize(2, 2)
            racer.penup()
            y_pos = 100 - (i * spacing)
            racer.goto(starting_x, y_pos)
            race_turtles.append((turtle_name, racer))

        # Carrera: mover cada tortuga aleatoriamente hasta cruzar la meta
        winner_turtle_name = None
        while not winner_turtle_name:
            for t_name, racer in race_turtles:
                racer.forward(random.randint(1, 10))
                if racer.xcor() >= screen.window_width() / 2 - 40:
                    winner_turtle_name = t_name
                    break

        # Actualizar resultados y balances
        results = f"Resultados de la Ronda {self.current_round}:\n\n"
        results += f"🏆 ¡{winner_turtle_name} ha ganado la carrera! 🏆\n\n"
        for player_name, bet_info in self.current_round_bets.items():
            bet_amount = bet_info["bet_amount"]
            chosen_turtle = bet_info["bet"]
            if chosen_turtle == winner_turtle_name:
                self.players[player_name]["balance"] += bet_amount
                results += (
                    f"¡{player_name} apostó a {winner_turtle_name} y ganó {bet_amount} monedas! "
                    f"Nuevo balance: {self.players[player_name]['balance']}\n"
                )
            else:
                self.players[player_name]["balance"] -= bet_amount
                results += (
                    f"{player_name} apostó a {chosen_turtle} y perdió {bet_amount} monedas. "
                    f"Nuevo balance: {self.players[player_name]['balance']}\n"
                )

        messagebox.showinfo("Fin de la Ronda", results)

        # En lugar de cerrar la ventana con screen.bye(), se limpia la pantalla para poder reutilizarla
        screen.clear()
        self.root.deiconify()
        self.play_next_round()

    def show_final_results(self):
        """Muestra los resultados finales y cierra la aplicación."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        final_results = "Resultados Finales:\n\n"
        for player_name in self.players_order:
            balance = self.players[player_name]["balance"]
            final_results += f"{player_name}: {balance} monedas\n"
        messagebox.showinfo("Juego Terminado", final_results)
        self.root.destroy()


def main():
    app = TurtleRaceGUI()
    app.root.mainloop()


if __name__ == "__main__":
    main()
