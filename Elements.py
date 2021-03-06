#from zzt import *
from Dictionaries import *
import Tyger
import pygame
#from Oop import *
import Oop

#board.render[x][y] is on line 1160 obj
#Skipped Clockwise(), Blink(), UnderOver()shouldn't need, UpdateStat()shouldn't need

#Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (x, y), 0, 0, 0, 0, 0, 0)
#To spawn an empty

#position is the position in the array of stat objects

#Random integer shortcut! ie rnd(1,100)
rnd = lambda min, max: Tyger.random.randint(min, max)

def activate(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, world, allboards, screen):
    #Thingsdict[name]
    #print board.room[x][y].name
    #Check if it's a valid cycle for the Element to move on
    
    if board.statcoords[position][0] == -1: #Flash the message if needed
        if board.statcoords[position][1] > -35:
            FlashDict = {0:Tyger.green, 1:Tyger.blue, 2:Tyger.white, 3:Tyger.yellow, 4:Tyger.purple, 5:Tyger.red, 6:Tyger.cyan}
            #print "CycleS:", cycles % 7
            tempimg = pygame.Surface((8*len(board.msg), 14)) #Create a surface for the message
            tempimg.fill(Tyger.bgdarkblue)    
            for x in range(0, len(board.msg)): #Then for every character of text in that list... (chopping off the .zzt)
                tempchar = Tyger.makeimage(ord(board.msg[x]), FlashDict[cycles % 7], Tyger.bgblack) #Create the character
                tempimg.blit(tempchar, (x*8,0)) #Stamp it onto the surface for the line
            Oop.TextMessage = tempimg
            temp = board.statcoords[position][1] - 1
            board.statcoords[position] = (-1, temp)
        else:
            board.msg = ""
            board.msglength = 0
            DestroyStat(board, -1, -35)
            for temp in xrange(0,59):
                board.render[24][temp] = 1
            #print "Stats now look like:", board.statcoords
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    #print Tyger.options[0]
    if health > 0 and board.room[board.statcoords[0][0]][board.statcoords[0][1]].name == "player":
        try:
            if cycles % board.room[x][y].cycle != 0:
                return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        except ZeroDivisionError:
            if board.room[x][y].name == "passage":
                return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
            #print "Divided by 0! " + str(board.room[x][y].name) + "'s cycle is seen as: " + str(board.room[x][y].cycle)
            #print str(board.room[x][y])
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
    
    if board.room[x][y].name == "player" and health > 0:
        #print str(board.statcoords[0])
        return Player(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, allboards, screen)
    elif board.room[x][y].name == "monitor":
        return Monitor(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, world, allboards, screen)
    elif board.room[x][y].name == "object":
        return Object(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, screen)
    elif board.room[x][y].name == "bullet":
        #print "Bullet time."
        return Bullet(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    elif board.room[x][y].name == "star":
        return Star(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    elif board.room[x][y].name == "lion":
        return Lion(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    elif board.room[x][y].name == "ruffian":
        return Ruffian(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    elif board.room[x][y].name == "shark":
        return Shark(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    elif board.room[x][y].name == "slime":
        return Slime(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    elif board.room[x][y].name == "pusher":
        #print "Whatever"
        return Pusher(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    elif board.room[x][y].name == "bomb":
        return Bomb(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed) #What makes me a good demoman?
    elif board.room[x][y].name == "blinkwall":
        return Blink(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    elif board.room[x][y].name == "bear":
        return Bear(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    elif board.room[x][y].name == "scroll":
        Scroll(board, x, y, cycles)
    elif board.room[x][y].name == "clockwise":
        return Clockwise(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def Bear(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed):
    #Bears hibernate unless a player is near them. Compare the X and Y coords of the player and the bear.
    dir = None
    deltaX = abs(x - board.statcoords[0][0])
    deltaY = abs(y - board.statcoords[0][1])
    print "Distance X/Y | Param1", deltaX, deltaY, board.room[x][y].param1
    
    #Are you aligned?
    #I don't quite understand why this is needed.
    if (x == board.statcoords[0][0]):
        if y > board.statcoords[0][1]:
            dir = "west"
        else:
            dir = "east"
    elif(y == board.statcoords[0][1]):
        if x > board.statcoords[0][0]:
            dir = "north"
        else:
            dir = "south"
    print "----------------------------------------", dir
    if (deltaX <= board.room[x][y].param1) and (dir != "north") and (dir != "south"): #E/W movement
        print "Tiggered X axis", (board.statcoords[0][0] - x)
        #print str(board.statcoords[0][0] - x)
        if ((board.statcoords[0][1] - y) < 0) or dir == "west" : #West
            print "WEST!"
            if BearDict[board.room[x][y-1].name] == "walkable": #Move
                board.roomunder[x][y-1] = board.room[x][y-1] #Under setup
                board.room[x][y-1] = board.room[x][y] #Move
                board.render[x][y-1] = 1 #Render old tile
                board.statcoords[position] = (x, y-1) #New Stat
                board.room[x][y] = board.roomunder[x][y] #Erase old bear
                board.render[x][y] = 1 #Render new tile
            elif BearDict[board.room[x][y-1].name] == "hurt": #Move
                health = health - 10
                DestroyStat(board, x, y)
                board.room[x][y] = board.roomunder[x][y]
                board.render[x][y] = 1
            elif BearDict[board.room[x][y-1].name] == "destroy": #Mr. Gorbachev, tear down this wall!
                print "Destroy"
                board.room[x][y] = board.roomunder[x][y]
                board.render[x][y] = 1
                board.room[x][y-1] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (x, y-1), 0, 0, 0, 0, 0, 0)
                board.render[x][y-1] = 1
                DestroyStat(board, x, y)
                DestroyStat(board, x, y-1)
        elif ((board.statcoords[0][1] + y) > 0) or dir == "east": #East
            if BearDict[board.room[x][y+1].name] == "walkable": #Move
                board.roomunder[x][y+1] = board.room[x][y+1] #Under setup
                board.room[x][y+1] = board.room[x][y] #Move
                board.render[x][y+1] = 1
                board.statcoords[position] = (x, y+1) #New Stat
                board.room[x][y] = board.roomunder[x][y] #Erase old bear
                board.render[x][y] = 1
            elif BearDict[board.room[x][y+1].name] == "hurt": #Move
                health = health - 10
                DestroyStat(board, x, y)
                board.room[x][y] = board.roomunder[x][y]
                board.render[x][y] = 1
            elif BearDict[board.room[x][y+1].name] == "destroy": #Mr. Gorbachev, tear down this wall!
                board.room[x][y] = board.roomunder[x][y]
                board.render[x][y] = 1
                board.room[x][y+1] =Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (x, y+1), 0, 0, 0, 0, 0, 0)
                board.render[x][y+1] = 1
                DestroyStat(board, x, y)
                DestroyStat(board, x, y+1)
        else:
            print "Failure E/W"
    elif (deltaY <= board.room[x][y].param1): #N/S movement
        print "Triggered Y axis"
        print str(board.statcoords[0][0] - x)
        if ((board.statcoords[0][0] - x) < 0) or dir == "north": #North
            print "NORTH!"
            if BearDict[board.room[x-1][y].name] == "walkable": #Move
                print "Move"
                board.roomunder[x-1][y] = board.room[x-1][y] #Under setup
                board.render[x-1][y] = 1
                board.room[x-1][y] = board.room[x][y] #Move
                board.statcoords[position] = (x-1, y) #New Stat
                board.room[x][y] = board.roomunder[x][y] #Erase old bear
                board.render[x][y] = 1
            elif BearDict[board.room[x-1][y].name] == "hurt": #Move
                health = health - 10
                DestroyStat(board, x, y)
                board.room[x][y] = board.roomunder[x][y]
                board.render[x][y] = 1
            elif BearDict[board.room[x-1][y].name] == "destroy": #Mr. Gorbachev, tear down this wall!
                print "Destroy"
                board.room[x][y] = board.roomunder[x][y]
                board.render[x][y] = 1
                board.room[x-1][y] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (x-1, y), 0, 0, 0, 0, 0, 0)
                board.render[x-1][y] = 1
                board.render[x-1][y] = 1
                DestroyStat(board, x, y)
                DestroyStat(board, x-1, y)
        elif ((board.statcoords[0][0] + x) > 0) or dir == "south": #South
            print "South!"
            if BearDict[board.room[x+1][y].name] == "walkable": #Move
                board.roomunder[x+1][y] = board.room[x+1][y] #Under setup
                board.render[x+1][y] = 1
                board.room[x+1][y] = board.room[x][y] #Move
                board.statcoords[position] = (x+1, y) #New Stat
                board.room[x][y] = board.roomunder[x][y] #Erase old bear
                board.render[x][y] = 1
            elif BearDict[board.room[x+1][y].name] == "hurt": #Move
                health = health - 10
                DestroyStat(board, x, y)
                board.room[x][y] = board.roomunder[x][y]
                board.render[x][y] = 1
            elif BearDict[board.room[x+1][y].name] == "destroy": #Mr. Gorbachev, tear down this wall!
                board.room[x][y] = board.roomunder[x][y]
                board.render[x][y] = 1
                board.room[x+1][y] =Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (x+1, y), 0, 0, 0, 0, 0, 0)
                board.render[x+1][y] = 1
                DestroyStat(board, x, y)
                DestroyStat(board, x+1, y)
        else:
            print "Failure N/S"
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def Blink(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed):
    #Easier directional refences
    if board.room[x][y].xstep > 127:
        board.room[x][y].xstep = board.room[x][y].xstep-65536
    if board.room[x][y].ystep > 127:
        board.room[x][y].ystep = board.room[x][y].ystep-65536
    
    ns = board.room[x][y].ystep
    ew = board.room[x][y].xstep
    #Param 1 = Start time
    #Param 2 = Period
    #Param 3 = Time left?
    #Come up with what type of blink wall to blink into existence
    if (board.room[x][y].ystep == -1 or board.room[x][y].ystep == 1) and board.room[x][y].xstep == 0:
        wall = Tyger.Spawn("vertray", 186, board.room[x][y].foreground, board.room[x][y].background, (0, 0), 0, 0, 0, 0, 0, 0)
    else:
        wall = Tyger.Spawn("horizray", 205, board.room[x][y].foreground, board.room[x][y].background, (0, 0), 0, 0, 0, 0, 0, 0)
    
    #Set param3 timer to param1, start time
    #print str(board.room[x][y].param1) + " | " + str(board.room[x][y].param2) + " | " + str(board.room[x][y].param3) 
    #If we still have the initial delay...
    
    #board.room[x][y].param3 = board.room[x][y].param3 + 1 #Increase the wall's timer
    if board.room[x][y].param3 > (board.room[x][y].param1 + (board.room[x][y].param2) * 4):
        board.room[x][y].param3 = board.room[x][y].param1
    
    if board.room[x][y].param3 > board.room[x][y].param1: #If the current timer is more than the start time...
        #if ((board.room[x][y].param3 + 1) * 2)>= (board.room[x][y].param1 + board.room[x][y].param2): #And less than the start time + the period, turn the wall on
        print str(board.room[x][y].param3 - board.room[x][y].param1) + " < " + str((board.room[x][y].param2 + 1) + board.room[x][y].param1)
        if (board.room[x][y].param3 - board.room[x][y].param1) < (board.room[x][y].param2 + 1 + board.room[x][y].param1): #And less than the start time + the period, turn the wall on
            print "Line goes on"
            while board.room[x+ns][y+ew].name == "empty" or board.room[x+ns][y+ew].name == "gem" or board.room[x+ns][y+ew].name == "bullet" or board.room[x+ns][y+ew].name == "lion" or board.room[x+ns][y+ew].name == "tiger" or board.room[x+ns][y+ew].name == "bear" or board.room[x+ns][y+ew].name == "ruffian" or board.room[x+ns][y+ew].name == "head" or board.room[x+ns][y+ew].name == "segment":
                    if board.room[x+ns][y+ew].name == "player": #Handle player zapping
                        print "You got owned."
                    
                    board.playerbullets = board.playerbullets - ((board.room[x+ns][y+ew].param1 == 0)*board.room[x+ns][y+ew].name == "bullet") #Reduce playerbullet count if applicable.
                    DestroyStat(board, x+ns, y+ew) #Destroy the stat if necessary
                    board.room[x+ns][y+ew] = wall #Draw the wall
                    board.render[x+ns][y+ew] = 1
                    #Increase directional variables
                    if ns != 0:
                        ns = ns + board.room[x][y].ystep
                    if ew != 0:
                        ew = ew + board.room[x][y].xstep
        else:
            print "Line goes off"
            #Disable the ray
            while board.room[x+ns][y+ew].name == "horizray" or board.room[x+ns][y+ew].name == "vertray":
                if (board.room[x+ns][y+ew].name == "horizray" and wall.name == "vertray") or (board.room[x+ns][y+ew].name == "vertray" and wall.name == "horizray"):
                    break
                board.room[x+ns][y+ew] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (x+ns, y+ew), 0, 0, 0, 0, 0, 0) #Erase the wall
                board.render[x+ns][y+ew] = 1
                #Increase directional variables
                if ns != 0:
                    ns = ns + board.room[x][y].ystep
                if ew != 0:
                    ew = ew + board.room[x][y].xstep
    #print "Param 3 is " + str(board.room[x][y].param3)
    board.room[x][y].param3 = board.room[x][y].param3 + 1 #Increase the wall's timer
    """
    if board.room[x][y].param3 < board.room[x][y].param1:
        print "Trigger 1 " + str(board.room[x][y].param1) + " " + str(board.room[x][y].param2) + " " + str(board.room[x][y].param3)
        #Increase param3
        #print "Increasing P3. Was... " + str(board.room[x][y].param3)
        board.room[x][y].param3 = board.room[x][y].param3 + 1 #Eventually this wait time will end
        blah = board.room[x][y].param3 + 1 #Python why do i need both these lines for anything to occur?
        board.room[x][y].param3 = blah
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board #Be done with it?
        #print "New P3:" + str(board.room[x][y].param3)
    elif board.room[x][y].param3 == board.room[x][y].param1:
        print "Trigger 2 " + str(board.room[x][y].param1) + " " + str(board.room[x][y].param2) + " " + str(board.room[x][y].param3)
        #Starting time is over, we now need to loop the beam
        board.room[x][y].param3 = ((board.room[x][y].param2 + 1) * 2 + 1) + board.room[x][y].param1
        #print "Loop beam" + str(board.room[x][y].param3)
    if board.room[x][y].param3 > board.room[x][y].param2:
        #Now determin if the wall should be on or off
        print "Trigger 3 " + str(board.room[x][y].param1) + " " + str(board.room[x][y].param2) + " " + str(board.room[x][y].param3)
        if (board.room[x][y].param3 - board.room[x][y].param1) > (board.room[x][y].param2 + 1): #If the offset time is more than the period, take a shine of the laser beam
            #print str(x+ns) + " " + str(y+ew)
            while board.room[x+ns][y+ew].name == "empty" or board.room[x+ns][y+ew].name == "gem" or board.room[x+ns][y+ew].name == "bullet" or board.room[x+ns][y+ew].name == "lion" or board.room[x+ns][y+ew].name == "tiger" or board.room[x+ns][y+ew].name == "bear" or board.room[x+ns][y+ew].name == "ruffian" or board.room[x+ns][y+ew].name == "head" or board.room[x+ns][y+ew].name == "segment":
                if board.room[x+ns][y+ew].name == "player": #Handle player zapping
                    print "You got owned."
                
                board.playerbullets = board.playerbullets - ((board.room[x+ns][y+ew].param1 == 0)*board.room[x+ns][y+ew].name == "bullet") #Reduce playerbullet count if applicable.
                DestroyStat(board, x+ns, y+ew) #Destroy the stat if necessary
                board.room[x+ns][y+ew] = wall #Draw the wall
                #Increase directional variables
                if ns != 0:
                    ns = ns + board.room[x][y].ystep
                if ew != 0:
                    ew = ew + board.room[x][y].xstep
            #print "ON        " + str(board.room[x][y].param1) + " " + str(board.room[x][y].param2) + " " + str(board.room[x][y].param3)
        else:
            #Disable the ray
            while board.room[x+ns][y+ew].name == "horizray" or board.room[x+ns][y+ew].name == "vertray":
                if (board.room[x+ns][y+ew].name == "horizray" and wall.name == "vertray") or (board.room[x+ns][y+ew].name == "vertray" and wall.name == "horizray"):
                    break
                board.room[x+ns][y+ew] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (x+ns, y+ew), 0, 0, 0, 0, 0, 0) #Erase the wall
                #Increase directional variables
                if ns != 0:
                    ns = ns + board.room[x][y].ystep
                if ew != 0:
                    ew = ew + board.room[x][y].xstep
            #print "OFF       " + str(board.room[x][y].param1) + " " + str(board.room[x][y].param2) + " " + str(board.room[x][y].param3)
        #Reduce the timer
        board.room[x][y].param3 = board.room[x][y].param3 - 1
    else:
        #Reduce the timer anyway?
        board.room[x][y].param3 = board.room[x][y].param3 - 1
    """
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def Bomb(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed): #What makes me a good demoman?
    #print "If I were a bad demoman, I wouldn't be sittin here discussin it with ya now would I?"
    if board.room[x][y].param1 == 0: #If it's not activated there isn't anything to do.
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board #KA-BEWM
    elif board.room[x][y].param1 == 1: #Ya appear to have trodden on a mine!
        #print "Ohhh they're gonna haf-ta glue you back together... IN HELL. " + str(rnd(1,100))
        health = Explode(board, x, y, health, ecycles)
        board.room[x][y].param1 = -1
    elif board.room[x][y].param1 == -1: #Cleanup
        CleanBomb(board, x, y)
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board #Ahm gonna be all over ya, like shingles!
    else: #Couldn't ya see the bloody bomb?!
        board.room[x][y].param1 = board.room[x][y].param1 - 1 #Decrease the fuse
        board.render[x][y] = 1 #Render this
    #Update timer character
    if board.room[x][y].param1 + 48 > 255:
        board.room[x][y].character = board.room[x][y].param1 + 48 - 255
        board.render[x][y] = 1
    else:
        board.room[x][y].character = board.room[x][y].param1 + 48
        board.render[x][y] = 1
        if board.room[x][y].param1 == 1 or board.room[x][y].param1 == -1:
            board.room[x][y].character = 11
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board #Ahm drunk, YOU don't have an excuse!
    
def BorderCheck(x, y):
    #Freespaces in which dirs
    free = [True, True, True, True]
    if x == 0: #top
        free[0] = False
    if x == 24: #bottom
        free[1] = False
    if y == 0: #left
        free[2] = False
    if y == 59: #right
        free[3] = False
    
    return free

def Bullet(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed):
    bullet = board.room[x][y]
    #print str(bullet.xstep) + "/" + str(bullet.ystep)
    if bullet.xstep > 127:
        bullet.xstep = bullet.xstep-65536
    if bullet.ystep > 127:
        bullet.ystep = bullet.ystep-65536
    #print str(bullet.xstep) + "/" + str(bullet.ystep)
    #print str((x+bullet.ystep)) + "or" + str(y+bullet.xstep) + "or" + str(x+bullet.ystep) + " or " + str(y+bullet.xstep) #If you're going over an edge
    if (x+bullet.ystep > 24) or (y+bullet.xstep > 59) or (x+bullet.ystep < 0) or (y+bullet.xstep < 0): #If you're going over an edge
        board.room[x][y] = board.roomunder[x][y] #Destroy the old bullet.
        board.statcoords[position] = "pop" #Destroy the stat
        board.playerbullets = board.playerbullets - (bullet.param1 == 0) #Reduce playerbullet count if applicable.
        board.render[x][y] = 1
    elif BulletDict[board.room[x+bullet.ystep][y+bullet.xstep].name] == "solid": #Check for ricochets to deflect off of
        if abs(bullet.ystep) < 2 and abs(bullet.xstep) < 2: #Seriously, check for ricochets.
            move = False
            if board.room[x+bullet.xstep][y+bullet.ystep].name == "ricochet" or board.room[x+bullet.xstep][y+bullet.ystep*-1].name == "ricochet": #Travel N/S, bounce E/W
                #print "T south, B E/W"
                temp = bullet.xstep
                bullet.xstep = bullet.ystep
                bullet.ystep = temp
                move = True
            elif board.room[x-bullet.xstep][y-bullet.ystep].name == "ricochet" or board.room[x+bullet.xstep*-1][y+bullet.ystep].name == "ricochet": #Travel E/W, bounce N/S
                #print "T E/W, B N/S"
                temp = bullet.ystep
                bullet.ystep = bullet.xstep
                bullet.xstep = temp
                move = True
            if move:
                board.render[x][y] = 1 #Render this
                Bullet(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed) #Move again if you're deflecting
            else:
                board.room[x][y] = board.roomunder[x][y] #Destroy the old bullet.
                board.render[x][y] = 1 #Render this
                board.statcoords[position] = "pop" #Destroy the stat
                board.playerbullets = board.playerbullets - (bullet.param1 == 0) #Reduce playerbullet count if applicable.
    elif BulletDict[board.room[x+bullet.ystep][y+bullet.xstep].name] == "walkable": #The bullet can move here no problem.
        board.roomunder[x+bullet.ystep][y+bullet.xstep] = board.room[x+bullet.ystep][y+bullet.xstep] #Put what's about to be covered on the under array
        bullet.background = board.room[x+bullet.ystep][y+bullet.xstep].background #Update graphic in case of fake wall giving us a background
        board.room[x+bullet.ystep][y+bullet.xstep] = bullet #Move the bullet into the new location.
        board.render[x+bullet.ystep][y+bullet.xstep] = 1 #Render this
        board.room[x][y] = board.roomunder[x][y] #Destroy the old bullet.
        board.render[x][y] = 1 #Render this
        board.statcoords[position] = (x+bullet.ystep, y+bullet.xstep) #Update stat location
    elif BulletDict[board.room[x+bullet.ystep][y+bullet.xstep].name] == "hurt": #Haha you got shot what's the matter with you
        if ecycles == 0:
            health = health - 10 #Way to go
            if board.zap == 1:
                #Move player to enterX/enterY coords
                board.render[board.enterY][board.enterX] = 1 #Render this
                board.room[board.enterY][board.enterX] = board.room[board.statcoords[0][0]][board.statcoords[0][1]]
                board.room[board.statcoords[0][0]][board.statcoords[0][1]] = board.roomunder[board.statcoords[0][0]][board.statcoords[0][1]]
                board.statcoords[0] = (board.enterY, board.enterX)
        board.room[x][y] = board.roomunder[x][y] #Destroy the old bullet.
        board.render[x][y] = 1 #Render this
        board.statcoords[position] = "pop" #Destroy the stat
        board.playerbullets = board.playerbullets - (bullet.param1 == 0) #Reduce playerbullet count if applicable.
    elif BulletDict[board.room[x+bullet.ystep][y+bullet.xstep].name] == "destroy":
        shot = board.room[x+bullet.ystep][y+bullet.xstep].name
        score = score + (shot=="lion")+(shot=="bear")+(shot=="head")+(shot=="segment") + (2*(shot=="ruffian"))+(2*(shot=="tiger"))+(2*(shot=="segment" and board.room[x+bullet.ystep][y+bullet.xstep].follownum == 65535)) #Add score for killing built-ins
        
        #Destroy the stat of the destroyed object if it has stats.
        DestroyStat(board, x+bullet.ystep, y+bullet.xstep)
        board.room[x+bullet.ystep][y+bullet.xstep] = board.roomunder[x][y]
        board.render[x+bullet.ystep][y+bullet.xstep] = 1 #Render this
        board.render[x][y] = 1 #Render this
        #If you shot a creature its stat needs to be destroyed as well
        board.room[x][y] = board.roomunder[x][y] #Destroy the old bullet.
        board.statcoords[position] = "pop" #Destroy the stat
        board.playerbullets = board.playerbullets - (bullet.param1 == 0) #Reduce playerbullet count if applicable.
        
    elif BulletDict[board.room[x+bullet.ystep][y+bullet.xstep].name] == "ricochet":
        board.room[x][y].xstep = -1 * board.room[x][y].xstep
        board.room[x][y].ystep = -1 * board.room[x][y].ystep
        #Make it move again 
        board.roomunder[x+bullet.ystep][y+bullet.xstep] = board.room[x+bullet.ystep][y+bullet.xstep] #Put what's about to be covered on the under array
        bullet.background = board.room[x+bullet.ystep][y+bullet.xstep].background #Update graphic in case of fake wall giving us a background
        board.room[x+bullet.ystep][y+bullet.xstep] = bullet #Move the bullet into the new location.
        board.room[x][y] = board.roomunder[x][y] #Destroy the old bullet.
        board.render[x+bullet.ystep][y+bullet.xstep] = 1 #Render this
        board.render[x][y] = 1 #Render this
        board.statcoords[position] = (x+bullet.ystep, y+bullet.xstep) #Update stat location
    elif BulletDict[board.room[x+bullet.ystep][y+bullet.xstep].name] == "Shot":
        Oop.SendJump(board.room[x+bullet.ystep][y+bullet.xstep], ":shot") #Send the object to the label
        board.room[x][y] = board.roomunder[x][y] #Destroy the old bullet.
        board.render[x][y] = 1 #Render this
        board.statcoords[position] = "pop" #Destroy the stat
        board.playerbullets = board.playerbullets - (bullet.param1 == 0) #Reduce playerbullet count if applicable.
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def ChangeBoard(board, input, allboards, x, y, screen, ammo, torches, gems, score, health, keys, tcycles, ecycles, timepassed):
    #See which way you're headed
    if input == "up":
        i1 = 24
        i2 = y
        destination = board.boardnorth
    if input == "down":
        i1 = 0
        i2 = y
        destination = board.boardsouth
    if input == "left":
        i1 = x
        i2 = 59
        destination = board.boardwest
    if input == "right":
        i1 = x
        i2 = 0
        destination = board.boardeast
        
   
    if destination <= 0:
        return ammo, torches, health, tcycles, ecycles, gems, score, keys, timepassed, input, board
    #Check what's occupying the space we want to move to
    
    #A key you already have or a door with a key you don't have
    if (allboards[destination].room[i1][i2].name == "key"):
        slot = KeyDict[allboards[destination].room[i1][i2].foregroundcolor]
        if keys[slot] == 1:
            print "Couldn't walk due to double keys"
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    if (allboards[destination].room[i1][i2].name == "door"):
        slot = DoorDict[allboards[destination].room[i1][i2].backgroundcolor]
        print str(slot) + " this door."
        if keys[slot] == 0:
            print "Couldn't walk due to door"
        else:
            allboards[destination].room[i1][i2] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (i1, i2), 0, 0, 0, 0, 0, 0) #Destroy the door
            keys[slot] = 0
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
            
    #Unlit bombs.
    if (allboards[destination].room[i1][i2].name == "bomb" and allboards[destination].room[i1][i2].param1 == 0):
        allboards[destination].room[i1][i2].param1 = 9
    
    #A player.
    if (allboards[destination].room[i1][i2].name == "player"):
        board = allboards[destination]
        board.render = []
        for x in xrange(0,25):
            board.render.append([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
        timepassed = 0
    #    allboards[destination].room[i1][i2] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (i1, i2), 0, 0, 0, 0, 0, 0)
    
    #Other items
    if allboards[destination].room[i1][i2].name == "ammo" or allboards[destination].room[i1][i2].name == "torch" or allboards[destination].room[i1][i2].name == "gem" or allboards[destination].room[i1][i2].name == "forest":
        item = allboards[destination].room[i1][i2].name
        print "Item: " + item
        ammo = ammo + 5*(item == "ammo")
        print "Ammo: " + str(ammo)
        torches = torches + 1*(item == "torch")
        gems = gems + 1*(item == "gem")
        score = score + 10*(item == "gem")
        health = health + 1*(item == "gem")
        
        if ecycles == 0:
            print "Magic"
            health = health - 10*(item == "lion" or item == "tiger" or item =="bear" or item == "ruffian" or item == "head" or item == "segment")
        allboards[destination].room[i1][i2] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (i1, i2), 0, 0, 0, 0, 0, 0)
    #If we're just walking onto empty space
    if (CollisionDict[allboards[destination].room[i1][i2].name]) == "walkable": #No work needed
        allboards[destination].roomunder[i1][i2] = allboards[destination].room[i1][i2] #Place the empty/fake beneath where the player will soon be
        
        #Destroy the destination board's current player location. This is probably the worst line of code ever.
        allboards[destination].room[allboards[destination].statcoords[0][0]][allboards[destination].statcoords[0][1]] = UnderOver(allboards[destination].room[allboards[destination].statcoords[0][0]][allboards[destination].statcoords[0][1]].underID, allboards[destination].room[allboards[destination].statcoords[0][0]][allboards[destination].statcoords[0][1]].underColor, allboards[destination].statcoords[0])
        allboards[destination].statcoords[0] = (i1, i2) #Update the stat information for the new player's location
        allboards[destination].room[i1][i2] = Tyger.Spawn("player", 2, Tyger.white, Tyger.bgdarkblue, (i1, i2), 0, 0, 1, 0, 0, 0) #Spawn a new player
        
        #Update the desination board's enterX/Y coords for being zapped
        allboards[destination].enterY = i1
        allboards[destination].enterX = i2
        
        #Now jump to the correct board.
        board = allboards[destination]
        
        #Force it to render
        for x in xrange(0,25):
            for y in xrange(0,60):
                board.render[x][y] = 1
                #board.render.append([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
            #print "Appending stuff"
        timepassed = 0
    return ammo, torches, health, tcycles, ecycles, gems, score, keys, timepassed, input, board

def Cheats(ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board, x, y, screen):
    #Rendering fix for breaking the window with long cheats
    for temp in xrange(54,60):
        board.render[14][temp] = 1
    #cheat = raw_input("?")
    cheat = Tyger.TypedInput("$Input your cheat: \n!;\n", "@Cheat!", screen, board)
    cheat = cheat.lower()
    
    #Did you even type anything?
    if cheat == "":
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, "null", board
        
    if cheat == "ammo":
        ammo = ammo + 5
    elif cheat == "torches":
        torches = torches + 3
    elif cheat == "gems":
        gems = gems + 5
    elif cheat == "score":
        score = score + 100
    elif cheat == "health":
        health = health + 50
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].name = "player"
    elif cheat == "dark": #World's dumbest cheat
        print "Lights out!"
        print board.dark
        board.dark = 1
    elif cheat == "-dark" or cheat == "light": #World's greatest cheat
        print "Lights on!"
        board.dark = 0
        if cheat == "-dark":
            flags = Oop.Clear(cheat[1:].upper(), flags)
    elif cheat == "keys":
        keys = [1, 1, 1, 1, 1, 1, 1, 1]
    elif cheat == "time":
        timepassed = timepassed - 30
    elif cheat == "zap":
        if x-1 >= 0:
            board.room[x-1][y] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
            DestroyStat(board, x-1, y)
            board.render[x-1][y] = 1
        if x+1 <= 24:
            board.room[x+1][y] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
            DestroyStat(board, x+1, y)
            board.render[x+1][y] = 1
        if y-1 >=0:
            board.room[x][y-1] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
            DestroyStat(board, x, y-1)
            board.render[x][y-1] = 1
        if y+1 <= 59:
            board.room[x][y+1] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
            DestroyStat(board, x, y+1)
            board.render[x][y+1] = 1
    elif cheat == "idspispopd" or cheat == "noclip":
        global CollisionDict
        global ClipDict
        global NoClipDict
        
        if CollisionDict == ClipDict: #Turn on noclip
            CollisionDict = NoClipDict
            print "Noclip"
        else:
            CollisionDict = ClipDict
            print "Yesclip"
    elif cheat == "energized" or cheat == "iddqd":
        ecycles = -1
    elif cheat == "idfa" or cheat == "idkfa":
        ammo = 32767
        torches = 32767
        gems = 32767
        health = 32767
        if cheat == "idkfa":
            keys = [1, 1, 1, 1, 1, 1, 1, 1]
    elif cheat == "^^vv<><>bastart" or cheat == "^^vv<><>baselectstart":
        health = 3000
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].name = "player"
    elif cheat == "count leaves":
        health = 6
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].name = "player"
        ammo = 9
        torches = 1
        gems = 0
        score = 5
    elif cheat == "kill":
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].name = "RIP"
    elif cheat == "explode":
        Explode(board, board.statcoords[0][0], board.statcoords[0][1], health, ecycles)
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].name = "RIP"
    elif cheat[0] == "+":
        flags = Oop.Set(cheat[1:].upper(), flags)
        print str(flags)
    elif cheat[0] == "-":
        flags = Oop.Clear(cheat[1:].upper(), flags)
    elif cheat[0] == "#" or cheat[0] == "/" or cheat[0] == "?":
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].oop = cheat
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].oopLength = len(cheat)
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].line = 0
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].xstep = 0
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].ystep = 0
        ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board = Object(board, board.statcoords[0][0], board.statcoords[0][1], "null", 0, 0, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, screen)
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, "null", board
    
