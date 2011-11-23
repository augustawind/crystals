"""world - methods for world generation and manipulation"""

from pyglet.sprite import Sprite
from pyglet.graphics import Batch, OrderedGroup

TILE_WIDTH = 24
TILE_HEIGHT = 24

class Entity(Sprite):
    """A tangible thing. Populates Rooms."""

    def __init__(self, name, walkable, image):
        super(Entity, self).__init__(image)

        self.name = name
        self.walkable = walkable

    def get_name(self):
        return self.name

    def is_walkable(self):
        return self.walkable

class Portal:
    """A set of coordinates that is connected to a Room. When an Entity is
    moved into the coordinates of a portal, it is transported to the connected
    Room by World."""
    
    def __init__(self, x, y, room):
        self.x = x
        self.y = y
        self.room = room
    
    def get_coords(self):
        return self.x, self.y
    
    def get_room(self):
        return self.room
        
class Room:
    """A 3-dimensional grid that contains Entities and Portals to other Rooms.
    Populates a World."""

    def __init__(self, name, width, height, _map=[], portals=[]):
        self.name = name
        self.width = width
        self.height = height
        self.portals = portals

        self.batch = Batch()

        self.entities = {'Character': [], 'Item': [], 'Terrain': []}

        if _map:
            self._map = _map
            self._init_entities()
        else:
            self._map = [[[] for x in width] for y in height]

    def _init_entities(self):
        for y in range(len(self._map)):
            for x in range(len(self._map[y])):
                for entity in self._map[y][x]:
                    self._init_entity(entity, x, y)

    def _init_entity(self, entity, x, y):
        entity.batch = self.batch
        self._update_entity(entity, x, y)
        self.entities[str(entity)].append(entity)

    def _update_entity(self, entity, x, y):
        entity.set_position(x * TILE_WIDTH, y * TILE_HEIGHT)

    def get_terrain(self):
        return self.entities['Terrain']

    def get_items(self):
        return self.entities['Item']

    def get_characters(self):
        return self.entities['Character']

    def get_coords(self, entity):
        x, y = entity.position
        return x / TILE_WIDTH, y / TILE_HEIGHT

    def is_walkable(self, x, y):
        return all([e.is_walkable() for e in self._map[y][x]])

    def add_portals(self, *portals):
        self.portals.extend(portals)

    def _place_entity(self, entity, x, y):
        if (0 <= x < self.width and 0 <= y < self.height and
                self.is_walkable(x, y)):
            self._map[y][x].append(entity)
            return True
        else:
            return False

    def add_entity(self, entity, x, y):
        if self._place_entity(entity, x, y):
            self._init_entity(entity, x, y)
            return True
        else:
            return False

    def insert_entity(self, entity, x, y, z=0):
        self._map[y][x].insert(z, entity)

    def remove_entity(self, entity, x, y):
        self._map[y][x].remove(entity)
     
    def delete_entity(self, entity, x, y):
        self.remove_entity(entity, x, y)
        self.entities[str(entity)].remove(entity)

    def pop_entity(self, x, y, z=-1):
        return self._map[y][x].pop(z)

    def move_entity(self, entity, new_x, new_y):
        if self._place_entity(entity, new_x, new_y):
            self._update_entity(entity, new_x, new_y)
            x, y = self.get_coords(entity)
            self.remove_entity(entity, x, y)
            return True
        else:
            return False

    def get_portal(self, x, y):
        for portal in self.portals:
            px, py = portal.get_coords()
            if (px == x) and (py == y):
                return portal
    
    def get_portal_from_room(self, room):
        for portal in self.portals:
            if portal.get_room() is room:
                return portal
    
    def draw(self):
        self.batch.draw()

