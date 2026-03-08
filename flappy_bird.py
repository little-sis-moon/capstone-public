#--------------------------------------------------------------------------------------------------importing (duh)
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import subprocess
import sys
import pathlib as pl
import random
import math
import time



#--------------------------------------------------------------------------------------------------global variables
global running
global pipes
global scoreboxes
global pipe_offset_max
global top_pipe_y
global bottom_pipe_y
global pipe_speed
global pipe_spawn_time
global life
global iframes
global max_iframes
global level
global levels
global score
global xp_to_level_up
global gravity
global flap_height
global max_flappy_y_vel
global pipe_gap

#--------------------------------------------------------------------------------------------------these commands get run for gamemodes without gravity

directions=[[0,"Left","flappy_x_vel=flap_height*(-1*max_flaps)"],[1,"Right","flappy_x_vel=flap_height*(1*max_flaps)"],[2,"Up","flappy_y_vel=flap_height*(-1*max_flaps)"],[3,"Down","flappy_y_vel=flap_height*(1*max_flaps)"]]

#--------------------------------------------------------------------------------------------------initializing all the basic stuff
playerdirection=None
screen_x=(20)*64
screen_y=(12)*64
screen_buffer=32
runtime=0
framerate=30
gravity=1

#--------------------------------------------------------------------------------------------------setting the image files up
flappy_path=os.path.join(str(pl.Path(__file__).parent) + "/visuals/flappy/doodle_flappy.png")
top_pipe_path=os.path.join(str(pl.Path(__file__).parent) + "/visuals/flappy/pipe_transparent_top.png")
bottom_pipe_path=os.path.join(str(pl.Path(__file__).parent) + "/visuals/flappy/pipe_transparent_bottom.png")
ground_path=os.path.join(str(pl.Path(__file__).parent) + "/visuals/flappy/ground.png")
scorebox_path=os.path.join(str(pl.Path(__file__).parent) + "/visuals/flappy/scorebox.png")
#for some reason font isnt initialized when everything else is?
pygame.font.init()

scoreboard_font_path=os.path.join(str(pl.Path(__file__).parent) + "/fonts/pxi.ttf")
scoreboard_font=pygame.font.Font(scoreboard_font_path,40)

health_font_path=os.path.join(str(pl.Path(__file__).parent) + "/fonts/pxi.ttf")
health_font=pygame.font.Font(health_font_path,40)

warning_font_path=os.path.join(str(pl.Path(__file__).parent) + "/fonts/pxi.ttf")
warning_font=pygame.font.Font(warning_font_path,40)

next_level_font_path=os.path.join(str(pl.Path(__file__).parent) + "/fonts/pxi.ttf")
next_level_font=pygame.font.Font(next_level_font_path,40)
#--------------------------------------------------------------------------------------------------initial flappy stuff
flappy_x=64
flappy_y=64
flappy_x_vel=0
flappy_y_vel=0

#--------------------------------------------------------------------------------------------------resetting powerups
max_flaps=1
flaps=max_flaps
default_flap_height=32
flap_height=default_flap_height
max_flappy_y_vel=16
max_flappy_x_vel=16



#--------------------------------------------------------------------------------------------------initializing different gamemodes
flap_types=[[0,"ice",1],[1,"linear",.66],[2,"snake",.5],[3,"freedom",.7]]
slow_mode=False
slow_modifier=.5
life=3
max_iframes=60
max_ns_frames=15
ns_frames=200
iframes=200
score=0
too_high_count=0

#--------------------------------------------------------------------------------------------------setting the default gamemode
gamemode=1
#^^^^^^^^^^^^^^change this variable lmao

flap_type=str(flap_types[gamemode][1])

#ground stuff
#--------------------------------------------------------------------------------------------------ground location and speed
ground_x=screen_x
ground_paralax=4

#pipe initialization
#--------------------------------------------------------------------------------------------------pipe & scorebox initialization
pipe_speed=(8)
pipes=[[None,None,None,None,0]]
#     [[pipe #,x,y,top/bottom,active?]]
empty_score_box=[[None,None,None,0,0]]
scoreboxes=empty_score_box
#	   [[box #, x, y, points,active?]]
#pipe spawning stuff
pipe_spawn_time=(48)#
#24 is probably minimum for free movement
#about 48 for linear flapping
pipe_timer=pipe_spawn_time/2
pipe_gap=(16)*16 #192
top_pipe_y=64-(pipe_gap/2)
bottom_pipe_y=screen_y-64+(pipe_gap/2)
scorebox_y=screen_y/2
pipe_offset_max=128
scoreboxes_spawn=True
pipes_spawn=True

