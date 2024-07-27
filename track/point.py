# 두 점 사이의 방향을 계산하는 함수
def calculate_direction(point1, point2):
    return point2[0]-point1[0], point2[1]-point1[1]

# 공의 위치 리스트를 받아 방향 리스트를 계산하는 함수
def calculate_directions(positions):
    directions = []
    for i in range(1, len(positions)):
        directions.append(calculate_direction(positions[i-1], positions[i]))
    return directions

# 두 공이 충돌했는지 확인하는 함수
def check_collision(point1, direction1, point2, direction2, threshold=1.0):
    return direction1 != direction2 and distance(point1, point2) < threshold

# 공이 쿠션에 부딧혔는지 확인하는 함수
def check_cushion_collision(direction, other_directions):
    return direction not in other_directions

# 두 점 사이의 거리를 계산하는 함수
def distance(point1, point2):
    return ((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)**0.5

# 각 공의 위치 리스트를 받아 점수를 계산하는 함수
def calculate_score(white_positions, red_positions, yellow_positions):
    white_directions = calculate_directions(white_positions)  # 하얀 공의 방향 리스트 계산
    red_directions = calculate_directions(red_positions)  # 빨간 공의 방향 리스트 계산
    yellow_directions = calculate_directions(yellow_positions)  # 노란 공의 방향 리스트 계산

    collisions = []  # 부딧힌 공들의 ID를 저장하는 리스트
    cushion_collisions = 0  # 쿠션에 부딧힌 횟수

    # 각 방향에 대해
    for i in range(len(white_directions)):
        # 하얀 공과 빨간 공이 충돌했는지 확인
        if check_collision(white_positions[i], white_directions[i], red_positions[i], red_directions[i]):
            collisions.append('red')  # 충돌했다면 'red'를 리스트에 추가
        # 하얀 공과 노란 공이 충돌했는지 확인
        if check_collision(white_positions[i], white_directions[i], yellow_positions[i], yellow_directions[i]):
            collisions.append('yellow')  # 충돌했다면 'yellow'를 리스트에 추가
        # 아직 쿠션에 부딧힌 적이 없거나 마지막으로 부딧힌 것이 쿠션이 아니라면
        if not collisions or collisions[-1] != 'cushion':
            # 하얀 공이 쿠션에 부딧혔는지 확인
            if check_cushion_collision(white_directions[i], [red_directions[i], yellow_directions[i]]):
                collisions.append('cushion')  # 부딧혔다면 'cushion'을 리스트에 추가
                cushion_collisions += 1  # 쿠션에 부딧힌 횟수를 1 증가

    # 빨간 공과 노란 공 모두에 부딧히고, 쿠션에 3번 이상 부딧힌 경우 1점 획득
    if 'red' in collisions and 'yellow' in collisions and cushion_collisions >= 3:
        return 1
    # 그렇지 않은 경우 점수 없음
    else:
        return 0
