import pygame
import pickle
from os import path


pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
margin = 100
screen_width = 600 #x width
screen_height = 600 + margin #y height
sizex = 40 #availiable grids x
sizey = 20 #availiable grids y
tile_size = int(screen_width/sizex)
cols = int((screen_height - margin)/sizey)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')


#load images
bg_img = pygame.image.load('bg.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height - margin))
block_img = pygame.image.load('block.png')
chain_img = pygame.image.load('chain.png')
ladder_img = pygame.image.load('ladder.png')
coin_img = pygame.image.load('coin.png')
restart_img = pygame.image.load('restart_btn.png')
start_img = pygame.image.load('start_btn.png')
exit_img = pygame.image.load('exit_btn.png')
load_img = pygame.image.load('coin.png')
save_img = pygame.image.load('exit_btn.png')

#define game variables
clicked = False
level = 1

#define colours
white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

#create empty tile list
world_data = []
for row in range(sizex):
	r = [0] * sizex
	world_data.append(r)

#create boundary
for tile in range(0, 40):
	world_data[19][tile] = 1
#	world_data[0][tile] = 1
#	world_data[tile][0] = 1
#	world_data[tile][19] = 1

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_grid():
	for x in range(sizex + 1):
		for y in range(sizey + 1):
			#vertical lines
			pygame.draw.line(screen, white, (x * tile_size, 0), (x * tile_size, (screen_height - margin)))
			#horizontal lines
			pygame.draw.line(screen, white, (0, y * cols), (screen_width, y * cols))

def draw_world():
	for row in range(sizey):
		for col in range(sizex):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1:
					#dirt blocks
					img = pygame.transform.scale(block_img, (tile_size,cols))
					screen.blit(img, (col * tile_size, row * cols))
				if world_data[row][col] == 2:
					#chain blocks
					img = pygame.transform.scale(chain_img, (tile_size,cols))
					screen.blit(img, (col * tile_size, row * cols))
				if world_data[row][col] == 3:
					#ladder blocks
					img = pygame.transform.scale(ladder_img,(tile_size,cols))
					screen.blit(img, (col * tile_size, row * cols))
				if world_data[row][col] == 4:
					#ladder right side blocks
					imgs = pygame.transform.flip(ladder_img, True, False)
					img = pygame.transform.scale(imgs, (tile_size,cols))
					screen.blit(img, (col * tile_size, row * cols))
				if world_data[row][col] == 7:
					#coin
					img = pygame.transform.scale(coin_img, (tile_size // 2, cols // 2))
					screen.blit(img, (col * tile_size + (tile_size // 4), row * cols + (cols // 4)))
				if world_data[row][col] == 8:
					#exit
					img = pygame.transform.scale(exit_img, (tile_size, int(cols * 1.5)))
					screen.blit(img, (col * tile_size, row * cols - (cols // 2)))

class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

#create load and save buttons
save_img = pygame.transform.scale(save_img, (tile_size+30 , int(tile_size * 0.75)))
save_button = Button(screen_width // 2 - 150, screen_height - 80, save_img)
load_img = pygame.transform.scale(load_img, (tile_size+30, int(tile_size * 0.75)))
load_button = Button(screen_width // 2 + 50, screen_height - 80, load_img)


#main game loop
run = True
while run:

	clock.tick(fps)

	#draw background
	screen.fill(green)
	screen.blit(bg_img, (0, 0))

	#load and save level
	if save_button.draw():
		#save level data
		pickle_out = open(f'level{level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
	if load_button.draw():
		#load in level data
		if path.exists(f'level{level}_data'):
			pickle_in = open(f'level{level}_data', 'rb')
			world_data = pickle.load(pickle_in)


	#show the grid and draw the level tiles
	draw_grid()
	draw_world()


	#text showing current level
	draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
	draw_text('Press UP or DOWN to change level', font, white, tile_size, screen_height - 40)

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#mouseclicks to change tiles
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // cols
			#check that the coordinates are within the tile area
			if x < sizex and y < sizey:
				#update tile value
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] += 1
					if world_data[y][x] > 8:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 8
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		#up and down key presses to change level number
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1

	#update game display window
	pygame.display.update()

pygame.quit()

