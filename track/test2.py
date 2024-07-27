import math

def solve_quadratic(a, b, c):
    # Calculate discriminant
    D = b**2 - 4*a*c
    # If discriminant is negative, then there are no real solutions
    if D < 0:
        return []
    # Calculate two solutions
    x1 = (-b + math.sqrt(D)) / (2*a)
    x2 = (-b - math.sqrt(D)) / (2*a)
    return [x1, x2]

def find_cushion(tar_loc, tar_dir, cushion):
    a, b = tar_loc
    v1, v2 = tar_dir
    xmin, ymin, xlength, ylength = cushion
    xmax = xmin + xlength
    ymax = ymin + ylength
    intersections = []

    if v1 == 0:
        # v1 is 0, the line equation is x = a
        if xmin <= a <= xmax:
            intersections.append(["cushion", (x, y)])
            if v2 > 0:
                # Calculate the intersection with the bottom line (y = ymin)
                intersections.append(["cushion", (a, ymax)])
            elif v2 < 0:
                # Calculate the intersection with the top line (y = ymax)
                intersections.append(["cushion", (a, ymin)])
    else:
        # v1 is not 0, the line equation is y = v2/v1*(x - a) + b
        # Calculate the intersections with the vertical lines (x = xmin and x = xmax)
        for x in [xmin, xmax]:
            y = v2/v1*(x - a) + b
            if ymin <= y <= ymax:
                if v1 > 0 and x > a:
                    intersections.append(["cushion", (x, y)])
                elif v1 < 0 and x < a:
                    intersections.append(["cushion", (x, y)])

        # Calculate the intersections with the horizontal lines (y = ymin and y = ymax)
        for y in [ymin, ymax]:
            x = v1/v2*(y - b) + a
            if xmin <= x <= xmax:
                if v1 > 0 and x > a:
                    intersections.append(["cushion", (x, y)])
                elif v1 < 0 and x < a:
                    intersections.append(["cushion", (x, y)])


    return intersections

def find_intersections(tar_loc, tar_dir, ball_loc, ball_num, r = 26):
    a, b = tar_loc
    v1, v2 = tar_dir
    c, d = ball_loc
    if v1 == 0:
        A = 1
        B = -2*d
        C = (a - c)**2 + d**2 - r**2

        # Solve the quadratic equation
        solutions_y = solve_quadratic(A, B, C)
        intersections = []

        for y in solutions_y:
            # Check if the solution is larger than 0
            if v2 > 0 and  y > b:
                intersections.append([ball_num, (a, y)])
            elif v2 < 0 and y < b:
                    # 'x' is 'a' for this case
                    intersections.append([ball_num, (a, y)])
        return intersections
    else:
        # Coefficients for the quadratic equation
        A = v2**2/v1**2 + 1
        B = 2*((v2/v1)*(b-d) - c - a*(A - 1))
        C = c**2 + (b-d)**2 - r**2 + (a**2)*(A - 1) - 2*a*(v2/v1)*(b-d)

        # Solve the quadratic equation
        solutions_x = solve_quadratic(A, B, C)
        intersections = []

        for x in solutions_x:
            # Check if the solution is larger than 'a'
            if v1 > 0 and x > a:
                # Calculate the corresponding 'y'
                y = v2/v1*(x-a) + b
                intersections.append([ball_num, (x, y)])
            elif v1 < 0 and x < a:
                # Calculate the corresponding 'y'
                y = v2/v1*(x-a) + b
                intersections.append([ball_num, (x, y)])
        return intersections
    
def find_nearest_point_squared(A, points):
    # Initialize minimum distance and nearest point
    min_distance_squared = math.inf
    nearest_point = None
    # Iterate over all points
    for point in points:
        # Calculate squared Euclidean distance
        distance_squared = (point[1][0] - A[0]) ** 2 + (point[1][1] - A[1]) ** 2
        
        # Update minimum distance and nearest point
        if distance_squared < min_distance_squared:
            min_distance_squared = distance_squared
            nearest_point = point
            
    return nearest_point