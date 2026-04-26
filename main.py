import random
import os
import time

BLUE ="\033[94m"  # Modrá
WHITE ="\033[97m"  # Bílá
RED = "\033[91m"  # Červená
YELLOW = "\033[93m" #žlutá
CYAN= "\033[96m"    #tyrkysová
BOLD = "\033[1m"   #tučné písmo
RESET= "\033[0m"  #reset
GREEN = '\033[92m'   # Pro tvůj Dashboard
PURPLE = '\033[95m'  # Pro AI Dashboard
GRAY = '\033[90m'    # Pro "Vodu" nebo vedlejší info
NAVY = "\033[38;5;25m"
OLIVE = "\033[38;5;64m"
GOLD  = '\033[38;5;220m'
ORANGE = '\033[38;5;208m'


class Ship:
    """Reprezentuje loď na herním poli"""


    def __init__(self,name,coordinates):
        self.original_coordinates= set(coordinates)
        self.hits_coordinates = set()
        self.name = name

    def take_damage(self,x,y):
        """
        Zaznamenává zásah na dané souřadnici.
        Vrací True při zásahu, jinak False.
        """

        if (x,y) in self.original_coordinates:
            self.hits_coordinates.add((x, y))
            return True

        return False

    def is_sunk(self):
        return len(self.hits_coordinates)==len(self.original_coordinates)


class Board:

    def __init__(self):
        self._size = 20
        self._active_ships_count = 10
        self.ships = []
        self.ship_map= {}
        self.grid = {}
        self.fleet_length = None

        for x in range(self._size):
            for y in range(self._size):
                self.grid[(x, y)] = "~"

    @property
    def active_ships_count(self):
        return self._active_ships_count

    @property
    def size(self):
        return self._size

    def add_ship(self,ship):
        for x, y in ship.original_coordinates:
            if not (0 <= x < self._size and 0 <= y < self._size):
                return False

        for x,y in ship.original_coordinates:
            for dx in range(-1,2):
                for dy in range(-1,2):
                    if (x+dx,y+dy) in self.ship_map:
                        return False

        self.ships.append(ship)
        for (x,y) in ship.original_coordinates:
            self.ship_map[(x,y)] = ship
            self.grid[(x,y)] = "X"
        return True




    def receive_shot(self,x,y):
        check_coordinates = (0 <= x < self._size and 0 <= y < self._size)

        if not check_coordinates:
            return "Invalid"
        if self.grid[(x,y)] in ["W","H"]:
            return "Invalid"

        ship = self.ship_map.get((x, y))

        if ship:
            ship.take_damage(x,y)
            self.grid[(x, y)] = "H"

            if ship.is_sunk():
                self._active_ships_count -=1
                print(f"Loď {ship.name} je potopena!")
                return "Sunk"

            return "Hit"
        else:
            self.grid[(x,y)] = "W"

            return "Water"



    def auto_populate(self):
            for length in self.fleet_length:
                while True:
                    coordinates = []
                    start_x = random.randrange(0,self._size)
                    start_y = random.randrange(0,self._size)
                    direction = random.choice(["V","H"])

                    for i in range(length):
                        if direction == "V":
                            new_coords = (start_x,start_y+i)
                            coordinates.append(new_coords)
                        if direction == "H":
                            new_coords = (start_x+i,start_y)
                            coordinates.append(new_coords)
                    if self.add_ship(Ship("Křižník",coordinates)):
                        break



    def endgame(self):
        return True if self.active_ships_count == 0 else False


    def display(self,hidden = False):



        # Horní řada s čísly
        print("   ", end="")
        for x in range(self._size):
            print(f"{BOLD}{OLIVE}{x + 1:<3}{RESET}", end="")
        print()

        # Vykreslení řádků
        for y in range(self._size):
            letter = chr(65 + y)
            print(f"{BOLD}{OLIVE}{letter:<3}{RESET}", end="")

            for x in range(self._size):
                actual_symbol = self.grid[x, y]

                # Logika schování lodi
                display_symbol = "~" if hidden and actual_symbol == "X" else actual_symbol
                if display_symbol == "~":
                    formatted_text = f"{BLUE}{display_symbol:<3}{RESET}"
                elif display_symbol == "X":
                    formatted_text = f"{WHITE}{display_symbol:<3}{RESET}"
                elif display_symbol == "W":
                    formatted_text = f"{YELLOW}{display_symbol:<3}{RESET}"
                elif display_symbol == "H":
                    formatted_text = f"{RED}{display_symbol:<3}{RESET}"


                print(formatted_text, end="")
            print()




