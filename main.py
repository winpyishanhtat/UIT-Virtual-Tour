import viz
import vizshape
import vizcam
import math

# 1. Initialize Vizard with High Quality Settings
viz.setMultiSample(8) 
viz.go()

# 2. Setup Realistic Lighting & Environment
viz.clearcolor(0.5, 0.7, 0.95) 

# Main Sun Light (Warm)
sun = viz.addLight()
sun.setPosition(1, 2, 0.5)
sun.setEuler(45, 45, 0)
sun.intensity(1.3)
sun.color(1.0, 0.95, 0.9) 

# Fill Light (Cool/Blueish shadows)
fill = viz.addLight()
fill.setPosition(-1, 0.5, -1)
fill.intensity(0.4)
fill.color(0.6, 0.7, 0.8)

# ==========================================
# 3. Dimensions
# ==========================================
B_WIDTH = 18   
B_DEPTH = 14   
GAP_X = 14      
GAP_Z = 15

FLOOR_HEIGHT = 4.0
NUM_FLOORS = 6
B_HEIGHT = FLOOR_HEIGHT * NUM_FLOORS

HALL_HEIGHT = FLOOR_HEIGHT * 2 
HALL_Z_POS = (GAP_Z/2 + B_DEPTH/2) 
BRIDGE_Y = FLOOR_HEIGHT * 3.5 

# ==========================================
# 4. Realistic Materials & Colors
# ==========================================
CONCRETE_COLOR = [0.75, 0.75, 0.72] 
DARK_CONCRETE = [0.5, 0.5, 0.5]
ROAD_COLOR = [0.15, 0.15, 0.15]      
GRASS_COLOR = [0.2, 0.5, 0.2]     
ROOF_METAL_COLOR = [0.2, 0.25, 0.3] 
FRAME_COLOR = [0.1, 0.1, 0.1] 
STEEL_BEAM_COLOR = [0.25, 0.25, 0.3] 
RAIL_PANEL_COLOR = [0.1, 0.1, 0.15]
GLASS_COLOR = [0.2, 0.4, 0.6] 
STRIP_COLOR = [1.0, 0.35, 0.0]

# Edges
X_MAX_EDGE = (GAP_X/2 + B_WIDTH)
X_MIN_EDGE = -(GAP_X/2 + B_WIDTH)
Z_MAX_EDGE = (GAP_Z/2 + B_DEPTH)
Z_MIN_EDGE = -(GAP_Z/2 + B_DEPTH)

# ==========================================
# 5. Geometry Builders
# ==========================================

def create_styled_building(x, z, w, d, h, style):
    """ 
    Building with realistic depth but retaining the original 'Strips' style.
    """
    # 1. Main Glass/Dark Core (Inset slightly to create depth)
    core = vizshape.addBox(size=(w-0.8, h, d-0.8))
    core.setPosition(x, h/2, z)
    core.color(0.95, 1.0, 1.0) 
    
    # 2. Glass Layer
    glass_skin = vizshape.addBox(size=(w-0.85, h, d-0.85))
    glass_skin.setPosition(x, h/2, z)
    glass_skin.color(GLASS_COLOR)
    glass_skin.alpha(0.4); glass_skin.shininess(90); glass_skin.specular(1, 1, 1)

    # 3. Concrete Floor Slabs
    for i in range(NUM_FLOORS + 1):
        y_pos = i * FLOOR_HEIGHT if i > 0 else 0.2
        if i == NUM_FLOORS: y_pos = h - 0.2
        
        slab = vizshape.addBox(size=(w, 0.4, d))
        slab.setPosition(x, y_pos, z)
        slab.color(CONCRETE_COLOR)

    # 4. ORIGINAL STYLE: Decorative Orange Strips
    if style == 'front':
        num, sw, sd, f_dir = 8, 0.4, 0.2, -1
    elif style == 'back':
        num, sw, sd, f_dir = 15, 0.2, 0.4, 1
    else: return 

    for i in range(num):
        if style == 'front':
             off = -w/2 + 2 + (i * ((w-4)/(num-1)))
             z_p = z + (d/2 * f_dir) - 0.1 
        else:
             off = -w/2 + (i * (w/(num-1)))
             z_p = z + (d/2 * f_dir) + 0.1
        
        strip = vizshape.addBox(size=(sw, h, sd))
        strip.setPosition(x + off, h/2, z_p) 
        strip.color(STRIP_COLOR)
        strip.shininess(30) 

