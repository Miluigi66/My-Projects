import random
import sys
import pygame
import numpy as np
import math

# Initialize Pygame
pygame.init()

# The screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Testing 4D Matrix Rendering")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Preload fonts to avoid recreating them in the loop
font_small = pygame.font.SysFont('Arial', HEIGHT // 50)
font_large = pygame.font.SysFont('Arial', HEIGHT // 20)


BASE_MATRIX = np.identity(5)  # 5x5 identity matrix for 4D transformations (x, y, z, w, homogenous coordinate)

tesseract = [{
    # 4D hypercube (tesseract) vertices
        "vertices": [
        np.array([[-1], [-1], [-1], [-1], [1]]),
        np.array([[1], [-1], [-1], [-1], [1]]),
        np.array([[1], [1], [-1], [-1], [1]]),
        np.array([[-1], [1], [-1], [-1], [1]]),
        np.array([[-1], [-1], [1], [-1], [1]]),
        np.array([[1], [-1], [1], [-1], [1]]),
        np.array([[1], [1], [1], [-1], [1]]),
        np.array([[-1], [1], [1], [-1], [1]]),
        np.array([[-1], [-1], [-1], [1], [1]]),
        np.array([[1], [-1], [-1], [1], [1]]),
        np.array([[1], [1], [-1], [1], [1]]),
        np.array([[-1], [1], [-1], [1], [1]]),
        np.array([[-1], [-1], [1], [1], [1]]),
        np.array([[1], [-1], [1], [1], [1]]),
        np.array([[1], [1], [1], [1], [1]]),
        np.array([[-1], [1], [1], [1], [1]])
        ],
    
    # Pivot point
    "pivot": np.array([[0], [0], [0], [0], [1]], dtype=float),
    
    # Tesseract edges
    "edges": [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
        (8, 9), (9, 10), (10, 11), (11, 8),
        (12, 13), (13, 14), (14, 15), (15, 12),
        (8, 12), (9, 13), (10, 14), (11, 15),
        (0, 8), (1, 9), (2, 10), (3, 11), (4, 12), (5, 13), (6, 14), (7, 15)
    ],
    
    # Tesseract faces (24 cubic faces)
    "faces": [
        ((0, 1, 2, 3), (255, 0, 0)),
        ((4, 5, 6, 7), (0, 255, 0)),
        ((0, 1, 5, 4), (0, 0, 255)),
        ((2, 3, 7, 6), (255, 255, 0)),
        ((0, 3, 7, 4), (255, 0, 255)),
        ((1, 2, 6, 5), (0, 255, 255)),
        ((8, 9, 10, 11), (128, 0, 0)),
        ((12, 13, 14, 15), (0, 128, 0)),
        ((8, 9, 13, 12), (0, 0, 128)),
        ((10, 11, 15, 14), (128, 128, 0)),
        ((8, 11, 15, 12), (128, 0, 128)),
        ((9, 10, 14, 13), (0, 128, 128)),
        ((0, 1, 9, 8), (200, 100, 0)),
        ((2, 3, 11, 10), (100, 200, 0)),
        ((4, 5, 13, 12), (0, 200, 100)),
        ((6, 7, 15, 14), (200, 0, 100)),
        ((0, 3, 11, 8), (100, 0, 200)),
        ((1, 2, 10, 9), (0, 100, 200)),
        ((4, 7, 15, 12), (200, 100, 50)),
        ((5, 6, 14, 13), (100, 200, 50)),
        ((0, 4, 12, 8), (150, 150, 0)),
        ((1, 5, 13, 9), (150, 0, 150)),
        ((2, 6, 14, 10), (0, 150, 150)),
        ((3, 7, 15, 11), (150, 150, 150))
    ]
}]



def calculate_position_with_matrix(inputObect, transformation_matrix):
    
    # Apply the transformation matrix to the pivot point.
    # Recompute it from the transformed vertices so it stays centered on the object.
    transformed_pivot = transformation_matrix @ inputObect["pivot"]
    
    # Apply the transformation matrix to each vertex
    transformed_vertices = []
    for vertex in inputObect["vertices"]:
        transformed_vertex = transformation_matrix @ vertex
        transformed_vertices.append(transformed_vertex)
    
    #transformed_pivot = sum(transformed_vertices) / len(transformed_vertices)
    #transformed_pivot[4][0] = 1
    
    
    return transformed_vertices, transformed_pivot



def sort_high_to_low(all_vertices, all_faces):
    sorted_faces = []
    for face in all_faces:
        vertices_indices = face[0]
        depths = [all_vertices[index][2] for index in vertices_indices]
        avg_depth = sum(depths) / len(depths)
        sorted_faces.append((avg_depth, face))

    sorted_faces.sort(reverse=True, key=lambda x: x[0])
    return [face for _, face in sorted_faces]


def moveObject(key):   

    total_movement_matrix = BASE_MATRIX.copy()
    
    # Speed modifiers
    if key[pygame.K_LSHIFT]:
        s = .5
    elif key[pygame.K_LCTRL]:
        s = .01
    else:
        s = .1
    # Movement:
    # Movement y
    if key[pygame.K_c]:
        total_movement_matrix[1][4] -= s  # Move down in y-axis
    if key[pygame.K_SPACE]:
        total_movement_matrix[1][4] += s  # Move up in y-
    # Movement z
    if key[pygame.K_w]:
        total_movement_matrix[2][4] += s # Move forward in z-axis
    if key[pygame.K_s]:
        total_movement_matrix[2][4] -= s # Move backward in z-axis
    # Movement x
    if key[pygame.K_a]:
        total_movement_matrix[0][4] -= s # Move left in x-axis
    if key[pygame.K_d]:
        total_movement_matrix[0][4] += s # Move right in x-axis
    # Movement w    
    if key[pygame.K_q]:
        total_movement_matrix[3][4] -= s
    if key[pygame.K_e]:
        total_movement_matrix[3][4] += s
    # Random movement for testing
    if key[pygame.K_p]:
        total_movement_matrix[random.randint(0, 4)][4] += random.uniform(-s, s) # Move randomly in x, y, or z-axis
        
    # Rotation:
    angle = s / 10  # Rotation angle in radians, scaled down for smoother rotation
    if key[pygame.K_KP_8]:
        # Rotate around x-axis
        rotation_matrix = np.array([[1, 0, 0, 0, 0],
                                    [0, math.cos(angle), -math.sin(angle), 0, 0],
                                    [0, math.sin(angle), math.cos(angle), 0, 0],
                                    [0, 0, 0, 1, 0],
                                    [0, 0, 0, 0, 1]],
                                   dtype=float)
        total_movement_matrix = rotation_matrix @ total_movement_matrix
    if key[pygame.K_KP_2]:
        # Rotate around x-axis in the opposite direction
        rotation_matrix = np.array([[1, 0, 0, 0, 0],
                                    [0, math.cos(-angle), -math.sin(-angle), 0, 0],
                                    [0, math.sin(-angle), math.cos(-angle), 0, 0],
                                    [0, 0, 0, 1, 0],
                                    [0, 0, 0, 0, 1]],
                                   dtype=float)
        total_movement_matrix = rotation_matrix @ total_movement_matrix
    if key[pygame.K_KP_4]:
        # Rotate around y-axis
        rotation_matrix = np.array([[math.cos(angle), 0, math.sin(angle), 0, 0],
                                    [0, 1, 0, 0, 0],
                                    [-math.sin(angle), 0, math.cos(angle), 0, 0],
                                    [0, 0, 0, 1, 0],
                                    [0, 0, 0, 0, 1]],
                                   dtype=float)
        total_movement_matrix = rotation_matrix @ total_movement_matrix
    if key[pygame.K_KP_6]:
        # Rotate around y-axis in the opposite direction
        rotation_matrix = np.array([[math.cos(-angle), 0, math.sin(-angle), 0, 0],
                                    [0, 1, 0, 0, 0],
                                    [-math.sin(-angle), 0, math.cos(-angle), 0, 0],
                                    [0, 0, 0, 1, 0],
                                    [0, 0, 0, 0, 1]],
                                   dtype=float)
        total_movement_matrix = rotation_matrix @ total_movement_matrix
    if key[pygame.K_KP_7]:
        # Rotate around z-axis
        rotation_matrix = np.array([[math.cos(angle), -math.sin(angle), 0, 0, 0],
                                    [math.sin(angle), math.cos(angle), 0, 0, 0],
                                    [0, 0, 1, 0, 0],
                                    [0, 0, 0, 1, 0],
                                    [0, 0, 0, 0, 1]],
                                   dtype=float)
        total_movement_matrix = rotation_matrix @ total_movement_matrix
    if key[pygame.K_KP_9]:
        # Rotate around z-axis in the opposite direction
        rotation_matrix = np.array([[math.cos(-angle), -math.sin(-angle), 0, 0, 0],
                                    [math.sin(-angle), math.cos(-angle), 0, 0, 0],
                                    [0, 0, 1, 0, 0],
                                    [0, 0, 0, 1, 0],
                                    [0, 0, 0, 0, 1]],
                                   dtype=float)
        total_movement_matrix = rotation_matrix @ total_movement_matrix
    if key[pygame.K_KP_1]:
        # Roate around w-axis
        rotation_matrix = np.array([[math.cos(angle), 0, 0, -math.sin(angle), 0],
                                    [0, 1, 0, 0, 0],
                                    [0, 0, 1, 0, 0],
                                    [math.sin(angle), 0, 0, math.cos(angle), 0],
                                    [0, 0, 0, 0, 1]],
                                   dtype=float)
        total_movement_matrix = rotation_matrix @ total_movement_matrix
    if key[pygame.K_KP_3]:
        # Rotate around w-axis in the opposite direction
        rotation_matrix = np.array([[math.cos(-angle), 0, 0, -math.sin(-angle), 0],
                                    [0, 1, 0, 0, 0],
                                    [0, 0, 1, 0, 0],
                                    [math.sin(-angle), 0, 0, math.cos(-angle), 0],
                                    [0, 0, 0, 0, 1]],
                                   dtype=float)
        total_movement_matrix = rotation_matrix @ total_movement_matrix
    if key[pygame.K_KP_5]:
        pass
    
    # Extra keys
    if key[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()  # Quits Game
    
    return total_movement_matrix
            
    



"""
What the matrix does when multiplied by a vertex (x, y, z, w, 1 for homogenous coordinates):
w = 1 for homogenous coordinates
[   [multiplier, 0, 0, 0, add to x],
    [0, multiplier, 0, 0, add to y],
    [0, 0, multiplier, 0, add to z],
    [0, 0, 0, multiplier, add to w],
    [nothing, nothing, nothing, nothing, nothing]
]
"""

angle = 0.05  # Rotation angle in radians 

# This helped... https://math.stackexchange.com/questions/1402362/can-rotations-in-4d-be-given-an-explicit-matrix-form

# Moving the tesseract
constant_matrix = np.array([[1, 0, 0, 0, 0],
                            [0, math.cos(angle), -math.sin(angle), 0, 0],
                            [0, math.sin(angle), math.cos(angle),0, 0],
                            [0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 1]],
                           dtype=float)

# Moving the tesseract
constant_matrix = np.array([[math.sin(angle), -math.cos(angle), 0, 0, 0],
                            [math.cos(angle), math.sin(angle), 0, 0, 0],
                            [0, 0, 1, 0, 0],
                            [0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 1]],
                           dtype=float)

# Moving the tesseract
constant_matrix = np.array([[math.cos(angle), 0, 0, -math.sin(angle), 0],
                            [0, 1, 0, 0, 0],
                            [0, 0, 1, 0, 0],
                            [math.sin(angle), 0, 0, math.cos(angle), 0],
                            [0, 0, 0, 0, 1]],
                           dtype=float)


# Main loop
def main():
    running = True
    clock = pygame.time.Clock()
    w_range_shift = 0  # Variable to shift the range of w values being rendered
    
    y_to_w = False  # Flag to toggle between y and w for rendering
    all_vertices_edges_render = False  # Flag to toggle rendering of all vertices and edges regardless of w range
    render_faces = True
    render_vertices = True
    render_edges = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    all_vertices_edges_render = not all_vertices_edges_render
                if event.key == pygame.K_KP_MINUS:
                    render_faces = not render_faces
                if event.key == pygame.K_KP_MULTIPLY:
                    render_vertices = not render_vertices
                if event.key == pygame.K_KP_DIVIDE:
                    render_edges = not render_edges
                if event.key == pygame.K_KP_5:
                    y_to_w = not y_to_w
                if event.key == pygame.K_LEFTBRACKET:
                    w_range_shift -= 1
                if event.key == pygame.K_RIGHTBRACKET:
                    w_range_shift += 1

        # Clear the screen
        screen.fill(BLACK)

        # Updates the players moving matrix based on user input
        keys = pygame.key.get_pressed()
        movement_matrix = moveObject(keys)
        tesseract[0]["vertices"], tesseract[0]["pivot"] = calculate_position_with_matrix(tesseract[0], movement_matrix)

        # Applies the constant matrix to the tesseract vertices and pivot
        #tesseract[0]["vertices"], tesseract[0]["pivot"] = calculate_position_with_matrix(tesseract[0], constant_matrix)
        
        
        toRender = sort_high_to_low(tesseract[0]["vertices"], tesseract[0]["faces"])
        
        
        # Render the faces
        if render_faces:
            for face in toRender:
                vertices_indices, color = face
                #points_to_render = []
                #points_in_w = []
                #points_not_in_w = []
                points = []
                for index in vertices_indices:
                    x, y, z, w, _ = tesseract[0]["vertices"][index]
                    # Simple perspective projection
                    factor = 200 / (z + 5)  # Adjust the factor for better visualization
                    x = int(x * factor + WIDTH // 2)
                    if y_to_w:
                        y = int(-w * factor + HEIGHT // 2)
                    else:
                        y = int(-y * factor + HEIGHT // 2)
                        #if w_range_shift <= w <= w_range_shift + 1:
                            #points_in_w.append((x, y))
                        #else:
                            #points_not_in_w.append((x, y))
                    
                    points.append((x, y))
            
                '''Not really working But here for future me to look at 
                # Finds how much of w should be rendered based on how many points are in the w range vs not in the w range, then renders that percentage of the face
                if (not points_in_w == []) and (not points_not_in_w == []):
                    percentage_in_w = len(points_in_w) / (len(points_in_w) + len(points_not_in_w))
                    points_to_render = points_in_w + points_not_in_w[:int((1 - percentage_in_w) * len(points_not_in_w))]
                    pygame.draw.polygon(screen, color, points_to_render)
                elif not points_in_w == []:
                    pass  # Don't render faces that are fully in the w range
                elif not points_not_in_w == []:
                    points_to_render = points_not_in_w
                    pygame.draw.polygon(screen, color, points_to_render)
                '''
                pygame.draw.polygon(screen, color, points)
        
            
        # Renders the vertices
        if render_vertices:
            for vertex in tesseract[0]["vertices"]:
                x, y, z, w, _ = vertex
                factor = 200 / (z + 5)
                x = int(x * factor + WIDTH // 2)
                if all_vertices_edges_render:
                    y = int(-y * factor + HEIGHT // 2)
                    pygame.draw.circle(screen, WHITE, (x, y), 5)
                else:
                    y = int(-y * factor + HEIGHT // 2)
                    if w_range_shift <= w <= w_range_shift + 1:  # Only render vertices within a certain range of w values
                        pygame.draw.circle(screen, WHITE, (x, y), 5)
        
        
        # Render the edges
        if render_edges:
            for edge in tesseract[0]["edges"]:
                start, end = edge
                x1, y1, z1, w1, _ = tesseract[0]["vertices"][start]
                x2, y2, z2, w2, _ = tesseract[0]["vertices"][end]
                factor1 = 200 / (z1 + 5)
                factor2 = 200 / (z2 + 5)
                x1 = int(x1 * factor1 + WIDTH // 2)
                x2 = int(x2 * factor2 + WIDTH // 2)
                if all_vertices_edges_render:
                    y1 = int(-y1 * factor1 + HEIGHT // 2)
                    y2 = int(-y2 * factor2 + HEIGHT // 2)
                    pygame.draw.line(screen, WHITE, (x1, y1), (x2, y2), 1)
                else:
                    y1 = int(-y1 * factor1 + HEIGHT // 2)
                    y2 = int(-y2 * factor2 + HEIGHT // 2)
                    
                    w_min = w_range_shift
                    w_max = w_range_shift + 1
                    w1_in = w_min <= w1 <= w_max
                    w2_in = w_min <= w2 <= w_max
                    
                    if w1_in and w2_in:
                        # Both endpoints in range
                        pygame.draw.line(screen, WHITE, (x1, y1), (x2, y2), 1)
                    elif w1_in and not w2_in:
                        # w1 in range, w2 out - interpolate to boundary
                        boundary_w = w_max if w2 > w_max else w_min
                        if w1 != w2:
                            t = (boundary_w - w1) / (w2 - w1)
                            x2_new = int(x1 + t * (x2 - x1))
                            y2_new = int(y1 + t * (y2 - y1))
                        else:
                            x2_new, y2_new = x2, y2
                        pygame.draw.line(screen, WHITE, (x1, y1), (x2_new, y2_new), 1)
                    elif w2_in and not w1_in:
                        # w2 in range, w1 out - interpolate to boundary
                        boundary_w = w_max if w1 > w_max else w_min
                        if w1 != w2:
                            t = (boundary_w - w2) / (w1 - w2)
                            x1_new = int(x2 + t * (x1 - x2))
                            y1_new = int(y2 + t * (y1 - y2))
                        else:
                            x1_new, y1_new = x1, y1
                        pygame.draw.line(screen, WHITE, (x1_new, y1_new), (x2, y2), 1)

        
        # Display metrics
        metrics = [
            (f"FPS: {int(clock.get_fps())}", 0, 0),
            (f"The dimension you are in is {('xyzw' if not y_to_w else 'xwzy')}", 0, 15),
            (f"The matrix that is currently being applied to the tesseract is:", 0, 30),
                (f"{movement_matrix[0]}" , 15, 45),
                (f"{movement_matrix[1]}" , 15, 60),
                (f"{movement_matrix[2]}" , 15, 75),
                (f"{movement_matrix[3]}" , 15, 90),
            (f"The pivot point is at: {tesseract[0]["pivot"]}" , 0, 105),
            (f"Key bindings:", 0, 120),
            (f"use [ and ] to shift what range of w you see by 1", 15, 135),
                (f"The w range is: {w_range_shift} to {w_range_shift + 1}" , 15, 150),
                    (f"L_TAB: toggle rendering of all vertices and edges (regardless of w range): {'ON' if all_vertices_edges_render else 'OFF'}", 30, 165),
                (f"Press: NP_- : toggle faces: {'ON' if render_faces else 'OFF'}", 15, 180),
                (f"Press: NP_* : toggle vertices: {'ON' if render_vertices else 'OFF'}", 15, 195),
                (f"Press: NP_/ : toggle edges: {'ON' if render_edges else 'OFF'}", 15, 210),
                (f"Press: NP_5 : toggle between using y or w for rendering: {'w' if y_to_w else 'y'}", 15, 225),
        ]
        for text, x, y in metrics:
            surface = font_small.render(text, False, WHITE)
            screen.blit(surface, (x, y))

        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()
    
if __name__ == "__main__":
    main()
