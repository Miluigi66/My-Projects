import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Rendering Engine")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load and transform the image
#ANY WORK
image = pygame.image.load("stocl.jpg")
image = pygame.transform.scale(image, (200, 200))  # Adjust the size as needed

vertices = [
    (-1, -1, -1),
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, 1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1)
]

# Pivot point
pivot = (0, 0, 0)  # Pivot point

# Cube edges
# (start_vertex, end_vertex)
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Cube faces
# ((vertex1, vertex2, vertex3, vertex4), color)
faces = [
    ((0, 1, 2, 3), (255, 0, 0)),
    ((4, 5, 6, 7), (0, 255, 0)),
    ((0, 1, 5, 4), (0, 0, 255)),
    ((2, 3, 7, 6), (255, 255, 0)),
    ((0, 3, 7, 4), (255, 0, 255)),
    ((1, 2, 6, 5), (0, 255, 255))
]

def project(x, y, z, scale, distance):
    factor = scale / (distance + z)
    x = x * factor + WIDTH // 2
    y = -y * factor + HEIGHT // 2
    return int(x), int(y)

# Draw faces and edges (edges are turned off by default because that overlaps the faces)
def draw_faces_and_edges(transformed_vertices):
    # Calculate the average depth of each face
    face_depths = []
    for face in faces:
        vertices_indices, color = face
        avg_depth = np.mean([transformed_vertices[i][2] for i in vertices_indices])
        face_depths.append((avg_depth, face))
    
    # Sort faces by depth (furthest to closest)
    face_depths.sort(reverse=True, key=lambda x: x[0])
    
    # Draw faces in sorted order
    for i, face in face_depths:
        vertices_indices, color = face
        points = [project(*transformed_vertices[i], 400, 4) for i in vertices_indices]
        
        # Draw the image on the first face
        if face == faces[0]:
            image_points = [project(*transformed_vertices[i], 400, 4) for i in vertices_indices]
            image_rect = pygame.Rect(min(p[0] for p in image_points), min(p[1] for p in image_points),
                                     max(p[0] for p in image_points) - min(p[0] for p in image_points),
                                     max(p[1] for p in image_points) - min(p[1] for p in image_points))
            screen.blit(pygame.transform.scale(image, (image_rect.width, image_rect.height)), image_rect)
        else:
            pygame.draw.polygon(screen, color, points)

    # Calculate the average depth of each edge
    edge_depths = []
    for edge in edges:
        avg_depth = np.mean([transformed_vertices[i][2] for i in edge])
        edge_depths.append((avg_depth, edge))
    
    # Sort edges by depth (furthest to closest)
    edge_depths.sort(reverse=True, key=lambda x: x[0])
    
    # Draw edges in sorted order
    for _, edge in edge_depths:
        points = []
        for vertex in edge:
            x, y, z = transformed_vertices[vertex]
            points.append(project(x, y, z, 400, 4))
        #pygame.draw.line(screen, WHITE, points[0], points[1], 1)

def main():
    clock = pygame.time.Clock()
    angle_x = 0
    angle_y = 0
    angle_z = 0
    pos_x = 0
    pos_y = 0
    pos_z = 0
    distance = 4
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            angle_y -= 0.1
        if keys[pygame.K_RIGHT]:
            angle_y += 0.1
        if keys[pygame.K_UP]:
            angle_x -= 0.1
        if keys[pygame.K_DOWN]:
            angle_x += 0.1
        if keys[pygame.K_e]:
            angle_z -= 0.1
        if keys[pygame.K_q]:
            angle_z += 0.1
        if keys[pygame.K_s]:
            pos_z -= 0.1
        if keys[pygame.K_w]:
            pos_z += 0.1
        if keys[pygame.K_a]:
            pos_x -= 0.1
        if keys[pygame.K_d]:
            pos_x += 0.1
        if keys[pygame.K_SPACE]:
            pos_y += 0.1
        if keys[pygame.K_c]:
            pos_y -= 0.1

        screen.fill(BLACK)
        #pygame.draw.rect(screen, (0, 255, 0), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
        # Rotate cube
        cos_angle_x = math.cos(angle_x)
        sin_angle_x = math.sin(angle_x)
        cos_angle_y = math.cos(angle_y)
        sin_angle_y = math.sin(angle_y)
        cos_angle_z = math.cos(angle_z)
        sin_angle_z = math.sin(angle_z)

        transformed_vertices = []
        for x, y, z in vertices:
            # Translate to pivot
            x -= pivot[0]
            y -= pivot[1]
            z -= pivot[2]
            # Rotate around x-axis
            y, z = y * cos_angle_x - z * sin_angle_x, z * cos_angle_x + y * sin_angle_x
            # Rotate around y-axis
            x, z = x * cos_angle_y - z * sin_angle_y, z * cos_angle_y + x * sin_angle_y
            # Rotate around z-axis
            x, y = x * cos_angle_z - y * sin_angle_z, y * cos_angle_z + x * sin_angle_z
            # Translate back from pivot
            x += pivot[0] + pos_x
            y += pivot[1] + pos_y
            z += pivot[2] + pos_z
            transformed_vertices.append((x, y, z))

        # Draw faces
        draw_faces_and_edges(transformed_vertices)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
