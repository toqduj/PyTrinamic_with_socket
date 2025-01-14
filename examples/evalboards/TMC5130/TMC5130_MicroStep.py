################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

#!/usr/bin/env python3
'''
Visualize the microstep table of the TMC5130

The connection to a Landungsbrücke is established over USB. TMCL commands are
used for communicating with the IC.

Created on 15.05.2019
Updated on 27.03.2023 by ASU

@author: LH
'''

import time
import math
import matplotlib.pyplot as plot
import pytrinamic

from pytrinamic.connections.connection_manager import ConnectionManager
from pytrinamic.evalboards.TMC5130_eval import TMC5130_eval

MEASURE = False

pytrinamic.show_info()

# These are the values from the default microstep table.
# Set MEASURE to True to read out the values from the IC. Once this has been
# completed it is faster to copy the values here instead of scanning again
# for every script iteration.
# The tuple consists of (MSCNT, CUR_A, CUR_B)
measured = [(0, 0, 247), (1, 1, 247), (2, 3, 247), (3, 4, 247), (4, 6, 247), (5, 7, 247), (6, 9, 247), (7, 10, 247), (8, 12, 247), (9, 13, 247), (10, 15, 246), (11, 16, 246), (12, 18, 246), (13, 20, 246), (14, 21, 246), (15, 23, 246), (16, 24, 246), (17, 26, 246), (18, 27, 245), (19, 29, 245), (20, 30, 245), (21, 32, 245), (22, 33, 245), (23, 35, 244), (24, 36, 244), (25, 38, 244), (26, 39, 244), (27, 41, 243), (28, 42, 243), (29, 44, 243), (30, 45, 243), (31, 47, 242), (32, 48, 242), (33, 50, 242), (34, 51, 241), (35, 53, 241), (36, 54, 241), (37, 56, 240), (38, 57, 240), (39, 59, 240), (40, 60, 239), (41, 61, 239), (42, 63, 239), (43, 64, 238), (44, 66, 238), (45, 67, 237), (46, 69, 237), (47, 70, 237), (48, 72, 236), (49, 73, 236), (50, 75, 235), (51, 76, 235), (52, 78, 234), (53, 79, 234), (54, 80, 233), (55, 82, 233), (56, 83, 232), (57, 85, 232), (58, 86, 231), (59, 88, 231), (60, 89, 230), (61, 90, 230), (62, 92, 229), (63, 93, 228), (64, 95, 228), (65, 96, 227), (66, 97, 227), (67, 99, 226), (68, 100, 225), (69, 102, 225), (70, 103, 224), (71, 104, 224), (72, 106, 223), (73, 107, 222), (74, 108, 222), (75, 110, 221), (76, 111, 220), (77, 113, 219), (78, 114, 219), (79, 115, 218), (80, 117, 217), (81, 118, 217), (82, 119, 216), (83, 121, 215), (84, 122, 214), (85, 123, 214), (86, 125, 213), (87, 126, 212), (88, 127, 211), (89, 128, 211), (90, 130, 210), (91, 131, 209), (92, 132, 208), (93, 134, 207), (94, 135, 206), (95, 136, 206), (96, 137, 205), (97, 139, 204), (98, 140, 203), (99, 141, 202), (100, 142, 201), (101, 144, 200), (102, 145, 200), (103, 146, 199), (104, 147, 198), (105, 149, 197), (106, 150, 196), (107, 151, 195), (108, 152, 194), (109, 153, 193), (110, 155, 192), (111, 156, 191), (112, 157, 190), (113, 158, 189), (114, 159, 188), (115, 160, 187), (116, 162, 186), (117, 163, 185), (118, 164, 184), (119, 165, 183), (120, 166, 182), (121, 167, 181), (122, 168, 180), (123, 169, 179), (124, 171, 178), (125, 172, 177), (126, 173, 176), (127, 174, 175), (128, 175, 174), (129, 176, 173), (130, 177, 172), (131, 178, 171), (132, 179, 169), (133, 180, 168), (134, 181, 167), (135, 182, 166), (136, 183, 165), (137, 184, 164), (138, 185, 163), (139, 186, 162), (140, 187, 160), (141, 188, 159), (142, 189, 158), (143, 190, 157), (144, 191, 156), (145, 192, 155), (146, 193, 153), (147, 194, 152), (148, 195, 151), (149, 196, 150), (150, 197, 149), (151, 198, 147), (152, 199, 146), (153, 200, 145), (154, 200, 144), (155, 201, 142), (156, 202, 141), (157, 203, 140), (158, 204, 139), (159, 205, 137), (160, 206, 136), (161, 206, 135), (162, 207, 134), (163, 208, 132), (164, 209, 131), (165, 210, 130), (166, 211, 128), (167, 211, 127), (168, 212, 126), (169, 213, 125), (170, 214, 123), (171, 214, 122), (172, 215, 121), (173, 216, 119), (174, 217, 118), (175, 217, 117), (176, 218, 115), (177, 219, 114), (178, 219, 113), (179, 220, 111), (180, 221, 110), (181, 222, 108), (182, 222, 107), (183, 223, 106), (184, 224, 104), (185, 224, 103), (186, 225, 102), (187, 225, 100), (188, 226, 99), (189, 227, 97), (190, 227, 96), (191, 228, 95), (192, 228, 93), (193, 229, 92), (194, 230, 90), (195, 230, 89), (196, 231, 88), (197, 231, 86), (198, 232, 85), (199, 232, 83), (200, 233, 82), (201, 233, 80), (202, 234, 79), (203, 234, 78), (204, 235, 76), (205, 235, 75), (206, 236, 73), (207, 236, 72), (208, 237, 70), (209, 237, 69), (210, 237, 67), (211, 238, 66), (212, 238, 64), (213, 239, 63), (214, 239, 61), (215, 239, 60), (216, 240, 59), (217, 240, 57), (218, 240, 56), (219, 241, 54), (220, 241, 53), (221, 241, 51), (222, 242, 50), (223, 242, 48), (224, 242, 47), (225, 243, 45), (226, 243, 44), (227, 243, 42), (228, 243, 41), (229, 244, 39), (230, 244, 38), (231, 244, 36), (232, 244, 35), (233, 245, 33), (234, 245, 32), (235, 245, 30), (236, 245, 29), (237, 245, 27), (238, 246, 26), (239, 246, 24), (240, 246, 23), (241, 246, 21), (242, 246, 20), (243, 246, 18), (244, 246, 16), (245, 246, 15), (246, 247, 13), (247, 247, 12), (248, 247, 10), (249, 247, 9), (250, 247, 7), (251, 247, 6), (252, 247, 4), (253, 247, 3), (254, 247, 1), (255, 247, 0), (256, 247, -1), (257, 247, -2), (258, 247, -4), (259, 247, -5), (260, 247, -7), (261, 247, -8), (262, 247, -10), (263, 247, -11), (264, 247, -13), (265, 247, -14), (266, 246, -16), (267, 246, -17), (268, 246, -19), (269, 246, -21), (270, 246, -22), (271, 246, -24), (272, 246, -25), (273, 246, -27), (274, 245, -28), (275, 245, -30), (276, 245, -31), (277, 245, -33), (278, 245, -34), (279, 244, -36), (280, 244, -37), (281, 244, -39), (282, 244, -40), (283, 243, -42), (284, 243, -43), (285, 243, -45), (286, 243, -46), (287, 242, -48), (288, 242, -49), (289, 242, -51), (290, 241, -52), (291, 241, -54), (292, 241, -55), (293, 240, -57), (294, 240, -58), (295, 240, -60), (296, 239, -61), (297, 239, -62), (298, 239, -64), (299, 238, -65), (300, 238, -67), (301, 237, -68), (302, 237, -70), (303, 237, -71), (304, 236, -73), (305, 236, -74), (306, 235, -76), (307, 235, -77), (308, 234, -79), (309, 234, -80), (310, 233, -81), (311, 233, -83), (312, 232, -84), (313, 232, -86), (314, 231, -87), (315, 231, -89), (316, 230, -90), (317, 230, -91), (318, 229, -93), (319, 228, -94), (320, 228, -96), (321, 227, -97), (322, 227, -98), (323, 226, -100), (324, 225, -101), (325, 225, -103), (326, 224, -104), (327, 224, -105), (328, 223, -107), (329, 222, -108), (330, 222, -109), (331, 221, -111), (332, 220, -112), (333, 219, -114), (334, 219, -115), (335, 218, -116), (336, 217, -118), (337, 217, -119), (338, 216, -120), (339, 215, -122), (340, 214, -123), (341, 214, -124), (342, 213, -126), (343, 212, -127), (344, 211, -128), (345, 211, -129), (346, 210, -131), (347, 209, -132), (348, 208, -133), (349, 207, -135), (350, 206, -136), (351, 206, -137), (352, 205, -138), (353, 204, -140), (354, 203, -141), (355, 202, -142), (356, 201, -143), (357, 200, -145), (358, 200, -146), (359, 199, -147), (360, 198, -148), (361, 197, -150), (362, 196, -151), (363, 195, -152), (364, 194, -153), (365, 193, -154), (366, 192, -156), (367, 191, -157), (368, 190, -158), (369, 189, -159), (370, 188, -160), (371, 187, -161), (372, 186, -163), (373, 185, -164), (374, 184, -165), (375, 183, -166), (376, 182, -167), (377, 181, -168), (378, 180, -169), (379, 179, -170), (380, 178, -172), (381, 177, -173), (382, 176, -174), (383, 175, -175), (384, 174, -176), (385, 173, -177), (386, 172, -178), (387, 171, -179), (388, 169, -180), (389, 168, -181), (390, 167, -182), (391, 166, -183), (392, 165, -184), (393, 164, -185), (394, 163, -186), (395, 162, -187), (396, 160, -188), (397, 159, -189), (398, 158, -190), (399, 157, -191), (400, 156, -192), (401, 155, -193), (402, 153, -194), (403, 152, -195), (404, 151, -196), (405, 150, -197), (406, 149, -198), (407, 147, -199), (408, 146, -200), (409, 145, -201), (410, 144, -201), (411, 142, -202), (412, 141, -203), (413, 140, -204), (414, 139, -205), (415, 137, -206), (416, 136, -207), (417, 135, -207), (418, 134, -208), (419, 132, -209), (420, 131, -210), (421, 130, -211), (422, 128, -212), (423, 127, -212), (424, 126, -213), (425, 125, -214), (426, 123, -215), (427, 122, -215), (428, 121, -216), (429, 119, -217), (430, 118, -218), (431, 117, -218), (432, 115, -219), (433, 114, -220), (434, 113, -220), (435, 111, -221), (436, 110, -222), (437, 108, -223), (438, 107, -223), (439, 106, -224), (440, 104, -225), (441, 103, -225), (442, 102, -226), (443, 100, -226), (444, 99, -227), (445, 97, -228), (446, 96, -228), (447, 95, -229), (448, 93, -229), (449, 92, -230), (450, 90, -231), (451, 89, -231), (452, 88, -232), (453, 86, -232), (454, 85, -233), (455, 83, -233), (456, 82, -234), (457, 80, -234), (458, 79, -235), (459, 78, -235), (460, 76, -236), (461, 75, -236), (462, 73, -237), (463, 72, -237), (464, 70, -238), (465, 69, -238), (466, 67, -238), (467, 66, -239), (468, 64, -239), (469, 63, -240), (470, 61, -240), (471, 60, -240), (472, 59, -241), (473, 57, -241), (474, 56, -241), (475, 54, -242), (476, 53, -242), (477, 51, -242), (478, 50, -243), (479, 48, -243), (480, 47, -243), (481, 45, -244), (482, 44, -244), (483, 42, -244), (484, 41, -244), (485, 39, -245), (486, 38, -245), (487, 36, -245), (488, 35, -245), (489, 33, -246), (490, 32, -246), (491, 30, -246), (492, 29, -246), (493, 27, -246), (494, 26, -247), (495, 24, -247), (496, 23, -247), (497, 21, -247), (498, 20, -247), (499, 18, -247), (500, 16, -247), (501, 15, -247), (502, 13, -248), (503, 12, -248), (504, 10, -248), (505, 9, -248), (506, 7, -248), (507, 6, -248), (508, 4, -248), (509, 3, -248), (510, 1, -248), (511, 0, -248), (512, -1, -248), (513, -2, -248), (514, -4, -248), (515, -5, -248), (516, -7, -248), (517, -8, -248), (518, -10, -248), (519, -11, -248), (520, -13, -248), (521, -14, -248), (522, -16, -247), (523, -17, -247), (524, -19, -247), (525, -21, -247), (526, -22, -247), (527, -24, -247), (528, -25, -247), (529, -27, -247), (530, -28, -246), (531, -30, -246), (532, -31, -246), (533, -33, -246), (534, -34, -246), (535, -36, -245), (536, -37, -245), (537, -39, -245), (538, -40, -245), (539, -42, -244), (540, -43, -244), (541, -45, -244), (542, -46, -244), (543, -48, -243), (544, -49, -243), (545, -51, -243), (546, -52, -242), (547, -54, -242), (548, -55, -242), (549, -57, -241), (550, -58, -241), (551, -60, -241), (552, -61, -240), (553, -62, -240), (554, -64, -240), (555, -65, -239), (556, -67, -239), (557, -68, -238), (558, -70, -238), (559, -71, -238), (560, -73, -237), (561, -74, -237), (562, -76, -236), (563, -77, -236), (564, -79, -235), (565, -80, -235), (566, -81, -234), (567, -83, -234), (568, -84, -233), (569, -86, -233), (570, -87, -232), (571, -89, -232), (572, -90, -231), (573, -91, -231), (574, -93, -230), (575, -94, -229), (576, -96, -229), (577, -97, -228), (578, -98, -228), (579, -100, -227), (580, -101, -226), (581, -103, -226), (582, -104, -225), (583, -105, -225), (584, -107, -224), (585, -108, -223), (586, -109, -223), (587, -111, -222), (588, -112, -221), (589, -114, -220), (590, -115, -220), (591, -116, -219), (592, -118, -218), (593, -119, -218), (594, -120, -217), (595, -122, -216), (596, -123, -215), (597, -124, -215), (598, -126, -214), (599, -127, -213), (600, -128, -212), (601, -129, -212), (602, -131, -211), (603, -132, -210), (604, -133, -209), (605, -135, -208), (606, -136, -207), (607, -137, -207), (608, -138, -206), (609, -140, -205), (610, -141, -204), (611, -142, -203), (612, -143, -202), (613, -145, -201), (614, -146, -201), (615, -147, -200), (616, -148, -199), (617, -150, -198), (618, -151, -197), (619, -152, -196), (620, -153, -195), (621, -154, -194), (622, -156, -193), (623, -157, -192), (624, -158, -191), (625, -159, -190), (626, -160, -189), (627, -161, -188), (628, -163, -187), (629, -164, -186), (630, -165, -185), (631, -166, -184), (632, -167, -183), (633, -168, -182), (634, -169, -181), (635, -170, -180), (636, -172, -179), (637, -173, -178), (638, -174, -177), (639, -175, -176), (640, -176, -175), (641, -177, -174), (642, -178, -173), (643, -179, -172), (644, -180, -170), (645, -181, -169), (646, -182, -168), (647, -183, -167), (648, -184, -166), (649, -185, -165), (650, -186, -164), (651, -187, -163), (652, -188, -161), (653, -189, -160), (654, -190, -159), (655, -191, -158), (656, -192, -157), (657, -193, -156), (658, -194, -154), (659, -195, -153), (660, -196, -152), (661, -197, -151), (662, -198, -150), (663, -199, -148), (664, -200, -147), (665, -201, -146), (666, -201, -145), (667, -202, -143), (668, -203, -142), (669, -204, -141), (670, -205, -140), (671, -206, -138), (672, -207, -137), (673, -207, -136), (674, -208, -135), (675, -209, -133), (676, -210, -132), (677, -211, -131), (678, -212, -129), (679, -212, -128), (680, -213, -127), (681, -214, -126), (682, -215, -124), (683, -215, -123), (684, -216, -122), (685, -217, -120), (686, -218, -119), (687, -218, -118), (688, -219, -116), (689, -220, -115), (690, -220, -114), (691, -221, -112), (692, -222, -111), (693, -223, -109), (694, -223, -108), (695, -224, -107), (696, -225, -105), (697, -225, -104), (698, -226, -103), (699, -226, -101), (700, -227, -100), (701, -228, -98), (702, -228, -97), (703, -229, -96), (704, -229, -94), (705, -230, -93), (706, -231, -91), (707, -231, -90), (708, -232, -89), (709, -232, -87), (710, -233, -86), (711, -233, -84), (712, -234, -83), (713, -234, -81), (714, -235, -80), (715, -235, -79), (716, -236, -77), (717, -236, -76), (718, -237, -74), (719, -237, -73), (720, -238, -71), (721, -238, -70), (722, -238, -68), (723, -239, -67), (724, -239, -65), (725, -240, -64), (726, -240, -62), (727, -240, -61), (728, -241, -60), (729, -241, -58), (730, -241, -57), (731, -242, -55), (732, -242, -54), (733, -242, -52), (734, -243, -51), (735, -243, -49), (736, -243, -48), (737, -244, -46), (738, -244, -45), (739, -244, -43), (740, -244, -42), (741, -245, -40), (742, -245, -39), (743, -245, -37), (744, -245, -36), (745, -246, -34), (746, -246, -33), (747, -246, -31), (748, -246, -30), (749, -246, -28), (750, -247, -27), (751, -247, -25), (752, -247, -24), (753, -247, -22), (754, -247, -21), (755, -247, -19), (756, -247, -17), (757, -247, -16), (758, -248, -14), (759, -248, -13), (760, -248, -11), (761, -248, -10), (762, -248, -8), (763, -248, -7), (764, -248, -5), (765, -248, -4), (766, -248, -2), (767, -248, -1), (768, -248, 0), (769, -248, 1), (770, -248, 3), (771, -248, 4), (772, -248, 6), (773, -248, 7), (774, -248, 9), (775, -248, 10), (776, -248, 12), (777, -248, 13), (778, -247, 15), (779, -247, 16), (780, -247, 18), (781, -247, 20), (782, -247, 21), (783, -247, 23), (784, -247, 24), (785, -247, 26), (786, -246, 27), (787, -246, 29), (788, -246, 30), (789, -246, 32), (790, -246, 33), (791, -245, 35), (792, -245, 36), (793, -245, 38), (794, -245, 39), (795, -244, 41), (796, -244, 42), (797, -244, 44), (798, -244, 45), (799, -243, 47), (800, -243, 48), (801, -243, 50), (802, -242, 51), (803, -242, 53), (804, -242, 54), (805, -241, 56), (806, -241, 57), (807, -241, 59), (808, -240, 60), (809, -240, 61), (810, -240, 63), (811, -239, 64), (812, -239, 66), (813, -238, 67), (814, -238, 69), (815, -238, 70), (816, -237, 72), (817, -237, 73), (818, -236, 75), (819, -236, 76), (820, -235, 78), (821, -235, 79), (822, -234, 80), (823, -234, 82), (824, -233, 83), (825, -233, 85), (826, -232, 86), (827, -232, 88), (828, -231, 89), (829, -231, 90), (830, -230, 92), (831, -229, 93), (832, -229, 95), (833, -228, 96), (834, -228, 97), (835, -227, 99), (836, -226, 100), (837, -226, 102), (838, -225, 103), (839, -225, 104), (840, -224, 106), (841, -223, 107), (842, -223, 108), (843, -222, 110), (844, -221, 111), (845, -220, 113), (846, -220, 114), (847, -219, 115), (848, -218, 117), (849, -218, 118), (850, -217, 119), (851, -216, 121), (852, -215, 122), (853, -215, 123), (854, -214, 125), (855, -213, 126), (856, -212, 127), (857, -212, 128), (858, -211, 130), (859, -210, 131), (860, -209, 132), (861, -208, 134), (862, -207, 135), (863, -207, 136), (864, -206, 137), (865, -205, 139), (866, -204, 140), (867, -203, 141), (868, -202, 142), (869, -201, 144), (870, -201, 145), (871, -200, 146), (872, -199, 147), (873, -198, 149), (874, -197, 150), (875, -196, 151), (876, -195, 152), (877, -194, 153), (878, -193, 155), (879, -192, 156), (880, -191, 157), (881, -190, 158), (882, -189, 159), (883, -188, 160), (884, -187, 162), (885, -186, 163), (886, -185, 164), (887, -184, 165), (888, -183, 166), (889, -182, 167), (890, -181, 168), (891, -180, 169), (892, -179, 171), (893, -178, 172), (894, -177, 173), (895, -176, 174), (896, -175, 175), (897, -174, 176), (898, -173, 177), (899, -172, 178), (900, -170, 179), (901, -169, 180), (902, -168, 181), (903, -167, 182), (904, -166, 183), (905, -165, 184), (906, -164, 185), (907, -163, 186), (908, -161, 187), (909, -160, 188), (910, -159, 189), (911, -158, 190), (912, -157, 191), (913, -156, 192), (914, -154, 193), (915, -153, 194), (916, -152, 195), (917, -151, 196), (918, -150, 197), (919, -148, 198), (920, -147, 199), (921, -146, 200), (922, -145, 200), (923, -143, 201), (924, -142, 202), (925, -141, 203), (926, -140, 204), (927, -138, 205), (928, -137, 206), (929, -136, 206), (930, -135, 207), (931, -133, 208), (932, -132, 209), (933, -131, 210), (934, -129, 211), (935, -128, 211), (936, -127, 212), (937, -126, 213), (938, -124, 214), (939, -123, 214), (940, -122, 215), (941, -120, 216), (942, -119, 217), (943, -118, 217), (944, -116, 218), (945, -115, 219), (946, -114, 219), (947, -112, 220), (948, -111, 221), (949, -109, 222), (950, -108, 222), (951, -107, 223), (952, -105, 224), (953, -104, 224), (954, -103, 225), (955, -101, 225), (956, -100, 226), (957, -98, 227), (958, -97, 227), (959, -96, 228), (960, -94, 228), (961, -93, 229), (962, -91, 230), (963, -90, 230), (964, -89, 231), (965, -87, 231), (966, -86, 232), (967, -84, 232), (968, -83, 233), (969, -81, 233), (970, -80, 234), (971, -79, 234), (972, -77, 235), (973, -76, 235), (974, -74, 236), (975, -73, 236), (976, -71, 237), (977, -70, 237), (978, -68, 237), (979, -67, 238), (980, -65, 238), (981, -64, 239), (982, -62, 239), (983, -61, 239), (984, -60, 240), (985, -58, 240), (986, -57, 240), (987, -55, 241), (988, -54, 241), (989, -52, 241), (990, -51, 242), (991, -49, 242), (992, -48, 242), (993, -46, 243), (994, -45, 243), (995, -43, 243), (996, -42, 243), (997, -40, 244), (998, -39, 244), (999, -37, 244), (1000, -36, 244), (1001, -34, 245), (1002, -33, 245), (1003, -31, 245), (1004, -30, 245), (1005, -28, 245), (1006, -27, 246), (1007, -25, 246), (1008, -24, 246), (1009, -22, 246), (1010, -21, 246), (1011, -19, 246), (1012, -17, 246), (1013, -16, 246), (1014, -14, 247), (1015, -13, 247), (1016, -11, 247), (1017, -10, 247), (1018, -8, 247), (1019, -7, 247), (1020, -5, 247), (1021, -4, 247), (1022, -2, 247), (1023, -1, 247), (0, 0, 247)]

