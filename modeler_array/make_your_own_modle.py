import pygame
import math
import numpy as np

#models
print("Importing modles.... (Might take a while)")
from model import MODLES
print("DONEEEEEEEEEEE")
#modles
# Quick fix
quick_fix = False

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Rendering Engine")

# Colors
invert_colors = False
if invert_colors:
    WHITE = (0, 0, 0)
    BLACK = (255, 255, 255)
else:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

# Darken effect
# Bigger number = less darkening
darken_effect = 50

# Is the user creating a custom shape?
making = False
# Show edges?
show_edges = False
# Allows for moving vertices (makes 2 vertices one to move one to save)
moving_vertice = False
vertice_to_move = 0
prev_vertices = (0, 0, 0)
# Allows for the creation of custom shapes
class HumanMadeShape:
    # Initialize vertices, edges, and faces
    def __init__(self):
        if quick_fix or input("Do you want to edit the shape? (y/n): ") == "y":
            global making
            making = True
            print("Keybinds:")
            print("(Once slected you can move virtces)")
            print("b: Add a vertex ")
            print("n: Add an edge")
            print("m: Add a face")
            print(",: Set pivot point")
            print(".: Remove something")
            print("/: Turn edge shows on/off")
            print("p: Move a vertice")
        self.vertices = []
        self.edges = []
        self.faces = []
        self.pivot = (0, 0, 0)
        if quick_fix == False:
            if input("Do you already have a work in progress shape? (y/n): ") == "y":
                if input ("Do you want to import a file? (y/n): ") == "y":
                    self.import_shape_from_file()
                else:
                    self.import_shape_manually()
        else:
            self.vertices = MODLES['square']["vertices"]
            self.edges = MODLES['square']["edges"]
            self.faces = MODLES['square']["faces"]
            self.pivot = MODLES['square']["pivot"]
        
    def add_new_vertex(self, x, y, z):
        self.vertices.append((x, y, z))

    def add_new_edge(self, start_vertex, end_vertex):
        self.edges.append((start_vertex, end_vertex))

    def add_new_face(self, vertex_indices, color):
        self.faces.append((vertex_indices, color))

    def remove_previous_vertex(self, vertex_index):
        self.vertices.pop(vertex_index)

    def remove_previous_edge(self, edge_index):
        self.edges.pop(edge_index)  

    def remove_previous_face(self, face_index):
        self.faces.pop(face_index)

    def set_pivot(self, x, y, z):
        self.pivot = (x, y, z)
    
    def export_shape(self):
        data = {
            "vertices": self.vertices,
            "edges": self.edges,
            "faces": self.faces,
            "pivot": self.pivot
        }
        shape_name = input("Enter the name of the shape: ")
        with open("modles.py", "a") as file:
            file.write(f"\nTEMP_MOVE = {{'{shape_name}': {data}}}")
            
    
    def import_shape_from_file(self):
        
        while True:
            print("Available shapes:")
            for key in MODLES.keys():
                print(key)
            input_model = input("Enter the model you want to import: ")
            if input_model in MODLES:
                self.vertices = MODLES[input_model]["vertices"]
                self.edges = MODLES[input_model]["edges"]
                self.faces = MODLES[input_model]["faces"]
                self.pivot = MODLES[input_model]["pivot"]
                break
            else:
                print("Model not found.")
        
    def import_shape_manually(self):
        print("Be careful with the format of the input")
        print("Format for vertices: [(x1, y1, z1), (x2, y2, z2), ...]")
        self.vertices = eval(input("Enter the vertices of the shape: "))
        print("Format for edges: [(start_vertex1, end_vertex1), (start_vertex2, end_vertex2), ...]")
        self.edges = eval(input("Enter the edges of the shape: "))
        print("Format for faces: [((vertex1, vertex2, vertex3, ..., vertexn), color1), ...]")
        self.faces = eval(input("Enter the faces of the shape: "))
        print("Format for pivot: (x, y, z)")
        self.pivot = eval(input("Enter the pivot point of the shape: "))

# Initialize the shape
working_shape = HumanMadeShape()
vertices = working_shape.vertices
edges = working_shape.edges
faces = working_shape.faces
pivot = working_shape.pivot


def project(x, y, z, scale, distance):
    factor = scale / (distance + z)
    x = x * factor + WIDTH // 2
    y = -y * factor + HEIGHT // 2
    return int(x), int(y)

