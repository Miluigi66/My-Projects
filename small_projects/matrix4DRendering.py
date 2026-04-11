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
font_small = pygame.font.SysFont('Arial', 20)
font_large = pygame.font.SysFont('Arial', 30)


BASE_MATRIX = np.array([[1, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 1]], 
                       dtype=float)


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
    "pivot": (0, 0, 0, 0),
    
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
    
    # Apply the transformation matrix pivot to the pivot point
    pivot = np.array([[inputObect["pivot"][0]], [inputObect["pivot"][1]], [inputObect["pivot"][2]], [inputObect["pivot"][3]], [1]])
    transformed_pivot = transformation_matrix @ pivot
    
    # Apply the transformation matrix to each vertex
    transformed_vertices = []
    for vertex in inputObect["vertices"]:
        transformed_vertex = transformation_matrix @ vertex
        transformed_vertices.append(transformed_vertex)
    
    
    return transformed_vertices, (transformed_pivot[0][0], transformed_pivot[1][0], transformed_pivot[2][0], transformed_pivot[3][0])



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

# Moving the tesseract
movement_matrix = np.array([[1, 0, 0, 0, 0],
                            [0, math.cos(angle), -math.sin(angle), 0, 0],
                            [0, math.sin(angle), math.cos(angle),0, 0],
                            [0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 1]], 
                           dtype=float)

# Moving the tesseract
movement_matrix = np.array([[math.sin(angle), -math.cos(angle), 0, 0, 0],
                            [math.cos(angle), math.sin(angle), 0, 0, 0],
                            [0, 0, 1, 0, 0],
                            [0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 1]], 
                           dtype=float)

# Moving the tesseract
movement_matrix = np.array([[1, 0, 0, 0, 0],
                            [0, 1, 0, 0, 0],
                            [0, 0, math.cos(angle), -math.sin(angle), 0],
                            [0, 0, math.sin(angle), math.cos(angle), 0],
                            [0, 0, 0, 0, 1]], 
                           dtype=float)


# Main loop
def main():
    y_to_w = False  # Flag to toggle between y and w for rendering
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_to_w = True
                elif event.key == pygame.K_DOWN:
                    y_to_w = False
        
        # Clear the screen
        screen.fill(BLACK)

        # Updates the players moving matrix based on user input
        keys = pygame.key.get_pressed()
        tesseract[0]["vertices"], tesseract[0]["pivot"] = calculate_position_with_matrix(tesseract[0], moveObject(keys))

        # Applies the movement matrix to the tesseract vertices and pivot
        tesseract[0]["vertices"], tesseract[0]["pivot"] = calculate_position_with_matrix(tesseract[0], movement_matrix)
        toRender = sort_high_to_low(tesseract[0]["vertices"], tesseract[0]["faces"])
        
        
        # Render the faces
        for face in toRender:
            vertices_indices, color = face
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
                points.append((x, y))
            pygame.draw.polygon(screen, color, points)
            
        # Renders the vertices
        for vertex in tesseract[0]["vertices"]:
            x, y, z, w, _ = vertex
            factor = 200 / (z + 5)
            x = int(x * factor + WIDTH // 2)
            if y_to_w:
                y = int(-w * factor + HEIGHT // 2)
            else:
                y = int(-y * factor + HEIGHT // 2)
            pygame.draw.circle(screen, WHITE, (x, y), 5)
        
        
        
        # Display metrics
        metrics = [
            (f"FPS: {int(clock.get_fps())}", 0, 0),
            (f"Press UP to render using w coordinate, DOWN to render using y coordinate", 0, 30),
            (f"The matrix that is currently being applied to the tesseract is:", 0, 60),
            (f"{movement_matrix[0]}" , 30, 90),
            (f"{movement_matrix[1]}" , 30, 120),
            (f"{movement_matrix[2]}" , 30, 150),
            (f"{movement_matrix[3]}" , 30, 180),
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