class Player:

    def __init__(self,name):
        self.name = name
        self.board = None
        self.opponent_board = None



    def get_shot(self):
        pass


    def register_shot_result(self,x,y,result):
        pass

class HumanPlayer(Player):


    def __init__(self,name):
        super().__init__(name)

    def get_shot(self):
        while True:
            order = input("Zadej souřadnice (např.B5): ")
            if len(order)<2:
                print("Špatné instrukce. Zkus to znova.")
                continue
            try:
                y = ord(order[0].upper()) - ord("A")
                x = int(order[1:]) -1

                if 0 <= x < self.board.size and 0 <= y < self.board.size:
                    return x,y

            except ValueError:
                print("Špatné instrukce. Zkus to znova.")


class AIPlayer(Player):


    def __init__(self,name):
        super().__init__(name)
        self.target_to_hit= []
        self.shot = set()
        self.current_ship_hits= []


    def get_shot(self):
        target = None

        while self.target_to_hit:
            temp_x, temp_y = self.target_to_hit.pop(0)
            if (temp_x,temp_y) not in self.shot:
                target = (temp_x,temp_y)
                break

        if target is None:
            while True:
                y = random.randrange(0,self.board.size)
                x = random.randrange(0,self.board.size)
                if (x,y) not in self.shot:
                    target = (x,y)
                    break

        final_x, final_y = target
        self.shot.add((final_x,final_y))
        return final_x, final_y

    def register_shot_result(self,x,y,result):
        if result == "Hit":
            self.current_ship_hits.append((x, y))
            if len(self.current_ship_hits) == 1:

                coordinates_to_hit = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
                for (nx,ny) in coordinates_to_hit:
                    if not (0 <= nx < self.board.size and 0 <= ny < self.board.size):
                        continue
                    if (nx,ny) in self.shot:
                        continue

                    if (nx,ny)  in self.target_to_hit:
                        continue

                    if (nx,ny) in self.current_ship_hits:
                        continue


                    self.target_to_hit.append((nx,ny))
            else:
                hit1 = self.current_ship_hits[0]
                hit2 = self.current_ship_hits[1]
                if hit1[0] == hit2[0]:   # Stejné X -> Horizontální loď
                    self.target_to_hit = [a for a in self.target_to_hit if a[0]==hit1[0]]
                    all_y =[a[1] for a in self.current_ship_hits]
                    min_y,max_y = min(all_y), max(all_y)
                    row_x = hit1[0]
                    potential_target = [(row_x,min_y-1),(row_x,max_y+1)]
                    for nx,ny in potential_target:
                        if 0<= nx <self.board.size and 0<=ny<self.board.size:
                            if (nx,ny) not in self.shot and (nx,ny) not in self.target_to_hit:
                                self.target_to_hit.append((nx,ny))

                if hit1[1] == hit2[1]:  # Stejné Y -> Vertikální loď
                    self.target_to_hit = [a for a in self.target_to_hit if a[1] == hit1[1]]
                    all_x = [a[0] for a in self.current_ship_hits]
                    min_x,max_x = min(all_x),max(all_x)
                    row_y = hit1[1]
                    potential_target = [(min_x-1,row_y),(max_x+1,row_y)]
                    for nx,ny in potential_target:
                        if 0<=nx<self.board.size and 0<=ny<self.board.size:
                            if (nx,ny) not in self.shot and (nx,ny) not in self.target_to_hit:
                                self.target_to_hit.append((nx,ny))


        if result == "Sunk":
            for sx, sy in self.current_ship_hits:
                for dx in range(-1,2):
                    for dy in range(-1,2):
                        nx,ny = sx+dx, sy + dy
                        if 0<= nx <self.board.size and 0<= ny <self.board.size:
                            self.shot.add((nx,ny))


            self.target_to_hit.clear()
            self.current_ship_hits.clear()

