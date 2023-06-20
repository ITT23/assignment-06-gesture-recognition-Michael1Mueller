# $1 gesture recognizer from https://depts.washington.edu/acelab/proj/dollar/index.html translated into python code with additional help from chatGpt
import math
import time

NumUnistrokes = 5
NumPoints = 64
SquareSize = 250.0
Origin = (0, 0)
Diagonal = math.sqrt(SquareSize * SquareSize + SquareSize * SquareSize)
HalfDiagonal = 0.5 * Diagonal
AngleRange = math.radians(45.0)
AnglePrecision = math.radians(2.0)
Phi = 0.5 * (-1.0 + math.sqrt(5.0))


class Point:
    def __init__(self, x, y):
        self.X = x
        self.Y = y


class Rectangle:
    def __init__(self, x, y, width, height):
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height


class Unistroke:
    def __init__(self, name, points):
        self.Name = name
        self.Points = resample(points, NumPoints)
        radians = indicative_angle(self.Points)
        self.Points = rotate_by(self.Points, -radians)
        self.Points = scale_to(self.Points, SquareSize)
        self.Points = translate_to(self.Points, Origin)


class Result:
    def __init__(self, name, score, ms):
        self.Name = name
        self.Score = score
        self.Time = ms


class DollarRecognizer:
    def __init__(self):
        self.Unistrokes = []
        self.Unistrokes.append(Unistroke("triangle", [Point(137, 139), Point(135, 141), Point(133, 144), Point(132, 146), Point(130, 149), Point(128, 151), Point(126, 155), Point(123, 160), Point(120, 166), Point(116, 171), Point(112, 177), Point(107, 183), Point(102, 188), Point(100, 191), Point(95, 195), Point(90, 199), Point(86, 203), Point(82, 206), Point(80, 209), Point(75, 213), Point(73, 213), Point(70, 216), Point(67, 219), Point(64, 221), Point(61, 223), Point(60, 225), Point(62, 226), Point(65, 225), Point(67, 226), Point(74, 226), Point(77, 227), Point(85, 229), Point(91, 230), Point(99, 231), Point(108, 232), Point(116, 233), Point(125, 233), Point(134, 234), Point(145, 233), Point(153, 232), Point(160, 233), Point(170, 234), Point(177, 235), Point(179, 236), Point(186, 237), Point(193, 238), Point(198, 239), Point(200, 237), Point(202, 239), Point(204, 238), Point(206, 234), Point(205, 230), Point(202, 222), Point(197, 216), Point(192, 207), Point(186, 198), Point(179, 189), Point(174, 183), Point(170, 178), Point(164, 171), Point(161, 168), Point(154, 160), Point(148, 155), Point(143, 150), Point(138, 148), Point(136, 148)]))
        self.Unistrokes.append(Unistroke("v", [Point(32, 206), Point(32, 205), Point(32, 204), Point(33, 202), Point(34, 201), Point(34, 200), Point(35, 198), Point(35, 197), Point(36, 196), Point(37, 194), Point(39, 191), Point(40, 188), Point(43, 184), Point(45, 180), Point(47, 177), Point(48, 174), Point(50, 171), Point(52, 168), Point(54, 164), Point(56, 160), Point(59, 155), Point(61, 151), Point(65, 146), Point(65, 145), Point(68, 139), Point(72, 132), Point(76, 126), Point(79, 121), Point(80, 120), Point(82, 116), Point(83, 115), Point(86, 110), Point(89, 106), Point(89, 105), Point(92, 100), Point(93, 100), Point(96, 95), Point(98, 91), Point(99, 91), Point(101, 87), Point(102, 87), Point(105, 83), Point(107, 80), Point(109, 77), Point(111, 74), Point(112, 74), Point(113, 72), Point(113, 71), Point(115, 68), Point(118, 66), Point(120, 63), Point(122, 60), Point(125, 57), Point(125, 56), Point(129, 52), Point(133, 46), Point(135, 43), Point(137, 41), Point(138, 40), Point(139, 39), Point(139, 40), Point(141, 44), Point(141, 45), Point(143, 53), Point(143, 54), Point(147, 63), Point(147, 64), Point(147, 65), Point(153, 77), Point(154, 77), Point(155, 78), Point(161, 90), Point(162, 91), Point(168, 103), Point(169, 104), Point(175, 115), Point(175, 116), Point(180, 124), Point(180, 125), Point(183, 132), Point(183, 133), Point(186, 139), Point(187, 140), Point(188, 146), Point(189, 146), Point(190, 151), Point(191, 151), Point(191, 152), Point(192, 157), Point(192, 158), Point(194, 163), Point(194, 164), Point(196, 169), Point(196, 170), Point(197, 175), Point(197, 176), Point(199, 180), Point(200, 184), Point(201, 187), Point(202, 190), Point(203, 192), Point(203, 193), Point(204, 195), Point(204, 196), Point(205, 198), Point(206, 200), Point(206, 201), Point(207, 201), Point(207, 202), Point(207, 203), Point(207, 204), Point(208, 205), Point(208, 206)]))
        self.Unistrokes.append(Unistroke("caret", [Point(24, 48), Point(25, 50), Point(25, 51), Point(26, 51), Point(26, 52), Point(27, 54), Point(27, 55), Point(27, 56), Point(28, 56), Point(30, 60), Point(31, 61), Point(31, 62), Point(32, 63), Point(34, 68), Point(35, 68), Point(35, 69), Point(35, 71), Point(36, 71), Point(37, 71), Point(41, 79), Point(41, 80), Point(42, 82), Point(43, 83), Point(47, 89), Point(47, 90), Point(47, 91), Point(48, 91), Point(49, 92), Point(49, 94), Point(50, 94), Point(54, 101), Point(54, 102), Point(55, 102), Point(55, 103), Point(55, 104), Point(55, 105), Point(59, 112), Point(60, 113), Point(60, 114), Point(61, 115), Point(61, 116), Point(65, 123), Point(65, 124), Point(66, 125), Point(66, 126), Point(67, 126), Point(67, 127), Point(70, 133), Point(71, 133), Point(71, 134), Point(72, 134), Point(72, 135), Point(73, 136), Point(77, 143), Point(77, 144), Point(78, 145), Point(78, 146), Point(79, 146), Point(82, 151), Point(83, 152), Point(83, 153), Point(84, 153), Point(84, 154), Point(85, 155), Point(88, 160), Point(88, 161), Point(89, 161), Point(89, 162), Point(89, 163), Point(90, 163), Point(93, 169), Point(93, 170), Point(94, 170), Point(94, 171), Point(95, 172), Point(95, 173), Point(98, 178), Point(98, 179), Point(99, 180), Point(99, 181), Point(102, 186), Point(102, 187), Point(102, 188), Point(103, 188), Point(103, 189), Point(105, 193), Point(105, 194), Point(106, 195), Point(107, 199), Point(108, 200), Point(108, 201), Point(109, 203), Point(110, 203), Point(110, 204), Point(111, 206), Point(111, 207), Point(113, 209), Point(113, 210), Point(113, 211), Point(114, 211), Point(115, 212), Point(115, 213), Point(115, 214), Point(117, 216), Point(118, 216), Point(120, 211), Point(125, 201), Point(131, 192), Point(131, 191), Point(136, 182), Point(143, 171), Point(149, 160), Point(149, 159), Point(155, 150), Point(161, 140), Point(166, 133), Point(170, 127), Point(175, 121), Point(179, 116), Point(180, 115), Point(184, 110), Point(188, 103), Point(193, 96), Point(193, 95), Point(197, 90), Point(200, 84), Point(204, 78), Point(208, 73), Point(212, 67), Point(214, 62), Point(216, 58), Point(217, 56)]))
        self.Unistrokes.append(Unistroke("rectangle", [Point(29, 154), Point(30, 144), Point(31, 133), Point(31, 124), Point(32, 115), Point(32, 106), Point(32, 98), Point(32, 91), Point(32, 90), Point(32, 84), Point(32, 78), Point(32, 76), Point(32, 75), Point(32, 74), Point(33, 74), Point(36, 74), Point(48, 74), Point(56, 74), Point(63, 74), Point(69, 74), Point(75, 75), Point(93, 76), Point(94, 76), Point(114, 78), Point(127, 78), Point(135, 78), Point(144, 78), Point(153, 78), Point(161, 78), Point(162, 78), Point(170, 78), Point(177, 78), Point(183, 78), Point(188, 78), Point(191, 78), Point(193, 78), Point(195, 78), Point(197, 78), Point(199, 78), Point(202, 78), Point(204, 78), Point(206, 78), Point(208, 77), Point(211, 77), Point(213, 77), Point(214, 77), Point(214, 80), Point(214, 84), Point(214, 85), Point(214, 91), Point(214, 98), Point(214, 105), Point(214, 106), Point(214, 113), Point(214, 120), Point(214, 126), Point(214, 132), Point(214, 137), Point(213, 142), Point(213, 143), Point(213, 148), Point(213, 153), Point(213, 158), Point(213, 163), Point(213, 164), Point(213, 169), Point(214, 171), Point(214, 172), Point(214, 174), Point(214, 175), Point(212, 175), Point(207, 175), Point(198, 175), Point(191, 175), Point(183, 175), Point(175, 175), Point(174, 175), Point(165, 175), Point(154, 175), Point(143, 175), Point(133, 175), Point(124, 174), Point(123, 173), Point(116, 173), Point(115, 172), Point(108, 172), Point(100, 172), Point(92, 172), Point(91, 172), Point(83, 172), Point(75, 172), Point(67, 172), Point(59, 172), Point(51, 172), Point(43, 172), Point(38, 172), Point(37, 172), Point(36, 172)]))
        self.Unistrokes.append(Unistroke("arrow", [Point(27, 96), Point(30, 96), Point(31, 96), Point(44, 98), Point(60, 103), Point(84, 110), Point(85, 110), Point(113, 115), Point(115, 115), Point(149, 120), Point(174, 127), Point(175, 127), Point(180, 129), Point(176, 130), Point(169, 131), Point(160, 132), Point(151, 133), Point(145, 134), Point(138, 136), Point(134, 137), Point(131, 138), Point(129, 138), Point(130, 138), Point(137, 138), Point(138, 138), Point(147, 137), Point(158, 136), Point(165, 136), Point(166, 136), Point(172, 135), Point(176, 135), Point(178, 134), Point(179, 134), Point(181, 134), Point(184, 133), Point(186, 133), Point(187, 133), Point(189, 133), Point(190, 133), Point(192, 133), Point(194, 133), Point(195, 133), Point(195, 132), Point(195, 131), Point(194, 130), Point(191, 125), Point(189, 120), Point(189, 119), Point(186, 114), Point(182, 108), Point(178, 102), Point(173, 96), Point(167, 90), Point(163, 84), Point(162, 82), Point(162, 81)]))

    def recognize(self, points):
        t0 = time.time()
        candidate = Unistroke("", points)

        u = -1
        b = float('inf')
        for i in range(len(self.Unistrokes)):
            d = distance_at_best_angle(candidate.Points, self.Unistrokes[i], -AngleRange, +AngleRange, AnglePrecision)
            if d < b:
                b = d
                u = i

        t1 = time.time()
        if u == -1:
            print("NO MATCH")
            return "No match."
        else:
            return Result(self.Unistrokes[u].Name, 1.0 - b / HalfDiagonal, (t1 - t0)*1000)

    def add_gesture(self, name, points):
        self.Unistrokes.append(Unistroke(name, points))
        num = sum(1 for unistroke in self.Unistrokes if unistroke.Name == name)
        return num

    def delete_user_gestures(self):
        self.Unistrokes = self.Unistrokes[:NumUnistrokes]
        return NumUnistrokes
    

