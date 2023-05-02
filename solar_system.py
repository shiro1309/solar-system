import pygame as pg, math, sys

class Planet:
    AU = 149.6e6*1000 # in meter
    G = 6.67428e-11
    SCALE = 12 / AU
    MINI_SCALE = 100 /AU
    TIMESTEP = 3600*24 # one day 
    
    def __init__(self, x, y, radius, color, mass, app):
        self.app = app
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.ring = False
        
        self.sun = False # needed for the orbit
        self.dist_to_sun = 0
        
        self.x_vel = 0
        self.y_vel = 0
        
    def draw(self, display, planet, planet_name, size):
        x = self.x * self.SCALE + size[0] / 2
        y = self.y * self.SCALE + size[1] / 2
        
        pg.draw.circle(display, self.color, (x, y), self.radius)
        
        if self.ring:
            pg.draw.circle(display, self.color, (x, y), self.radius+5, 1)

        if not self.sun:
            distance_text = self.app.FONT.render(f"{planet_name} - {round(self.dist_to_sun/self.AU, 3)}AU", 1, self.app.color["white"])
            display.blit(distance_text, (0, 32*(planet-1)))
    
    def mini_draw(self, display, size):
        #display.fill((0,0,0))
        x = self.x * self.MINI_SCALE + size[0] / 2
        y = self.y * self.MINI_SCALE + size[1] / 2
        if x > -20:
            pg.draw.circle(display, self.color, (x, y), self.radius)
        
        if self.ring:
            pg.draw.circle(display, self.color, (x, y), self.radius+5, 1)

        
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distence = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        if other.sun:
            self.dist_to_sun = distence
            
        force = self.G * self.mass * other.mass / distence**2
        
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta)* force
        force_y = math.sin(theta)* force
        return force_x, force_y
    
    def update(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
            
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        
        #self.orbit.append((self.x, self.y))
        
class App:
    def __init__(self):
        pg.init()
        
        self.color = {
            "white" : (255, 255, 255),
            "black" : (0, 0, 0),
            "yellow": (255,255,0),
            "blue": (0,0,255),
            "red": (188,39,50),
            "gray": (71, 71, 71),
            "orange": (201, 100, 62),
            "yellow-orange": (186, 154, 80),
            "light-blue": (102, 201, 204),
            "dark-light-blue": (51, 143, 145)
        }
        
        self.FONT = pg.font.SysFont("comicsans", 16)
        
        star = Planet(0, 0, 20, self.color["yellow"], 1.98892e30, self)
        star.sun = True
        
        earth = Planet(-1*Planet.AU, 0, 10, self.color["blue"], 5.9742e24, self)
        earth.y_vel = 29.783e3
        
        mars = Planet(-1.524* Planet.AU, 0, 6, self.color["red"], 6.39e23, self)
        mars.y_vel = 24.077e3
        
        mercury = Planet(0.387* Planet.AU, 0, 4, self.color["gray"], 3.3e23, self)
        mercury.y_vel = -47.4e3
        
        venus = Planet(0.723 * Planet.AU, 0, 10, self.color["white"], 4.8685e24, self)
        venus.y_vel = -35.02e3
        
        jupiter = Planet(5.20238*Planet.AU, 0, 8, self.color["orange"], 1.8982e27, self)
        jupiter.y_vel = -13.06e3
        
        saturn = Planet(9.58202*Planet.AU, 0, 7, self.color["yellow-orange"], 5.683e26, self)
        saturn.y_vel = -9.69e3
        saturn.ring = True
        
        uranus = Planet(19.19126*Planet.AU, 0, 10, self.color["light-blue"], 8.681e25, self)
        uranus.y_vel = -6.8e3
        
        neptune = Planet(30.13*Planet.AU, 0, 10, self.color["dark-light-blue"], 1.024e26, self)
        neptune.y_vel = -5.43e3
        
        self.planets = [star, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
        self.planet_names = ["sun", "mercury", "venus","earth", "mars", "jupiter", "saturn", "uranus", "neptun"]
        self.sun_lock = True
        
        self.res = self.width, self.height = 1600, 900
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(self.res)
        self.display = pg.Surface((417,417))
        pg.display.set_caption("solar sim")
    
    def run(self):
        while True:
            self.screen.fill(self.color["black"])
            self.display.fill(self.color["black"])
            n = 0
            if self.sun_lock:
                self.planets[0].x = 0
                self.planets[0].y = 0
            
            for planet in self.planets:
                planet.update(self.planets)
                planet.draw(self.screen, n, self.planet_names[n], (900,900))
                planet.mini_draw(self.display, (417,417))
                n += 1
            pg.draw.rect(self.screen, self.color["gray"], (422,422,52,52))
            pg.draw.rect(self.screen, self.color["black"], (423,423,50,50))
            
            pg.draw.rect(self.screen, self.color["gray"], (1099,39,419,419))
            self.screen.blit(self.display,(1100,40))
            
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()    
                    
            self.clock.tick()
            pg.display.update()                        
   
if __name__ == "__main__":
    app = App()
    app.run()