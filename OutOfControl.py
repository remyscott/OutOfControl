import pygame, random, math
from dataclasses import dataclass
import copy

SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 720

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

font = pygame.image.load('font.png').convert()

letters = {"a": 0,
		   "b": 1,
		   "c": 2,
		   "d": 3,
		   "e": 4,
		   "f": 5,
		   "g": 6,
		   "h": 7,
		   "i": 8,
		   "j": 9,
		   "k": 10,
		   "l": 11,
		   "m": 12,
		   "n": 13,
		   "o": 14,
		   "p": 15,
		   "q": 16,
		   "r": 17,
		   "s": 18,
		   "t": 19,
		   "u": 20,
		   "v": 21,
		   "w": 22,
		   "x": 23,
		   "y": 24,
		   "z": 25,
		   ":": 26,
		   ".": 27,
		   " ": 28}

selected = 0

@dataclass
class Cell:
	updated: bool
	material: int
	color_offset: tuple
    



def generate_world(chunks_x, chunks_y):
	
	#creates grid of chunks
	gen = []
	for x in range(0,chunks_x):
		gridrow = []
		for y in range(0,chunks_y):
			gridrow.append(Chunk(x, y, 0))
		gen.append(gridrow)
		
	#gen = [[Chunk(x, y, 100) for y in range(chunks_y)] for x in range(chunks_x)]
	
	return(gen)




def character(char_id):
	surface = pygame.Surface((8, 8))
	surface.blit(font, (0,0), (char_id*8, 0, 8, 8))
	surface.set_colorkey((255,255,255))
	
	return(surface)
	
def generate_button(name, color):

	surface = pygame.Surface(((8*len(name))+2,10))
	
	surface.fill(color)
	
	
	i = 0
	
	for c in name:
		surface.blit(character(letters[c]), ((i*8),1))
		i += 1
	
	surface = pygame.transform.scale(surface, ((i*16)+4,20))
	
	return(surface)



