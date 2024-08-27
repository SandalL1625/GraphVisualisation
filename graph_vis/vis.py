import sys
import pygame
import random as rn

build_graph = False
run = True

pygame.init()
pygame.display.set_caption('Graph Visualisation')
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)

nodes_group = pygame.sprite.Group()
edges_group = []

graph = {}


def terminate():
    pygame.quit()
    sys.exit()


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, r=20, color=(0, 255, 0)):
        super().__init__()
        self.r = r
        self.color = color
        self.connects = []
        self.image = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.r, self.r), self.r)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def change_color(self, color):
        self.color = color
        pygame.draw.circle(self.image, color, (self.r, self.r), self.r)

    def random_pos(self, x_d, y_d):
        self.rect.x = rn.randrange(x_d[0], x_d[1], 1)
        self.rect.y = rn.randrange(y_d[0], y_d[1], 1)

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(*mouse_pos)


class Edge:
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2
        self.draw_lines()

    def draw_lines(self):
        pygame.draw.line(screen, (0, 0, 0), self.n1.rect.center, self.n2.rect.center, 5)


def preset_1():
    return rn.randrange(6, 10, 1), rn.randrange(2, 3) - 0.5


def generate_random_graph(num, edge_part):
    edge_num = int(num * edge_part)
    nodes = []
    for i in range(num):
        node = Node((0, 0))
        node.change_color((rn.randrange(1, 256, 1), rn.randrange(1, 256, 1), rn.randrange(1, 256, 1)))
        node.random_pos((100, width - 100), (80, height - 80))
        while pygame.sprite.spritecollideany(node, nodes_group):
            node.random_pos((100, width - 100), (80, height - 80))
        nodes_group.add(node)
        nodes.append(node)
        graph[node] = []
    for i in range(edge_num):
        n1, n2 = tuple(rn.choices(nodes, k=2))
        while n2 in graph[n1]:
            n1, n2 = tuple(rn.choices(nodes, k=2))
        edges_group.append(Edge(n1, n2))
        graph[n1].append(n2)
        graph[n2].append(n1)


def kill_all():
    global edges_group
    global graph
    nodes_group.empty()
    edges_group = []
    graph = {}


def connect(n1, n2):
    graph[n1].append(n2)
    graph[n2].append(n1)
    edges_group.append(Edge(n1, n2))


def add(pos, color=(0, 255, 0)):
    node = Node(pos, color=color)
    nodes_group.add(node)
    graph[node] = []


def start():
    global build_graph

    picked = None

    while run:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    build_graph = not build_graph

            if event.type == pygame.MOUSEBUTTONDOWN:
                if build_graph:
                    for node in nodes_group:
                        if node.check_click(event.pos):
                            if picked:
                                if picked == node:
                                    break
                                connect(node, picked)
                                picked = None
                            else:
                                picked = node
                            break
                    else:
                        picked = None
                        add(event.pos)
                else:
                    kill_all()
                    generate_random_graph(*preset_1())

        for edge in edges_group:
            edge.draw_lines()
        nodes_group.draw(screen)
        pygame.display.flip()

    pygame.quit()


start()