def create_detailed_hall(x, z, w, h, d):
    """ Glass Hall """
    vizshape.addBox(size=(w, 0.2, d), pos=(x, 0.1, z), color=CONCRETE_COLOR)
    g = vizshape.addBox(size=(w-0.1, h, d-0.2), pos=(x, h/2, z), color=[0.7, 0.8, 0.9])
    g.alpha(0.3); g.shininess(50)
    fc, bt = [0.2, 0.2, 0.2], 0.2
    for i in range(7): 
        xo = -w/2 + (i * (w/6))
        vizshape.addBox(size=(bt, h, bt), pos=(x+xo, h/2, z-d/2), color=fc)
        vizshape.addBox(size=(bt, h, bt), pos=(x+xo, h/2, z+d/2), color=fc)
    for i in range(5):
        yp = (i * (h/4))
        vizshape.addBox(size=(w, bt, bt), pos=(x, yp, z-d/2), color=fc)
        vizshape.addBox(size=(w, bt, bt), pos=(x, yp, z+d/2), color=fc)
    vizshape.addBox(size=(w, 0.5, d), pos=(x, h, z), color=DARK_CONCRETE)
    create_railing(x, h + 0.25, z, w, d)

def create_railing(x, y, z, w, d):
    c = [0.3, 0.3, 0.3]
    rh = 1.0
    vizshape.addBox(size=(w, 0.1, 0.1), pos=(x, y+rh, z-d/2), color=c)
    vizshape.addBox(size=(w, 0.1, 0.1), pos=(x, y+rh, z+d/2), color=c)
    vizshape.addBox(size=(0.1, 0.1, d), pos=(x-w/2, y+rh, z), color=c)
    vizshape.addBox(size=(0.1, 0.1, d), pos=(x+w/2, y+rh, z), color=c)
    for i in range(11):
        off = -w/2 + (i * (w/10))
        vizshape.addBox(size=(0.1, rh, 0.1), pos=(x+off, y+rh/2, z-d/2), color=c)

def create_slim_elevator(x, z, roof_height):
    width = 2.5 
    depth = 2.5
    shaft_h = roof_height - 1.0 
    
    shaft = vizshape.addBox(size=(width, shaft_h, depth))
    shaft.setPosition(x, shaft_h/2, z)
    shaft.color(0.6, 0.8, 0.9)
    shaft.alpha(0.3)
    shaft.shininess(100)
    
    spine = vizshape.addBox(size=(0.6, shaft_h, 0.6))
    spine.setPosition(x, shaft_h/2, z)
    spine.color(CONCRETE_COLOR)
    
    frame_thick = 0.1
    for cx in [-width/2, width/2]:
        for cz in [-depth/2, depth/2]:
            vizshape.addBox(size=(frame_thick, shaft_h, frame_thick), 
                            pos=(x+cx, shaft_h/2, z+cz), 
                            color=FRAME_COLOR)
    num_grids = 20
    for i in range(num_grids):
        y = i * (shaft_h/num_grids)
        vizshape.addBox(size=(width, frame_thick, depth), pos=(x, y, z), color=FRAME_COLOR)
    
    car = vizshape.addBox(size=(2.0, 2.5, 2.0))
    car.setPosition(x, FLOOR_HEIGHT*2.5, z)
    car.color(0.8, 0.8, 0.8)

