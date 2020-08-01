from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from util import Queue, Stack

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "projects/adventure/maps/test_line.txt"
# map_file = "projects/adventure/maps/test_cross.txt"
# map_file = "projects/adventure/maps/test_loop.txt"
# map_file = "projects/adventure/maps/test_loop_fork.txt"
map_file = "projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


graph = {}

# create dictionary for each room when visited


def add_room_to_graph():
    room = {}
    for exit in player.current_room.get_exits():
        room[exit] = "?"
        graph[player.current_room.id] = room

# Algorithm to find random exit that hasn't been explored yet


def find_unvisited_path():
    # unexplored = []
    direction = None
    for exit in player.current_room.get_exits():
        if graph[player.current_room.id][exit] == "?":
            # unexplored.append(exit)
            direction = exit

    # return random.choice(unexplored)
    return direction


def path_to_unvisited_room(starting_room):
    q = Queue()
    q.enqueue([starting_room])
    visited = set()

    while q.size() > 0:
        path = q.dequeue()
        room = path[-1]

        if list(graph[room].values()).count('?') != 0:
            return path
        if room not in visited:
            visited.add(room)

            for next_room in graph[room].values():
                new_path = path.copy()
                new_path.append(next_room)
                q.enqueue(new_path)


opposite_to_direction = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e', }
add_room_to_graph()

while True:
    if list(graph[player.current_room.id].values()).count('?') != 0:
        previous_roomid = player.current_room.id
        available_exit = find_unvisited_path()
        player.travel(available_exit)
        traversal_path.append(available_exit)
        if player.current_room.id not in graph:
            add_room_to_graph()
        graph[previous_roomid][available_exit] = player.current_room.id

        graph[player.current_room.id][opposite_to_direction[available_exit]
                                      ] = previous_roomid

    else:
        path = path_to_unvisited_room(player.current_room.id)
        if not path:
            break
        for room_id in path:
            for direction in graph[player.current_room.id]:
                if graph[player.current_room.id][direction] == room_id:
                    player.travel(direction)
                    traversal_path.append(direction)
                    break


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