with ConnectionManager().connect() as myInterface:
    eval = TMC5130_eval(myInterface)
    #eval.showChipInfo()
    ic = eval.ics[0]
    motor = eval.motors[0]

    MSLUT_ = [
            eval.read_register(ic.REG.MSLUT_0),
            eval.read_register(ic.REG.MSLUT_1),
            eval.read_register(ic.REG.MSLUT_2),
            eval.read_register(ic.REG.MSLUT_3),
            eval.read_register(ic.REG.MSLUT_4),
            eval.read_register(ic.REG.MSLUT_5),
            eval.read_register(ic.REG.MSLUT_6),
            eval.read_register(ic.REG.MSLUT_7),
        ]

    ranges = [
            (eval.read_register_field(ic.FIELD.X1), eval.read_register_field(ic.FIELD.W0)),
            (eval.read_register_field(ic.FIELD.X2), eval.read_register_field(ic.FIELD.W1)),
            (eval.read_register_field(ic.FIELD.X3), eval.read_register_field(ic.FIELD.W2)),
            (257, eval.read_register_field(ic.FIELD.W3)),
        ]

    print(ranges)
    if not(ranges[0][0] <= ranges[1][0] <= ranges[2][0] <= ranges[3][0]):
        print("Error: Condition X1 <= X2 <= X3 <= X4 not satisfied")

    for i in range(0, 8):
        print("MSLUT_{0}:      0x{1:08X}".format(i, MSLUT_[i]))

    print("MSLUT_SEL:    0x{0:08X}".format(eval.read_register(ic.REG.MSLUTSEL)))
    print("MSLUT_START:  0x{0:08X}".format(eval.read_register(ic.REG.MSLUTSTART)))
    print()

    start = eval.read_register_field(ic.FIELD.START_SIN)
    values = [ (0, start) ]

    for i in range(1, 257):
        for j in range(0, 4):
            if i < ranges[j][0]:
                offset = ranges[j][1] - 1
                break

        bitValue   = ((MSLUT_[math.floor((i)/32) & 7] >> ((i) % 32) ) & 1)
        deltaValue = bitValue + offset
        newValue   = values[i-1][1] + deltaValue

        values += [(i, newValue)]

    for i in range(257, 513):
        newValue = values[511-i][1]
        values += [(i, newValue)]

    for i in range(513, 1024):
        newValue = -values[i-512][1] - 1
        values += [(i, newValue)]

    # Generate the cosine wave
    newValues = []
    for i in range(0, 1024):
        tmp = values[i]
        newValues += [(tmp[0], tmp[1], values[(i+256) % 1024][1])]

    values = newValues
    del newValues

    # Measure the MS values from the IC directly. Can be skipped to save time
    if MEASURE:
        eval.write_register_field(ic.FIELD.IRUN, 10)
        eval.write_register(ic.REG.A1, 10000)
        eval.write_register(ic.REG.V1, 500000)
        eval.write_register(ic.REG.D1, 10000)
        eval.write_register(ic.REG.DMAX, 500)
        eval.write_register(ic.REG.VSTART, 0)
        eval.write_register(ic.REG.VSTOP, 10)
        eval.write_register(ic.REG.AMAX, 1000)

        if eval.read_register(ic.REG.MSCNT) != 0:
            # ToDo: Move to 0 instead of erroring out
            print("Error: Motor not at MS 0")
            exit(1)

        measured = []
        for i in range(0, 1025):
            CUR_A = eval.read_register_field(ic.FIELD.CUR_A)
            if CUR_A >=256:
                CUR_A -= 512
            CUR_B = eval.read_register_field(ic.FIELD.CUR_B)
            if CUR_B >=256:
                CUR_B -= 512
            STEP  = eval.read_register_field(ic.FIELD.MSCNT)

            measured = measured + [(STEP, CUR_A, CUR_B)]
            motor.move_to(1, 1000)
            time.sleep(0.1)

        motor.move_to(0, 1000)


print(values)
print(measured)

plot.figure(num=1, clear=True)
plot.plot([(x[1], x[2]) for x in values])
plot.show(block=False)
plot.figure(num=2, clear=True)
plot.plot([x[1] for x in values], [x[2] for x in values], '.')
ax = plot.gca()
ax.add_artist(plot.Circle((0, 0), 248, fill=False, color='black'))
plot.show()

plot.close('all')
