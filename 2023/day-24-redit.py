
import os

from sympy import symbols, solve

os.chdir("C:/Repos/advent-of-code-python/2023")

hails = []
for line in open(r"inputs\day-24.txt").readlines()[:3]:
    line = line.strip().split(" @ ")
    pos = [int(i) for i in line[0].split(", ")]
    vel = [int(i) for i in line[1].split(", ")]
    hails.append((pos, vel))
    
X1, V1 = hails[0]
X2, V2 = hails[1]
X3, V3 = hails[2]

# components of hail position vectors - known parameters
x1, y1, z1 = X1
x2, y2, z2 = X2
x3, y3, z3 = X3
# components of hail velocity vectors - known parameters
vx1, vy1, vz1 = V1
vx2, vy2, vz2 = V2
vx3, vy3, vz3 = V3

# position vector components - unknowns
x = symbols('x')
y = symbols('y')
z = symbols('z')
# velocity vector components - unknowns
vx = symbols('vx')
vy = symbols('vy')
vz = symbols('vz')

# equations for the cross products being the null vector
equations = [
    # first hail
    (y1-y)*(vz1-vz)-(z1-z)*(vy1-vy), 
    (z1-z)*(vx1-vx)-(x1-x)*(vz1-vz), 
    (x1-x)*(vy1-vy)-(y1-y)*(vx1-vx),
    
    # second hail
    (y2-y)*(vz2-vz)-(z2-z)*(vy2-vy), 
    (z2-z)*(vx2-vx)-(x2-x)*(vz2-vz), 
    (x2-x)*(vy2-vy)-(y2-y)*(vx2-vx),
    
    # third hail
    (y3-y)*(vz3-vz)-(z3-z)*(vy3-vy), 
    (z3-z)*(vx3-vx)-(x3-x)*(vz3-vz), 
    (x3-x)*(vy3-vy)-(y3-y)*(vx3-vx)
]

solution = solve(equations, [x, y, z, vx, vy, vz], dict=True)[0]
print(solution[x] + solution[y] + solution[z])
