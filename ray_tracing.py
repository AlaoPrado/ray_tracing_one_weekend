import sys
import numpy as np
import random
import math

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
    def pointAtParameter(self, t):
        return self.origin + t * self.direction

class HitRecord:
    def __init__(self, successful = False, t = 0, p = np.array([0,0,0]), normal = np.array([0,0,0]), material = None):
        self.successful = successful
        self.t = t
        self.p = p
        self.normal = normal
        self.material = material

class ScatterRecord:
    def __init__(self, successful = False, scattered = np.array([0,0,0]), albedo = np.array([0,0,0])):
        self.successful = successful
        self.scattered = scattered
        self.albedo = albedo

class Lambertian:
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray, hitRecord):
        scatterRecord = ScatterRecord()
        target = hitRecord.p + hitRecord.normal + randomInunitSphere()
        scatterRecord.scattered = Ray(hitRecord.p, target - hitRecord.p)
        scatterRecord.attenuation = self.albedo
        scatterRecord.successful = True
        return scatterRecord

class Metal:
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        if(fuzz < 1):
            self.fuzz = fuzz
        else:
            self.fuzz = 1

    def scatter(self, ray, hitRecord):
        scatterRecord = ScatterRecord()
        reflected = reflect(unitVector(ray.direction), hitRecord.normal)
        scatterRecord.scattered = Ray(hitRecord.p, reflected + self.fuzz * randomInunitSphere())
        scatterRecord.attenuation = self.albedo
        scatterRecord.successful = np.dot(scatterRecord.scattered.direction, hitRecord.normal) > 0
        return scatterRecord

class Dielectric:
    def __init__(self, refIdx):
        self.refIdx = refIdx

    def scatter(self, ray, hitRecord):
        scatterRecord = ScatterRecord()
        reflected = reflect(unitVector(ray.direction), hitRecord.normal)
        scatterRecord.attenuation = np.array([1.0, 1.0, 1.0])
        scatterRecord.successful = True
        if(np.dot(ray.direction, hitRecord.normal) > 0):
            outwardNormal = -hitRecord.normal
            niOverNt = self.refIdx
            cosine = self.refIdx * np.dot(ray.direction, hitRecord.normal) / squareLength(ray.direction)
        else:
            outwardNormal = hitRecord.normal
            niOverNt = 1.0 / self.refIdx
            cosine = -np.dot(ray.direction, hitRecord.normal) / squareLength(ray.direction)
        refractedData = RefractData(ray.direction, outwardNormal, niOverNt)
        if(refractedData.successful):
            refracted = refract(refractedData)
            reflectProb = schlick(cosine, self.refIdx)
        else:
            reflectProb = 1.0
        if(random.uniform(0,1) < reflectProb):
            scatterRecord.scattered = Ray(hitRecord.p, reflected)
        else:
            scatterRecord.scattered = Ray(hitRecord.p, refracted)
        return scatterRecord

class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material
    def hit(self, ray, tMin, tMax):
        hitRecord = HitRecord()
        oc = ray.origin - self.center
        a = np.dot(ray.direction, ray.direction)
        b = 2.0 * np.dot(oc, ray.direction)
        c = np.dot(oc, oc) - self.radius*self.radius
        discriminant = b*b - 4*a*c

        if(discriminant > 0):
            t = (-b - (discriminant)**0.5) / (2 * a)
            if(t < tMax and t > tMin):
                hitRecord.t = t
                hitRecord.p = ray.pointAtParameter(t)
                hitRecord.normal = (hitRecord.p - self.center) / self.radius
                hitRecord.successful = True
                hitRecord.material = self.material
            else:
                t = (-b + (discriminant)**0.5) / (2 * a)
                if(t < tMax and t > tMin):
                    hitRecord.t = t
                    hitRecord.p = ray.pointAtParameter(t)
                    hitRecord.normal = (hitRecord.p - self.center) / self.radius
                    hitRecord.successful = True
                    hitRecord.material = self.material
        return hitRecord

class HitableList:
    def __init__(self):
        self.list = []

    def hit(self, ray, tMin, tMax):
        hitRecord = HitRecord()
        closestSoFar = tMax
        for hitable in self.list:
            tempRecord = hitable.hit(ray, tMin, closestSoFar)
            if(tempRecord.successful):
                hitRecord = tempRecord
                closestSoFar = tempRecord.t
        return hitRecord

class Camera:
    def __init__(self, lookfrom, lookat, vup, vfov, aspect, aperture, focusDist):
        self.lensRadius = aperture / 2
        theta = vfov * math.pi / 180
        halfHeight = math.tan(theta/2)
        halfWidth = aspect * halfHeight
        self.origin = lookfrom
        w = unitVector(lookfrom - lookat)
        u = unitVector(np.cross(vup, w))
        v = np.cross(w, u)
        self.lowerLeftCorner = self.origin - halfWidth*focusDist*u - halfHeight*focusDist*v - focusDist*w
        self.horizontal = 2*halfWidth*focusDist*u
        self.vertical = 2*halfHeight*focusDist*v

    def getRay(self, u, v):
        rd = self.lensRadius * randomInUnitDisk()
        offset = u * rd[0] + v * rd[1]
        return Ray(self.origin + offset, self.lowerLeftCorner + u * self.horizontal + v * self.vertical - self.origin - offset)

class Screen:
    def __init__(self, width, height):
        self.witdh = width
        self.height = height
        self.pixels = x = np.zeros((width,height,3))

    def writeInFile(file):
        for j in range(self.height - 1, -1, -1):
            for i in range(self.witdh):
                r = self.pixels[self.witdh][self.height][0]
                g = self.pixels[self.witdh][self.height][1]
                b = self.pixels[self.witdh][self.height][2]
                file.write(str(r) + " " + str(g) + " " + str(b) + "\n")

