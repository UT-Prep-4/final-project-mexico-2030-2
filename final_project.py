#Name(s):
#Final Project - Build Something Worth Showing Off
'''
This is the big one. At the end of camp you will demo this project at the
SHOWCASE, and it should be good enough to put on a resume or mention in a
college application. That means it is not just "code that works." It is a
project you designed, built, polished, and can explain.

WHAT MAKES IT SHOWCASE-WORTHY (the autograder checks for these):
  1. ORGANIZED: your code is split into clear, purposeful segments (functions optional), not one
     giant blob. (Aim for at least 3-4 functions with real jobs.)
  2. SUBSTANTIAL: this is a multi-day build, bigger than the mini-project.
  3. REAL LOGIC: decisions (if/elif/else) and repetition (loops) working together.
  4. DOCUMENTED: fill out PROJECT.md so a stranger (or a college admissions
     reader!) can understand what you built and how to run it.

Whether it is impressive, creative, and demo-ready is judged by humans at
showcase, not by the autograder.

============================= PICK YOUR TRACK =================================

TRACK A: IMAGE PROCESSING PROGRAM
  Build a program that opens an image and transforms it with a special
  function you write yourself: brightness adjustment, a color filter overlay,
  grayscale, mirror, pixelate, or invent your own effect.
  The Pillow library is preinstalled. The core moves:

      from PIL import Image
      img = Image.open("photo.png")
      width, height = img.size
      pixel = img.getpixel((x, y))          # (red, green, blue), each 0-255
      img.putpixel((x, y), (r, g, b))       # set a pixel
      img.save("output.png")                # then click it in VS Code to view!

  Brightness is a for loop over every pixel that multiplies r, g, b by a
  factor the user chooses (careful: values must stay between 0 and 255).
  A filter overlay nudges every pixel toward a color (add red, drop blue...).
  Level up: ask the user which effect to apply with input(), show a menu,
  process any image file they name, draw the result with turtle or pygame.

TRACK B: ADVENTURE GAME
  Build a text adventure where the player explores, makes choices, and wins
  or loses based on decisions and luck. Use random for surprises: treasure,
  traps, enemy encounters, dice rolls, critical hits.
  The shape of it: one function per location or scene, input() for choices,
  an inventory list, health or gold as numbers, and random.randint() for
  the unexpected. Level up: turn-based combat, a map, multiple endings,
  ASCII art title screens, a save-your-score high score.

TRACK C: YOUR OWN IDEA
  A bigger game (pygame or turtle), a quiz app, a tool that solves a real
  problem you have, a simulation, generative turtle art... Pitch it to your
  instructor FIRST, then build it. The four requirements above still apply.

=============================== PLAN FIRST ====================================
Before you write code, fill this in (it will keep you honest all week):

  MY PROJECT: (one sentence)
  THE PIECES I NEED TO BUILD: (list 3-6 functions or parts)
  WHAT I WILL DEMO AT SHOWCASE: (the 60-second version)

==============================================================================
Build your project below (and split it into more .py files if it gets big;
the grader reads all of them). Delete this line and start!
'''
#imports------
import pygame as pg
from pygame.math import Vector2

#------------------ final project ---------------------------
#initialize pygame
pg.init()

#create clock
clock = pg.time.Clock()

waypoints = [
  (100,100),
  (400, 200),
  (400, 100),
  (200, 300)
]

#create game window
screen = pg.display.set_mode((640, 640))
pg.display.set_caption("Castle TD")

#load images
enemy_image = pg.image.load('').conver_alpha()

enemy = Enemy((waypoints), enemy_image)

#create groups
enemy_group = pg.sprite.Group()
enemy_group.add(enemy)


#updage groups
enemy_group.update()
#game loop
run = True
while run:

  clock.tick(60)

  screen.fill("grey100")

  #enemy path
  pg.draw.lines(screen, "grey0", False, waypoints)

  #draw groups
  enemy_group.draw(screen)

  for event in pg.event.get():
    if event.type == pg.QUIT:
      run = False

  #update display
  pg.display.flip()

pg.quit()

#------------------ enemies ---------------------------
class Enemy(pg.sprite.Sprite):
  def __init__(self, waypoints, image):
    pg.sprite.Sprite.__init_(self)
    self.waypoints = waypoints
    self.pos = Vector2(self.waypoints[0])
    self.target_waypoints = 1
    self.speed = 2
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.center = self.pos

  def update(self):
    self.move

  def move(self):
    self.target = Vector2(self.waypoints[self.target_waypoint])
    self.movement = self.target - self.pos
    self.pos += self.movement.normalize() * self.speed
    self.rect.center = self.poslf.target_waypoint])
    self.movement = self.target - self.pos()lf.pos += (self.movement.normalisze())self.rect.center = self.pos * self.speed