class World:
    """A collection of rooms that should be connected to each other by portals.
    """
    
    def __init__(self, rooms, initial_room, hero, ordered_entities):
        self.rooms = rooms
        self.current_room = initial_room
        self.hero = hero

        self.render_groups = []
        for i in range(len(ordered_entities)):
            self.render_groups.append(OrderedGroup(i))
            for entity in ordered_entities[i]:
                entity.group = self.render_groups[-1]

    def get_hero(self):
        return self.hero

    def get_terrain(self):
        return self.current_room.get_terrain()

    def get_items(self):
        return self.current_room.get_items()

    def get_characters(self):
        return self.current_room.get_characters()
    
    def is_walkable(self, x, y):
        return self.current_room.is_walkable(x, y)

    def get_portal(self, x, y):
        return self.current_room.get_portal(x, y)
    
    def get_coords(self, entity):
        return self.current_room.get_coords(entity)
    
    def add_entity(self, entity, x, y):
        self.current_room.add_entity(entity, x, y)
    
    def insert_entity(self, entity, x, y, z=0):
        self.current_room.add_entity(entity, x, y, z)
    
    def remove_entity(self, entity, x, y):
        self.current_room.remove_entity(entity, x, y)

                                               90     def add_portals(self, *portals):
                                                    91         self.portals.extend(portals)
                                                     92 
                                                      93     def _place_entity(self, entity, x, y):
                                                           94         if (0 <= x < self.width and 0 <= y < self.height and
                                                                    95                 self.is_walkable(x, y)):
                                                                96             self._map[y][x].append(entity)
                                                                 97             return True
                                                                  98         else:
                                                                       99             return False
                                                                       100 
                                                                       101     def add_entity(self, entity, x, y):
                                                                           102         if self._place_entity(entity, x, y):
                                                                               103             self._init_entity(entity, x, y)
                                                                               104             return True
                                                                               105         else:
                                                                                   106             return False
                                                                                   107 
                                                                                   108     def insert_entity(self, entity, x, y, z=0):
                                                                                       109         self._map[y][x].insert(z, entity)
                                                                                       110 
                                                                                       111     def remove_entity(self, entity, x, y):
                                                                                           112         self._map[y][x].remove(entity)
                                                                                           113 
                                                                                           114     def delete_entity(self, entity, x, y):
                                                                                               115         self.remove_entity(entity, x, y)
                                                                                               116         self.entities[str(entity)].remove(entity)
                                                                                               117 
                                                                                               118     def pop_entity(self, x, y, z=-1):
                                                                                                   119         return self._map[y][x].pop(z)
                                                                                                   120 
                                                                                                    38         return self.room
                                                                                                     39 
                                                                                                      40 class Room:
                                                                                                           41     """A 3-dimensional grid that contains Entities and Portals to other Rooms.
                                                                                                            42     Populates a World."""
                                                                                                             43 
                                                                                                              44     def __init__(self, name, width, height, _map=[], portals=[]):
                                                                                                                   45         self.name = name
                                                                                                                    46         self.width = width
                                                                                                                     47         self.height = height
                                                                                                                      48         self.portals = portals
                                                                                                                       49 
                                                                                                                        50         self.batch = Batch()
                                                                                                                         51 
                                                                                                                          52         self.entities = {'Character': [], 'Item': [], 'Terrain': []}
                                                                                                                           53 
                                                                                                                            54         if _map:
                                                                                                                                 55             self._map = _map
                                                                                                                                  56             self._init_entities()
                                                                                                                                   57         else:
                                                                                                                                        58             self._map = [[[] for x in width] for y in height]
                                                                                                                                         59 
                                                                                                                                          60     def _init_entities(self):
                                                                                                                                               61         for y in range(len(self._map)):
                                                                                                                                                    62             for x in range(len(self._map[y])):
                                                                                                                                                         63                 for entity in self._map[y][x]:
                                                                                                                                                              64                     self._init_entity(entity, x, y)
                                                                                                                                                               65 
                                                                                                                                                                66     def _init_entity(self, entity, x, y):
                                                                                                                                                                     67         entity.batch = self.batch
                                                                                                                                                                      68         self._update_entity(entity, x, y)
                                                                                                                                                                       69         self.entities[str(entity)].append(entity)
                                                                                                                                                                        70 
                                                                                                                                                                         71     def _update_entity(self, entity, x, y):
                                                                                                                                                                              72         entity.set_position(x * TILE_WIDTH, y * TILE_HEIGHT)
                                                                                                                                                                               73 
                                                                                                                                                                                74     def get_terrain(self):
                                                                                                                                                                                     75         return self.entities['Terrain']
                                                                                                                                                                                      76 
                                                                                                                                                                                       77     def get_items(self):
                                                                                                                                                                                            78         return self.entities['Item']
                                                                                                                                                                                             79 
                                                                                                                                                                                              80     def get_characters(self):
                                                                                                                                                                                                   81         return self.entities['Character']
                                                                                                                                                                                                    82 
                                                                                                                                                                                                     83     def get_coords(self, entity):
                                                                                                                                                                                                          84         x, y = entity.position
                                                                                                                                                                                                           85         return x / TILE_WIDTH, y / TILE_HEIGHT
                                                                                                                                                                                                            86 
                                                                                                                                                                                                             87     def is_walkable(self, x, y):
                                                                                                                                                                                                                  88         return all([e.is_walkable() for e in self._map[y][x]])
                                                                                                                                                                                                                   89 
                                                                                                                                                                                                                    90     def add_portals(self, *portals):
                                                                                                                                                                                                                         91         self.portals.extend(portals)
                                                                                                                                                                                                                          92 
                                                                                                                                                                                                                           93     def _place_entity(self, entity, x, y):
                                                                                                                                                                                                                                94         if (0 <= x < self.width and 0 <= y < self.height and
                                                                                                                                                                                                                                         95                 self.is_walkable(x, y)):
                                                                                                                                                                                                                                     96             self._map[y][x].append(entity)
                                                                                                                                                                                                                                      97             return True
                                                                                                                                                                                                                                       98         else:
                                                                                                                                                                                                                                            99             return False
                                                                                                                                                                                                                                            100 
                                                                                                                                                                                                                                            101     def add_entity(self, entity, x, y):
                                                                                                                                                                                                                                                102         if self._place_entity(entity, x, y):
                                                                                                                                                                                                                                                    103             self._init_entity(entity, x, y)
                                                                                                                                                                                                                                                    104             return True
                                                                                                                                                                                                                                                    105         else:
                                                                                                                                                                                                                                                        106             return False
                                                                                                                                                                                                                                                        107 
                                                                                                                                                                                                                                                        108     def insert_entity(self, entity, x, y, z=0):
                                                                                                                                                                                                                                                            109         self._map[y][x].insert(z, entity)
                                                                                                                                                                                                                                                            110 
                                                                                                                                                                                                                                                            111     def remove_entity(self, entity, x, y):
                                                                                                                                                                                                                                                                112         self._map[y][x].remove(entity)
                                                                                                                                                                                                                                                                113 
                                                                                                                                                                                                                                                                114     def delete_entity(self, entity, x, y):
                                                                                                                                                                                                                                                                    115         self.remove_entity(entity, x, y)
                                                                                                                                                                                                                                                                    116         self.entities[str(entity)].remove(entity)
                                                                                                                                                                                                                                                                    117 
                                                                                                                                                                                                                                                                    118     def pop_entity(self, x, y, z=-1):
                                                                                                                                                                                                                                                                        119         return self._map[y][x].pop(z)
                                                                                                                                                                                                                                                                        120 
                                                                                                                                                                                                                                                                        121     def move_entity(self, entity, new_x, new_y):
                                                                                                                                                                                                                                                                            122         if self._place_entity(entity, new_x, new_y):
                                                                                                                                                                                                                                                                                123             self._update_entity(entity, new_x, new_y)
                                                                                                                                                                                                                                                                                124             x, y = self.get_coords(entity)
                                                                                                                                                                                                                                                                                125             self.remove_entity(entity, x, y)
                                                                                                                                                                                                                                                                                126             return True
                                                                                                                                                                                                                                                                                127         else:
                                                                                                                                                                                                                                                                                    128             return False
                                                                                                                                                                                                                                                                                    129 
                                                                                                                                                                                                                                                                                    130     def get_portal(self, x, y):
                                                                                                                                                                                                                                                                                        131         for portal in self.portals:
                                                                                                                                                                                                                                                                                            132             px, py = portal.get_coords()
                                                                                                                                                                                                                                                                                            133             if (px == x) and (py == y):
                                                                                                                                                                                                                                                                                                134                 return portal
                                                                                                                                                                                                                                                                                                135 
                                                                                                                                                                                                                                                                                                136     def get_portal_from_room(self, room):
                                                                                                                                                                                                                                                                                                    137         for portal in self.portals:
                                                                                                                                                                                                                                                                                                        138             if portal.get_room() is room:
                                                                                                                                                                                                                                                                                                            139                 return portal
                                                                                                                                                                                                                                                                                                            140 
                                                                                                                                                                                                                                                                                                            141     def draw(self):
                                                                                                                                                                                                                                                                                                                142         self.batch.draw()
                                                                                                                                                                                                                                                                                                                143 
                                                                                                                                                                                                                                                                                                                144 class World:
                                                                                                                                                                                                                                                                                                                    145     """A collection of rooms that should be connected to each other by portals.
                                                                                                                                                                                                                                                                                                                    146     """
                                                                                                                                                                                                                                                                                                                    147 
                                                                                                                                                                                                                                                                                                                    148     def __init__(self, rooms, initial_room, hero, ordered_entities):
                                                                                                                                                                                                                                                                                                                        149         self.rooms = rooms
                                                                                                                                                                                                                                                                                                                        150         self.current_room = initial_room
                                                                                                                                                                                                                                                                                                                        151         self.hero = hero
                                                                                                                                                                                                                                                                                                                        152 
                                                                                                                                                                                                                                                                                                                        153         self.render_groups = []
                                                                                                                                                                                                                                                                                                                        154         for i in range(len(ordered_entities)):
                                                                                                                                                                                                                                                                                                                            155             self.render_groups.append(OrderedGroup(i))
                                                                                                                                                                                                                                                                                                                            156             for entity in ordered_entities[i]:
                                                                                                                                                                                                                                                                                                                                157                 entity.group = self.render_groups[-1]
                                                                                                                                                                                                                                                                                                                                158 
                                                                                                                                                                                                                                                                                                                                159     def get_hero(self):
                                                                                                                                                                                                                                                                                                                                    160         return self.hero
                                                                                                                                                                                                                                                                                                                                    161 
                                                                                                                                                                                                                                                                                                                                    162     def get_terrain(self):
                                                                                                                                                                                                                                                                                                                                        163         return self.current_room.get_terrain()
                                                                                                                                                                                                                                                                                                                                        164 
                                                                                                                                                                                                                                                                                                                                        165     def get_items(self):
                                                                                                                                                                                                                                                                                                                                            166         return self.current_room.get_items()
                                                                                                                                                                                                                                                                                                                                            167 
                                                                                                                                                                                                                                                                                                                                            168     def get_characters(self):
                                                                                                                                                                                                                                                                                                                                                169         return self.current_room.get_characters()
                                                                                                                                                                                                                                                                                                                                                170 
                                                                                                                                                                                                                                                                                                                                                171     def is_walkable(self, x, y):
                                                                                                                                                                                                                                                                                                                                                    172         return self.current_room.is_walkable(x, y)
                                                                                                                                                                                                                                                                                                                                                    173 
                                                                                                                                                                                                                                                                                                                                                    174     def get_portal(self, x, y):
                                                                                                                                                                                                                                                                                                                                                        175         return self.current_room.get_portal(x, y)
                                                                                                                                                                                                                                                                                                                                                        176 
                                                                                                                                                                                                                                                                                                                                                        177     def get_coords(self, entity):
                                                                                                                                                                                                                                                                                                                                                            178         return self.current_room.get_coords(entity)
                                                                                                                                                                                                                                                                                                                                                            179 
                                                                                                                                                                                                                                                                                                                                                            180     def add_entity(self, entity, x, y):
                                                                                                                                                                                                                                                                                                                                                                181         self.current_room.add_entity(entity, x, y)
                                                                                                                                                                                                                                                                                                                                                                182 
                                                                                                                                                                                                                                                                                                                                                                183     def insert_entity(self, entity, x, y, z=0):
                                                                                                                                                                                                                                                                                                                                                                    182 
                                                                                                                                                                                                                                                                                                                                                                    183     def insert_entity(self, entity, x, y, z=0):
                                                                                                                                                                                                                                                                                                                                                                        184         self.current_room.add_entity(entity, x, y, z)
                                                                                                                                                                                                                                                                                                                                                                        185 
                                                                                                                                                                                                                                                                                                                                                                        186     def remove_entity(self, entity, x, y):
                                                                                                                                                                                                                                                                                                                                                                            187         self.current_room.remove_entity(entity, x, y)
                                                                                                                                                                                                                                                                                                                                                                            188 
                                                                                                                                                                                                                                                                                                                                                                            189     def pop_entity(self, x, y, z=-1):
                                                                                                                                                                                                                                                                                                                                                                                190         self.current_room.pop_entity(x, y, z)
                                                                                                                                                                                                                                                                                                                                                                                191 
                                                                                                                                                                                                                                                                                                                                                                                192     def move_entity(self, entity, new_x, new_y):
                                                                                                                                                                                                                                                                                                                                                                                    193         if entity.get_name() == 'Hero':
                                                                                                                                                                                                                                                                                                                                                                                        194             print new_x, new_y
                                                                                                                                                                                                                                                                                                                                                                                        195         if self.current_room.move_entity(entity, new_x, new_y):
                                                                                                                                                                                                                                                                                                                                                                                            196             if entity.get_name() == 'Hero':
                                                                                                                                                                                                                                                                                                                                                                                                197                 print self.get_coords(entity)
                                                                                                                                                                                                                                                                                                                                                                                                198             portal = self.get_portal(new_x, new_y)
                                                                                                                                                                                                                                                                                                                                                                                                199             if portal:
                                                                                                                                                                                                                                                                                                                                                                                                    200                 self.portal_entity(entity, portal)
                                                                                                                                                                                                                                                                                                                                                                                                    201                 print self.get_coords(entity)
                                                                                                                                                                                                                                                                                                                                                                                                    202             if entity.get_name() == 'Hero':
                                                                                                                                                                                                                                                                                                                                                                                                        203                 print
                                                                                                                                                                                                                                                                                                                                                                                                        204             return True
                                                                                                                                                                                                                                                                                                                                                                                                        205         else:
                                                                                                                                                                                                                                                                                                                                                                                                            206             if entity.get_name() == 'Hero':
                                                                                                                                                                                                                                                                                                                                                                                                                207                 print
                                                                                                                                                                                                                                                                                                                                                                                                                208             return False
                                                                                                                                                                                                                                                                                                                                                                                                                209 
                                                                                                                                                                                               210     def step_entity(self, entity, x_step, y_stjkef pop_entity(self, x, y, z=-1):
        self.current_room.pop_entity(x, y, z)
    
    def move_entity(self, entity, new_x, new_y):
        if entity.get_name() == 'Hero':
            print new_x, new_y
        if self.current_room.move_entity(entity, new_x, new_y):
            if entity.get_name() == 'Hero':
                print self.get_coords(entity)
            portal = self.get_portal(new_x, new_y)
            if portal:
                self.portal_entity(entity, portal)
                print self.get_coords(entity)
            if entity.get_name() == 'Hero':
                print
            return True
        else:
            if entity.get_name() == 'Hero':
                print
            return False

    def step_entity(self, entity, x_step, y_step):
        x, y = self.get_coords(entity)
        return self.move_entity(entity, x + x_step, y + y_step)

    def portal_entity(self, entity, portal):
        self.current_room.deletee_entity_entity(entity, *portal.get_coords())
        old_room = self.current_room
        self.current_room = portal.get_room()
        recieving_portal = self.current_room.get_portal_from_room(
            old_room)
        x, y = recieving_portal.get_coords()
        self.add_entity(entity, x, y)
    
    def draw(self):
        self.current_room.draw()
                