# Draw faces and edges (sometimes)
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
    for depth, face in face_depths:
        vertices_indices, color = face
        points = [project(*transformed_vertices[i], 400, 4) for i in vertices_indices]
        
        # Darken the color based on depth
        darken_factor = max(0, min(1, 1 - depth / darken_effect))  # Adjust the divisor to control the darkening effect
        darkened_color = tuple(int(c * darken_factor) for c in color)
        
        pygame.draw.polygon(screen, darkened_color, points)

    if show_edges:    
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
            pygame.draw.line(screen, WHITE, points[0], points[1], 1)
        # Draw a small circle at each vertex
        for vertex in range(len(vertices)):
            x, y, z = transformed_vertices[vertex]
            screen_x, screen_y = project(x, y, z, 400, 4)
            pygame.draw.circle(screen, WHITE, (screen_x, screen_y), 6)
            # Draw the index of the vertice
            vector_font = pygame.font.SysFont('Arial', 16)
            vector_number = vector_font.render(str(vertex), True, (255, 0, 0))  # Red color for visibility
            screen.blit(vector_number, (screen_x - 5, screen_y - 5))
    # Draw a small circle at the vertex being moved
    #if moving_vertice:
    #    x, y, z = pos_moving_vertice
    #    screen_x, screen_y = project(x, y, z, 400, 4)
    #    pygame.draw.circle(screen, WHITE, (screen_x, screen_y), 6)
        