class BattleShipGame:

    def __init__(self):
        self.common_fleet= [random.randint(2, 7) for _ in range(10)]
        #Bojiště
        self.player_board = Board()
        self.AI_player_board = Board()
        #rozmístíme lodě
        self.player_board.fleet_length=self.common_fleet
        self.player_board.auto_populate()

        self.AI_player_board.fleet_length=self.common_fleet
        self.AI_player_board.auto_populate()

        #Aktivace hráčů
        self.human_player = HumanPlayer("Zrezlá Kotva")
        self.human_player.board = self.player_board
        self.human_player.opponent_board = self.AI_player_board

        self.AI_player = AIPlayer("Stříbrná Sára")
        self.AI_player.board = self.AI_player_board
        self.AI_player.opponent_board= self.player_board

        #první hráč
        self.players = [self.human_player,self.AI_player]
        self.current_player = random.choice(self.players)


    def play(self):
        boat = "🚢  "

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Hraješ za {GREEN}{BOLD}{self.human_player.name}{RESET}, tvůj soupeř je {PURPLE}{BOLD}{self.AI_player.name}{RESET} \n")
            print("-  "*20)
            print(f"{GREEN}Zbývající lodě od {self.human_player.name}{RESET}: {boat*self.player_board.active_ships_count}")
            print(f"{PURPLE}Zbývající lodě od {self.AI_player.name}{RESET} : {boat*self.AI_player_board.active_ships_count}")
            if self.current_player == self.human_player:
                print(f"Hraje: {GREEN}{BOLD}{self.current_player.name}{RESET}")
            else:
                print(f"Hraje: {PURPLE}{BOLD}{self.current_player.name}{RESET}")
            print("-  " * 20)




            print()
            print(f"Mapa {GREEN}{BOLD}{self.human_player.name}{RESET}")
            self.human_player.board.display()
            print("\n\n")
            print(f"Mapa {PURPLE}{BOLD}{self.AI_player.name}{RESET}:")
            self.AI_player_board.display(hidden=True)
            print("\n\n")

            x,y = self.current_player.get_shot()
            if self.current_player == self.AI_player:
                print(f"{PURPLE}{BOLD}{self.current_player.name}{RESET} uvažuje....")
                time.sleep(1)
                letter = chr(65+y)
                number = x+1
                print(f"{PURPLE}{BOLD}{self.current_player.name}{RESET} sřílí na {BOLD}{letter}{number}{RESET}!")
                time.sleep(1)

            result = self.current_player.opponent_board.receive_shot(x,y)
            self.current_player.register_shot_result(x,y,result)

            if result =="Water":
                print(f"{YELLOW}Voda{RESET}, hraje druhý hráč.")
                if self.current_player == self.human_player:
                   self.current_player = self.AI_player
                else:
                    self.current_player = self.human_player
                time.sleep(2.5)

            elif result == "Invalid":
                print("Tady jsi už střílej, zadej jiné souřadnice.")
                time.sleep(2.5)
            elif result in ["Hit","Sunk"]:
                print(f"{RED}Zásah!{RESET}")
                print(f"{ORANGE}Pokračuješ v tahu{RESET}")
                time.sleep(2.5)
                if self.current_player.opponent_board.endgame():
                    print(f"{GOLD}Vyhrál {self.current_player.name}!{RESET}")
                    break



if __name__ == "__main__":
    game = BattleShipGame()
    game.play()