class RefractData:
    def __init__(self, v, n, niOverNt):
        self.uv = unitVector(v)
        self.n = n
        self.niOverNt = niOverNt
        self.dt = np.dot(self.uv, n)
        self.discriminant = 1.0 - niOverNt * niOverNt * (1 - self.dt * self.dt)
        self.successful = self.discriminant > 0

def norm(v):
    return (v**2).sum()**0.5

def unitVector(v):
    return v / norm(v)

def reflect(v, normal):
    return v - 2 * np.dot(v,normal) * normal

def refract(rD): # rD = refractData
    return rD.niOverNt * (rD.uv - rD.n * rD.dt) - rD.n * rD.discriminant**0.5

def schlick(cosine, refIdx):
    r0 = (1 - refIdx)/ (1 + refIdx)
    r0 = r0 * r0
    return r0 + (1 - r0) * (1 - cosine)**5

def squareLength(v):
    return (v**2).sum()

def randomInunitSphere():
    p = 2.0 * np.array([random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)]) - 1
    while(squareLength(p) >= 1):
        p = 2.0 * np.array([random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)]) - 1
    return p

def randomInUnitDisk():
    p = 2.0*np.array([random.uniform(0,1), random.uniform(0,1), 0]) - np.array([1,1,0])
    while(np.dot(p,p) >= 1.0):
        p = 2.0*np.array([random.uniform(0,1), random.uniform(0,1), 0]) - np.array([1,1,0])
    return p

def randomScene():
    scene = HitableList()
    scene.list.append(Sphere(np.array([0, -1000, 0]), 1000, Lambertian(np.array([0.5, 0.5, 0.5]))))
    for a in range(-11, 12, 1):
        for b in range(-11, 12, 1):
            chooseMat = random.uniform(0,1)
            center = np.array([a+0.9*random.uniform(0,1), 0.2, b+0.9*random.uniform(0,1)])
            if(squareLength(center - np.array([4,0.2,0])) > 0.9):
                if(chooseMat < 0.8): #diffuse
                    scene.list.append(Sphere(center, 0.2, Lambertian(np.array([random.uniform(0,1)*random.uniform(0,1), random.uniform(0,1)*random.uniform(0,1), random.uniform(0,1)*random.uniform(0,1)]))))
                elif(chooseMat < 0.95): #metal
                    scene.list.append(Sphere(center, 0.2, Metal(np.array([0.5*(1 + random.uniform(0,1)), 0.5*(1 + random.uniform(0,1)), 0.5*(1 + random.uniform(0,1))]), 0.5*random.uniform(0,1))))
                else: #glass
                    scene.list.append(Sphere(center, 0.2, Dielectric(1.5)))
    scene.list.append(Sphere(np.array([0, 1, 0]), 1.0, Dielectric(1.5)))
    scene.list.append(Sphere(np.array([-4, 1, 0]), 1.0, Lambertian(np.array([0.4, 0.2, 0.1]))))
    scene.list.append(Sphere(np.array([4, 1, 0]), 1.0, Metal(np.array([0.7, 0.6, 0.5]), 0.0)))
    return scene

def calculateColor(ray, world, depth):
    tMax = 100000.0
    tMin = 0.001
    maxDepth = 8
    hitRecord = world.hit(ray, tMin, tMax)
    if(hitRecord.successful):
        if(depth < maxDepth):
            scatterRecord = hitRecord.material.scatter(ray, hitRecord)
            if scatterRecord.successful:
                color = scatterRecord.attenuation * calculateColor(scatterRecord.scattered, world, depth + 1)
            else:
                color = np.array([0, 0, 0])
        else:
            color = np.array([0, 0, 0])
    else:
        unit_direction = unitVector(ray.direction)
        t = 0.5 * ((unit_direction[1]) + 1.0)
        color = (1.0 - t) * np.array([1.0, 1.0, 1.0]) + t * np.array([0.5, 0.7, 1.0])
    return color

def main():
    if(len(sys.argv) == 4):
        fileName = sys.argv[1]
        nx = int(sys.argv[2])
        ny = int(sys.argv[3])
        ns = 100
    else:
        if(len(sys.argv) == 5):
            fileName = sys.argv[1]
            nx = int(sys.argv[2])
            ny = int(sys.argv[3])
            ns = int(sys.argv[4])
        else:
            fileName = "img.ppm"
            nx = 480
            ny = 340
            ns = 100
            
    file = open(fileName, "w")
    file.write("P3\n")
    file.write(str(nx) + " " + str(ny) + "\n")
    file.write("255\n")

    lookfrom = np.array([13,2,3])
    lookat = np.array([0,0,0])
    distToFocus = 10.0
    aperture = 0.1
    camera = Camera(lookfrom, lookat, np.array([0,1,0]), 20, nx/ny, aperture, distToFocus)

    world = randomScene()
    for j in range(ny - 1, -1, -1):
        for i in range(nx):
            color = np.array([0,0,0])
            for s in range(ns):
                u = (i + random.uniform(0,1)) / nx
                v = (j + random.uniform(0,1)) / ny
                ray = camera.getRay(u, v)
                color = color + calculateColor(ray, world, 0)
            color = color / ns
            color = color ** 0.5
            ir = int(255.99 * color[0])
            ig = int(255.99 * color[1])
            ib = int(255.99 * color[2])
            file.write(str(ir) + " " + str(ig) + " " + str(ib) + "\n")
    file.close()

main()