class Button(pygame.sprite.Sprite):
	def __init__(self, img, material, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.img = img
		self.rect = self.img.get_rect()
		self.material = material
		self.x = x
		self.y = y 
	
	def update(self):
		if self.rect.collidepoint(mouse_x-self.x, mouse_y-self.y) and mouse_click:
			global selected
			
			selected = self.material
			
			
		
		display.blit(self.img, (self.x, self.y))

class Materials:
	empty = 0
	sand = 1
	gravel = 2
	water = 3

class Element():
	acceptible_moves = [Materials.empty]
	color_variation = 0
	
	color = (255,192,203)
	
		
	def move(x, y):
		print("what have you done!!! Element.move() is being called!")
		
class Empty(Element):
	color = (245, 245, 245)
	def move(x, y):
		pass

class Liquid(Element):
	acceptible_moves = [Materials.empty]
	def move(chunk_x, chunk_y, chunk_relative_x, chunk_relative_y):
		world_x = chunk_x*chunk_size +chunk_relative_x
		world_y = chunk_y*chunk_size +chunk_relative_y
		
		def try_move(xrel, yrel):
			return(get_cell_world_coord(world_x+xrel, world_y+yrel).material in Liquid.acceptible_moves)
		
		def do_move(xrel, yrel):
			different_chunks = check_diffent_chunks(chunk_relative_x+xrel, chunk_relative_y+yrel)
			swapcells(different_chunks, chunk_x, chunk_y, world_x, world_y, world_x+xrel, world_y+yrel)
			
			wakeup_neighbors(chunk_x, chunk_y, chunk_relative_x, chunk_relative_y)
			return(True)
		if try_move(0,1):
			return(do_move(0,1))

		first_dir = random.randint(0,1)*2 - 1
		second_dir = first_dir*-1

		if try_move(first_dir,1):
			return(do_move(first_dir,1))

		if try_move(second_dir,1):
			return(do_move(second_dir,1))
		
		if try_move(first_dir,0):
			return(do_move(first_dir,0))

		if try_move(second_dir,0):
			return(do_move(second_dir,0))

class Solid(Element):
	def move(x, y):
		print("what have you done!!! Solid.move() is being called!")




class ImmoveableSolid(Solid):
	def move(x, y):
		pass

class MoveableSolid(Solid):
	acceptible_moves = [Materials.empty]
	def move(chunk_x, chunk_y, chunk_relative_x, chunk_relative_y):
		world_x = chunk_x*chunk_size +chunk_relative_x
		world_y = chunk_y*chunk_size +chunk_relative_y
		
		def try_move(xrel, yrel):
			return(get_cell_world_coord(world_x+xrel, world_y+yrel).material in MoveableSolid.acceptible_moves)
		
		def do_move(xrel, yrel):
			different_chunks = check_diffent_chunks(chunk_relative_x+xrel, chunk_relative_y+yrel)
			swapcells(different_chunks, chunk_x, chunk_y, world_x, world_y, world_x+xrel, world_y+yrel)
			
			wakeup_neighbors(chunk_x, chunk_y, chunk_relative_x, chunk_relative_y)
			return(True)
		if try_move(0,1):
			return(do_move(0,1))

		first_dir = random.randint(0,1)*2 - 1
		second_dir = first_dir*-1

		if try_move(first_dir,1):
			return(do_move(first_dir,1))

		if try_move(second_dir,1):
			return(do_move(second_dir,1))
			

class Sand(MoveableSolid):
	color_variation = 15
	color = (255,220,100)

class Gravel(MoveableSolid):
	color_variation = 30
	color = (170,170,150)

class Water(Liquid):
	color = (100,100,200)

id_to_material = [Empty, Sand, Gravel, Water]

material_names = ['empty', 'sand', 'gravel', 'water']


	
buttons = pygame.sprite.Group()
for i in range(len(id_to_material)):
	new_button = Button(generate_button(material_names[i], id_to_material[i].color), i, 728,8+i*28)
	buttons.add(new_button)

color_offsets_num = 5
color_offsets = []

for i in range(len(id_to_material)):
	base_color = id_to_material[i].color
	color_offset_for_material = [base_color]
	for a in range(color_offsets_num-1):
		rd = random.randint(-id_to_material[i].color_variation,id_to_material[i].color_variation)
		cr = base_color[0] + rd
		cb = base_color[1] + rd
		cg = base_color[2] + rd
		if cr > 255:
			cr = 255
		elif cr < 0:
			cr = 0
		if cb > 255:
			cb = 255
		elif cb < 0:
			cb = 0
		if cg > 255:
			cg = 255
		elif cg < 0:
			cg = 0
		color_offset_for_material.append((cr, cb, cg))
	
	color_offset_for_material = tuple(color_offset_for_material)
	color_offsets.append(color_offset_for_material)
 
def check_diffent_chunks(chunk_relative_x, chunk_relative_y):
	if chunk_relative_x < 0 or chunk_relative_y < 0 or chunk_relative_x >= chunk_size or chunk_relative_y >= chunk_size:
		return(True)
	return(False)

def wakeup_neighbors(chunk_x, chunk_y,chunk_relative_x, chunk_relative_y):
	if chunk_relative_x == 0 and not chunk_x == 0:
		create_chunk(chunk_x-1, chunk_y)
		world[chunk_x-1][chunk_y].updated_by_other = True
	
	if chunk_relative_y == 0 and not chunk_y == 0:
		create_chunk(chunk_x, chunk_y-1)
		world[chunk_x][chunk_y-1].updated_by_other = True
	
	if chunk_relative_x == chunk_size-1 and not chunk_x == chunks_x-1:
		create_chunk(chunk_x+1, chunk_y)
		world[chunk_x+1][chunk_y].updated_by_other = True
	
	if chunk_relative_y == chunk_size-1 and not chunk_y == chunks_y-1:
		create_chunk(chunk_x, chunk_y+1)
		world[chunk_x][chunk_y+1].updated_by_other = True
	
	
	return(False)
	

class Chunk(pygame.sprite.Sprite):
	def __init__(self, x, y, sandprobability):
		pygame.sprite.Sprite.__init__(self)
		self.surf = pygame.Surface((chunk_size, chunk_size))
		self.grid = []
		self.x, self.y = x, y
		self.updated_by_other = False
		for x in range(0,chunk_size):
			gridrow = []
			for y in range(0,chunk_size):
				gridrow.append(
					Cell(
						material = Materials.empty, 
						updated = False,
						color_offset = random.randint(0,color_offsets_num-1)
					)
				)
			self.grid.append(gridrow)
			

		self.shouldstepnextframe = True
		self.shouldstepthisframe = True
		
	def updated_to_false(self):
		for x in range(0,chunk_size):
			for y in range(0,chunk_size):  
				self.grid[x][y].updated = False
			
	def render(self):
		for x in range(chunk_size):
			for y in range(chunk_size):
				color_to_draw = color_offsets[self.grid[x][y].material][self.grid[x][y].color_offset]
				if self.surf.get_at((x, y)) != color_to_draw:
					self.surf.set_at((x,y), color_to_draw)
				
	def update(self):
		
		self.shouldstepthisframe = self.shouldstepnextframe
		self.shouldstepnextframe = False
		if self.updated_by_other:
			self.shouldstepthisframe = True
			self.shouldstepnextframe = True
		self.updated_by_other = False
		
		if self.shouldstepthisframe:
			#generates a random order to update columbs in
			order = list(range(0,chunk_size))
			random.shuffle(order)
		
			
			empty = True
			moved = False
			
			#updating
			for x in order:
				for y in range(chunk_size-1, -1, -1):
					if self.grid[x][y].material != Materials.empty:
						empty = False
					
						#if not updated
						if not self.grid[x][y].updated:
							world_x, world_y = self.chunk_to_world(x, y)
							
							
							
							
							if id_to_material[self.grid[x][y].material].move(self.x, self.y, x, y):
								moved = True
								
							
			
					
			
			if moved:
				self.shouldstepnextframe = True
				
			return(empty)
			
	def chunk_to_world(self,chunk_x,chunk_y):
		chunk_x = chunk_x + self.x * chunk_size
		chunk_y = chunk_y + self.y * chunk_size
			
		return(chunk_x, chunk_y)
			
	

			

	
			
def swapcells(different_chunks, chunk_x, chunk_y, x1, y1, x2, y2):
	
	
	
	chunk_x = math.floor(x1/chunk_size)
	chunk_y = math.floor(y1/chunk_size)
	
	cell1 = get_cell_world_coord(x1,y1)
	cell1.updated = True
	cell2 = get_cell_world_coord(x2,y2)
	
	if different_chunks:
		chunk_x_2 = math.floor(x2/chunk_size)
		chunk_y_2 = math.floor(y2/chunk_size)
		world[chunk_x][chunk_y].grid[x1%chunk_size][y1%chunk_size] = cell2
		world[chunk_x_2][chunk_y_2].grid[x2%chunk_size][y2%chunk_size] = cell1
		world[chunk_x_2][chunk_y_2].updated_by_other = True
	else:
		world[chunk_x][chunk_y].grid[x1%chunk_size][y1%chunk_size] = cell2
		world[chunk_x][chunk_y].grid[x2%chunk_size][y2%chunk_size] = cell1
		

class Void():
	material = -1
def get_cell_world_coord(x, y):
	
	if x == -1 or x == chunk_size*chunks_x or y == -1 or y == chunk_size*chunks_y:
		return(Void)
		
	chunk_x = math.floor(x/chunk_size)
	chunk_y = math.floor(y/chunk_size)
	
	chunk_relative_x = x % chunk_size
	chunk_relative_y = y % chunk_size
		
	create_chunk(chunk_x, chunk_y)
	cell = world[chunk_x][chunk_y].grid[chunk_relative_x][chunk_relative_y]
	
	return(cell)

def create_chunk(x,y):
	if world[x][y] == "empty":
		world[x][y] = Chunk(x, y, 0)
running = True

chunk_size = 10
chunks_x = 18
chunks_y = 18
world = generate_world(chunks_x, chunks_y)

emptychunk = pygame.Surface((1,1))
emptychunk.fill(Empty.color)
mouse_down = False

total_updates = 0
time_last_frame = 0

time = 0
time_since_last_render = 60
cellpixelsize = min((1080 / chunks_x) / chunk_size,(720 / chunks_y) / chunk_size)
chunkpixelsize = int(cellpixelsize*chunk_size)


while running:
	
	mouse_click = False
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		
			
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_click = True
			mouse_down = True
			
		if event.type == pygame.MOUSEBUTTONUP:

			mouse_down = False
			 
	time_last_frame = time
	
	
	time = pygame.time.get_ticks()
	
	#framerate = 1000/(time-time_last_frame)
	#total_updates += 1
	
	#if total_updates % int(framerate) == 0:
	#	print(f'Running at {framerate:.0f} fps')
	
	
	#if framerate >= 60:
	#	clock.tick(60)
	
	
	mouse_x, mouse_y = pygame.mouse.get_pos()
	
	
	
	
	#draw sand
	if mouse_down:
		if not int(mouse_x/chunkpixelsize) > chunks_x-1:
			create_chunk(int(mouse_x/chunkpixelsize),int(mouse_y/chunkpixelsize))
			world[int(mouse_x/chunkpixelsize)][int(mouse_y/chunkpixelsize)].grid[int(mouse_x/cellpixelsize)%chunk_size][int(mouse_y/cellpixelsize)%chunk_size].material = selected
			world[int(mouse_x/chunkpixelsize)][int(mouse_y/chunkpixelsize)].shouldstepnextframe = True
	
	
	
	
	time_since_last_render += time-time_last_frame
	if time_since_last_render >= 100/6:
		time_since_last_render = 0
		#updated to false chunks
		for x in range(0, chunks_x):
			for y in range(0, chunks_y):
				if not world[x][y] == "empty":
					world[x][y].updated_to_false()
	
		#update chunks
		for x in range(chunks_x-1, -1, -1):
			for y in range(chunks_y-1, -1, -1):
				if not world[x][y] == "empty":
					if world[x][y].update() == True:
						world[x][y] = "empty"
		#chunks render
		for x in range(0, chunks_x):
			for y in range(0, chunks_y):
				if not world[x][y] == "empty":
					world[x][y].render()
				
		#render chunks
		for x in range(0, chunks_x):
			for y in range(0, chunks_y):
				if not world[x][y] == "empty":
					display.blit(pygame.transform.scale(world[x][y].surf,  (chunkpixelsize, chunkpixelsize)), (x*chunkpixelsize, y*chunkpixelsize))
				else:
					display.blit(pygame.transform.scale(emptychunk, (chunkpixelsize, chunkpixelsize)), (x*chunkpixelsize, y*chunkpixelsize))
		
	
	buttons.update()	
	pygame.display.update()
	
	
pygame.quit()