def create_z_axis_bridges_and_stairs(x_pos, z_start, z_end, num_levels=4):
    """
    ULTRA-REALISTIC BRIDGE & STAIR SYSTEM (No Supports Under Bridge)
    """
    bridge_length = abs(z_end - z_start)
    bridge_center_z = (z_start + z_end) / 2
    
    stair_run = 5.0
    stair_width = 2.0
    num_steps = 10
    rail_height = 1.2 # Safety rail height
    
    # === GROUND TO FLOOR 1 STAIRCASE ===
    g_start_z = z_start + B_DEPTH/2 + stair_run 
    g_end_z = z_start + B_DEPTH/2
    g_start_pos = [x_pos, 0.1, g_start_z]
    g_end_pos = [x_pos, FLOOR_HEIGHT, g_end_z]
    
    # Calculate orientation
    g_center = [(g_start_pos[0]+g_end_pos[0])/2, (g_start_pos[1]+g_end_pos[1])/2, (g_start_pos[2]+g_end_pos[2])/2]
    dx, dy, dz = [p2-p1 for p1, p2 in zip(g_start_pos, g_end_pos)]
    g_length = math.sqrt(dx**2 + dy**2 + dz**2)
    g_yaw = math.degrees(math.atan2(dx, dz))
    g_pitch = -math.degrees(math.asin(dy/g_length))
    
    g_group = viz.addGroup()
    g_group.setPosition(g_center)
    g_group.setEuler(g_yaw, g_pitch, 0)
    
    # 1. Heavy C-Channel Stringers (Side Supports)
    stringer_h = 0.3
    stringer_w = 0.08
    vizshape.addBox(size=(stringer_w, stringer_h, g_length), pos=(-stair_width/2, -0.15, 0), parent=g_group, color=STEEL_BEAM_COLOR)
    vizshape.addBox(size=(stringer_w, stringer_h, g_length), pos=(stair_width/2, -0.15, 0), parent=g_group, color=STEEL_BEAM_COLOR)
    
    # 2. Floating Treads with Nosing
    for step in range(num_steps):
        progress = (step / (num_steps - 1)) - 0.5
        z_local = progress * g_length
        # Tread
        t = vizshape.addBox(size=(stair_width-0.2, 0.05, 0.28), pos=(0, 0.1, z_local), parent=g_group, color=DARK_CONCRETE)
        t.shininess(30)
    
    # 3. Detailed Railings with Mid-Rails
    # Posts
    num_posts = 4
    for p in range(num_posts):
        zp = -g_length/2 + (p * g_length/(num_posts-1))
        # Left Post
        vizshape.addBox(size=(0.05, rail_height, 0.05), pos=(-stair_width/2-0.05, 0.5, zp), parent=g_group, color=FRAME_COLOR)
        # Right Post
        vizshape.addBox(size=(0.05, rail_height, 0.05), pos=(stair_width/2+0.05, 0.5, zp), parent=g_group, color=FRAME_COLOR)
    
    # Handrails (Top)
    vizshape.addBox(size=(0.06, 0.06, g_length), pos=(-stair_width/2-0.05, rail_height, 0), parent=g_group, color=FRAME_COLOR)
    vizshape.addBox(size=(0.06, 0.06, g_length), pos=(stair_width/2+0.05, rail_height, 0), parent=g_group, color=FRAME_COLOR)
    
    # Mid-rails (Safety bars)
    vizshape.addBox(size=(0.03, 0.03, g_length), pos=(-stair_width/2-0.05, rail_height/2, 0), parent=g_group, color=FRAME_COLOR)
    vizshape.addBox(size=(0.03, 0.03, g_length), pos=(stair_width/2+0.05, rail_height/2, 0), parent=g_group, color=FRAME_COLOR)
    
    # Landing Pad
    vizshape.addBox(size=(3, 0.2, 3), pos=(x_pos, 0.1, g_start_z), color=CONCRETE_COLOR)


    # --- UPPER LEVELS (BRIDGES & STAIRS) ---
    for i in range(1, num_levels + 1):
        y_pos = i * FLOOR_HEIGHT
        
        # === REALISTIC TRUSS BRIDGE (NO GROUND SUPPORT) ===
        bridge_group = viz.addGroup()
        bridge_group.setPosition(x_pos, y_pos, bridge_center_z)
        
        # 1. Deck with thickness
        deck_width = 3.0
        deck = vizshape.addBox(size=(deck_width, 0.2, bridge_length), parent=bridge_group, color=CONCRETE_COLOR)
        deck.setPosition(0, 0, 0)
        
        # 2. Truss Support Structure Underneath (Attached to deck, no ground pillars)
        # Main longitudinal beams
        vizshape.addBox(size=(0.2, 0.4, bridge_length), pos=(-deck_width/2+0.2, -0.3, 0), parent=bridge_group, color=STEEL_BEAM_COLOR)
        vizshape.addBox(size=(0.2, 0.4, bridge_length), pos=(deck_width/2-0.2, -0.3, 0), parent=bridge_group, color=STEEL_BEAM_COLOR)
        
        # Cross bracing
        num_cross = int(bridge_length / 2)
        for c in range(num_cross + 1):
            zp = -bridge_length/2 + (c * 2.0)
            vizshape.addBox(size=(deck_width, 0.15, 0.15), pos=(0, -0.3, zp), parent=bridge_group, color=STEEL_BEAM_COLOR)
        
        # 3. Connection Plates to Building
        plate_size = 3.2
        vizshape.addBox(size=(plate_size, 0.6, 0.2), pos=(0, -0.1, -bridge_length/2), parent=bridge_group, color=FRAME_COLOR)
        vizshape.addBox(size=(plate_size, 0.6, 0.2), pos=(0, -0.1, bridge_length/2), parent=bridge_group, color=FRAME_COLOR)

        # 5. Bridge Railings (Glass + Steel)
        # Posts
        for p in range(int(bridge_length/2) + 1):
            zp = -bridge_length/2 + (p * 2.0)
            vizshape.addBox(size=(0.05, 1.1, 0.05), pos=(-deck_width/2, 0.55, zp), parent=bridge_group, color=FRAME_COLOR)
            vizshape.addBox(size=(0.05, 1.1, 0.05), pos=(deck_width/2, 0.55, zp), parent=bridge_group, color=FRAME_COLOR)
        
        # Top Rail
        vizshape.addBox(size=(0.08, 0.08, bridge_length), pos=(-deck_width/2, 1.1, 0), parent=bridge_group, color=FRAME_COLOR)
        vizshape.addBox(size=(0.08, 0.08, bridge_length), pos=(deck_width/2, 1.1, 0), parent=bridge_group, color=FRAME_COLOR)
        
        # Glass Panels
        gp1 = vizshape.addBox(size=(0.02, 1.0, bridge_length), pos=(-deck_width/2, 0.5, 0), parent=bridge_group, color=GLASS_COLOR)
        gp1.alpha(0.3); gp1.shininess(100)
        gp2 = vizshape.addBox(size=(0.02, 1.0, bridge_length), pos=(deck_width/2, 0.5, 0), parent=bridge_group, color=GLASS_COLOR)
        gp2.alpha(0.3); gp2.shininess(100)
        
        # === UPPER CONNECTING STAIRS ===
        if i < num_levels:
            if i % 2 != 0: 
                start_z = z_start + B_DEPTH / 2
                end_z = start_z + stair_run
            else: 
                start_z = z_end - B_DEPTH / 2
                end_z = start_z - stair_run
            
            start_pos = [x_pos, y_pos, start_z]
            end_pos = [x_pos, y_pos + FLOOR_HEIGHT, end_z]
            center_pos = [(p1+p2)/2 for p1, p2 in zip(start_pos, end_pos)]
            dx, dy, dz = [p2-p1 for p1, p2 in zip(start_pos, end_pos)]
            length = math.sqrt(dx**2 + dy**2 + dz**2)
            yaw = math.degrees(math.atan2(dx, dz))
            pitch = -math.degrees(math.asin(dy/length)) 
            
            stair_group = viz.addGroup()
            stair_group.setPosition(center_pos)
            stair_group.setEuler(yaw, pitch, 0)
            
            # Stringers
            vizshape.addBox(size=(0.08, 0.35, length), pos=(-stair_width/2, -0.15, 0), parent=stair_group, color=STEEL_BEAM_COLOR)
            vizshape.addBox(size=(0.08, 0.35, length), pos=(stair_width/2, -0.15, 0), parent=stair_group, color=STEEL_BEAM_COLOR)
            
            # Detailed Treads
            for step in range(num_steps):
                progress = (step / (num_steps - 1)) - 0.5
                z_local = progress * length
                t = vizshape.addBox(size=(stair_width-0.1, 0.05, 0.28), pos=(0, 0.1, z_local), parent=stair_group, color=DARK_CONCRETE)
                t.shininess(40)
            
            # Railings with Mid-Rails
            # Handrails
            vizshape.addBox(size=(0.06, 0.06, length), pos=(-stair_width/2-0.05, 1.1, 0), parent=stair_group, color=FRAME_COLOR)
            vizshape.addBox(size=(0.06, 0.06, length), pos=(stair_width/2+0.05, 1.1, 0), parent=stair_group, color=FRAME_COLOR)
            
            # Posts
            for p in range(4):
                zp = -length/2 + (p * length/3)
                vizshape.addBox(size=(0.04, 1.1, 0.04), pos=(-stair_width/2-0.05, 0.55, zp), parent=stair_group, color=FRAME_COLOR)
                vizshape.addBox(size=(0.04, 1.1, 0.04), pos=(stair_width/2+0.05, 0.55, zp), parent=stair_group, color=FRAME_COLOR)
            
            # Safety Mesh Panels
            p1 = vizshape.addBox(size=(0.02, 0.9, length), pos=(-stair_width/2-0.05, 0.55, 0), parent=stair_group, color=RAIL_PANEL_COLOR)
            p1.alpha(0.6)
            p2 = vizshape.addBox(size=(0.02, 0.9, length), pos=(stair_width/2+0.05, 0.55, 0), parent=stair_group, color=RAIL_PANEL_COLOR)
            p2.alpha(0.6)