def resample(points, n):
    I = path_length(points) / (n - 1)
    D = 0.0
    newpoints = [points[0]]
    i = 1
    while i < len(points):
        d = distance(points[i - 1], points[i])
        if (D + d) >= I:
            qx = points[i - 1].X + ((I - D) / d) * (points[i].X - points[i - 1].X)
            qy = points[i - 1].Y + ((I - D) / d) * (points[i].Y - points[i - 1].Y)
            q = Point(qx, qy)
            newpoints.append(q)
            points.insert(i, q)
            D = 0.0
        else:
            D += d
        i += 1
    if len(newpoints) == n - 1:
        newpoints.append(Point(points[-1].X, points[-1].Y))
    return newpoints


def indicative_angle(points):
    c = centroid(points)
    return math.atan2(c.Y - points[0].Y, c.X - points[0].X)


def rotate_by(points, radians):
    c = centroid(points)
    cos = math.cos(radians)
    sin = math.sin(radians)
    newpoints = []
    for i in range(len(points)):
        qx = (points[i].X - c.X) * cos - (points[i].Y - c.Y) * sin + c.X
        qy = (points[i].X - c.X) * sin + (points[i].Y - c.Y) * cos + c.Y
        newpoints.append(Point(qx, qy))
    return newpoints


def scale_to(points, size):
    B = bounding_box(points)
    newpoints = []
    for i in range(len(points)):
        qx = points[i].X * (size / B.Width)
        qy = points[i].Y * (size / B.Height)
        newpoints.append(Point(qx, qy))
    return newpoints


