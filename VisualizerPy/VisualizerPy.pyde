add_library('peasycam') 
from peasy import PeasyCam
from slider import Slider, TimeSlider
    
times = []
positions = []
rotations = []
minRender = 0
maxRender = 0
camActive = True
resolution = 1
sliderStart = TimeSlider(0,len(positions)-1,0)
sliderEnd = TimeSlider(0,len(positions)-1,len(positions)-1)
sliderResolution = Slider(1,10,1)

def setup():
    global times, positions, rotations, sliderStart, sliderEnd, maxRender, resolution
    points = loadStrings('../Data/P02_L_C1.txt')[1:]
    print(points[0].split())
    
    # separate data into multiple arrays
    for p in points:
        try:
            s = p.split()
            times += [s[0] + s[1]]
            positions += [(float(s[2][1:-1]), float(s[3][:-1]), float(s[4][:-1]))]
            rotations += [(float(s[5][1:-1]), float(s[6][:-1]), float(s[7][:-1]), float(s[8][:-1]))]
        except:
            print(p.split())
            continue
        
    # Map points to screen space
    x_co = [p[0] for p in positions]
    y_co = [p[1] for p in positions]
    z_co = [p[2] for p in positions]
    min_x, max_x = min(x_co), max(x_co)
    min_y, max_y = min(y_co), max(y_co)
    min_z, max_z = min(z_co), max(z_co)
    st_range = 350
    en_range = 650
    for i in range(len(positions)):
        positions[i] = [map(positions[i][0], min_x, max_x, st_range, en_range), map(positions[i][1], min_y, max_y, 450, 550), map(positions[i][2], min_z, max_z, st_range, en_range)]
        
    sliderStart = TimeSlider(0,len(positions)-1,0)
    sliderEnd = TimeSlider(0,len(positions)-1,len(positions)-1)
    maxRender = len(positions)-resolution
    
    # Setup camera
    size(1000, 1000, P3D)
    global cam
    cam = PeasyCam(this, positions[0][0], positions[0][2], positions[0][1], 100)
    cam.setMinimumDistance(5)
    cam.setMaximumDistance(500)
    sliderStart.position(20,20)
    sliderEnd.position(320,20)
    sliderResolution.position(620, 20)
    
def draw():
    # Draw walking path
    global resolution, minRender, maxRender
    clear()
    if camActive:
        drawLine(resolution)
    else:
        drawLine(resolution+3) #increase speed for better slider sensitivity
        
        cam.beginHUD()
        #calling value() draws the slider as well
        minRender = int(sliderStart.value(times))
        maxRender = int(sliderEnd.value(times))
        resolution = int(sliderResolution.value())
        cam.endHUD()
    
def keyTyped():
    global camActive
    if key == ' ':
        camActive = not camActive
        cam.setActive(camActive)

def drawLine(resolution):
    global positions, minRender, maxRender
    background(155)
    for i in range(minRender, maxRender - resolution, resolution):
        p1 = positions[i]
        p2 = positions[i+resolution]
        line(p1[0], p1[2], p1[1], p2[0], p2[2], p2[1])
        stroke(0, map(i, minRender, maxRender - resolution, 0, 255), 0)
    
    st = positions[0]
    translate(st[0], st[2], st[1])
    stroke(255, 0, 0)
    sphere(1)
    stroke(0)
    translate(-st[0], -st[2], -st[1])
    
    