if flap_type=="snake" or flap_type=="freedom":
	scoreboxes_spawn=False
#	print("IM NOT GONNA SPAWN SCOREBOXES")

#end of pipe spawning stuff
#--------------------------------------------------------------------------------------------------loading images to variables
flappy=pygame.image.load(flappy_path)
top_pipe=pygame.image.load(top_pipe_path)
bottom_pipe=pygame.image.load(bottom_pipe_path)
scorebox=pygame.image.load(scorebox_path)
#--------------------------------------------------------------------------------------------------making rects
flappy_rect=flappy.get_rect()
top_pipe_rect=top_pipe.get_rect()
bottom_pipe_rect=bottom_pipe.get_rect()
scorebox_rect=scorebox.get_rect()

ground=pygame.image.load(ground_path)
ground_rect=ground.get_rect()
running=False


#--------------------------------------------------------------------------------------------------making screen & clock
screen = pygame.display.set_mode((screen_x,screen_y))
clock = pygame.time.Clock()

warning_too_high=False
warning_blink_timer=0
warning_blink_timer_max=1*framerate



#levelling
#--------------------------------------------------------------------------------------------------level up system & powerups
level=0
levels=[[0,3,1,0],[1,4,2,5],[2,5,3,10],[3,6,3,15],[4,6,5,21],[5,7,6,28],[6,7,6,35],[7,8,6,42],[8,8,7,49],[9,9,8,55],[10,9,8,62],[11,10,8,70],[12,10,9,80],[13,11,11,94],[14,12,12,102],[15,12,14,112],[16,12,14,119],[17,13,15,133],[18,14,15,147],[19,15,15,164],[20,18,18,210],[21,19,20,220],[22,3,1,240],[23,3,1,250],[24,25,25,275],[25,9999,9999,9999]]
      #[[id, HP,flaps,xp required]]

			#should probably add pipes & gravity increasing too
#powerups
powerups=[[0,"level_up","func_level_up(1)"],[],[],[]]
#[id,name,effect]
xp_to_level_up=0

def func_level_up(amount):
	global level
	global levels
	global score
	global life
	global xp_to_level_up
	global pipe_speed
	global pipe_spawn_time
	global gravity
	global flap_height
	global max_flappy_y_vel
	global pipe_gap

	level+=amount
	life=levels[level][1]
	pipe_speed+=1
	pipe_spawn_time-=(int(4/(math.sqrt(level))))
	pipe_gap-=level

#these kinda just made it unfun to play
#	gravity+=((level^2)/16)
	
#	temp_var=8

#	flap_height+=int(temp_var/math.sqrt(level))
#	max_flappy_y_vel+=int(temp_var/math.sqrt(level))
def func_spawn_pipe():
	global pipes
	global scoreboxes
	global pipe_offset_max
	global top_pipe_y
	global bottom_pipe_y
	top_pipe_y=64-(pipe_gap/2)
	bottom_pipe_y=screen_y-64+(pipe_gap/2)
	for i in range(1):
#--------------------------------------------------------------------------------------------------generating pipe gaps
		if pipes[i][0]!=None: #pipes[i][4] != 0:
			pipe_offset=random.randint(-1*pipe_offset_max,pipe_offset_max)
			top_pipe=[len(pipes),screen_x-screen_buffer,top_pipe_y+pipe_offset,"Top",1]
			bottom_pipe=[len(pipes),screen_x-screen_buffer,bottom_pipe_y+pipe_offset,"Bottom",1]
#--------------------------------------------------------------------------------------------------adding pipes to render list
			pipes.append(top_pipe)
			pipes.append(bottom_pipe)
#--------------------------------------------------------------------------------------------------if there isnt any pipes, makes a default pipe. (this spawns on top of flappy so you need to make him have iframes for a bit)
		else:
			pipes=[[len(pipes),screen_x-screen_buffer,128,None,0]]
#--------------------------------------------------------------------------------------------------same things for scoreboxes
		if scoreboxes[i][0]!=None:
			score_box=[len(pipes),screen_x-screen_buffer,scorebox_y,1,1]
			scoreboxes.append(score_box)
		else:
			scoreboxes=[[len(pipes),screen_x-screen_buffer,screen_y/2,0,0]]


def func_move_pipes(extra_updates):
	global pipes
	global pipe_speed
#--------------------------------------------------------------------------------------------------moves pipes (lol)
	for f in range(extra_updates+1):
		for i in range(len(pipes)):
			if pipes[i][4] != 0:
				pipes[i][1]-=pipe_speed
		for i in range(len(scoreboxes)):
			if scoreboxes[i][4]!=0:
				scoreboxes[i][1]-=pipe_speed

