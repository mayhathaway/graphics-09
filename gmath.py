import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normalize(normal)
    normalize(view)
    normalize(light[LOCATION])

    Ia = calculate_ambient(ambient, areflect)
    Id = calculate_diffuse(light, dreflect, normal)
    Is = calculate_specular(light, sreflect, view, normal)

    r = Ia[0] + Id[0] + Is[0]
    g = Ia[1] + Id[1] + Is[1]
    b = Ia[2] + Id[2] + Is[2]

    return [int(r), int(g), int(b)]

def calculate_ambient(alight, areflect):
    r = alight[0] * areflect[0]
    g = alight[1] * areflect[1]
    b = alight[2] * areflect[2]

    return limit_color([r, g, b])

def calculate_diffuse(light, dreflect, normal):
    dp = dot_product(normal, light[LOCATION])

    r = light[COLOR][0] * dreflect[0] * dp
    g = light[COLOR][1] * dreflect[1] * dp
    b = light[COLOR][2] * dreflect[2] * dp

def calculate_specular(light, sreflect, view, normal):
    cos = 2 * dot_product(light[LOCATION], normal)
    r = [(cos * normal[0]) - light[LOCATION][0],
     (cos * normal[1]) - light[LOCATION][1],
     (cos * normal[2]) - light[LOCATION][2]]

    spec = dot_product(r, view)
    if spec <= 0:
        return [0, 0, 0]
    spec = spec ** SPECULAR_EXP

    r = light[COLOR][0] * sreflect[0] * spec
    g = light[COLOR][1] * sreflect[1] * spec
    b = light[COLOR][2] * sreflect[2] * spec

    return limit_color([r, g, b])

def limit_color(color):
    clr = color
    for x in clr:
        if x > 255:
            x = 255
    return clr

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