def CleanBomb(board, x, y):
    #24,59
    for offset in range(-4, 5):
        #Check for borders
        if x-4 < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x-4][y+offset].name == "breakable": #If there's some explosion here
            board.room[x-4][y+offset] = board.roomunder[x-4][y+offset]
            board.render[x-4][y+offset] = 1
    
    for offset in range(-5, 6):
        #Check for borders
        if x-3 < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x-3][y+offset].name == "breakable": #If there's some explosion here
            board.room[x-3][y+offset] = board.roomunder[x-3][y+offset]
            board.render[x-3][y+offset] = 1

    for offset in range(-6, 7):
        #Check for borders
        if x-2 < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x-2][y+offset].name == "breakable": #If there's some explosion here
            board.room[x-2][y+offset] = board.roomunder[x-2][y+offset]
            board.render[x-2][y+offset] = 1

    for offset in range(-6, 7):
        #Check for borders
        if x-1 < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x-1][y+offset].name == "breakable": #If there's some explosion here
            board.room[x-1][y+offset] = board.roomunder[x-1][y+offset]
            board.render[x-1][y+offset] = 1
    
    for offset in range(-7, 8):
        #Check for borders
        if x < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x][y+offset].name == "breakable": #If there's some explosion here
            board.room[x][y+offset] = board.roomunder[x][y+offset]
            board.render[x][y+offset] = 1

    for offset in range(-4, 5):
            #Check for borders
        if x+4 < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x+4][y+offset].name == "breakable": #If there's some explosion here
            board.room[x+4][y+offset] = board.roomunder[x+4][y+offset]
            board.render[x+4][y+offset] = 1

    for offset in range(-5, 6):
            #Check for borders
        if x+3 < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x+3][y+offset].name == "breakable": #If there's some explosion here
            board.room[x+3][y+offset] = board.roomunder[x+3][y+offset]
            board.render[x+3][y+offset] = 1

    for offset in range(-6, 7):
            #Check for borders
        if x+2 < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x+2][y+offset].name == "breakable": #If there's some explosion here
            board.room[x+2][y+offset] = board.roomunder[x+2][y+offset]
            board.render[x+2][y+offset] = 1
    
    for offset in range(-6, 7):
            #Check for borders
        if x+1 < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x+1][y+offset].name == "breakable": #If there's some explosion here
            board.room[x+1][y+offset] = board.roomunder[x+1][y+offset]
            board.render[x+1][y+offset] = 1
            
    #Lastly, destroy the bomb itself.
    DestroyStat(board, x, y)
    #print str(board.roomunder[x][y])
    board.room[x][y] = board.roomunder[x][y]
    board.render[x][y] = 1
    