def func_die():
#--------------------------------------------------------------------------------------------------doesn't work too well; will probably remove soon
	global running
	pygame.quit()
	running=False
	time.sleep(1)
	print("You Lose.")
#	try_again=input("Try Again? Y/N: ")
	#so idfk how strings work with .lower so this might not ever work
	#never mind it randomly started working now
	#so ig i just have to setup the reinitialization of everything
	#wow that word sucks to spell lmaoooo
	#never mind...
	#no doesnt work. fucking computers and their lack of consent. No means No!
#	if try_again.lower()=="y" or try_again.lower()=="yes" or try_again=="1":
#		print("restarting...")
#		pygame.init()
#	elif try_again.lower=="n" or try_again.lower=="no" or try_again=="0":
	sys.exit()
#	else:
#		print("ERROR: Invalid Command. Please Retry.")
#		func_die()
def func_launch():
#--------------------------------------------------------------------------------------------------dude im a fucking genious
	global running
	running=True


def func_damage(amount,coefficient):
	global life
	global iframes
	global max_iframes
	extraupdates=0
	while True:
		if coefficient>framerate:
			coefficient-=framerate
			extraupdates+=1
		else:
			break
	for i in range(extraupdates+1):
		life-=amount
#	print(str(life) + " health remaining")
#depricated: text renders this now

	iframes=max_iframes/coefficient

	#print("extraupdates: " + str(extraupdates))
	#print("coefficient: " + str(coefficient))
	
	
	


#--------------------------------------------------------------------------------------------------anything that needs to be run before the game can go here or in the func_launch def.
func_launch()

while running:
#--------------------------------------------------------------------------------------------------quits the game if the [X] button is pressed
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			running=False
#START game logic
#--------------------------------------------------------------------------------------------------detects key presses and incriments time
	keys=pygame.key.get_pressed()
	runtime+=1
	func_move_pipes(0)
	pipe_timer-=1
	
	if flappy_y<=0:
		warning_blink_timer+=1
		warning_too_high=True
		
	elif warning_blink_timer!=0:
		warning_blink_timer-=1
	if warning_blink_timer>=warning_blink_timer_max:
		warning_blink_timer=0
		too_high_count+=1


	if flappy_y>0:
		warning_too_high=False
		too_high_count=0

	if too_high_count>=5 and iframes<=0:
		func_damage(1,1*(too_high_count-4))
#--------------------------------------------------------------------------------------------------spawns pipes every little bit
	if pipe_timer==0:
		func_spawn_pipe()
		pipe_timer=pipe_spawn_time
       
#START player movement
#--------------------------------------------------------------------------------------------------velocity cap
	if flappy_y_vel>max_flappy_y_vel:
		flappy_y_vel=max_flappy_y_vel
	if flappy_x_vel>max_flappy_x_vel:
		flappy_x_vel=max_flappy_x_vel
#--------------------------------------------------------------------------------------------------moves location from velocity
	flappy_y+=flappy_y_vel
	flappy_x+=flappy_x_vel
#--------------------------------------------------------------------------------------------------different flap types
	flap_height=default_flap_height
	for i in range(len(flap_types)):
		if flap_type==flap_types[i][1]:
			flap_height*=flap_types[i][2]
			flap_height*=flap_types[i][2]
	if slow_mode==True:
		flap_height*=slow_modifier

	if flap_type=="snake" or flap_type=="freedom":
		flappy_y_vel=0
		flappy_x_vel=0

	if flap_type != "snake" and flap_type != "freedom":
		flappy_y_vel+=gravity

	elif keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
		slow_mode=True
	else:
		slow_mode=False

#START player control
	if keys[pygame.K_UP] and flaps>0:
		if flap_type=="ice":
			flappy_y_vel-=(flap_height+gravity)
		elif flap_type=="linear":
			flappy_y_vel=(-1*flap_height)

	
		flaps-=1
	elif flap_type=="snake":
		if keys[pygame.K_LEFT] and playerdirection!="Right":
			playerdirection="Left"
		if keys[pygame.K_RIGHT] and playerdirection!="Left":
			playerdirection="Right"
		if keys[pygame.K_UP] and playerdirection!="Down":
			playerdirection="Up"
		if keys[pygame.K_DOWN] and playerdirection!="Up":
			playerdirection="Down"
	
		if keys[pygame.K_SPACE]:
			playerdirection=None
		for i in range(len(directions)):
			if directions[i][1]==playerdirection:
				flappy_x_vel=0
				flappy_y_vel=0
				exec(directions[i][2])
	elif flap_type=="freedom":
		if keys[pygame.K_UP]:
			flappy_y-=flap_height
		if keys[pygame.K_DOWN]:
			flappy_y+=flap_height
		if keys[pygame.K_LEFT]:
			flappy_x-=flap_height
		if keys[pygame.K_RIGHT]:
			flappy_x+=flap_height
	elif not keys[pygame.K_UP] and flaps<max_flaps:
		flaps+=1
