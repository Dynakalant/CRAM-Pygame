import pygame
import random
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

SCREEN_WIDTH  = 1200
SCREEN_HEIGHT = 700

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()

player = pygame.Rect(screen_rect.centerx, screen_rect.bottom, 0, 0)
start = pygame.math.Vector2(player.center)
end = start
length = 5

# Gun parameters
ammo = 0
reload = 0
reload_timer = 0
SPEED = 1.3
spread = 0.020
fuze = 480
gravity = 0.001
auto_acq = True


projectile_base_cooldown = 200 # Affects initial spawn rate of incoming projectiles
projectile_cooldown = 0
MIN_COOLDOWN = 25
increasing_projectile_rate = True # If true, the rate of projectile spawn will slowly increase.

# Containers storing all bullets, projectiles, and radar contacts
all_bullets = []
all_projectiles = []

all_radar_contacts = []

# Counters for projectiles
shots = 0 
intercepted = 0

max_burst_count = 150

indicators = True

clock = pygame.time.Clock()
run = True

pygame.mouse.set_visible(False)

while run:
    in_use = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_a:
                if auto_acq:
                    auto_acq = False
                elif not auto_acq:
                    auto_acq = True
            elif event.key == pygame.K_v:
                if indicators:
                    indicators = False
                else:
                    indicators = True
        elif event.type == pygame.MOUSEMOTION:
            mouse = pygame.mouse.get_pos()
            end = start + (mouse - start).normalize() * length
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        max_burst_count += 1
    elif keys[pygame.K_f] and max_burst_count > 0:
        max_burst_count -= 1

    for bullet in all_bullets:
        if bullet[3]:
            bullet[0] += bullet[1]
            bullet[1][1] = bullet[1][1] + gravity
            bullet[2] -= 1

    screen.fill((0,0,0))
    radar_detection_range = 800

    if indicators:
        pygame.draw.circle(screen, (0,26,0), start, radar_detection_range, 4)
        pygame.draw.circle(screen, (0,43,0), start, 500, 8)

    pygame.draw.line(screen, WHITE, (player.x, player.y), (player.x, player.y - 3))

    myfont = pygame.font.Font(None,25)
    cannon_surf = myfont.render("Ammo Expended: " + str(ammo), 1, (255,255,255))
    cannon_pos = [30,30]
    screen.blit(cannon_surf, cannon_pos)

    if projectile_cooldown <= 0:
        prectangle = [0,0,1,1]
        pspeed = 0.9  + random.randrange(0,100)/100

        exist = True
        lead = (0,0)
        hittable = False
        velx_store = [0,False]
        vely_store = [0,False]
        t_store = 0
        threat = 0 

        ang = math.radians(random.randrange(10,45))
        pspeedx = pspeed*math.cos(ang)
        pspeedy = pspeed*math.sin(ang)

        all_projectiles.append([prectangle, pspeedx, pspeedy, exist, lead, hittable, threat, velx_store, vely_store, t_store, max_burst_count])
        projectile_cooldown += projectile_base_cooldown

        if increasing_projectile_rate:
            if projectile_base_cooldown != MIN_COOLDOWN:
                projectile_base_cooldown -= 1
    else:
        projectile_cooldown -= 1


    projectiles_inrange = 0

    remove_bullets = []
    remove_projectiles = []

    for p in range (len(all_projectiles)):
        if all_projectiles[p][3]:
            all_projectiles[p][2] += gravity
            speedx = all_projectiles[p][1]
            speedy = all_projectiles[p][2]
            all_projectiles[p][0][0] += speedx
            all_projectiles[p][0][1] += speedy 
            target_posx = all_projectiles[p][0][0]
            target_posy = all_projectiles[p][0][1]
            
            pygame.draw.rect(screen, (5,5,200), pygame.Rect(all_projectiles[p][0]))
            if pygame.math.Vector2(start).distance_to((all_projectiles[p][0][0], all_projectiles[p][0][1])) <= (radar_detection_range - random.randint(0,50)):
                if indicators:
                    pygame.draw.rect(screen, (0,255,0), pygame.Rect(all_projectiles[p][0][0]-12.5, all_projectiles[p][0][1]-12.5, 25,25),1)

                # -- auto-targeting algorithm
                #Notes: This works and accounts for gravity because both the projectile and bullet have the same gravity,
                #so it cancels out and works perfectly. I need to modify this to still work when the projectile's 
                #acceleration is taken into account.

                target_velx = speedx
                target_vely = speedy
                gun_x = start[0]
                gun_y = start[1]

                #exvar = pygame.math.Vector2(start).distance_to((all_projectiles[p][0][0], all_projectiles[p][0][1]))

                #all_projectiles[p][7][0] x
                #all_projectiles[p][8][0] y


                a = ((target_velx)**2) + ((target_vely)**2) - (SPEED)**2
                b = 2 * ((target_velx * (target_posx - gun_x)) + ((target_vely) * (target_posy - gun_y)))
                c = ((target_posx - gun_x)**2) + (target_posy - gun_y)**2

                disc = (b**2) - 4 * a * c
                
                t1 = (-b + math.sqrt(abs(disc))) / (2 * a)
                t2 = (-b - math.sqrt(abs(disc))) / (2 * a)


                if t1 > t2:
                    t = t2
                elif t1 <= t2:
                    t = t1
                
                all_projectiles[p][9] = t

                #ycompensate = ((yaccel * t) + target_velx) #(gravity * all_projectiles[p][9])

                

                aimX = t * target_velx + target_posx
                aimY = t * (target_vely) + target_posy
                
                if disc <= 0:
                    #not in range
                    all_projectiles[p][5] = False
                    if indicators:
                        pygame.draw.line(screen, (0,255,0), (target_posx - 12.5, target_posy - 12.5), (target_posx + 12.5, target_posy + 12.5))
                        pygame.draw.line(screen, (0,255,0), (target_posx - 12.5, target_posy + 12.5), (target_posx + 12.5, target_posy - 12.5))
                else:
                    if indicators:
                        projectiles_inrange += 1
                        pygame.draw.line(screen, (0,255,0), (target_posx, target_posy), (aimX, aimY))
                        pygame.draw.circle(screen, (0,255,0), (aimX, aimY), random.randint(60,65) / 10, 1)
                    all_projectiles[p][5] = True
                all_projectiles[p][4] = (aimX, aimY) #append aim lead coordinates to the projectile, to be (possibly) fired at by the gun later
            if target_posy > 700:
                shots += 1
                pygame.draw.circle(screen, (255,165,0), (all_projectiles[p][0][0], all_projectiles[p][0][1]), random.randint(2,10))
                remove_projectiles.append(p)
    
    tracer = True if (not ammo % 5) else False

    mousec = pygame.mouse.get_pos()
    mousex = mousec[0]
    mousey = mousec[1]
    
    if not auto_acq:
        screen.blit(myfont.render("MANUAL", 1, (180,0,0)), [350, 50])
    
        if indicators:
            pygame.draw.line(screen, (0,200,0), (mousex - 6.25, mousey), (mousex + 6.25, mousey))
            pygame.draw.line(screen, (0,200,0), (mousex, mousey - 6.25), (mousex, mousey + 6.25))
        if (pygame.mouse.get_pressed()[0]):
                
            width = 1
            ammo += 1
            bullet_fuze = fuze + random.randrange(0,35)
            active = True
            
            dist = pygame.math.Vector2(start).distance_to((mousex, mousey))

            rand_l = (-1 * dist * spread)
            rand_u = (dist * spread)

            mousex = mousec[0] + random.uniform(rand_l, rand_u)
            mousey = mousec[1] + random.uniform(rand_l, rand_u)

            mouse = (mousex, mousey)
            
            distance = mouse - start

            position = pygame.math.Vector2(start) # duplicate # start position in start of canon
            #position = pygame.math.Vector2(end)   # duplicate # start position in end of canon
            speed = distance.normalize() * SPEED
            
            all_bullets.append([position, speed, bullet_fuze, active, width, tracer])
    elif auto_acq:
        if indicators:
            pygame.draw.line(screen, (0,200,0), (mousex, mousey), (mousex, mousey))
        screen.blit(myfont.render("AUTO", 1, (180,0,0)), [350, 50])
        smallest = 1000
        for projectile in all_projectiles:
            dist = pygame.math.Vector2(start).distance_to((projectile[0][0], projectile[0][1]))
            dist_to_lead = pygame.math.Vector2(start).distance_to((projectile[4][0], projectile[4][1]))
            if projectile[0][1] < radar_detection_range and projectile[4][1] < radar_detection_range and dist_to_lead < radar_detection_range and dist < radar_detection_range and dist < smallest and projectile[5] and projectile[10] and not in_use:
                in_use = True

                smallest = dist
                width = 1
                ammo += 1
                projectile[10] -= 1

                bullet_fuze = fuze + random.randrange(0,35)
                active = True

                coordx = projectile[4][0]
                coordy = projectile[4][1]

                dist = pygame.math.Vector2(start).distance_to((coordx, coordy))

                rand_l = (-1 * dist * spread)
                rand_u = (dist * spread)

                coordx += random.uniform(rand_l, rand_u)
                coordy += random.uniform(rand_l, rand_u) + (gravity * projectile[9])
                
                coord = (coordx, coordy)

                distance = coord - start
                position = pygame.math.Vector2(start)
                speed = distance.normalize() * SPEED
                all_bullets.append([position, speed, bullet_fuze, active, width, tracer])
                if indicators:
                    pygame.draw.line(screen, (0,200,0), (projectile[4][0] - 6.25, projectile[4][1]), (projectile[4][0] + 6.25, projectile[4][1]))
                    pygame.draw.line(screen, (0,200,0), (projectile[4][0], projectile[4][1] - 6.25), (projectile[4][0], projectile[4][1] + 6.25))
                
    for i in range(len(all_bullets)):
        # need to convert `float` to `int` because `screen` use only `int` values
        pos_x = int(all_bullets[i][0].x)
        pos_y = int(all_bullets[i][0].y)
        if all_bullets[i][2] > 0:
            if all_bullets[i][5]:
                pygame.draw.rect(screen, (255, 0, 0), (pos_x, pos_y, all_bullets[i][4], all_bullets[i][4]))
            for p in range(len(all_projectiles)):
                if (pygame.Rect(all_projectiles[p][0]).colliderect(pos_x, pos_y, all_bullets[i][4], all_bullets[i][4]) ):
                    shots += 1
                    all_projectiles[p][0][0] += 10000
                    all_projectiles[p][0][1] += 10000
                    all_projectiles[p][3] = False
                    all_bullets[i][2] = 0
                    pygame.draw.circle(screen, WHITE, (pos_x, pos_y), random.randint(4,7))
                    all_bullets[i][3] = False
                    remove_bullets.append(i)
                    if p not in remove_projectiles:
                        remove_projectiles.append(p)
                    intercepted += 1
            #pygame.draw.line(screen, (255,0,0), (pos_x, pos_y), (pos_x, pos_y))
        elif all_bullets[i][3]:
            pygame.draw.circle(screen, WHITE, (pos_x, pos_y), 3)
            all_bullets[i][3] = False
            remove_bullets.append(i)
    
    remove_bullets.sort()
    remove_bullets.reverse()
    for rbullet in remove_bullets:
        all_bullets.pop(rbullet)
    
    remove_projectiles.sort()
    remove_projectiles.reverse()
    for rprojectile in remove_projectiles:
        all_projectiles.pop(rprojectile)

    hit_percentage = round(intercepted / shots * 100, 2) if shots != 0 else "-"
    hits_surf = myfont.render(f'Intercepted: {intercepted}/{shots} ({hit_percentage}%)', 1, (255,255,255))
    hits_pos = [30,60]
    screen.blit(hits_surf, hits_pos)

    screen.blit(myfont.render(f'Burst Count: {max_burst_count}', 1, (255,255,255)), (30,90))

    clock.tick(75)
    screen.blit(myfont.render(f'FPS: {round(clock.get_fps(), 2)}', 1, (255,255,255)), (15,675))

    pygame.display.update()

pygame.quit()

