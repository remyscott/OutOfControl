import pygame, random, math
from dataclasses import dataclass
import copy

SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 720

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()




@dataclass
class Cell:
	updated: bool
	material: int

class Materials:
	empty = 0
	sand = 1

def generate_world(chunks_x, chunks_y):
	
	#creates grid of chunks
	gen = []
	for x in range(0,chunks_x):
		gridrow = []
		for y in range(0,chunks_y):
			gridrow.append(Chunk(x, y, 100))
		gen.append(gridrow)
		
	#gen = [[Chunk(x, y, 100) for y in range(chunks_y)] for x in range(chunks_x)]
	
	return(gen)

class Chunk(pygame.sprite.Sprite):
	def __init__(self, x, y, sandprobability):
		pygame.sprite.Sprite.__init__(self)
		self.surf = pygame.Surface((chunk_size, chunk_size))
		self.grid = []
		self.x, self.y = x, y
		
		for x in range(0,chunk_size):
			gridrow = []
			for y in range(0,chunk_size):
				gridrow.append(
					Cell(
						material = Materials.sand if random.randint(0, 1000) < sandprobability else Materials.empty, 
						updated = False
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
				if self.grid[x][y].material == Materials.empty:
					self.surf.set_at((x,y), (255,255,255))
					
				if self.grid[x][y].material == Materials.sand:
					self.surf.set_at((x,y), (255,255,0))
	def update(self):
		self.shouldstepthisframe = self.shouldstepnextframe
		self.shouldstepnextframe = False
		
		
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
						
						if self.grid[x][y].material == Materials.sand:
							world_x, world_y = self.chunk_to_world(x, y)
							if MoveableSolid.move(world_x, world_y):
								moved = True
							
			
					
					
			if moved:
				self.shouldstepnextframe = True
		
		
			return(empty)
	def chunk_to_world(self,chunk_x,chunk_y):
		chunk_x = chunk_x + self.x * chunk_size
		chunk_y = chunk_y + self.y * chunk_size
			
		return(chunk_x, chunk_y)
			
#global coordinates to chunk coordinates	
def get_chunk(x, y):
	chunk_x = math.floor(x/chunk_size)
	chunk_y = math.floor(y/chunk_size)

	
	return(chunk_x, chunk_y)
	

			
class Element():
	
	def move(x, y):
		print("what have you done!!! Element.move() is being called!")
		

class Solid(Element):
	def move(x, y):
		print("what have you done!!! Solid.move() is being called!")

class ImmoveableSolid(Solid):
	def move(x, y):
		pass

class MoveableSolid(Solid):
	def move(x, y):
		if y+1 < chunks_y * chunk_size:
			if get_cell_world_coord(x, y+1).material == Materials.empty:
				swapcells(x ,y ,x ,y+1)
				return(True)
				
			elif x+1 < chunks_x * chunk_size and get_cell_world_coord(x+1, y+1).material == Materials.empty:
				swapcells(x ,y ,x+1 ,y+1)
				return(True)
			
			elif x-1 >= 0 and get_cell_world_coord(x-1, y+1).material == Materials.empty:
				swapcells(x ,y ,x-1 ,y+1)
				return(True)
			
def swapcells(x1, y1, x2, y2):
	chunk_x_1 = math.floor(x1/chunk_size) 
	chunk_y_1 = math.floor(y1/chunk_size)
	
	chunk_x_2 = math.floor(x2/chunk_size)
	chunk_y_2 = math.floor(y2/chunk_size)
	
	cell1 = get_cell_world_coord(x1,y1)
	cell1.updated = True
	cell2 = get_cell_world_coord(x2,y2)
	cell2.updated = True
	
	world[chunk_x_1][chunk_y_1].grid[x1%chunk_size][y1%chunk_size] = cell2
	world[chunk_x_2][chunk_y_2].grid[x2%chunk_size][y2%chunk_size] = cell1
	
def get_cell_world_coord(x, y):
	chunk_x = math.floor(x/chunk_size)
	chunk_y = math.floor(y/chunk_size)
	chunk_relative_x = x % chunk_size
	chunk_relative_y = y % chunk_size
	
	if world[chunk_x][chunk_y] == "empty":
		world[chunk_x][chunk_y] = Chunk(chunk_x, chunk_y, 0)
		
	world[chunk_x][chunk_y].shouldstepnextframe = True
	
	cell = world[chunk_x][chunk_y].grid[chunk_relative_x][chunk_relative_y]
	
	return(cell)

running = True

chunk_size = 10
chunks_x = 16
chunks_y = 16
world = generate_world(chunks_x, chunks_y)

emptychunk = pygame.Surface((1,1))
emptychunk.fill((255,255,255))
mouse_down = False

total_updates = 0
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
			 
	
	
	total_updates += 1
	time = pygame.time.get_ticks()
    
	clock.tick(30)
    
	if total_updates %10 == 0:
		print(f'Running at {1000/(time/total_updates):.2f} fps')
	
	mouse_x, mouse_y = pygame.mouse.get_pos()
	
	
	
	
					
	
	
	
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
				display.blit(pygame.transform.scale(world[x][y].surf, (int(720/chunks_x),int(720/chunks_y))), (x*(720/chunks_x), y*(720/chunks_y)))
			else:
				display.blit(pygame.transform.scale(emptychunk, (int(720/chunks_x), int(720/chunks_y))), (x*(720/chunks_x), y*(720/chunks_y)))
					
	pygame.display.update()
	
pygame.quit()