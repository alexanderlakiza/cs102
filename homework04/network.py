from api import get_friends
import igraph
import numpy as np
from igraph import Graph, plot

def get_network(user_id, as_edgelist=True):
    
    edges = []
    sec_friends = []  # друзья друзей
    friends = get_friends(user_id,'bdate,sex')
    first_friends = [friends[i]['id'] for i in range(len(friends))]  # id-ки друзей анализируемого пользователя
    
    for o in range(len(first_friends)):
        sec_friends.append(get_friends(first_friends[o],'bdate,sex'))  # список для каждого друга с его списком друзей
    
    for i in range(len(sec_friends)):
        try:
            for j in range(len(sec_friends[i])):  # проходим через друзей друзей
                for k in range(len(first_friends)):
                    if sec_friends[i][j]['id'] == first_friends[k]:  # находим совпадения с изначальным списком друзей
                        edges.append((i, k))
        except:
            pass
    #edges = [(0, 4), (0, 9), (0, 16), (0, 24), (0, 29), (0, 37), (0, 62), (0, 71), (0, 75), (0, 77), (0, 84), (3, 5), (3, 7), (3, 9), (3, 16), (3, 19), (3, 23), (3, 29), (3, 30), (3, 32), (3, 45), (3, 47), (3, 49), (3, 54), (3, 56), (3, 57), (3, 59), (3, 62), (3, 71), (3, 75), (3, 81), (3, 82), (4, 0), (4, 6), (4, 14), (4, 23), (4, 24), (4, 36), (4, 37), (4, 47), (4, 59), (4, 61), (4, 75), (4, 77), (4, 81), (5, 3), (5, 7), (5, 29), (5, 47), (5, 71), (6, 4), (6, 12), (6, 13), (6, 19), (6, 23), (6, 24), (6, 25), (6, 29), (6, 33), (6, 37), (6, 39), (6, 48), (6, 54), (6, 57), (6, 60), (6, 62), (6, 69), (6, 72), (6, 75), (6, 80), (6, 81), (6, 82), (6, 87), (7, 3), (7, 5), (7, 29), (7, 47), (7, 56), (7, 62), (7, 64), (7, 69), (7, 71), (7, 87), (8, 10), (8, 26), (9, 0), (9, 3), (9, 14), (9, 16), (9, 19), (9, 23), (9, 24), (9, 29), (9, 47), (9, 49), (9, 59), (9, 61), (9, 62), (9, 69), (9, 71), (9, 75), (9, 82), (9, 86), (9, 87), (10, 8), (10, 20), (10, 26), (10, 38), (10, 40), (11, 15), (11, 21), (11, 22), (11, 38), (11, 43), (11, 50), (11, 53), (11, 55), (11, 70), (11, 74), (11, 85), (12, 6), (12, 25), (12, 28), (12, 31), (12, 39), (12, 48), (12, 60), (12, 72), (12, 80), (13, 6), (13, 39), (13, 51), (13, 75), (14, 4), (14, 9), (14, 23), (14, 24), (14, 34), (14, 42), (14, 52), (14, 57), (14, 59), (15, 11), (15, 21), (15, 22), (15, 38), (15, 40), (15, 43), (15, 44), (15, 50), (15, 53), (15, 55), (15, 65), (15, 70), (15, 74), (15, 85), (16, 0), (16, 3), (16, 9), (16, 14), (16, 23), (16, 24), (16, 32), (16, 36), (16, 37), (16, 52), (16, 66), (16, 71), (17, 48), (18, 29), (18, 37), (18, 45), (19, 3), (19, 6), (19, 9), (19, 23), (19, 24), (19, 29), (19, 30), (19, 33), (19, 37), (19, 42), (19, 45), (19, 47), (19, 57), (19, 59), (19, 61), (19, 62), (19, 64), (19, 69), (19, 71), (19, 75), (19, 86), (19, 87), (20, 10), (20, 26), (21, 11), (21, 15), (21, 22), (21, 38), (21, 43), (21, 44), (21, 50), (21, 53), (21, 55), (21, 65), (21, 67), (21, 70), (21, 74), (21, 85), (22, 11), (22, 15), (22, 21), (22, 38), (22, 40), (22, 43), (22, 44), (22, 50), (22, 53), (22, 55), (22, 67), (22, 70), (22, 74), (22, 85), (23, 3), (23, 4), (23, 6), (23, 9), (23, 14), (23, 16), (23, 19), (23, 24), (23, 29), (23, 37), (23, 42), (23, 47), (23, 49), (23, 57), (23, 59), (23, 61), (23, 62), (23, 64), (23, 69), (23, 71), (23, 75), (23, 77), (23, 84), (23, 86), (23, 87), (24, 0), (24, 4), (24, 6), (24, 9), (24, 14), (24, 16), (24, 19), (24, 23), (24, 29), (24, 36), (24, 37), (24, 42), (24, 47), (24, 49), (24, 57), (24, 59), (24, 61), (24, 62), (24, 69), (24, 71), (24, 75), (24, 77), (24, 79), (24, 82), (24, 84), (24, 86), (24, 87), (25, 6), (25, 31), (25, 39), (25, 60), (25, 80), (26, 8), (26, 10), (26, 20), (26, 40), (27, 35), (27, 63), (28, 12), (28, 31), (28, 39), (29, 0), (29, 3), (29, 5), (29, 6), (29, 7), (29, 9), (29, 18), (29, 19), (29, 23), (29, 24), (29, 32), (29, 37), (29, 45), (29, 47), (29, 57), (29, 61), (29, 62), (29, 64), (29, 69), (29, 71), (29, 77), (29, 81), (29, 86), (29, 87), (30, 3), (30, 19), (30, 42), (30, 47), (30, 59), (30, 61), (30, 86), (31, 12), (31, 25), (31, 28), (31, 39), (31, 48), (31, 60), (31, 80), (32, 3), (32, 16), (32, 29), (32, 47), (32, 56), (32, 64), (33, 6), (33, 19), (33, 64), (33, 86), (34, 14), (34, 52), (35, 27), (35, 54), (35, 63), (35, 64), (36, 4), (36, 16), (36, 24), (36, 66), (37, 0), (37, 4), (37, 6), (37, 16), (37, 18), (37, 19), (37, 23), (37, 24), (37, 29), (37, 42), (37, 45), (37, 47), (37, 50), (37, 58), (37, 59), (37, 61), (37, 62), (37, 69), (37, 71), (37, 75), (37, 77), (37, 79), (37, 86), (37, 87), (38, 10), (38, 11), (38, 15), (38, 21), (38, 22), (38, 40), (38, 43), (38, 44), (38, 50), (38, 53), (38, 65), (38, 67), (38, 70), (38, 74), (38, 85), (39, 6), (39, 12), (39, 13), (39, 25), (39, 28), (39, 31), (39, 48), (39, 60), (39, 72), (39, 80), (40, 10), (40, 15), (40, 22), (40, 26), (40, 38), (40, 43), (40, 44), (41, 78), (41, 79), (42, 14), (42, 19), (42, 23), (42, 24), (42, 30), (42, 37), (42, 45), (42, 47), (42, 57), (42, 59), (42, 61), (42, 62), (42, 69), (42, 71), (42, 86), (43, 11), (43, 15), (43, 21), (43, 22), (43, 38), (43, 40), (43, 44), (43, 50), (43, 53), (43, 55), (43, 65), (43, 67), (43, 70), (43, 74), (43, 85), (44, 15), (44, 21), (44, 22), (44, 38), (44, 40), (44, 43), (44, 53), (44, 55), (44, 67), (44, 85), (45, 3), (45, 18), (45, 19), (45, 29), (45, 37), (45, 42), (45, 59), (45, 62), (45, 69), (45, 81), (45, 87), (47, 3), (47, 4), (47, 5), (47, 7), (47, 9), (47, 19), (47, 23), (47, 24), (47, 29), (47, 30), (47, 32), (47, 37), (47, 42), (47, 57), (47, 59), (47, 61), (47, 62), (47, 64), (47, 69), (47, 71), (47, 81), (47, 86), (48, 6), (48, 12), (48, 17), (48, 31), (48, 39), (48, 60), (48, 72), (48, 80), (49, 3), (49, 9), (49, 23), (49, 24), (49, 56), (49, 59), (49, 64), (49, 71), (49, 75), (49, 82), (49, 87), (50, 11), (50, 15), (50, 21), (50, 22), (50, 37), (50, 38), (50, 43), (50, 53), (50, 55), (50, 70), (50, 85), (51, 13), (52, 14), (52, 16), (52, 34), (52, 66), (53, 11), (53, 15), (53, 21), (53, 22), (53, 38), (53, 43), (53, 44), (53, 50), (53, 55), (53, 67), (53, 74), (53, 85), (54, 3), (54, 6), (54, 35), (54, 57), (54, 59), (54, 81), (54, 87), (55, 11), (55, 15), (55, 21), (55, 22), (55, 43), (55, 44), (55, 50), (55, 53), (55, 65), (55, 67), (55, 74), (55, 85), (56, 3), (56, 7), (56, 32), (56, 49), (56, 64), (56, 71), (57, 3), (57, 6), (57, 14), (57, 19), (57, 23), (57, 24), (57, 29), (57, 42), (57, 47), (57, 54), (57, 61), (57, 62), (57, 71), (57, 75), (57, 86), (57, 87), (58, 37), (58, 75), (59, 3), (59, 4), (59, 9), (59, 14), (59, 19), (59, 23), (59, 24), (59, 30), (59, 33), (59, 37), (59, 42), (59, 45), (59, 47), (59, 49), (59, 54), (59, 61), (59, 62), (59, 64), (59, 75), (59, 82), (60, 6), (60, 12), (60, 25), (60, 31), (60, 39), (60, 48), (60, 80), (61, 4), (61, 9), (61, 19), (61, 23), (61, 24), (61, 29), (61, 30), (61, 37), (61, 42), (61, 47), (61, 57), (61, 59), (61, 62), (61, 64), (61, 69), (61, 75), (61, 86), (62, 0), (62, 3), (62, 6), (62, 7), (62, 9), (62, 19), (62, 23), (62, 24), (62, 29), (62, 37), (62, 42), (62, 45), (62, 47), (62, 57), (62, 59), (62, 61), (62, 64), (62, 69), (62, 71), (62, 75), (62, 77), (62, 81), (62, 82), (62, 86), (62, 87), (63, 27), (63, 35), (64, 7), (64, 19), (64, 23), (64, 29), (64, 32), (64, 33), (64, 35), (64, 47), (64, 49), (64, 56), (64, 59), (64, 61), (64, 62), (64, 81), (64, 83), (64, 86), (65, 15), (65, 21), (65, 38), (65, 43), (65, 55), (65, 70), (65, 74), (65, 85), (66, 14), (66, 52), (67, 21), (67, 22), (67, 38), (67, 43), (67, 44), (67, 53), (67, 55), (67, 70), (67, 74), (69, 6), (69, 7), (69, 9), (69, 19), (69, 23), (69, 24), (69, 29), (69, 37), (69, 42), (69, 45), (69, 47), (69, 61), (69, 62), (69, 71), (69, 81), (69, 87), (70, 11), (70, 15), (70, 21), (70, 22), (70, 38), (70, 43), (70, 50), (70, 65), (70, 67), (70, 74), (70, 85), (71, 0), (71, 3), (71, 5), (71, 7), (71, 9), (71, 16), (71, 19), (71, 23), (71, 24), (71, 29), (71, 37), (71, 42), (71, 47), (71, 49), (71, 56), (71, 57), (71, 62), (71, 69), (71, 75), (71, 77), (71, 87), (72, 6), (72, 12), (72, 39), (72, 48), (72, 80), (74, 11), (74, 15), (74, 21), (74, 22), (74, 38), (74, 43), (74, 53), (74, 55), (74, 65), (74, 67), (74, 70), (74, 85), (75, 0), (75, 3), (75, 4), (75, 6), (75, 9), (75, 13), (75, 19), (75, 23), (75, 24), (75, 37), (75, 49), (75, 57), (75, 58), (75, 59), (75, 61), (75, 62), (75, 71), (75, 77), (75, 79), (75, 86), (75, 87), (76, 79), (77, 0), (77, 4), (77, 23), (77, 24), (77, 29), (77, 37), (77, 62), (77, 71), (77, 75), (77, 84), (78, 41), (79, 24), (79, 37), (79, 41), (79, 75), (79, 76), (80, 6), (80, 12), (80, 25), (80, 31), (80, 39), (80, 48), (80, 60), (80, 72), (82, 3), (82, 6), (82, 9), (82, 24), (82, 49), (82, 59), (82, 62), (82, 83), (82, 86), (83, 64), (83, 81), (83, 82), (83, 86), (84, 0), (84, 23), (84, 24), (84, 77), (85, 11), (85, 15), (85, 21), (85, 22), (85, 38), (85, 43), (85, 44), (85, 50), (85, 53), (85, 55), (85, 65), (85, 70), (85, 74), (86, 9), (86, 19), (86, 23), (86, 24), (86, 29), (86, 30), (86, 33), (86, 37), (86, 42), (86, 47), (86, 57), (86, 59), (86, 61), (86, 62), (86, 64), (86, 75), (86, 81), (86, 82), (86, 83), (87, 6), (87, 7), (87, 9), (87, 19), (87, 23), (87, 24), (87, 29), (87, 37), (87, 45), (87, 49), (87, 54), (87, 57), (87, 62), (87, 69), (87, 71), (87, 75)]
    

    # magic:
    vertices = [n for n in range(1, len(friends) + 1)]
    g = Graph(vertex_attrs={"label":vertices},
            edges=edges, directed=False)
    N = len(vertices)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
    maxiter=1000,
    area=N**3,
    repulserad=N**3)
    g.simplify(multiple=True, loops=True)
    communities = g.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()
    print(clusters)
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    plot(g, **visual_style)

if __name__ == '__main__':
    get_network(369826180)