def main():
    
    global vertices
    global edges
    global faces
    global pivot
    
    clock = pygame.time.Clock()
    angle_x = 0
    angle_y = 0
    angle_z = 0
    pos_x = 0
    pos_y = 0
    pos_z = 0
    running = True
    can_move = True
    can_rotate = True
    
    #vertex moving variables
    vertex_pos_x = 0
    vertex_pos_y = 0
    vertex_pos_z = 0
    
    
    while running:
        # Single input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if making:
                        if input("Do you want to save your shape? (y/n): ") == "y":
                            working_shape.export_shape()
                    running = False
                if making:
                    if event.key == pygame.K_SLASH:
                        global show_edges
                        show_edges = not show_edges
                        print("Edges are now " + ("on" if show_edges else "off"))
                    # Vertex moving
                    elif event.key == pygame.K_p :
                        if input("Do you want to move a vertice? (y/n): ") == "y":
                            global moving_vertice
                            global vertice_to_move
                            if moving_vertice:
                                print("You are already moving a vertice")
                            else:
                                moving_vertice = True 
                                temp_vertices = ""
                                try:
                                    for i in range(len(vertices)):
                                        temp_vertices += (str(i) + ": " + str(vertices[i]) + " ")
                                    print("Here are the vertices you have: \n" + str(temp_vertices))
                                    vertice_to_move = int(input("Enter the index of the vertice you want to move: "))
                                    prev_vertices = transformed_vertices[vertice_to_move]
                                    vertex_pos_x, vertex_pos_y, vertex_pos_z = transformed_vertices[vertice_to_move]
                                except Exception as e:
                                    print(f"Error: {e}")
                    # Vertex moving
                    elif event.key == pygame.K_RETURN and moving_vertice:
                        working_shape.vertices[vertice_to_move] = (vertex_pos_x, vertex_pos_y, vertex_pos_z)
                        vertices = working_shape.vertices[:]
                        moving_vertice = False
                        print("Vertice moved")
                    # Vertex moving
                    elif event.key == pygame.K_BACKSPACE:
                        print("Undid moving vertice")
                        moving_vertice = False
                        working_shape.vertices[vertice_to_move] = prev_vertices
                        vertices = working_shape.vertices[:]
                    # Reste Rotation
                    elif event.key == pygame.K_r:
                        angle_x = 0
                        angle_y = 0
                        angle_z = 0
                        
                    
        # Continuous input
        keys = pygame.key.get_pressed()
        if can_rotate:
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
                
                
        if can_move:
            if moving_vertice:
                if keys[pygame.K_s]:
                    vertex_pos_z -= 0.1
                if keys[pygame.K_w]:
                    vertex_pos_z += 0.1
                if keys[pygame.K_a]:
                    vertex_pos_x -= 0.1
                if keys[pygame.K_d]:
                    vertex_pos_x += 0.1
                if keys[pygame.K_SPACE]:
                    vertex_pos_y += 0.1
                if keys[pygame.K_c]:
                    vertex_pos_y -= 0.1
                if keys[pygame.K_LSHIFT]:
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
                    
            else:
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
        
        # Manual shape slection
        if making:
            if keys[pygame.K_m]:
                try:
                    if input("Do you want to add a new face? (y/n): ") == "y":
                        print("Enter the vertices of the face you want to add: ")
                        while True:
                            print("Format for color: (r, g, b) up to 255")
                            temp_color = eval(input())
                            screen.fill(temp_color)
                            pygame.display.flip()
                            this_color = input("Is this the color you want? (y/n): (see screen for color)")
                            if this_color == "y":
                                break
                        temp_vertices = ""
                        for i in range(len(vertices)):
                            temp_vertices += (str(i) + ": " + str(vertices[i]) + " ")
                        print("Here are the vertices you have: \n" + str(temp_vertices))
                        print("Format for vertex: (vertex1, vertex2, vertex3, ..., vertexn)")
                        working_shape.add_new_face(eval(input()), temp_color)
                except Exception as e:
                    print(f"Error: {e}")
            if keys[pygame.K_n]:
                try:
                    if input("Do you want to add a new edge? (y/n): ") == "y":
                        print("Enter the vertice # of the edge you want to add: ")
                        temp_vertices = ""
                        for i in range(len(vertices)):
                            temp_vertices += (str(i) + ": " + str(vertices[i]) + " ")
                        print("Here are the vertices you have: \n" + str(temp_vertices))
                        print("Format: (vertex1, vertex2)")
                        working_shape.add_new_edge(*eval(input()))
                except Exception as e:
                    print(f"Error: {e}")
            if keys[pygame.K_b] and not moving_vertice:
                try:
                    if input("Do you want to add a new vertex? (y/n): ") == "y":
                        print("Enter the vertex you want to add: ")
                        print("Format: (x, y, z)")
                        working_shape.add_new_vertex(*eval(input()))
                except Exception as e:
                    print(f"Error: {e}")
            if keys[pygame.K_COMMA]:
                try:
                    print("Here are the vertices you have: \n" + str(vertices))
                    print("Enter the pivot point of the shape: ")
                    print("Format: (x, y, z)")
                    working_shape.set_pivot(*eval(input()))
                except Exception as e:
                    print(f"Error: {e}")
            if keys[pygame.K_PERIOD]:
                try:
                    if input("Do you want to remove something? (y/n): ") == "y":
                        what_to_remove = input("What do you want to remove? (vertex (v), edge (e), face (f)): ")
                        if what_to_remove == "v" or what_to_remove == "vertex" and not moving_vertice:
                            temp_vertices = ""
                            for i in range(len(vertices)):
                                temp_vertices += (str(i) + ": " + str(vertices[i]) + " ")
                            print("Enter the index of the vertex you want to remove: ")
                            print("Here are the vertices you have: \n" + str(temp_vertices))
                            working_shape.remove_previous_vertex(int(input()))
                        elif what_to_remove == "e" or what_to_remove == "edge":
                            temp_edges = ""
                            for i in range(len(edges)):
                                temp_edges += (str(i) + ": " + str(edges[i]) + " ")
                            print("Enter the index of the edge you want to remove: ")
                            print("Here are the edges you have: \n" + str(temp_edges))
                            working_shape.remove_previous_edge(int(input()))
                        elif what_to_remove == "f" or what_to_remove == "face":
                            temp_faces = ""
                            for i in range(len(faces)):
                                temp_faces += (str(i) + ": " + str(faces[i]) + " ")
                            print("Enter the index of the face you want to remove: ")
                            print("Here are the faces you have: \n" + str(temp_faces))
                            working_shape.remove_previous_face(int(input()))
                except Exception as e:
                    print(f"Error: {e}")

        
            # Mouse input
            # Color change the clicked face closest to the camera
            if pygame.mouse.get_pressed()[0]:
                touching_face = []
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, face in enumerate(faces):
                    vertices_indices, color = face
                    points = [project(*transformed_vertices[j], 400, 4) for j in vertices_indices]
                    polygon = pygame.draw.polygon(screen, color, points)
                    if polygon.collidepoint(mouse_x, mouse_y):
                        touching_face.append((vertices_indices, color))
                if touching_face:
                    face_depths = []
                    for face in touching_face:
                        vertices_indices, color = face
                        avg_depth = np.mean([transformed_vertices[i][2] for i in vertices_indices])
                        face_depths.append((avg_depth, face))
                    # Sort faces by depth (closest to furthest)
                    face_depths.sort(key=lambda x: x[0])
                    vertices_indices, color = face_depths[0][1]
                    points = [project(*transformed_vertices[i], 400, 4) for i in vertices_indices]
                    polygon = pygame.draw.polygon(screen, color, points)
                    
                    while True:
                        try:
                            new_color = (0,255,0)#eval(input("Enter the new color for the face (r, g, b): "))
                            face_index = faces.index(face_depths[0][1])
                            working_shape.faces[face_index] = (vertices_indices, new_color)
                            faces = working_shape.faces[:]
                            break
                        except Exception as e:
                            print(f"Error: {e}")
                                
                                


            
        
        screen.fill(BLACK)
        #pygame.draw.rect(screen, (0, 255, 0), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
        
        # Rotate 
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
        
        # If the user is moving a vertice says this one actually changed
        if moving_vertice:
            # Apply the same rotation to the vertex being moved
            x, y, z = vertex_pos_x, vertex_pos_y, vertex_pos_z
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
            transformed_vertices[vertice_to_move] = (x, y, z)
        # Draw faces
        draw_faces_and_edges(transformed_vertices)

        # See FPS
        fps = str(int(clock.get_fps()))
        font = pygame.font.SysFont('Arial', 30)
        fpssurface = font.render(fps, False, (255, 255, 255))
        screen.blit(fpssurface, (0, 0))


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