def translate_to(points, pt):
    c = centroid(points)
    print(c)
    newpoints = []
    for i in range(len(points)):
        qx = points[i].X + pt[0] - c.X
        qy = points[i].Y + pt[1] - c.Y
        newpoints.append(Point(qx, qy))
    return newpoints


def vectorize(points):
    sum = 0.0
    vector = []
    for i in range(len(points)):
        vector.append(points[i].X)
        vector.append(points[i].Y)
        sum += points[i].X * points[i].X + points[i].Y * points[i].Y
    magnitude = math.sqrt(sum)
    for i in range(len(vector)):
        vector[i] /= magnitude
    return vector


def optimal_cosine_distance(v1, v2):
    a = 0.0
    b = 0.0
    for i in range(0, len(v1), 2):
        a += v1[i] * v2[i] + v1[i + 1] * v2[i + 1]
        b += v1[i] * v2[i + 1] - v1[i + 1] * v2[i]
    angle = math.atan(b / a)
    return math.acos(a * math.cos(angle) + b * math.sin(angle))


def distance_at_best_angle(points, T, a, b, threshold):
    x1 = Phi * a + (1.0 - Phi) * b
    f1 = distance_at_angle(points, T, x1)
    x2 = (1.0 - Phi) * a + Phi * b
    f2 = distance_at_angle(points, T, x2)
    while abs(b - a) > threshold:
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = Phi * a + (1.0 - Phi) * b
            f1 = distance_at_angle(points, T, x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = (1.0 - Phi) * a + Phi * b
            f2 = distance_at_angle(points, T, x2)
    return min(f1, f2)


def distance_at_angle(points, T, radians):
    newpoints = rotate_by(points, radians)
    return path_distance(newpoints, T.Points)


def centroid(points):
    x = 0.0
    y = 0.0
    for i in range(len(points)):
        x += points[i].X
        y += points[i].Y
    x /= len(points)
    y /= len(points)
    return Point(x, y)


def bounding_box(points):
    minX = float('inf')
    maxX = float('-inf')
    minY = float('inf')
    maxY = float('-inf')
    for i in range(len(points)):
        minX = min(minX, points[i].X)
        minY = min(minY, points[i].Y)
        maxX = max(maxX, points[i].X)
        maxY = max(maxY, points[i].Y)
    return Rectangle(minX, minY, maxX - minX, maxY - minY)


def path_distance(pts1, pts2):
    d = 0.0
    for i in range(len(pts1)):
        d += distance(pts1[i], pts2[i])
    return d / len(pts1)


def path_length(points):
    d = 0.0
    for i in range(1, len(points)):
        d += distance(points[i - 1], points[i])
    return d


def distance(p1, p2):
    dx = p2.X - p1.X
    dy = p2.Y - p1.Y
    return math.sqrt(dx * dx + dy * dy)


def deg2_rad(d):
    return d * math.pi / 180.0


