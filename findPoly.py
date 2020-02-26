import itertools
import os

class Polygon():
    def __init__(self, offFile):
        self.vertices, self.faces = self.readOffFile(offFile)

    def readOffFile(self, offFile):
        data = open(offFile, "r")
        lines = data.readlines()
        numVertices, numFaces, _ = map(int, lines[1].split(" "))
        vertices, faces = self.splitVertsFaces(numVertices, numFaces, lines)
        data.close()
        return vertices, faces

    def splitVertsFaces(self, numVertices, numFaces, lines):
        vertices = []
        for i in range(2, numVertices + 2):
            line = lines[i].strip()
            line = line.replace("   ", ",")
            try:
                line = list(map(float, line.split(",")))
            except:
                line = list(map(float, line.split(", ")))
            vertices.append(line)
        faces = []
        for j in range(numVertices + 2, numVertices + numFaces + 2):
            line = list(map(int, lines[j].strip().split("\t")))
            faces.append(line)
        return vertices, faces

def checkTriangle(poly, index):
    _, p1, p2, p3 = poly.faces[index]
    v1, v2, v3 = poly.vertices[p1], poly.vertices[p2], poly.vertices[p3]
    x1 = [v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]]
    x2 = [v3[0] - v2[0], v3[1] - v2[1], v3[2] - v2[2]]
    crossProduct = xProduct(x1, x2)
    dot = dotProduct(crossProduct, v1)
    return dot > 0

def xProduct(v1,v2):
    cross = [v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[0] * v2[1] - v1[1] * v2[0]]
    return cross

def dotProduct(cross, v1):
    dot = 0
    for i in range(len(cross)):
        dot += cross[i] * v1[i]
    return dot

def checkQuad(poly, index):
    _, p1, p2, p3, p4 = poly.faces[index]
    v1, v2, v3, v4 = poly.vertices[p1], poly.vertices[p2], poly.vertices[p3], poly.vertices[p4]
    x1 = [v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]]
    x2 = [v3[0] - v2[0], v3[1] - v2[1], v3[2] - v2[2]]
    dotFirstThree = dotProduct(xProduct(x1, x2), v1)
    if dotFirstThree < 0:
        return False
    else:
        x1 = [v3[0] - v2[0], v3[1] - v2[1], v3[2] - v2[2]]
        x2 = [v4[0] - v3[0], v4[1] - v3[1], v4[2] - v3[2]]
        dotLastThree = dotProduct(xProduct(x1, x2), v1)
        return dotLastThree > 0

def findClockwise(poly):
    incorrect = []
    for i in range(len(poly.faces)):
        if poly.faces[i][0] == 3:
            if not checkTriangle(poly, i):
                incorrect.append(i)
        else:
            if not checkQuad(poly, i):
                incorrect.append(i)
    return incorrect

def findCorrectSequence(poly, incorrectIndices):
    length = len(poly.faces[0]) - 1
    for index in incorrectIndices:
        verts = poly.faces[index][1:]
        for perm in list(itertools.permutations(verts)):
            poly.faces[index] = [length] + list(perm)
            if length > 3:
                if checkQuad(poly, index):
                    break
            else:
                if checkTriangle(poly, index):
                    break
                
def rewriteFile(poly, offFile):
    data = open(offFile, "r")
    facesStart = 2 + len(poly.vertices)
    lines = data.readlines()
    for index in incorrectIndices:
        if poly.faces[index][0] < 4:
            lines[index + facesStart] = "{}\t{}\t{}\t{}\n".format(poly.faces[index][0], poly.faces[index][1], poly.faces[index][2], poly.faces[index][3])
        else:
            lines[index + facesStart] = "{}\t{}\t{}\t{}\t{}\n".format(poly.faces[index][0], poly.faces[index][1], poly.faces[index][2], poly.faces[index][3], poly.faces[index][4])
    data = open(offFile, "w")
    data.writelines(lines)
    data.close()

if __name__ == "__main__":
    loop = True
    while loop:
        offFile = str(input("Enter the name of the OFF file (inc. extention): "))
        if os.path.isfile(offFile) and offFile[-4:] == ".off":
            loop = False
        else:
            print("Enter a valid off file name")
    poly = Polygon(offFile)
    incorrectIndices = findClockwise(poly)
    print("There are {} clockwise defined faces in your off file\n".format(len(incorrectIndices)))
    findCorrectSequence(poly, incorrectIndices)
    if len(incorrectIndices) > 0:
        rewriteFile(poly, offFile)
        print("File has now been fixed")
    