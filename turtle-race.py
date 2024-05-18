import turtle
import random

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

# Mapeo de colores del español al inglés
color_mapping = {
    "roja": "red",
    "verde": "green",
    "azul": "blue",
    "naranja": "orange",
    "morada": "purple",
}

# Inicialización de los balances de los jugadores y la lista de colores disponibles
players = {}
available_colors = list(color_mapping.values())


def place_bet(player_name, available_colors):
    """Función para realizar una apuesta para un jugador específico."""
    print(f"{player_name}, tienes {players[player_name]['balance']} monedas.")

    # Si solo queda un color, se asigna automáticamente al último jugador.
    if (
        len(available_colors) == 1
        and len(players) - sum(1 for p in players.values() if p["bet"]) == 1
    ):
        chosen_color = available_colors.pop()
        print(
            f"Solo queda la tortuga {chosen_color}. {player_name} apostará por ella automáticamente."
        )
        players[player_name]["bet"] = chosen_color
        players[player_name]["balance"] -= 100
        return chosen_color

    # Permitir al jugador elegir un color de tortuga si hay más de una opción.
    while True:
        chosen_color_key = (
            input(
                f"{player_name}, elige una tortuga ({', '.join(color_mapping.keys())}): "
            )
            .strip()
            .lower()
        )
        if (
            chosen_color_key in color_mapping
            and color_mapping[chosen_color_key] in available_colors
        ):
            chosen_color = color_mapping[chosen_color_key]
            players[player_name]["bet"] = chosen_color
            players[player_name]["balance"] -= 100
            available_colors.remove(chosen_color)
            return chosen_color
        else:
            print("No es un color válido o ya ha sido elegido. Intenta de nuevo.")


# Solicitar el número de jugadores y tomar las apuestas
num_players = int(input("¿Cuántos jugadores participarán? "))

for i in range(num_players):
    player_name = input(f"Nombre del jugador {i + 1}: ")
    players[player_name] = {"balance": 500, "bet": None}
    place_bet(player_name, available_colors)

# Configurar la ventana
screen = turtle.Screen()
screen.title("Carrera de Tortugas")

# Crear las tortugas
turtles = []
starting_pos = -screen.window_width() / 2 + 20
for i, color in enumerate(color_mapping.values()):
    new_turtle = turtle.Turtle(shape="turtle")
    new_turtle.color(color)
    new_turtle.penup()
    new_turtle.goto(starting_pos, 100 - i * 50)
    turtles.append(new_turtle)


# Función para mover las tortugas
def move_turtles():
    for t in turtles:
        t.forward(random.randint(1, 10))


# Carrera
winner = None
while winner is None:
    move_turtles()
    for t in turtles:
        if t.xcor() >= screen.window_width() / 2 - 20:
            winner = t.color()[0]
            break

# Actualizar el balance de cada jugador basado en el resultado
bet_amount = 100  # La cantidad que se apuesta
for player_name, player_info in players.items():
    if player_info["bet"] == winner:
        print(f"Felicidades, {player_name}, tu tortuga {winner} ha ganado!")
        player_info["balance"] += bet_amount * 5  # Pago 5:1
    else:
        print(f"Lo siento, {player_name}, tu tortuga no ha ganado.")
    print(f"{player_name}, tu nuevo balance es {player_info['balance']} monedas.")

# Cerrar la ventana al hacer clic
screen.exitonclick()