def create_truss_bridge(x, y, z, length):
    """ Restored Hall Bridge (With Supports) """
    w, h, sc = 3.0, 2.5, [0.25, 0.25, 0.25]
    vizshape.addBox(size=(length, 0.2, w), pos=(x, y, z), color=DARK_CONCRETE)
    bs = 0.2
    vizshape.addBox(size=(length, bs, bs), pos=(x, y, z-w/2), color=sc)
    vizshape.addBox(size=(length, bs, bs), pos=(x, y, z+w/2), color=sc)
    vizshape.addBox(size=(length, bs, bs), pos=(x, y+h, z-w/2), color=sc)
    vizshape.addBox(size=(length, bs, bs), pos=(x, y+h, z+w/2), color=sc)
    nb = 6
    bl = length/nb
    for i in range(nb+1):
        px = (x-length/2) + (i*bl)
        vizshape.addBox(size=(bs, h, bs), pos=(px, y+h/2, z-w/2), color=sc)
        vizshape.addBox(size=(bs, h, bs), pos=(px, y+h/2, z+w/2), color=sc)
        if i < nb:
            bx = px + bl/2
            dl = math.sqrt(bl**2 + h**2)
            ang = math.degrees(math.atan(h/bl))
            d1 = vizshape.addBox(size=(bs, dl, bs), pos=(bx, y+h/2, z-w/2), color=sc); d1.setEuler(0,0,ang)
            d2 = vizshape.addBox(size=(bs, dl, bs), pos=(bx, y+h/2, z-w/2), color=sc); d2.setEuler(0,0,-ang)