#END player movement
#we dyin now
#--------------------------------------------------------------------------------------------------incrimenting iframes down
	if iframes>0:
		iframes-=1
	if ns_frames>0:
		ns_frames-=1
#--------------------------------------------------------------------------------------------------death
	if life<=0:
		func_die()
       #END game logic
#--------------------------------------------------------------------------------------------------wiping last frame & sets background to a color
	screen.fill(pygame.Color(75,75,75))
       #START rendering code
	screen.blit(flappy,flappy_rect)
	flappy_rect.center=(flappy_x,flappy_y)
#--------------------------------------------------------------------------------------------------Scoreboards
	if scoreboxes_spawn==True:
		for i in range(len(scoreboxes)):
			if scoreboxes[i][4]!=0:
				screen.blit(scorebox,scorebox_rect)
				scorebox_rect.center=(scoreboxes[i][1],scoreboxes[i][2])
				if scoreboxes[i][1]<=0 and scoreboxes[i][4]!=0:
					scoreboxes[i][4]=0
#--------------------------------------------------------------------------------------------------Touching scoreboxes
			if (flappy_rect.colliderect(scorebox_rect)  and ns_frames<=0):
				score+=scoreboxes[i][3]
		#		print("Score: " + str(score))
#depricated, have a text rendered to screen.
				ns_frames=max_ns_frames
				if levels[level+1][3]<=score:
					func_level_up(1)
				xp_to_level_up=levels[level+1][3]-score
#--------------------------------------------------------------------------------------------------Pipes
	for i in range(len(pipes)):
		if pipes[i][4] != 0:
			if pipes[i][3] == "Top":
				screen.blit(top_pipe,top_pipe_rect)
				top_pipe_rect.center=(pipes[i][1],pipes[i][2])
			if pipes[i][3] == "Bottom":
				screen.blit(bottom_pipe,bottom_pipe_rect)
				bottom_pipe_rect.center=(pipes[i][1],pipes[i][2])

#--------------------------------------------------------------------------------------------------Touching pipes stuff
			if (flappy_rect.colliderect(top_pipe_rect) or flappy_rect.colliderect(bottom_pipe_rect)) and iframes<=0:
				func_damage(1,1)
				score-=1
			if pipes[i][1]<=0 and pipes[i][4]!=0:
				pipes[i][4]=0
#--------------------------------------------------------------------------------------------------Touching ground stuff
	if flappy_rect.colliderect(ground_rect):
		flappy_y_vel-=(gravity+8)
		if iframes<=0:
			func_damage(1,4)
	elif flappy_rect.colliderect(ground_rect):
		flappy_y+=flappy_y_vel/8

	elif flappy_y>screen_y-screen_buffer:
		flappy_y=screen_y-(4*screen_buffer)
		flappy_y_vel=0
	if ground_x>0:
		ground_x-=ground_paralax
	if ground_x<=0:
		ground_x=screen_x
#--------------------------------------------------------------------------------------------------Drawing ground
	screen.blit(ground,ground_rect)
	ground_rect.center=(ground_x,screen_y)
#--------------------------------------------------------------------------------------------------Drawing score text
	score_text=scoreboard_font.render("SCORE: " + str(score), True, (255,255,255))
	score_text_rect=score_text.get_rect()
	score_text_rect.center=(128,128)

	health_text=health_font.render("HP: " + str(life), True, (255,0,35))
	health_text_rect=health_text.get_rect()
	health_text_rect.center=(160,160)

	warning_text=warning_font.render("TURN BACK.",True,(255,255,0))
	warning_text_rect=warning_text.get_rect()
	warning_text_rect.center=(screen_x/2,32)

	next_level_text=next_level_font.render(" NEXT LEVEL: " + str(xp_to_level_up),True,(25,255,25))
	next_level_text_rect=next_level_text.get_rect()
	next_level_text_rect.center=(128,192)
	
	screen.blit(score_text,score_text_rect)
	screen.blit(health_text,health_text_rect)
	screen.blit(next_level_text,next_level_text_rect)
	if warning_too_high and warning_blink_timer<warning_blink_timer_max/2:
		screen.blit(warning_text,warning_text_rect)
#END rendering code
#--------------------------------------------------------------------------------------------------renders screen && keeps framerate consistant
	pygame.display.flip()
	clock.tick(framerate)
