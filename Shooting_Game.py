import pygame
import os
pygame.font.init() #Intilize the pygame font library
pygame.mixer.init() #sound mixer

BULLET_HIT_SOUND = pygame.mixer.Sound('./Assets/Gun+Silencer.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('./Assets/Grenade+1.mp3')

WIDTH , HEIGHT = 1200 , 800
WIN = pygame.display.set_mode((WIDTH , HEIGHT))


BLACK = (0 , 0 , 0)
RED = (255 , 0 , 0)
YELLOW  = (255 , 255 , 0)

pygame.display.set_caption("First Game")

FPS = 60
VEL = 5 #Velocity Of The Ship
BULLET_VEL = 8 #Velocity Of The Bullet
MAX_BULLETS = 8 #Atmost bullets we can hit at a time(1 fram reset main)

SPACESHIP_WIDTH  , SPACESHIP_HEIGHT  = 55 , 45 

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets' , 'spaceship_yellow.png'))

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE , (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)) , 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets' , 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE , (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)) , 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets' , 'space.png')) , (WIDTH ,HEIGHT))

BORDER = pygame.Rect(WIDTH//2 - 5, 0 , 10 , HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans' , 40) #our font we use
WINNER_FONT = pygame.font.SysFont('comicsans' , 100)

YELLOW_HIT = pygame.USEREVENT + 1 # -->1 --> 1 for unique event id represent code/number for a custom user event
RED_HIT = pygame.USEREVENT + 2 # -->2 represent code/number for a custom user event

def draw_window(red , yellow , red_bullets , yellow_bullets , red_health , yellow_health):

	#if we dont filll the scrren with white -> pygame does not reove the last draing we made it keeps on maing the drawing
	#If we dont draw a backgroung the it shows all the paingting of the objss check for urself
	# WIN.fill((255,255,255))

	#objects overlap each other from top to bottm as the are just scrrens 
	WIN.blit(SPACE , (0,0))
	pygame.draw.rect(WIN ,BLACK ,BORDER)

	red_health_text = HEALTH_FONT.render("Health: " + str(red_health) , 1 , (255 , 255 , 255)) #Use the font to render sone text inside the brakcets
	yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health) , 1 , (255 , 255 , 255))

	WIN.blit(red_health_text , (WIDTH-red_health_text.get_width()-10 , 10))
	WIN.blit(yellow_health_text , (10 , 10))

	WIN.blit(YELLOW_SPACESHIP, (yellow.x , yellow.y)) #Add on the screen on on which position that of yellow ractange
	WIN.blit(RED_SPACESHIP , (red.x , red.y))  #Add on the screen on on which position that of red ractange created in main
	
	for bullet in red_bullets:
		pygame.draw.rect(WIN , RED , bullet  )

	for bullet in yellow_bullets:
		pygame.draw.rect(WIN , YELLOW , bullet  )
	pygame.display.update()

def yellow_handle_Movement(keys_pressed , yellow):
	if keys_pressed[pygame.K_a] and yellow.x - VEL >0 :  #left
		yellow.x -= VEL
		
	if keys_pressed[pygame.K_d] and yellow.x + VEL < BORDER.x - yellow.width	:  #right
		yellow.x += VEL

	if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  #up
		yellow.y -= VEL

	if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT -5:  #down
		yellow.y += VEL

def red_handle_Movement(keys_pressed , red):
	if keys_pressed[pygame.K_LEFT] and red.x - VEL> BORDER.x + 10:  #left
		red.x -= VEL
		
	if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  #right
		red.x += VEL

	if keys_pressed[pygame.K_UP] and red.y - VEL > 0 :  #up
		red.y -= VEL

	if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT -5:  #down
		red.y += VEL

def handle_bullets(yellow_bullets , red_bullets , yellow  , red):
	for bullet in yellow_bullets:
		bullet.x += BULLET_VEL

		#works if both objects are rectangles and is used to check if the recangle reprsented yellow has collided with 
		#the bullet one
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RED_HIT)) #Event for a red player When an event is happen it gets queued in pygame.event.queueu in main
			yellow_bullets.remove(bullet)

		elif bullet.x > WIDTH:
			yellow_bullets.remove(bullet)

	for bullet in red_bullets:
		bullet.x -= BULLET_VEL
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(YELLOW_HIT)) #Event for a yellow player
			red_bullets.remove(bullet)
		elif bullet.x < 0:
			red_bullets.remove(bullet)

def draw_Winner(text):
	draw_text = WINNER_FONT.render(text , 1 , (255,255,255))
	WIN.blit(draw_text , ((WIDTH - draw_text.get_width()) //2 , (HEIGHT - draw_text.get_height())//2))
	pygame.display.update()
	pygame.time.delay(5000) #pause 1000 * secons we won

def main():
	#rectangles that control our spaceship
	red = pygame.Rect(700 , 300 , SPACESHIP_WIDTH,SPACESHIP_HEIGHT) #represent the box of the red spaceship
	yellow = pygame.Rect(100 , 300 , SPACESHIP_WIDTH ,SPACESHIP_HEIGHT) #represent the box of the yellow spaceship

	#For Bullets Each Guy Will Throw
	red_bullets = []
	yellow_bullets = []

	#health of the ships
	red_health = 10
	yellow_health = 10

	#The above variables are created before the pygame running and hence are there till the game end
	#More like a global variable
 
	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)
		for event in pygame.event.get(): #Here
			if event.type == pygame.QUIT:
				run  = False
				pygame.quit()

			if event.type == pygame.KEYDOWN: #event for keypresses
				#pygame.K_ is for the key we pressed

				#lctrl bullet will go to the right
				if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
					#first is the location (x) where bullet will spawn and 2nd is y coord rest is the width and height of the rectangle of bullets
					#yellow.x is the top left corner and same is yellow.y -2 -> bullet height
					bullet = pygame.Rect(yellow.x + yellow.width , yellow.y + yellow.height//2 - 2 , 10 , 15)
					yellow_bullets.append(bullet)
					# BULLET_FIRE_SOUND.play()

				if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
					#red will send bullet from its left side i.e top left corner so no width required
					bullet = pygame.Rect(red.x , red.y + red.height//2 - 2 , 10 , 15)
					red_bullets.append(bullet)
					# BULLET_FIRE_SOUND.play()

			if event.type == RED_HIT:
				BULLET_HIT_SOUND.play()	
				if(yellow_health<=3):
					red_health -= 2
				else:
					red_health -= 1


			if event.type == YELLOW_HIT:
				BULLET_HIT_SOUND.play()
				if(red_health<=3):
					yellow_health -= 2
				else:
					yellow_health -= 1


		winner_text = ""
		if red_health <= 0:
			winner_text = "Yellow Wins!"
			
		if yellow_health <= 0:		
			winner_text = "Red Wins!"

		if winner_text != "":
			 #someone won
			draw_Winner(winner_text)
			break;

		keys_pressed = pygame.key.get_pressed() #????
		yellow_handle_Movement(keys_pressed , yellow)
		red_handle_Movement(keys_pressed , red)

		handle_bullets(yellow_bullets , red_bullets , yellow , red)

		draw_window(red , yellow , yellow_bullets , red_bullets , red_health  , yellow_health)
		
	# pygame.quit() #quits the game
	main()

if __name__ == "__main__":
	main()