def add_gate(x, z, text):
    """ Adds a detailed sliding gate """
    gate_h = 3.0
    gate_w = 7.5
    
    # Gate Frame
    vizshape.addBox(size=(0.2, gate_h, gate_w), pos=(x, gate_h/2, z), color=FRAME_COLOR)
    # Gate Bars
    for i in range(15):
        zp = -gate_w/2 + (i * gate_w/14)
        vizshape.addBox(size=(0.2, gate_h-0.2, 0.1), pos=(x, gate_h/2, z+zp), color=STEEL_BEAM_COLOR)
        
    t = viz.addText3D(text, pos=(x, gate_h + 1.5, z), scale=[2,2,2], align=viz.ALIGN_CENTER)
    t.setEuler(-90, 0, 0) # Rotate to face outward

def create_realistic_fence(campus_w, campus_d):
    """ 
    High-Detail Fence with Plinth, Pillars, and Iron Bars 
    """
    fence_h = 2.5
    plinth_h = 0.4
    post_interval = 4.0
    
    # 1. Base Plinth (Concrete)
    # Left
    vizshape.addBox(size=(0.4, plinth_h, campus_d), pos=(-campus_w/2, plinth_h/2, 0), color=CONCRETE_COLOR)
    # Right
    vizshape.addBox(size=(0.4, plinth_h, campus_d), pos=(campus_w/2, plinth_h/2, 0), color=CONCRETE_COLOR)
    # Back
    vizshape.addBox(size=(campus_w, plinth_h, 0.4), pos=(0, plinth_h/2, campus_d/2), color=CONCRETE_COLOR)
    # Front
    vizshape.addBox(size=(campus_w, plinth_h, 0.4), pos=(0, plinth_h/2, -campus_d/2), color=CONCRETE_COLOR)
    
    # 2. Function to build a fence segment
    def build_fence_side(start_x, start_z, end_x, end_z):
        dist = math.sqrt((end_x-start_x)**2 + (end_z-start_z)**2)
        num_panels = int(dist / post_interval)
        
        dx = (end_x - start_x)
        dz = (end_z - start_z)
        angle = math.degrees(math.atan2(dx, dz))
        
        for i in range(num_panels + 1):
            ratio = i / num_panels
            px = start_x + dx * ratio
            pz = start_z + dz * ratio
            
            # Stone Pillar
            vizshape.addBox(size=(0.6, fence_h, 0.6), pos=(px, fence_h/2, pz), color=DARK_CONCRETE)
            
            # Iron Bars between pillars
            if i < num_panels:
                # Top and Bottom rails
                mid_x = px + (dx/num_panels)/2
                mid_z = pz + (dz/num_panels)/2
                panel_len = (dist/num_panels) - 0.5
                
                # Group for rotation
                panel_grp = viz.addGroup()
                panel_grp.setPosition(mid_x, fence_h/2, mid_z)
                panel_grp.setEuler(angle + 90, 0, 0) # Rotate to align
                
                # Rails
                vizshape.addBox(size=(panel_len, 0.1, 0.1), pos=(0, 0.8, 0), parent=panel_grp, color=FRAME_COLOR)
                vizshape.addBox(size=(panel_len, 0.1, 0.1), pos=(0, -0.8, 0), parent=panel_grp, color=FRAME_COLOR)
                
                # Vertical Pickets
                num_pickets = int(panel_len * 3)
                for p in range(num_pickets):
                    off = -panel_len/2 + (p * panel_len/(num_pickets-1))
                    vizshape.addBox(size=(0.05, 1.6, 0.05), pos=(off, 0, 0), parent=panel_grp, color=FRAME_COLOR)

    # 3. Build Sides (Leaving gaps for gates on the Left Side)
    
    # Define Gate Z positions aligned with buildings
    gate1_z = -(GAP_Z/2 + B_DEPTH/2) # Front building Z
    gate2_z = (GAP_Z/2 + B_DEPTH/2)  # Back building Z
    gate_width = 8.0
    
    left_x = -campus_w/2
    
    # Left Side: 3 Segments (Start -> Gate1, Gate1 -> Gate2, Gate2 -> End)
    # Segment 1: Front to Gate 1
    build_fence_side(left_x, -campus_d/2, left_x, gate1_z - gate_width/2)
    # Segment 2: Gate 1 to Gate 2
    build_fence_side(left_x, gate1_z + gate_width/2, left_x, gate2_z - gate_width/2)
    # Segment 3: Gate 2 to Back
    build_fence_side(left_x, gate2_z + gate_width/2, left_x, campus_d/2)
    
    # Right Side (Continuous)
    build_fence_side(campus_w/2, -campus_d/2, campus_w/2, campus_d/2)
    # Front (Continuous)
    build_fence_side(-campus_w/2, -campus_d/2, campus_w/2, -campus_d/2)
    # Back (Continuous)
    build_fence_side(-campus_w/2, campus_d/2, campus_w/2, campus_d/2)
    
    # 4. Add Gates
    add_gate(left_x, gate1_z, "Gate 1")
    add_gate(left_x, gate2_z, "Gate 2")