def Clockwise(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed):
    #\ | / -
    
    #Figure out the 9 important elements
    #border = [board.room[x-1][y-1], board.room[x-1][y], board.room[x-1][y+1],
    #        board.room[x][y-1], board.room[x][y+1], 
    #        board.room[x+1][y-1], board.room[x+1][y], board.room[x+1][y+1]]
    
    border = [board.room[x-1][y-1], board.room[x-1][y], board.room[x-1][y+1],
             board.room[x][y+1], board.room[x+1][y+1], board.room[x+1][y], board.room[x+1][y-1],
             board.room[x][y-1]]
    
    new = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    final = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    #new = border #8 is special and just used to be assigned back to 0
    #new.append("EXTRA")

    start = 0
    temp = 0
    while temp < 8: #was 8
        print "ON #", temp
        newtext = ""
        finaltext = ""
        #print border[temp].name, "IS THE NAME"
        if ConveyDict[border[temp].name] == "next":
            print "Appending", border[temp].name, "to NEW"
            new[temp+1] = border[temp] #Put the element in the next spot of the array to be the final results
            temp = temp + 1
            
        elif ConveyDict[border[temp].name] == "stop":
            for num in xrange(0,8):
                if new[num] != 0:
                    final[num-1] = new[num]
            final[temp+1] = border[temp]
            new = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Reset the new buffer
            print "final WITH TEMP", temp, final
            temp = temp + 1
        else:#go
            #new[temp+1] = border[temp] #Put the empty in the next spot of the array to be the final results
            #temp = temp + 1
            for num in xrange(0,9):
                if new[num] != 0:
                    final[num] = new[num]
            new = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Reset the new buffer
            print "FINAL WITH TEMP", temp, final, "\n"
            temp = temp + 1

    #Properly move the final tile.
    #new[0] = new[8]
    #new.pop(8)
    print "------------ cleanup"
    #Cleanup
    for num in xrange(0,9):
        if new[num] != 0:
            print "Appending", new[num].name
            final[num] = new[num]
        else:
            print "LENGTHS FIN, BORD", len(final), len(border)
            print "And num is", num
            try:
                final[num] = border[num]
            except:
                print "OH NO"

    
    #print "FINAL", str(final[0]), str(final[8])
    final[0] = final[-1]
    #print str(final[0])
    
    #final.pop(8)
    
    for thing in final:
        try:
            print thing.name
        except:
            print str(thing)
    
    
    board.room[x-1][y-1]= final[0]
    board.room[x-1][y]  = final[1]
    board.room[x-1][y+1]= final[2]
    board.room[x][y+1]  = final[3]
    board.room[x+1][y+1]= final[4]
    board.room[x+1][y]  = final[5]
    board.room[x+1][y-1]= final[6]
    board.room[x][y-1]  = final[7]
    
    
    #Tyger.Spawn("solid", 65, Tyger.blue, Tyger.bgblack, (0, 0), 0, 0, 0, 0, 0, 0)
    blah = 0
    #blah = raw_input("Hit enter!")
    if blah == "x":
        exit()
    
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
    
