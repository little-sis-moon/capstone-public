
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import subprocess
import sys
import pathlib as pl
import random

global running

screenx=(20)*64
screeny=(12)*64
screen_buffer=32

is_multiplayer=False

directions=[[0,"Left","player_x-=playerspeed"],[1,"Right","player_x+=playerspeed"],[2,"Up","player_y-=playerspeed"],[3,"Down","player_y+=playerspeed"]]
if is_multiplayer==True:
	directions2=[[0,"Left","player2_x-=playerspeed"],[1,"Right","player2_x+=playerspeed"],[2,"Up","player2_y-=playerspeed"],[3,"Down","player2_y+=playerspeed"]]
#tail_segments=[[0,None,None,0],[1,None,None,0],[2,None,None,0],[3,None,None,0],[4,None,None,0],[5,None,None,0],[6,None,None,0],[7,None,None,0],[8,None,None,0],[9,None,None,0],[10,None,None,0],[11,None,None,0],[12,None,None,0],[13,None,None,0],[14,None,None,0],[15,None,None,0],[16,None,None,0],[17,None,None,0],[18,None,None,0],[19,None,None,0],[20,None,None,0],[21,None,None,0],[22,None,None,0],[23,None,None,0],[24,None,None,0],[25,None,None,0],[26,None,None,0],[27,None,None,0],[28,None,None,0],[29,None,None,0],[30,None,None,0],[31,None,None,0],[32,None,None,0],[33,None,None,0],[34,None,None,0],[35,None,None,0],[36,None,None,0],[37,None,None,0],[38,None,None,0],[39,None,None,0],[40,None,None,0],[41,None,None,0],[42,None,None,0],[43,None,None,0],[44,None,None,0],[45,None,None,0],[46,None,None,0],[47,None,None,0],[48,None,None,0],[49,None,None,0],[50,None,None,0]]
max_length = 99999
max_apples = 3
playername="Player 1"
if is_multiplayer==True:
	player2name="Player 2"

player_leftbounds=False
if is_multiplayer==True:
	player2_leftbounds=False
player_died=False
if is_multiplayer==True:
	player2_died=False

tail_segments = [[i, None,None, 0] for i in range(max_length)]
if is_multiplayer==True:
	tail2_segments=[[i,None,None,0] for i in range(max_length)]

apples=[[i,random.randrange(32,screenx,64),random.randrange(32,screeny,64),0] for i in range(max_apples)]


playerpath=os.path.join(str(pl.Path(__file__).parent) + "/visuals/snake/snake.png")
if is_multiplayer==True:
	player2path=os.path.join(str(pl.Path(__file__).parent) + "/visuals/snake/snake2.png")

tailpath=os.path.join(str(pl.Path(__file__).parent) + "/visuals/snake/snake.png")
if is_multiplayer==True:
	tail2path=os.path.join(str(pl.Path(__file__).parent) + "/visuals/snake/snake2.png")

applepath=os.path.join(str(pl.Path(__file__).parent) + "/visuals/snake/apple.png")
bonus_applepath=os.path.join(str(pl.Path(__file__).parent) + "/visuals/snake/sand_x64.png")


apple=pygame.image.load(applepath)
apple_rect=apple.get_rect()

bonus_apple=pygame.image.load(bonus_applepath)
bonus_apple_rect=bonus_apple.get_rect()

player=pygame.image.load(playerpath)
player_rect=player.get_rect()

if is_multiplayer==True:
	player2=pygame.image.load(player2path)
if is_multiplayer==True:
	player2_rect=player2.get_rect()

tail=pygame.image.load(tailpath)
tail_rect=tail.get_rect()

if is_multiplayer==True:
	tail2=pygame.image.load(tail2path)
if is_multiplayer==True:
	tail2_rect=tail2.get_rect()

playerspeed=64
player_x=32
player_y=32
if is_multiplayer==True:
	player2_x=96
if is_multiplayer==True:
	player2_y=96
length=2
if is_multiplayer==True:
	length2=2
playerdirection=None
if is_multiplayer==True:
	player2direction=None

runtime=0



pygame.init()
'''
#pygame.joystick.init()

#controller_count=pygame.joystick.get_count()

#try:
	player_controller=pygame.joystick.Joystick(0)
	player_controller.init()

	player_controller_id=player_controller.get_instance_id()

	print(player_controller_id)
except Exception as e:
	print("No Controller Connected.")
	print("There are [" + str(controller_count) + "] controllers connected.")
	print(e)
'''

screen = pygame.display.set_mode((screenx,screeny))
clock = pygame.time.Clock()
running=True

def func_endgame(playername):
	global running
	if is_multiplayer==True:
		print(playername + " Wins")
	running=False