def create_campus_landscape():
    campus_depth = (B_DEPTH * 2 + GAP_Z + 60) 
    campus_width = (B_WIDTH * 2 + GAP_X + 80) 
    
    # Grass
    g = vizshape.addPlane(size=(campus_width, campus_depth), axis=vizshape.AXIS_Y, cullFace=False)
    g.setPosition(0, -0.2, 0)
    g.color(GRASS_COLOR)
    
    # Roads
    road_w = 12
    road_x = -(GAP_X/2 + B_WIDTH) - 15 # Left side road
    vizshape.addBox(size=(road_w, 0.1, campus_depth), pos=(road_x, -0.15, 0), color=ROAD_COLOR)
    
    # Connecting paths into gates
    gate1_z = -(GAP_Z/2 + B_DEPTH/2)
    gate2_z = (GAP_Z/2 + B_DEPTH/2)
    
    # Path from road to building through gate 1
    vizshape.addBox(size=(30, 0.1, 6), pos=(road_x + 15, -0.14, gate1_z), color=ROAD_COLOR)
    # Path from road to building through gate 2
    vizshape.addBox(size=(30, 0.1, 6), pos=(road_x + 15, -0.14, gate2_z), color=ROAD_COLOR)

    create_realistic_fence(campus_width, campus_depth)