def CreatureMove(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed):
    choices = [] #Possible ways to move
    canseek = False #Is it possible to move seek if the creature wants to?
    
    #If it matters, we'd like to know what kind of creature we're dealing with.
    creature = board.room[x][y].name
    #print "I'm a", creature, board.room[x][y].xstep, board.room[x][y].ystep
    #Figure out which way is seek
    
    if creature != "ruffian" or (board.room[x][y].xstep == 0 and board.room[x][y].ystep == 0):
        if ecycles != 0: #Energizers make smart creatures run away.
            temp = "opp seek"
        else:
            temp = "seek"
        seekdir = ParseDir([temp], x, y, board.statcoords[0][0], board.statcoords[0][1], board.room[x][y].xstep, board.room[x][y].ystep)
        if x+WalkDict[seekdir][1] < 0 or x+WalkDict[seekdir][1] >= 25 or y+WalkDict[seekdir][0] < 0 or y+WalkDict[seekdir][0] >= 60:
            None
        else:
            if board.room[x+WalkDict[seekdir][1]][y+WalkDict[seekdir][0]].name == "empty" or board.room[x+WalkDict[seekdir][1]][y+WalkDict[seekdir][0]].name == "fake" or board.room[x+WalkDict[seekdir][1]][y+WalkDict[seekdir][0]].name == "player":
                canseek = True
                #choices.append(seekdir)    
        if y+1 < 60:
            if board.room[x][y+1].name == "empty" or board.room[x][y+1].name == "fake" or board.room[x][y+1].name == "player":
                choices.append("e")
        if y-1 > 0:
            if board.room[x][y-1].name == "empty" or board.room[x][y-1].name == "fake" or board.room[x][y-1].name == "player":
                choices.append("w")
        if x+1 < 25:
            if board.room[x+1][y].name == "empty" or board.room[x+1][y].name == "fake" or board.room[x+1][y].name == "player":
                choices.append("s")
        if x-1 > 0:
            if board.room[x-1][y].name == "empty" or board.room[x-1][y].name == "fake" or board.room[x-1][y].name == "player":
                choices.append("n")
        if len(choices) == 0:
            choices.append("i")
        
        #Decide if the creature will try to move seek or randomly
        if (canseek == False) or (rnd(1, 10) >= board.room[x][y].param1 + 1): #Move randomly
            dir = choices[rnd(0,len(choices)-1)]
            if dir == "i": #Give it up creature. You're surrounded.
                return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        else: #Move seek
            dir = seekdir
        #If you're a ruffian, change x/y-step
        if creature == "ruffian":
            print "I need to change my X/Y step!"
            board.room[x][y].xstep, board.room[x][y].ystep = WalkDict[dir]
            print board.room[x][y].xstep, board.room[x][y].ystep
            #board.room[x][y].ystep = 
    else: #Ruffian related work
        #Convert the X/Ysteps into a proper direction
        dir = FlowDict[(board.room[x][y].xstep, board.room[x][y].ystep)]
        
        #Ruffians will revert to idling if they hit a border.
        #if (x-(dir == "n") <= 0 ) or (x+(dir == "s") > 25 ) or (y-(dir == "w") <= 0 ) or (y+(dir == "e") > 60 ):
        #    board.room[x][y].xstep = 0
        #    board.room[x][y].ystep = 0
        #    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
            
        if x-(dir == "n") < 0 or x+(dir == "s") > 24 or y-(dir == "w") < 0 or y + (dir == "e") > 59:
            print "That will crash"
            board.room[x][y].xstep = 0
            board.room[x][y].ystep = 0
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        if board.room[x-(dir=="n")+(dir =="s")][y-(dir=="w")+(dir=="e")].name != "empty":
            print "Can't go there"
            board.room[x][y].xstep = 0
            board.room[x][y].ystep = 0
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
    
    #print "I'm going to move...", dir
    #Now move it!
    if board.room[x+WalkDict[dir][1]][y+WalkDict[dir][0]].name == "player": #Hurt the player
        if ecycles == 0:
            health = health - 10 #Way to go
            if board.zap == 1:
                #Move player to enterX/enterY coords
                board.room[board.enterY][board.enterX] = board.room[board.statcoords[0][0]][board.statcoords[0][1]]
                board.room[board.statcoords[0][0]][board.statcoords[0][1]] = board.roomunder[board.statcoords[0][0]][board.statcoords[0][1]]
                board.statcoords[0] = (board.enterY, board.enterX)
        board.room[x][y] = board.roomunder[x][y] #Destroy the creature
        board.render[x][y] = 1
        board.statcoords[position] = "pop" #Destroy the creature's stat
    else:
        board.room[x+WalkDict[dir][1]][y+WalkDict[dir][0]] = board.room[x][y] #Move the creature
        board.room[x][y] = board.roomunder[x][y] #Remove the old creature
        board.render[x][y] = 1
        board.render[x+WalkDict[dir][1]][y+WalkDict[dir][0]] = 1
        UpdateStat(board, x, y, x+WalkDict[dir][1], y+WalkDict[dir][0]) #Update its stat
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
def DestroyStat(board, x, y):
    #Does anything have these coordinates?
    for temp in range(0, len(board.statcoords)):
        if board.statcoords[temp] == (x, y):
            board.statcoords[temp] = "pop"
            break

def DieItem(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, item, allboards, screen):
    injured = False
    
    board.render[x][y] = 1 #Render
    board.render[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")] = 1 #render
    
    #Update stats
    ammo = ammo + 5*(item == "ammo")
    torches = torches + 1*(item == "torch")
    gems = gems + 1*(item == "gem")
    score = score + 10*(item == "gem")
    health = health + 1*(item == "gem")
    
    if item == "energizer":
        ecycles = 75
        Oop.Send("#all:energize", board, None, -1, -1)
        
    if ecycles == 0:
            health = health - 10*(item == "lion" or item == "tiger" or item =="bear" or item == "ruffian" or item == "head" or item == "segment" or item == "bullet" or item == "star")
            if item == "lion" or item == "tiger" or item =="bear" or item == "ruffian" or item == "head" or item == "segment" or item == "bullet" or item == "star":
                injured = True
    
    #Keys
    if board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].name == "key":
        slot = KeyDict[board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].foregroundcolor]
        if keys[slot] == 1:
            Oop.MessageLine("You already have a " + KeyIndexDict[slot] + " key!", screen, board, "Low")
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        Oop.MessageLine("You now have the " + KeyIndexDict[slot] + " key.", screen, board, "Low")
        keys[slot] = 1
        
    #Doors
    if board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].name == "door":
        slot = DoorDict[board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].backgroundcolor]
        if keys[slot] == 0:
            Oop.MessageLine("The " + KeyIndexDict[slot] + " door is locked!", screen, board, "Low")
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        keys[slot] = keys[slot-1]
        print "Door opened!"
    
    #Pretend to be an empty so the player can walk on you
    #And kill the stat
    DestroyStat(board, x+(input=="down")-(input=="up"), y+(input=="right")-(input=="left"))
    board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
    
    if board.zap == 1 and injured == True:
        #Move player to enterX/enterY coords
        print "Welp " + str(board.enterX) + " | " + str(board.enterY)
        board.room[board.enterY][board.enterX] = board.room[x][y]
        board.statcoords[0] = (board.enterY, board.enterX)
        board.room[x][y] = board.roomunder[x][y]
        
        #Reset the Time remaining
        timepassed = 0
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
    #print "REFERENCE ---------------------------------------------------------"
    #print str(board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")])
    #Make the player try to move again onto the tile which is now an "empty"
    Player(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, allboards, screen)
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
def Explode(board, x, y, health, ecycles):
    #24,59
    
    
    
    for offset in range(-4, 5):
        #Check for borders
        if x-4 < 0: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x-4][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x-4, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x-4][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x-4][y+offset] = board.roomunder[x-4][y+offset]
            else:
                board.room[x-4][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x-4][y+offset].name] == "bombed": #If the thing is an object
            Oop.SendJump(board.room[x-4][y+offset], ":bombed")
            print "YOU'RE ALL BLOODY DEAD A"
        elif BombDict[board.room[x-4][y+offset].name] == "hurt" and ecycles == 0: #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10
        board.render[x-4][y+offset] = 1
    
    for offset in range(-5, 6):
        #Check for borders
        if x-3 < 0: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x-3][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x-3, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x-3][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x-3][y+offset] = board.roomunder[x-3][y+offset]
            else:
                board.room[x-3][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x-3][y+offset].name] == "bombed": #If the thing is an object
            Oop.SendJump(board.room[x-3][y+offset], ":bombed")
            print "YOU'RE ALL BLOODY DEAD -5,6"
        elif BombDict[board.room[x-3][y+offset].name] == "hurt": #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10
        board.render[x-3][y+offset] = 1

    for offset in range(-6, 7):
        #Check for borders
        if x-2 < 0: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x-2][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x-2, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x-2][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x-2][y+offset] = board.roomunder[x-2][y+offset]
            else:
                board.room[x-2][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x-2][y+offset].name] == "bombed": #If the thing is an object
            Oop.SendJump(board.room[x-2][y+offset], ":bombed")
            print "YOU'RE ALL BLOODY DEAD -6,7"
        elif BombDict[board.room[x-2][y+offset].name] == "hurt": #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10    
        board.render[x-2][y+offset] = 1
    
    for offset in range(-6, 7):
        #Check for borders
        if x-1 < 0: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x-1][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x-1, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x-1][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x-1][y+offset] = board.roomunder[x-1][y+offset]
            else:
                board.room[x-1][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x-1][y+offset].name] == "bombed": #If the thing is an object
            Oop.SendJump(board.room[x-1][y+offset], ":bombed")
            print "YOU'RE ALL BLOODY DEAD C"
        elif BombDict[board.room[x-1][y+offset].name] == "hurt": #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10   
        board.render[x-1][y+offset] = 1
    
    for offset in range(-7, 8):
        #Check for borders
        if x < 0: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x][y+offset] = board.roomunder[x][y+offset]
            else:
                board.room[x][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x][y+offset].name] == "bombed": #If the thing is an object
            Oop.SendJump(board.room[x][y+offset], ":bombed")
            print "YOU'RE ALL BLOODY DEAD D"
        elif BombDict[board.room[x][y+offset].name] == "hurt": #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10   
        board.render[x][y+offset] = 1
    
    for offset in range(-4, 5):
        #Check for borders
        if x+4 > 24: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x+4][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x+4, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x+4][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x+4][y+offset] = board.roomunder[x+4][y+offset]
            else:
                board.room[x+4][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x+4][y+offset].name] == "bombed": #If the thing is an object
            print board.room[x+4][y+offset].oop
            Oop.SendJump(board.room[x+4][y+offset], ":bombed")
            print "YOU'RE ALL BLOODY DEAD E"
        elif BombDict[board.room[x+4][y+offset].name] == "hurt": #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10
        board.render[x+4][y+offset] = 1
    
    for offset in range(-5, 6):
        #Check for borders
        if x+3 > 24: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x+3][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x+3, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x+3][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x+3][y+offset] = board.roomunder[x+3][y+offset]
            else:
                board.room[x+3][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x+3][y+offset].name] == "bombed": #If the thing is an object
            Oop.SendJump(board.room[x+3][y+offset], ":bombed")
            print "YOU'RE ALL BLOODY DEAD F"
        elif BombDict[board.room[x+3][y+offset].name] == "hurt": #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10
        board.render[x+3][y+offset] = 1

    for offset in range(-6, 7):
        #Check for borders
        if x+2 > 24: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x+2][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x+2, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x+2][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x+2][y+offset] = board.roomunder[x+2][y+offset]
            else:
                board.room[x+2][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x+2][y+offset].name] == "bombed": #If the thing is an object
            Oop.SendJump(board.room[x+2][y+offset], ":bombed")
            print "YOU'RE ALL BLOODY DEAD G"
        elif BombDict[board.room[x+2][y+offset].name] == "hurt": #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10    
        board.render[x+2][y+offset] = 1
    
    for offset in range(-6, 7):
        #Check for borders
        if x+1 > 24: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x+1][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x+1, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x+1][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x+1][y+offset] = board.roomunder[x+1][y+offset]
            else:
                board.room[x+1][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x+1][y+offset].name] == "bombed": #If the thing is an object
            print board.room[x+1][y+offset].oop
            Oop.SendJump(board.room[x+1][y+offset], ":bombed")
            print "YOU'RE ALL BLOODY DEAD H"
        elif BombDict[board.room[x+1][y+offset].name] == "hurt" and ecycles == 0: #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10
        board.render[x+1][y+offset] = 1
    
    return health

