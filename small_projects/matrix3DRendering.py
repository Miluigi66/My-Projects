import pygame
import numpy as np
import math

# Initialize Pygame
pygame.init()

# The screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Testing 3D Matrix Rendering")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

square = [{
        # Cube vertices
        "vertices": [
            np.array([[-1], [-1], [-1], [1]]),
            np.array([[1], [-1], [-1], [1]]),
            np.array([[1], [1], [-1], [1]]),
            np.array([[-1], [1], [-1], [1]]),
            np.array([[-1], [-1], [1], [1]]),
            np.array([[1], [-1], [1], [1]]),
            np.array([[1], [1], [1], [1]]),
            np.array([[-1], [1], [1], [1]])
        ],
        
        # Pivot point
        "pivot": (0, 0, 0),  # Pivot point
        
        # Cube edges
        "edges": [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ],
        
        # Cube faces
        "faces": [
            ((0, 1, 2, 3), (255, 0, 0)),
            ((4, 5, 6, 7), (0, 255, 0)),
            ((0, 1, 5, 4), (0, 0, 255)),
            ((2, 3, 7, 6), (255, 255, 0)),
            ((0, 3, 7, 4), (255, 0, 255)),
            ((1, 2, 6, 5), (0, 255, 255))
        ]
    }]


def calculate_position(inputObect, angle_x, angle_y, angle_z, pos_x, pos_y, pos_z):
    cos_angle_x = math.cos(angle_x)
    sin_angle_x = math.sin(angle_x)
    cos_angle_y = math.cos(angle_y)
    sin_angle_y = math.sin(angle_y)
    cos_angle_z = math.cos(angle_z)
    sin_angle_z = math.sin(angle_z)

    transformed_vertices = []
    for i in range(len(inputObect["vertices"])):
        x, y, z, w = inputObect["vertices"][i].flatten()
        # Translate to pivot
        x -= inputObect["pivot"][0]
        y -= inputObect["pivot"][1]
        z -= inputObect["pivot"][2]
        
        # Rotate around x-axis
        y, z = y * cos_angle_x - z * sin_angle_x, z * cos_angle_x + y * sin_angle_x
        # Rotate around y-axis
        x, z = x * cos_angle_y - z * sin_angle_y, z * cos_angle_y + x * sin_angle_y
        # Rotate around z-axis
        x, y = x * cos_angle_z - y * sin_angle_z, y * cos_angle_z + x * sin_angle_z
        
        # Apply position offsets
        x += inputObect["pivot"][0] + pos_x
        y += inputObect["pivot"][1] + pos_y
        z += inputObect["pivot"][2] + pos_z
        
        # Update pivot's position
        pivot = (inputObect["pivot"][0] + pos_x, inputObect["pivot"][1] + pos_y, inputObect["pivot"][2] + pos_z)
            
        transformed_vertices.append(np.array([[x], [y], [z], [w]]))
    
    return transformed_vertices, pivot


def calculate_position_with_matrix(inputObect, transformation_matrix):
    
    # Apply the transformation matrix pivot to the pivot point
    pivot = np.array([[inputObect["pivot"][0]], [inputObect["pivot"][1]], [inputObect["pivot"][2]], [1]])
    transformed_pivot = transformation_matrix @ pivot
    
    # Apply the transformation matrix to each vertex
    transformed_vertices = []
    for vertex in inputObect["vertices"]:
        transformed_vertex = transformation_matrix @ vertex
        transformed_vertices.append(transformed_vertex)
    
    
    return transformed_vertices, (transformed_pivot[0][0], transformed_pivot[1][0], transformed_pivot[2][0])



def sort_high_to_low(all_vertices, all_faces):
    sorted_faces = []
    for face in all_faces:
        vertices_indices = face[0]
        depths = [all_vertices[index][2] for index in vertices_indices]
        avg_depth = sum(depths) / len(depths)
        sorted_faces.append((avg_depth, face))

    sorted_faces.sort(reverse=True, key=lambda x: x[0])
    return [face for _, face in sorted_faces]


"""
What the matrix does when multiplied by a vertex (x, y, z, w):
w = 1 for homogenous coordinates
[   [multiplier, 0, 0, add to x],
    [0, multiplier, 0, add to y],
    [0, 0, multiplier, add to z],
    [nothing, nothing, nothing, nothing]  
]
"""

BASE_MATRIX = np.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

# X-axis rotation matrix (rotate by angle in radians)
angle_x = 0.005  # Rotation angle in radians (~2.9 degrees)
trying_to_figure_out_rotation = np.array([[1, 0, 0, 0],
                                            [0, math.cos(angle_x), -math.sin(angle_x), 0],
                                            [0, math.sin(angle_x), math.cos(angle_x), 0],
                                            [0, 0, 0, 1]])

# Main loop
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Clear the screen
        screen.fill(BLACK)

        #square[0]["vertices"], square[0]["pivot"] = calculate_position(square[0],0,0,0,.01,0,0)
        square[0]["vertices"], square[0]["pivot"] = calculate_position_with_matrix(square[0], trying_to_figure_out_rotation)
        toRender = sort_high_to_low(square[0]["vertices"], square[0]["faces"])
        
        # Render the faces
        for face in toRender:
            vertices_indices, color = face
            points = []
            for index in vertices_indices:
                x, y, z, _ = square[0]["vertices"][index]
                # Simple perspective projection
                factor = 200 / (z + 5)  # Adjust the factor for better visualization
                x = int(x * factor + WIDTH // 2)
                y = int(-y * factor + HEIGHT // 2)
                points.append((x, y))
            pygame.draw.polygon(screen, color, points)
            
        # Renders the vertices
        for vertex in square[0]["vertices"]:
            x, y, z, _ = vertex
            factor = 200 / (z + 5)
            x = int(x * factor + WIDTH // 2)
            y = int(-y * factor + HEIGHT // 2)
            pygame.draw.circle(screen, WHITE, (x, y), 5)
        
        # Update the display
        pygame.display.flip()
    
    pygame.quit()
    
if __name__ == "__main__":
    main()