def create_defined_roof(y):
    w = (B_WIDTH * 2) + GAP_X + 10
    d = (B_DEPTH * 2) + GAP_Z + 10
    
    glass = vizshape.addBox(size=(w, 0.05, d), pos=(0, y + 0.3, 0), color=[0.6, 0.8, 1.0])
    glass.alpha(0.5); glass.shininess(100)
    
    frame_h = 0.6
    vizshape.addBox(size=(w, frame_h, 0.5), pos=(0, y, d/2), color=ROOF_METAL_COLOR)
    vizshape.addBox(size=(w, frame_h, 0.5), pos=(0, y, -d/2), color=ROOF_METAL_COLOR)
    vizshape.addBox(size=(0.5, frame_h, d), pos=(-w/2, y, 0), color=ROOF_METAL_COLOR)
    vizshape.addBox(size=(0.5, frame_h, d), pos=(w/2, y, 0), color=ROOF_METAL_COLOR)
    
    for i in range(1, 9):
        z_pos = -d/2 + (i * d/9)
        vizshape.addBox(size=(w, 0.4, 0.3), pos=(0, y, z_pos), color=ROOF_METAL_COLOR)

def create_base_platform():
    total_w = (B_WIDTH * 2) + GAP_X + 4
    total_d = (B_DEPTH * 2) + GAP_Z + 4
    vizshape.addBox(size=(total_w, 0.2, total_d), pos=(0, -0.1, 0), color=CONCRETE_COLOR)