def Invisible(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, item):
    board.render[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")] = 1
    board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].name = "normal"
    if board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].param1 > 0:
        board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].character = board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].param1
    else:
        board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].character = 178
    board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].image = Tyger.makeimage(board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].character, board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].foreground, board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].background)
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def Lion(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed):
    CreatureMove(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def Monitor(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, world, allboards, screen):
    if input == "p":
        Tyger.playgame(world, allboards, screen)
        input = "playgame"
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def Object(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, screen):
    #print "I am being called on"
    object = board.room[x][y]
    progress = 0
    Moved = True
    NoAdvance = False
    #IfCmd = False
    #Retry = False
    #print str(object.line)
    while progress < 33: #Only 33 non-cycle ending commands can be executed at once.
        #print "In the loop"
        progress = progress + 1
        if (object.oop == None) or (object.line == -1): #No oop, no work
            #print "Current line # is... " + str(object.line)
            #print "Early break"
            break
        
        #print "Executing line...", object.line, object.oop[object.line:object.line+25]
        #print object.oop[object.line:]
        current = object.oop[object.line:].split("\n")[0]
        while current == "":
            #print "Yikes"
            object.line = object.line + 1 #Was +2
            if object.line >= object.oopLength:
                
                break
            #print "Line is... " + str(object.line + 1)
            #print str(object.oop[object.line + 1])
            current = object.oop[object.line:].split("\n")[0]
            #print "Blank lines..."
        if (object.line >= object.oopLength) or (object.line < 0):
            object.line = -1
            #print "Breaking"
            break
            
        #print "Object's line# is...", object.line
        if current[0] == "#" or current[0] == "/" or current[0] == "?" or current[0] == ":":
            #print "Formatting # oop"
            current = current.lower()
        if current[0] == " ":
            current = "_" + current[1:] #Replace space with an underscore for now!
        #print current + " " + str(object.line) + "           -Current command/line"
        if current == "\n" or current == "\r":
            #print "NEWLINE"
            current = "A NEWLINE"
        #Interpret any possible command:
        #print "++++", current + "=-=-=-="
        if current.split(" ")[0] == "#become": #Ends!
            #print "I don't know shit, we gonna keep movin"
            board.room[x][y], NoAdvance = Oop.Become(current.split(" ")[1:], board, x, y, current)
        elif current.split(" ")[0] == "#bind": #
            #print "A long body or tentacles are used to bind and squeeze the foe for two to five turns. It's super effective!\r"
            object = Oop.CopyCode(board, current.split(" ")[1], object)
            #print "Ok I'm at...", object.line
            continue #Maybe?
            #progress = 100
        elif current.split(" ")[0] == "#change": #Continues
            Oop.Change(current.split(" ")[1:], board, x, y, current)
        elif current.split(" ")[0] == "#char": #Continues
            object.param1 = Oop.Char(current.split(" ")[1])
            board.render[x][y] = 1
        elif current.split(" ")[0] == "#clear": #Continues
            Oop.Clear(current.split(" ")[1].upper(), flags)
        elif current.split(" ")[0] == "#cycle": #Continues
            object.cycle = Oop.Cycle(current.split(" ")[1], object.cycle)
        elif current.split(" ")[0] == "#die": #Ends!
            board.room[x][y] = Oop.Die(board, x, y)
            break
        elif current.split(" ")[0] == "#end": #Ends
            object.line = -1
            break
        elif current.split(" ")[0] == "#endgame": #Continues
            health = 0
        elif current.split(" ")[0] == "#give": #Continues
            ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys, NoAdvance = Oop.Give(ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys, current, board, NoAdvance)
        elif current.split(" ")[0] == "#go" or current.split(" ")[0] == "#try" or current.split(" ")[0][0] == "/" or current.split(" ")[0][0] == "?": #Ends
            #print "Calling on a go!"
            NoAdvance, Moved, progress = Oop.Go(current, x, y, board, object, NoAdvance, Moved, progress)
        elif current.split(" ")[0] == "#if": #Continues
            NoAdvance, Moved, object = Oop.If(current, object, x, y, board, ecycles, flags)
        elif current.split(" ")[0] == "#idle": #Ends
            progress = 100
        elif current.split(" ")[0] == "#lock": #Continues
            object.param2 = 1
        elif current.split(" ")[0] == "#play": #Continues
            print "I got my problems, and my problems they got me...\r"
        elif current.split(" ")[0] == "#put": #Continues
            #Oop.TextBox("Line pre #put" + str(object.line) + "\n", "-= Tyger Debug Info =-", screen)
            Oop.Put(board, current, x, y)
            #Oop.TextBox("Line post #put" + str(object.line) + "\n", "-= Tyger Debug Info =-", screen)
            #print NoAdvance, "is NOADVANCE!"
            #NoAdvance = False
        elif current.split(" ")[0] == "#restart": #Continues
            object.line = 0
            continue
        elif current.split(" ")[0] == "#restore": #continues
            object, board = Oop.Restore(object, board, current.split(" ")[1])
        elif current.split(" ")[0] == "#set": #continues
            flags = Oop.Set(current.split(" ")[1], flags)
        elif current.split(" ")[0] == "#shoot" or current.split(" ")[0] == "#throwstar": #Ends
            progress = 100
            health = Oop.Shoot(current, x, y, board, object, health)
        elif current.split(" ")[0] == "#take": #Continues
            ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys = Oop.Take(ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys, current)
            
        elif current.split(" ")[0] == "#unlock": #continues
            object.param2 = 0
        elif current.split(" ")[0] == "#walk": #Continues
            object.xstep, object.ystep = Oop.Walk(current, x, y, board, object)
        elif current.split(" ")[0] == "#zap": #Continues
            object, board = Oop.Zap(object, board, current.split(" ")[1])
        elif current.split(" ")[0] == "#send" or current.split(" ")[0][0] == "#":
            NoAdvance = Oop.Send(current, board, object, x, y)
        else: #Message Continues
            #print "WE HAVE A MESSAGE HERE!!!!"
            try:
                if current.split(" ")[0][0] != "#" and current.split(" ")[0][0] != "/" and current.split(" ")[0][0] != "?" and current.split(" ")[0][0] != "@" and current.split(" ")[0][0] != ":" and current.split(" ")[0][0] != "'":
                    NoAdvance, object = Oop.Message(object, screen, board)
                    #print "---------------" + current + "---------------"
            except IndexError:
                NoAdvance, object = Oop.Message(object, screen, board)
                #print "---------------" + current + "-----indexerror"
            #progress = progress - 1 #I don't think this is needed when the actual message box exists
        
    #Move to the next line if you're still going
        
        #print str(object.line) + " " + str(Moved) + " " + str(NoAdvance)
        #print "CODE CHECK!"
        if object.line != -1 and Moved == True and NoAdvance == False:
            #print "Advancing code"
            object.line = object.line + len(current) + 1
        """else:
            print "Didn't advance code automatically because..."
            if Moved == False:
                print "Moved is false!"
            if NoAdvance == True:
                print "NoAdvance is True!" """
        #print "Line is... " + str(object.line)
        #print str(object.oop[object.line + 1])
        if object.line >= object.oopLength:
            object.line = -1
            break
        
        NoAdvance = False
        Moved = True #Maybe? Play Fridgeraid to find out for sure.
        
        #if progress == 100: #No idea about this.
        #    print "Breaking progress!"
        #    break 
    #Post oop handling
    #if object.oopLength != 0:
        #print "Done OOPing about " + str(object.line) + " | " + str(object.oopLength)
    
    #Now get walking if you walk
    if object.xstep > 127:
        object.xstep = object.xstep-65536
    if object.ystep > 127:
        object.ystep = object.ystep-65536
    
    if (object.xstep != 0 or object.ystep != 0): #If you need to walk
        if (x+object.ystep) > 24 or (y+object.xstep) > 59 or (x+object.ystep) < 0 or (y+object.xstep) < 0: #Check for the board edge
            Oop.SendJump(object, ":thud")
        elif board.room[x+object.ystep][y+object.xstep].name == "fake" or board.room[x+object.ystep][y+object.xstep].name == "empty":
            board.roomunder[x+object.ystep][y+object.xstep] = board.room[x+object.ystep][y+object.xstep] #Put the fake on the under layer
            board.room[x+object.ystep][y+object.xstep] = object #Move the object
            board.room[x][y] = board.roomunder[x][y] #Destroy the old object and update its stat
            UpdateStat(board, x, y, x+object.ystep, y+object.xstep)
            board.render[x][y] = 1
            board.render[x+object.ystep][y+object.xstep] = 1
        else:
            Oop.SendJump(object, ":thud")
    #print "Returning!"
    #print "---------------------------------DONE!"
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board


def ParseDir(input, x, y, Px, Py, xstep, ystep):
    #print "Input is... " + str(input) + " " + str(len(input))
    choices = []
    #Tyger.Dprint(str(input))
    #blah = raw_input("Hit enter")
    if len(input) == 1:
        input = input[0].split(" ") #Fix for /opp seek
    if (input[0] == "n") or (input[0] == "s") or (input[0] == "e") or (input[0] == "w") or (input[0] == "i"):
        return input[0]
    elif input[0] == "flow":
        return FlowDict[(xstep,ystep)]
    elif input[0] == "seek":
        #if (Px == x):
        #    print "Matching X's!"
        if (Px < x): #If the player is to your left
            choices.append("n")
        elif (Px > x):
            choices.append("s")
        #if (Py == y):
        #    print "Matching Y's!"
        if (Py < y): #if the player is above you
            choices.append("w")
        elif (Py > y):
            choices.append("e")
        try:
            output = Tyger.random.sample(choices, 1)[0]
        except ValueError:
            output = "i"
        return output
    elif input[0] == "rndns":
        return Tyger.random.sample(["n", "s"], 1)[0]
    elif input[0] == "rndne":
        return Tyger.random.sample(["n", "e"], 1)[0]
    elif input[0] == "rnd":
        return Tyger.random.sample(["n", "s", "e", "w"], 1)[0]
    elif input[0] == "cw":
        key = input[1]
        if key == "seek":
            key = ParseDir([input[1]], x, y, Px, Py, xstep, ystep)
        elif key == "flow":
            return CwDict[FlowDict[(xstep, ystep)]]
        elif key == "rndns":
            return Tyger.random.sample(["e", "w"], 1)[0] #cw from N/S is E/W
        elif key == "rndne":
            return Tyger.random.sample(["e", "s"], 1)[0] #cw from N/E is E/S
        elif key == "rnd":
            return Tyger.random.sample(["n", "s", "e", "w"], 1)[0] #I hate you.
        return CwDict[key]
    elif input[0] == "ccw":
        key = input[1]
        if key == "seek":
            key = ParseDir([input[1]], x, y, Px, Py, xstep, ystep)
        elif key == "flow":
            return CcwDict[FlowDict[(xstep, ystep)]]
        elif key == "rndns":
            return Tyger.random.sample(["e", "w"], 1)[0] #ccw from N/S is E/W
        elif key == "rndne":
            return Tyger.random.sample(["e", "s"], 1)[0] #ccw from N/E is E/S
        elif key == "rnd":
            return Tyger.random.sample(["n", "s", "e", "w"], 1)[0] #I hate you.
        return CcwDict[key]
    elif input[0] == "opp":
        key = input[1]
        if key == "seek":
            key = ParseDir([input[1]], x, y, Px, Py, xstep, ystep)
        elif key == "flow":
            return OppDict[FlowDict[(xstep, ystep)]]
        elif key == "rndns":
            return Tyger.random.sample(["n", "s"], 1)[0]
        elif key == "rndne":
            return Tyger.random.sample(["s", "w"], 1)[0]
        elif key == "rnd":
            return Tyger.random.sample(["n", "s", "e", "w"], 1)[0] #I hate you.
        return OppDict[key]
    elif input[0] == "rndp":
        key = input[1]
        if key == "seek":
            key = ParseDir([input[1]], x, y, Px, Py, xstep, ystep)
        elif key == "flow":
            return Tyger.random.sample(RndpDict[FlowDict[(xstep, ystep)]], 1)[0]
        elif key == "rndns":
            return Tyger.random.sample(["e", "w"], 1)[0]
        elif key == "rndne" or key == "rnd":
            return Tyger.random.sample(["n", "s", "e", "w"], 1)[0] #I hate you.
        return Tyger.random.sample(RndpDict[key], 1)[0]
    print "You sent an invalid direction, I'll just idle." + str(input[0]) + " | " + str(input)
    return "i"

def Passage(board, input, allboards, x, y, screen, ammo, torches, gems, score, health, keys, tcycles, ecycles, timepassed, targetA, targetB, flags):
    #Find the board we're to travel to and the important passage color
    destination = board.room[targetA][targetB].param3
    color = board.room[targetA][targetB].background
    fg = board.room[targetA][targetB].foregroundcolor
    
    #Is there a passage on this board with a matching background of the one we entered?
    passage = False
    for temp in range(0, len(allboards[destination].statcoords)):
        target = allboards[destination].statcoords[temp]
        if allboards[destination].room[target[0]][target[1]].name == "passage" and allboards[destination].room[target[0]][target[1]].background == color and allboards[destination].room[target[0]][target[1]].foregroundcolor == fg:
            passage = True
            break
            
    if passage == False: #There's no passage on the destination board that meets our requirements
        print "Placing player where he currently is on that board."
        target = allboards[destination].statcoords[0] #We'll have to place you where the player is standing instead    
    #Destroy the destination board's current player location. This is probably the worst line of code ever and yet I have to use it again.
    allboards[destination].room[allboards[destination].statcoords[0][0]][allboards[destination].statcoords[0][1]] = UnderOver(allboards[destination].room[allboards[destination].statcoords[0][0]][allboards[destination].statcoords[0][1]].underID, allboards[destination].room[allboards[destination].statcoords[0][0]][allboards[destination].statcoords[0][1]].underColor, allboards[destination].statcoords[0])
    
    allboards[destination].statcoords[0] = target #Update the stat information for the new player's location
    
    if passage == True: #If there is a passage we have to put it on the under layer so the player doesn't crush it with his fat.
        allboards[destination].roomunder[target[0]][target[1]] = allboards[destination].room[target[0]][target[1]]
    
    #Then spawn the player in the proper position
    allboards[destination].room[target[0]][target[1]] = Tyger.Spawn("player", 2, Tyger.white, Tyger.bgdarkblue, (target[0], target[1]), 0, 0, 1, 0, 0, 0) #Spawn a new player
    
    #Now jump to the correct board.
    board = allboards[destination]
    
    #Render board
    for x in xrange(0,25):
        for y in xrange(0,60):
            board.render[x][y] = 1
    input = "null"
    
    #Set time and things
    timepassed = 0
    board.enterY = target[0]
    board.enterX = target[1]
    
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board


def Player(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, allboards, screen):
    #Reduce your energizer/tcycles and change graphics accordingly
    if tcycles > 0:
        tcycles = tcycles - 1
    if ecycles != 0:
        ecycles = ecycles - 1
        
        #Rerender
        board.render[x][y] = 1
        
        #Energizer Colors
        EnerDict = {0:Tyger.bgdarkgreen, 1:Tyger.bgdarkpurple, 2:Tyger.bgdarkblue, 3:Tyger.bgdarkred, 4:Tyger.bggray, 5:Tyger.bgdarkcyan, 6:Tyger.bgdarkyellow}
        
        #print str(board.room[x][y].background)
        #Update char (alternate between char 1 and 2)
        if board.room[x][y].character == 1 or ecycles == 0:
            board.room[x][y].character = 2            
        else:
            board.room[x][y].character = 1
        
        #Update color
        board.room[x][y].background = EnerDict[cycles % 7]
        if ecycles == 0:
            board.room[x][y].background = Tyger.bgdarkblue
    
    #Pausing
    #if input == "p":
    #    print "PAUSED"
    #    pygame.event.clear()
    #    event = pygame.event.wait()
    #    print str(event) + " 000"
    
    #Torch usage
    if board.dark != 0 and torches > 0 and tcycles == 0 and input == "Torch":
        torches = torches - 1
        tcycles = 196
    #Special Inventory Button
    if input == "Inventory":
        print "Iventory"
        if "I" in flags:
            "Flag found"
            Oop.Clear("I", flags)
            input = "null"
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        else:
            print "Flag I isn't set"
            flags = Oop.Set("I", flags)
            input = "null"
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    #Special Reload Button
    if input == "Reload":
        print "Reloading"
        if "R" in flags:
            "Flag found"
            Oop.Clear("R", flags)
            input = "null"
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        else:
            print "Flag R isn't set"
            flags = Oop.Set("R", flags)
            input = "null"
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
   
    #Oop based input
    if input[0] == "#" or input[0] == "/" or input[0] == "?":
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].oop = input
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].oopLength = len(input)
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].line = 0
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].xstep = 0
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].ystep = 0
        ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board = Object(board, board.statcoords[0][0], board.statcoords[0][1], "null", 0, 0, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, screen)
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
   
    #Cheating
    if input == "cheat":
        print "CHEATS"
        return Cheats(ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board, x, y, screen)
    #Board switching
    if (input == "up" and (x-1 < 0)) or (input == "down" and (x+1 > 24)) or (input == "left" and (y-1 < 0)) or (input == "right" and (y+1 > 59)): #Walking off the edge
        ammo, torches, health, tcycles, ecycles, gems, score, keys, timepassed, input, board = ChangeBoard(board, input, allboards, x, y, screen, ammo, torches, gems, score, health, keys, tcycles, ecycles, timepassed)
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

    #Shooting
    if input == "shootup" or input == "shootdown" or input == "shootleft" or input == "shootright":
            if ammo > 0 and (board.playerbullets + 1 <= board.shots) and (((x-1 >= 0) and input == "shootup") or ((x+1 <= 25) and input == "shootdown") or ((y-1 >= 0) and input == "shootleft") or ((y+1 <= 60) and input == "shootright")): #also make sure you can shoot another bullet (as in a 5th bullet when the limit is 4)
                #print "Playerbullets: " + str(board.playerbullets)
                tile = board.room[x-(input == "shootup")+(input == "shootdown")][y-(input == "shootleft")+(input == "shootright")]
                
                #Handle spawning a bullet if you should
                if tile.name == "empty":
                    bullet = Tyger.Spawn("bullet", 248, Tyger.white, Tyger.bgblack, tile.coords, ((input=="shootright") - (input=="shootleft")), ((input=="shootdown") - (input=="shootup")), 1, 0, 0, 0)
                elif tile.name == "fake" or tile.name == "water":
                    board.roomunder[x-(input == "shootup")+(input == "shootdown")][y-(input == "shootleft")+(input == "shootright")] = board.room[x-(input == "shootup")+(input == "shootdown")][y-(input == "shootleft")+(input == "shootright")]
                    bullet = Tyger.Spawn("bullet", 248, Tyger.white, board.room[x-(input == "shootup")+(input == "shootdown")][y-(input == "shootleft")+(input == "shootright")].background, tile.coords, ((input=="shootright") - (input=="shootleft")), ((input=="shootdown") - (input=="shootup")), 1, 0, 0, 0)
                elif tile.name == "object" and Tyger.options[4] == "True": #Point blank shooting option
                    Oop.SendJump(board.room[x-(input == "shootup")+(input == "shootdown")][y-(input == "shootleft")+(input == "shootright")], ":shot") #Send the object to the label
                    ammo = ammo - 1
                    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
                elif tile.name == "breakable": #Breakable walls can be shot at point blank
                    board.room[x-(input == "shootup")+(input == "shootdown")][y-(input == "shootleft")+(input == "shootright")] = board.roomunder[x-(input == "shootup")+(input == "shootdown")][y-(input == "shootleft")+(input == "shootright")]
                    DestroyStat(board, x-(input == "shootup")+(input == "shootdown"), y-(input == "shootleft")+(input == "shootright"))
                    ammo = ammo - 1
                    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
                else: #Otherwise we can't spawn a bullet
                    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
                
                ammo = ammo - 1
                board.playerbullets = board.playerbullets + 1
                board.room[x-(input == "shootup")+(input == "shootdown")][y-(input == "shootleft")+(input == "shootright")] = bullet
                board.render[x-(input == "shootup")+(input == "shootdown")][y-(input == "shootleft")+(input == "shootright")] = 1
                board.statcoords.append((x-(input == "shootup")+(input == "shootdown"), y-(input == "shootleft")+(input == "shootright")))
            else:
                if board.shots == 0:
                    print "Can't shoot in this place!"
                if ammo < 1:
                    print "Not enough ammo!"
                return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    #Moving
    
    #Check for no-stick clones
    
    if input == "up":
        targetA = x-1
        targetB = y
    elif input == "down":
        targetA = x+1
        targetB = y
    elif input == "left":
        targetA = x
        targetB = y-1
    elif input == "right":
        targetA = x
        targetB = y+1
    else:
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
    
    if CollisionDict[board.room[targetA][targetB].name] == "walkable" : #If the player didn't attempt to walk off the border
        if (Tyger.options[1] != "True" and position != 0):
            print "No sticky clones!"
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        board.roomunder[targetA][targetB] = board.room[targetA][targetB] #Put the space to be overwritten on the under layer
        board.room[targetA][targetB] = board.room[board.statcoords[0][0]][board.statcoords[0][1]] #The player occupies two tiles at once, quantum physics itc.
        #Render the two tiles
        board.render[board.statcoords[0][0]][board.statcoords[0][1]] = 1
        board.render[targetA][targetB] = 1
        #Replace old tile with what was underneath it
        board.room[board.statcoords[0][0]][board.statcoords[0][1]] = board.roomunder[board.statcoords[0][0]][board.statcoords[0][1]]
        board.statcoords[0] = (targetA, targetB)
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    elif CollisionDict[board.room[targetA][targetB].name] == "DieItem": #We need to handle this based on what you've bumped into
        if (Tyger.options[1] != "True" and position != 0):
            print "No sticky clones!"
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        #Render the two tiles
        board.render[board.statcoords[0][0]][board.statcoords[0][1]] = 1
        board.render[targetA][targetB] = 1
        return DieItem(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, board.room[targetA][targetB].name, allboards, screen)
    elif CollisionDict[board.room[targetA][targetB].name] == "InvisWall": #Invisible wall
        if (Tyger.options[1] != "True" and position != 0):
            print "No sticky clones!"
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        #Render the two tiles
        board.render[board.statcoords[0][0]][board.statcoords[0][1]] = 1
        board.render[targetA][targetB] = 1
        return Invisible(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, board.room[targetA][targetB].name)   
    elif CollisionDict[board.room[targetA][targetB].name] == "Passage": #Passage
        return Passage(board, input, allboards, x, y, screen, ammo, torches, gems, score, health, keys, tcycles, ecycles, timepassed, targetA, targetB, flags)
    elif CollisionDict[board.room[targetA][targetB].name] == "Scroll": #Scroll
        if (Tyger.options[1] != "True" and position != 0):
            print "No sticky clones!"
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board = Object(board, targetA, targetB, 0, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, screen)
        board.room[targetA][targetB] = board.room[x][y]
        board.room[x][y] = board.roomunder[x][y]
        DestroyStat(board, targetA, targetB)
        UpdateStat(board, x, y, targetA, targetB)
        #Render the two tiles
        board.render[board.statcoords[0][0]][board.statcoords[0][1]] = 1
        board.render[targetA][targetB] = 1
        input = "null"
    elif CollisionDict[board.room[targetA][targetB].name] == "Touch": #Object
        Oop.SendJump(board.room[targetA][targetB], ":touch", True)
        input = "null"
        #Testing...
        #Tyger.Dprint("successful :touch")
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    elif CollisionDict[board.room[targetA][targetB].name] == "Push": #Pushing
        if (Tyger.options[1] != "True" and position != 0):
            print "No sticky clones!"
            #Render the two tiles
            board.render[board.statcoords[0][0]][board.statcoords[0][1]] = 1
            board.render[targetA][targetB] = 1
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        if board.room[targetA][targetB].name == "bomb" and board.room[targetA][targetB].param1 == 0: #If it's a bomb, activate it.
            board.room[targetA][targetB].param1 = 9
            board.room[targetA][targetB].character = 57
            print "Bomb activated!"
            board.render[targetA][targetB] = 1
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board #Bombs don't move when you first light them
        #Render the two tiles
        board.render[board.statcoords[0][0]][board.statcoords[0][1]] = 1
        board.render[targetA][targetB] = 1
        return Push(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    elif CollisionDict[board.room[targetA][targetB].name] == "ChangeBoard": #Edge of boards that aren't edges
        if (Tyger.options[1] != "True" and position != 0):
            print "No sticky clones!"
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        ammo, torches, health, tcycles, ecycles, gems, score, keys, timepassed, input, board = ChangeBoard(board, input, allboards, x, y, screen, ammo, torches, gems, score, health, keys, tcycles, ecycles, timepassed)
    elif CollisionDict[board.room[targetA][targetB].name] == "slime": #Squished a slime
        if (Tyger.options[1] != "True" and position != 0):
            print "No sticky clones!"
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        #Render the two tiles
        board.render[board.statcoords[0][0]][board.statcoords[0][1]] = 1
        board.render[targetA][targetB] = 1
        board.room[targetA][targetB] = Tyger.Spawn("breakable", 177, board.room[targetA][targetB].foreground, board.room[targetA][targetB].background, (targetA, targetB), 0, 0, 0, 0, 0, 0) #Become a breakable wall
        DestroyStat(board, targetA, targetB)
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board



def Push(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, xstep=1, ystep=1):
    #print "We must poosh little boulder " + input + " " + str(xstep) + " " + str(ystep)
    offA = 0
    offB = 0
    crush = False
    xstep = abs(xstep)
    ystep = abs(ystep)
    results = [board.room[x][y]] #Place the element that's pushing in the array
    #print "Push func: Input = " + str(xstep) + " | " + str(ystep)
    
    if input == "n":
        input = "up"
    elif input == "s":
        input = "down"
    elif input == "w":
        input = "left"
    elif input == "e":
        input = "right"
    
    while True:
        if input=="up":
            offA = offA - ystep
        elif input=="down":
            offA = offA + ystep
        elif input=="left":
            offB = offB - xstep
        elif input=="right":
            offB = offB + xstep
        elif input=="NW":
            offA = offA - ystep
            offB = offB - xstep
        elif input=="SW":
            offA = offA + ystep
            offB = offB - xstep
        elif input=="NE":
            offA = offA - ystep
            offB = offB + xstep
        elif input=="SE":
            offA = offA + ystep
            offB = offB + xstep
        
        #print str(x+offA) + " " + str(y+offB)
        if (x+offA) > 24 or (y+offB) > 59 or (x+offA) < 0 or (y+offB) < 0: #Check for the board edge
            if crush == False:
                break
            if crush == True:
                results.append(Tyger.Spawn("normal", 42, Tyger.white, Tyger.bgdarkblue, (666, 777), 0, 0, 0, 0, 0, 0)) #Pretend there's a normal wall instead of an infinite void. Clever girl.
        else:
            #print "Moving along " + board.room[x+offA][y+offB].name + " | " + PushDict[results[-1].name]
            results.append(board.room[x+offA][y+offB]) #Add the next element to the array
        if (results[-1].name == "sliderns" and (input == "left" or input == "right")) or (results[-1].name == "sliderew" and (input == "up" or input == "down")):
            break
        if PushDict[results[-1].name] == "stop":
            #Can we crush something instead?
            if crush == True:
                #Crush that shit
                results.reverse() #Flip the array
                for temp in range(0, len(results)):
                    if PushDict[results[temp].name] == "crush":
                        results[temp].name = "empty"
                        results.reverse() #Flip the array back to normal
                        statpos = len(results)-temp #The item about to be crushed might have stats to be removed.
                        if input == "up" or input == "down":
                            DestroyStat(board, x+statpos, y)
                        else:
                            DestroyStat(board, x, y+statpos)
                        break
                #print "SUSPICION CONFIRMED."
                Push(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
                break
                #print str(results.pop())
                #force = True
            else:
                break #Fuck it we're not doing shit
        elif PushDict[results[-1].name] == "push":
            print "Push it to the limit " + results[-1].name
            continue
        if PushDict[results[-1].name] == "go":
            #Pop the last element as it's a fake or empty and MEANINGLESS.
            results.pop()
            while len(results) > 0:
                board.room[x+offA][y+offB] = results[-1]
                board.render[x+offA][y+offB] = 1 #Render the tiles
                print "Updating stats"
                if input == "right" or input == "down":
                    UpdateStat(board, x+(len(results)-1)*(offA > 0), y+(len(results)-1)*(offB > 0), x+offA, y+offB)
                elif input == "up":
                    UpdateStat(board, x-(len(results)-1)*(offA <= 0), y*(offB <= 0), x+offA, y+offB)
                elif input == "left":
                    UpdateStat(board, x*(offA <= 0), y-(len(results)-1)*(offB <= 0), x+offA, y+offB) #Why I can't combine Left and Up I will never understand.
                if input=="up":
                    offA = offA + ystep
                elif input=="down":
                    offA = offA - ystep
                elif input=="left":
                    offB = offB + xstep
                elif input=="right":
                    offB = offB - xstep
                results.pop() #Pop the used element
            board.room[x][y] = board.roomunder[x][y]
            #print str(board.statcoords) + "Done pushing?"
            break
        elif PushDict[results[-1].name] == "crush":
            #print "Crushable something found"
            crush = True
            continue
    
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board  
    
def Pusher(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed):
    pushdir = "TBA"
    
    #Fix those odd overflowing numbers
    if board.room[x][y].xstep > 127:
        board.room[x][y].xstep = board.room[x][y].xstep-65536
    if board.room[x][y].ystep > 127:
        board.room[x][y].ystep = board.room[x][y].ystep-65536
     
    #Figure out which direction to push in
    #print str(pushdir) + " in pusher func"
    #print board.room[x][y].name
    #print str(board.room[x][y].xstep)
    #print str(board.room[x][y].ystep)
    if (board.room[x][y].xstep < 0) and (board.room[x][y].ystep == 0):
        pushdir = "left"
    elif (board.room[x][y].xstep > 0) and (board.room[x][y].ystep == 0):
        pushdir = "right"
    elif (board.room[x][y].ystep < 0) and (board.room[x][y].xstep == 0):
        pushdir = "up"
    elif (board.room[x][y].ystep > 0) and (board.room[x][y].xstep == 0):
        pushdir = "down"
    elif (board.room[x][y].xstep < 0) and (board.room[x][y].ystep < 0):
        pushdir = "NW"
    elif (board.room[x][y].xstep < 0) and (board.room[x][y].ystep > 0):
        pushdir = "SW"
    elif (board.room[x][y].xstep > 0) and (board.room[x][y].ystep < 0):
        pushdir = "NE"
    elif (board.room[x][y].xstep > 0) and (board.room[x][y].ystep > 0):
        pushdir = "SE"
    else:
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
    #print "Sending Push function " + pushdir
    board.render[x][y] = 1 #Render
    Push(board, x, y, pushdir, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, board.room[x][y].xstep, board.room[x][y].ystep)
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def Ruffian(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed):
    #Ruffians have two modes: Still and Mobile. Which of these modes the Ruffian is in is dictated by how the Step parameters are set.
    #If X/Y is set to zero, the Ruffian is resting and does not move. Otherwise, the Ruffian moves like Flow, whichever direction the Step happens to be pointing.
    #Resting time is the likelihood that a Ruffian will switch between these two modes, ranging from Value 0 (90% chance) to 8 (10% chance).
    #When switching from Still to Mobile, it uses Intelligence to determine whether it will move randomly or towards the player.
    #The direction chosen by the Ruffian does not change until it stops moving (by switching back to Still mode, setting Step to [0,0])
    #- Saxxon
    
    #Simplify things a bit
    ruffian = board.room[x][y]
    resting = False
    if ruffian.xstep == 0 and ruffian.ystep == 0:
        resting = True

    
    
    #Should we change modes?
    if (rnd(1, 10) > ruffian.param1 + 1): #If we roll a high number, switch modes
        resting = not resting #I am rather fond of this line.
    
    #Now process what to do
    if resting:
        #We're resting. End of story.
        ruffian.xstep = 0
        ruffian.ystep = 0
    else:
        CreatureMove(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        
    
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def Scroll(board, x, y, cycles):
        ScrollDict = {0:Tyger.white, 1:Tyger.blue, 2:Tyger.green, 3:Tyger.cyan, 4:Tyger.red, 5:Tyger.purple, 6:Tyger.yellow}
        board.room[x][y].foreground = ScrollDict[cycles % 7]
        board.render[x][y] = 1 #Render

def Shark(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed):
    choices = [] #Possible ways to move
    canseek = False #Is it possible to move seek if the shark wants to?
    
    #Figure out which way is seek
    if ecycles != 0: #Energizers make smart sharks run away.
        temp = "opp seek"
    else:
        temp = "seek"
    seekdir = ParseDir([temp], x, y, board.statcoords[0][0], board.statcoords[0][1], board.room[x][y].xstep, board.room[x][y].ystep)
    if x+WalkDict[seekdir][1] < 0 or x+WalkDict[seekdir][1] >= 25 or y+WalkDict[seekdir][0] < 0 or y+WalkDict[seekdir][0] >= 60:
        None
    else:
        if board.room[x+WalkDict[seekdir][1]][y+WalkDict[seekdir][0]].name == "water" or board.room[x+WalkDict[seekdir][1]][y+WalkDict[seekdir][0]].name == "player":
            canseek = True
            #choices.append(seekdir)    
    if y+1 < 60:
        if board.room[x][y+1].name == "water" or board.room[x][y+1].name == "player":
            choices.append("e")
    if y-1 > 0:
        if board.room[x][y-1].name == "water" or board.room[x][y-1].name == "player":
            choices.append("w")
    if x+1 < 25:
        if board.room[x+1][y].name == "water" or board.room[x+1][y].name == "player":
            choices.append("s")
    if x-1 > 0:
        if board.room[x-1][y].name == "water" or board.room[x-1][y].name == "player":
            choices.append("n")
    if len(choices) == 0:
        choices.append("i")
    
    #Decide if the shark will try to move seek or randomly
    if (canseek == False) or (rnd(1, 10) >= board.room[x][y].param1 + 1): #Move randomly
        dir = choices[rnd(0,len(choices)-1)]
        if dir == "i": #Give it up lion. You're surrounded.
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    else: #Move seek
        dir = seekdir
    
    print "I'm going to move...", dir
    #Now move it!
    if board.room[x+WalkDict[dir][1]][y+WalkDict[dir][0]].name == "player": #Hurt the player
        if ecycles == 0:
            health = health - 10 #Way to go
            if board.zap == 1:
                #Move player to enterX/enterY coords
                board.room[board.enterY][board.enterX] = board.room[board.statcoords[0][0]][board.statcoords[0][1]]
                board.room[board.statcoords[0][0]][board.statcoords[0][1]] = board.roomunder[board.statcoords[0][0]][board.statcoords[0][1]]
                board.statcoords[0] = (board.enterY, board.enterX)
        board.room[x][y] = board.roomunder[x][y] #Destroy the shark!
        board.render[x][y] = 1
        board.statcoords[position] = "pop" #Destroy the shark's stat
    else:
        board.roomunder[x+WalkDict[dir][1]][y+WalkDict[dir][0]] = board.room[x+WalkDict[dir][1]][y+WalkDict[dir][0]]
        board.room[x+WalkDict[dir][1]][y+WalkDict[dir][0]] = board.room[x][y] #Move the shark
        board.room[x][y] = board.roomunder[x][y] #Remove the old shark
        board.render[x+WalkDict[dir][1]][y+WalkDict[dir][0]] = 1
        board.render[x][y] = 1
        UpdateStat(board, x, y, x+WalkDict[dir][1], y+WalkDict[dir][0]) #Update its stat
    
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def Slime(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed):
    slimestats = []
    #Increase slime counter
    if board.room[x][y].param1 < board.room[x][y].param2:
        board.room[x][y].param1 = board.room[x][y].param1 + 1
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        
    else: #Multiply
        board.room[x][y].param1 = 0
        free = BorderCheck(x, y)
        
        if free[0]:
            if board.room[x-1][y].name == "empty" or board.room[x-1][y].name == "fake":
                a = x-1
                b = y
                board.roomunder[a][b] = board.room[a][b]
                board.render[a][b] = 1
                #Fix colors (slimes only)
                bg = board.room[a][b].background
                board.room[a][b] = board.room[x][y]
                board.room[a][b].background = bg
                board.room[a][b] = board.room[x][y]
                board.statcoords[position] = "pop" #Destroy old stat
                board.statcoords.insert(position, (a,b)) #Add new stat

        if free[1]:
            if board.room[x+1][y].name == "empty" or board.room[x+1][y].name == "fake":
                a = x+1
                b = y
                board.roomunder[a][b] = board.room[a][b]
                board.render[a][b] = 1
                #Fix colors (slimes only)
                bg = board.room[a][b].background
                board.room[a][b] = board.room[x][y]
                board.room[a][b].background = bg
                board.room[a][b] = board.room[x][y]
                board.statcoords[position] = "pop" #Destroy old stat
                board.statcoords.insert(position, (a,b)) #Add new stat

        if free[2]:
            if board.room[x][y-1].name == "empty" or board.room[x][y-1].name == "fake":
                a = x
                b = y-1
                board.roomunder[a][b] = board.room[a][b]
                board.render[a][b] = 1
                #Fix colors (slimes only)
                bg = board.room[a][b].background
                board.room[a][b] = board.room[x][y]
                board.room[a][b].background = bg
                board.room[a][b] = board.room[x][y]
                board.statcoords[position] = "pop" #Destroy old stat
                board.statcoords.insert(position, (a,b)) #Add new stat

        if free[3]:
            if board.room[x][y+1].name == "empty" or board.room[x][y+1].name == "fake":
                a = x
                b = y+1
                board.roomunder[a][b] = board.room[a][b]
                board.render[a][b] = 1
                #Fix colors (slimes only)
                bg = board.room[a][b].background
                board.room[a][b] = board.room[x][y]
                board.room[a][b].background = bg
                board.room[a][b] = board.room[x][y]
                board.statcoords[position] = "pop" #Destroy old stat
                board.statcoords.insert(position, (a,b)) #Add new stat
                
        board.room[x][y] = Tyger.Spawn("breakable", 177, board.room[x][y].foreground, board.room[x][y].background, (x, y), 0, 0, 0, 0, 0, 0) #Become a breakable wall
        board.render[x][y]
        
    
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def Star(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed):
    #STARS PUSHTHINGS FFFFFFFFFFFFF
    #Animate the character
    StarChars = {92:179, 179:47, 47:45, 45:92}
    board.room[x][y].character = StarChars.get(board.room[x][y].character, 92)
    
    #Animate the color
    StarColors = {Tyger.yellow:Tyger.white, Tyger.white:Tyger.blue, Tyger.blue:Tyger.green, Tyger.green:Tyger.cyan, Tyger.cyan:Tyger.red, Tyger.red:Tyger.purple, Tyger.purple:Tyger.yellow}
    board.room[x][y].foreground = StarColors.get(board.room[x][y].foreground, Tyger.green)
    
    #Render it
    board.render[x][y] = 1
    
    #Move seek if it can
    seekdir = ParseDir(["seek"], x, y, board.statcoords[0][0], board.statcoords[0][1], board.room[x][y].xstep, board.room[x][y].ystep)
    #Figure out any borders
    free = BorderCheck(x, y)
    #print "BORDER:", free, seekdir
    
    #Reduce star life
    if board.room[x][y].param2 == 0:
        board.room[x][y].param2 = 255
    else:
        board.room[x][y].param2 = board.room[x][y].param2 - 1
        if board.room[x][y].param2 == 0:
            board.room[x][y] = board.roomunder[x][y] #Destroy the star
            board.statcoords[position] = "pop" #Destroy the star's stat
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
    if cycles % (board.room[x][y].cycle * 2) == 0: #Only move every other cycle despite being cycle one!
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
    if free[0] and seekdir == "n":
        print ObjectDict[board.room[x-1][y].name]
        if board.room[x-1][y].name == "player": #Hurt the player
            if ecycles == 0:
                health = health - 10 #Way to go
                if board.zap == 1:
                    #Move player to enterX/enterY coords
                    board.room[board.enterY][board.enterX] = board.room[board.statcoords[0][0]][board.statcoords[0][1]]
                    board.room[board.statcoords[0][0]][board.statcoords[0][1]] = board.roomunder[board.statcoords[0][0]][board.statcoords[0][1]]
                    board.statcoords[0] = (board.enterY, board.enterX)
            board.room[x][y] = board.roomunder[x][y] #Destroy the star
            board.statcoords[position] = "pop" #Destroy the star's stat
        elif ObjectDict[board.room[x-1][y].name] == "Push" or ObjectDict[board.room[x-1][y].name] == "walkable":
            #print "I need to push!"
            Oop.Go("#go n", x, y, board, board.room[x][y], False, False, False)
            board.render[x-1][y] = 1
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    if free[1] and seekdir == "s":
        print ObjectDict[board.room[x+1][y].name]
        if board.room[x-1][y].name == "player": #Hurt the player
            if ecycles == 0:
                health = health - 10 #Way to go
                if board.zap == 1:
                    #Move player to enterX/enterY coords
                    board.room[board.enterY][board.enterX] = board.room[board.statcoords[0][0]][board.statcoords[0][1]]
                    board.room[board.statcoords[0][0]][board.statcoords[0][1]] = board.roomunder[board.statcoords[0][0]][board.statcoords[0][1]]
                    board.statcoords[0] = (board.enterY, board.enterX)
            board.room[x][y] = board.roomunder[x][y] #Destroy the star
            board.statcoords[position] = "pop" #Destroy the star's stat
        elif ObjectDict[board.room[x+1][y].name] == "Push" or ObjectDict[board.room[x+1][y].name] == "walkable":
            #print "I need to push!"
            Oop.Go("#go s", x, y, board, board.room[x][y], False, False, False)
            board.render[x+1][y] = 1
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
            
    if free[2] and seekdir == "e":
        print ObjectDict[board.room[x][y+1].name]
        if board.room[x][y+1].name == "player": #Hurt the player
            if ecycles == 0:
                health = health - 10 #Way to go
                if board.zap == 1:
                    #Move player to enterX/enterY coords
                    board.room[board.enterY][board.enterX] = board.room[board.statcoords[0][0]][board.statcoords[0][1]]
                    board.room[board.statcoords[0][0]][board.statcoords[0][1]] = board.roomunder[board.statcoords[0][0]][board.statcoords[0][1]]
                    board.statcoords[0] = (board.enterY, board.enterX)
            board.room[x][y] = board.roomunder[x][y] #Destroy the star
            board.statcoords[position] = "pop" #Destroy the star's stat
        elif ObjectDict[board.room[x][y+1].name] == "Push" or ObjectDict[board.room[x][y+1].name] == "walkable":
            #print "I need to push!"
            Oop.Go("#go e", x, y, board, board.room[x][y], False, False, False)
            board.render[x][y+1] = 1
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    if free[3] and seekdir == "w":
        print ObjectDict[board.room[x][y-1].name]
        if board.room[x][y-1].name == "player": #Hurt the player
            if ecycles == 0:
                health = health - 10 #Way to go
                if board.zap == 1:
                    #Move player to enterX/enterY coords
                    board.room[board.enterY][board.enterX] = board.room[board.statcoords[0][0]][board.statcoords[0][1]]
                    board.room[board.statcoords[0][0]][board.statcoords[0][1]] = board.roomunder[board.statcoords[0][0]][board.statcoords[0][1]]
                    board.statcoords[0] = (board.enterY, board.enterX)
            board.room[x][y] = board.roomunder[x][y] #Destroy the star
            board.statcoords[position] = "pop" #Destroy the star's stat
        elif ObjectDict[board.room[x][y-1].name] == "Push" or ObjectDict[board.room[x][y-1].name] == "walkable":
            #print "I need to push!"
            Oop.Go("#go w", x, y, board, board.room[x][y], False, False, False)
            board.render[x][y-1] = 1
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def UnderOver(underID, underColor, coords):
    #Create an element based on what's underneath
    underColor = hex(underColor)[2:].upper()
    tile = Tyger.Element(IdDict[underID], CharDict[underID], Tyger.getFg(underColor), Tyger.getBg(underColor), coords)
    if tile.name == "empty":
        tile.image = Tyger.makeimage(tile.character, Tyger.black, Tyger.bgblack) #But change its graphic
    return tile
    #name="empty", character=32, foreground=black, background=bgblack, coords=(0,0), param1 = 0, param2 = 0, param3 = 0):
    #= zzt.Element()


def UpdateStat(board, x, y, a, b):
    #Does anything have these coordinates?
    #print "Updating Stat..." + str(x) + ", " + str(y)
    for temp in range(0, len(board.statcoords)):
        if board.statcoords[temp] == (x, y):
            #print "Updated!" + str(x) + "," + str(y) + " is now: " + str(a) + "," + str(b)
            board.statcoords[temp] = (a, b)
            break
    