while running:
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			running=False
	#START game logic
	keys=pygame.key.get_pressed()
	runtime+=1
	#START player movement
	if keys[pygame.K_LEFT] and playerdirection!="Right":
		playerdirection="Left"

	if keys[pygame.K_RIGHT] and playerdirection!="Left":
		playerdirection="Right"

	if keys[pygame.K_UP] and playerdirection!="Down":
		playerdirection="Up"

	if keys[pygame.K_DOWN] and playerdirection!="Up":
		playerdirection="Down"
	#if keys[pygame.K_SPACE]:
	#	length+=1
	#if is_multiplayer==True:
	#	length2+=1
	#start player 2
	
	if is_multiplayer==True:
		if keys[pygame.K_a] and player2direction!="Right":
			player2direction="Left"

	if is_multiplayer==True:
		if keys[pygame.K_d] and player2direction!="Left":
			player2direction="Right"

	if is_multiplayer==True:
		if keys[pygame.K_w] and player2direction!="Down":
			player2direction="Up"

	if is_multiplayer==True:
		if keys[pygame.K_s] and player2direction!="Up":
			player2direction="Down"
	#end player 2
	

	for i in range(len(directions)):
		if directions[i][1]==playerdirection:
			exec(directions[i][2])
		if is_multiplayer==True:
			if directions2[i][1]==player2direction:
				exec(directions2[i][2])
	for i in range(length):
		if tail_segments[i][3]>0:
			tail_segments[i][3]-=1
		if is_multiplayer==True:
			if tail2_segments[i][3]>0:
				tail2_segments[i][3]-=1
	#END player movement

	if player_x<screen_buffer or player_y<screen_buffer or player_x>screenx-screen_buffer or player_y>screeny-screen_buffer:
		player_leftbounds=True

	if is_multiplayer==True:
		if player2_x<screen_buffer or player2_y<screen_buffer or player2_x>screenx-screen_buffer or player2_y>screeny-screen_buffer:
			player2_leftbounds=True

	for i in range(length):
		if player_x==tail_segments[i][1] and player_y==tail_segments[i][2] and playerdirection is not None:
			player_died=True
		if is_multiplayer==True:
			if player_x==tail2_segments[i][1] and player_y==tail2_segments[i][2] and playerdirection is not None:
				player_died=True
		

	if is_multiplayer==True:
		for i in range(length2):
			if player2_x==tail2_segments[i][1] and player2_y==tail2_segments[i][2] and player2direction is not None:
				player2_died=True
			if player2_x==tail_segments[i][1] and player2_y==tail_segments[i][2] and player2direction is not None:
				player2_died=True
		


	for i in range(max_apples):
		if player_x==apples[i][1] and player_y==apples[i][2]:
			length+=1
			apples[i][1]=random.randrange(32,screenx,64)
			apples[i][2]=random.randrange(32,screeny,64)
		if is_multiplayer==True:
			if player2_x==apples[i][1] and player2_y==apples[i][2]:
				length2+=1
			apples[i][1]=random.randrange(32,screenx,64)
			apples[i][2]=random.randrange(32,screeny,64)

	if is_multiplayer==True:
		if player2_leftbounds or player2_died:
			func_endgame(playername)
	if player_leftbounds or player_died:
		if is_multiplayer==True:
			func_endgame(player2name)
		else:
			func_endgame("nobody")
	for i in range(length, 0, -1):
		tail_segments[i][1] = tail_segments[i-1][1]
		tail_segments[i][2] = tail_segments[i-1][2]
		tail_segments[0][1]=player_x
		tail_segments[0][2]=player_y
	if is_multiplayer==True:
		for i in range(length2,0,-1):
			tail2_segments[i][1] = tail2_segments[i-1][1]
			tail2_segments[i][2] = tail2_segments[i-1][2]
			tail2_segments[0][1]=player2_x
			tail2_segments[0][2]=player2_y






	#END game logic
	screen.fill(pygame.Color(75,75,75))
	#START rendering code
	tail_segments[0][1]=player_x
	tail_segments[0][2]=player_y
	if is_multiplayer==True:
		tail2_segments[0][1]=player2_x
		tail2_segments[0][2]=player2_y
	for i in range(length+1):
		segment_x=tail_segments[i][1]
		segment_y=tail_segments[i][2]
		if segment_x is not None and segment_y is not None:
			
			tail_rect.center=(segment_x,segment_y)
			screen.blit(tail,tail_rect)
	if is_multiplayer==True:
		for i in range(length2+1):
			segment2_x=tail2_segments[i][1]
			segment2_y=tail2_segments[i][2]
			if segment2_x is not None and segment2_y is not None:
			
				tail2_rect.center=(segment2_x,segment2_y)
				screen.blit(tail2,tail2_rect)


	screen.blit(player,player_rect)
	player_rect.center=(player_x,player_y)
	if is_multiplayer==True:
		screen.blit(player2,player2_rect)
		player2_rect.center=(player2_x,player2_y)
	for i in range(len(apples)):
		apple_x=apples[i][1]
		apple_y=apples[i][2]
		for f in range(len(apples)):
			if apple_x==apples[f][1] and apple_y==apples[f][2] and f!=i:
				screen.blit(bonus_apple,bonus_apple_rect)
				bonus_apple_rect.center=(apple_x,apple_y)
		else:
			screen.blit(apple,apple_rect)
			apple_rect.center=(apple_x,apple_y)

	#END rendering code
	pygame.display.flip()
	clock.tick(6)