def create_entrance_canopy_front():
    canopy_w = GAP_X + 20
    canopy_d = 10
    canopy_h = FLOOR_HEIGHT * 1.5
    z_bot   = -(GAP_Z/2 + B_DEPTH/2)
    pos_z = z_bot - B_DEPTH/2 - 6 
    
    roof = vizshape.addBox(size=(canopy_w, 0.5, canopy_d))
    roof.setPosition(0, canopy_h, pos_z)
    roof.color(0.95, 0.95, 0.95)
    
    corners = [(-canopy_w/2+1, pos_z-canopy_d/2+1), (canopy_w/2-1, pos_z-canopy_d/2+1),
               (-canopy_w/2+1, pos_z+canopy_d/2-1), (canopy_w/2-1, pos_z+canopy_d/2-1)]
    for cx, cz in corners:
        vizshape.addCylinder(height=canopy_h, radius=0.4, pos=(cx, canopy_h/2, cz), color=DARK_CONCRETE)

# ==========================================
# 5. Construction
# ==========================================

ground = vizshape.addPlane(size=(300, 300), axis=vizshape.AXIS_Y, cullFace=False)
ground.setPosition(0, -0.3, 0)
ground.color(0.9, 0.9, 0.9) 

create_campus_landscape()
create_base_platform()

x_right = (GAP_X/2 + B_WIDTH/2)
x_left  = -(GAP_X/2 + B_WIDTH/2)
z_top   = HALL_Z_POS
z_bot   = -(GAP_Z/2 + B_DEPTH/2)

# Buildings
create_styled_building(x_left, z_bot, B_WIDTH, B_DEPTH, B_HEIGHT, 'front')
create_styled_building(x_right, z_bot, B_WIDTH, B_DEPTH, B_HEIGHT, 'front')
create_styled_building(x_left, z_top, B_WIDTH, B_DEPTH, B_HEIGHT, 'back')
create_styled_building(x_right, z_top, B_WIDTH, B_DEPTH, B_HEIGHT, 'back')

roof_y = B_HEIGHT + 2

# Elevator
elevator_x = x_left + (B_WIDTH/2) + 1.25 
elevator_z = z_bot + 4 
create_slim_elevator(elevator_x, elevator_z, roof_y)

# 🔥 BRIDGES AND STAIRS (Z-AXIS)
bridge_z_start = z_bot + B_DEPTH / 2 
bridge_z_end   = z_top - B_DEPTH / 2 

create_z_axis_bridges_and_stairs(x_left, bridge_z_start, bridge_z_end, num_levels=5)
create_z_axis_bridges_and_stairs(x_right, bridge_z_start, bridge_z_end, num_levels=5)

create_entrance_canopy_front()
create_detailed_hall(0, z_top, GAP_X, HALL_HEIGHT, B_DEPTH)
create_truss_bridge(0, BRIDGE_Y, z_top + 3, GAP_X)

offset_s = 3
vizshape.addBox(size=(4, B_HEIGHT+2, 4), pos=(x_right + offset_s, (B_HEIGHT+2)/2, z_bot), color=[0.4,0.4,0.4])
vizshape.addBox(size=(4, B_HEIGHT+2, 4), pos=(x_left - offset_s, (B_HEIGHT+2)/2, z_top), color=[0.4,0.4,0.4])

create_defined_roof(roof_y)

# Roof supports
for pos in [[x_left-9, z_bot-7], [x_right+7, z_bot-7], [x_left-9, z_top+7], [x_right+7, z_top+7]]:
    vizshape.addCylinder(height=roof_y, radius=0.6, pos=(pos[0], roof_y/2, pos[1]), color=ROOF_METAL_COLOR)

# ==========================================
# 6. Navigation
# ==========================================
cam_x = -(GAP_X/2 + B_WIDTH) - 40
cam_z = z_bot
viz.MainView.setPosition([cam_x, 10, cam_z]) 
viz.MainView.lookAt([x_left, 10, cam_z])

walk_navigate = vizcam.WalkNavigate()
viz.cam.setHandler(walk_navigate)