from engine import *
from random import uniform
import glm

engine = Engine()

night = Model('./obj/night.obj','./texture/night_texture.jpg')
night.setLight(0.3,0,0,1)
night.setRotation(rotationAngle=90, vec_rotationAxis=glm.vec3(1,0,0))
night.setScale(glm.vec3(0.2, 0.2, 0.2))

grass = Model('./obj/grass.obj','./texture/grass_texture.png')
grass.setScale(glm.vec3(0.4, 1.0, 0.4))

soil = Model('./obj/soil.obj','./texture/soil_texture.png')
soil.setPosition(glm.vec3(0, 0.04, 0))

medievalHouse = Model('./obj/medieval house.obj','./texture/medieval house.png')
medievalHouse.setPosition(glm.vec3(0, 0, 0))
medievalHouse.setScale(glm.vec3(4.0, 4.0, 4.0))
medievalHouse.setRotation(rotationAngle=0, vec_rotationAxis=glm.vec3(0,1,0))

axe = Model('./obj/axe.obj','./texture/axe_texture.png')
axe.setPosition(glm.vec3(-20.0, 5.25, -10.65))
axe.setRotation(rotationAngle=-30, vec_rotationAxis=glm.vec3(1,0,0))

table = Model('./obj/table.obj','./texture/table_texture.png')
table.setPosition(glm.vec3(15.0, 0, -3.0))
table.setScale(glm.vec3(5.0, 5.0, 5.0))

checkers = Model('./obj/checkers.obj','./texture/checkers_texture.png')
checkers.setPosition(glm.vec3(12.0, 8.5, -1.0))
checkers.setScale(glm.vec3(12.0, 12.0, 12.0))
checkers.setRotation(rotationAngle=45, vec_rotationAxis=glm.vec3(0,1,0))

luz2 = Light('lightPos2', 'lightColor2')
luz2.setPosition(glm.vec3(15.0, 16.0, 0))
luz2.isVisible = False

luz3 = Light('lightPos3', 'lightColor3')
luz3.setPosition(glm.vec3(-10.0, 16.0, 0))
luz3.isVisible = False

tree1 = Model('./obj/tree.obj','./texture/tree_texture.png')
tree1.setPosition(glm.vec3(50, 0, -7))
tree1.setScale(glm.vec3(10.0, 10.0, 10.0))
tree1.setRotation(rotationAngle=-45, vec_rotationAxis=glm.vec3(0,1,0))

tree2 = Model('./obj/tree.obj','./texture/tree_texture.png')
tree2.setPosition(glm.vec3(22.2, 0, -78.5))
tree2.setScale(glm.vec3(10.0, 10.0, 10.0))
tree2.setRotation(rotationAngle=45, vec_rotationAxis=glm.vec3(0,1,0))

tree3 = Model('./obj/tree.obj','./texture/tree_texture.png')
tree3.setPosition(glm.vec3(-50, 0, 7))
tree3.setScale(glm.vec3(10.0, 10.0, 10.0))
tree3.setRotation(rotationAngle=135, vec_rotationAxis=glm.vec3(0,1,0))

tree4 = Model('./obj/tree.obj','./texture/tree_texture.png')
tree4.setPosition(glm.vec3(-22.2, 0, 78.5))
tree4.setScale(glm.vec3(10.0, 10.0, 10.0))
tree4.setRotation(rotationAngle=-135, vec_rotationAxis=glm.vec3(0,1,0))

bush1 = Model('./obj/bush.obj','./texture/bush_texture.png')
bush1.setPosition(glm.vec3(40, 0, 15))
bush1.setScale(glm.vec3(10.0, 10.0, 10.0))
bush1.setRotation(rotationAngle=-90, vec_rotationAxis=glm.vec3(0,1,0))

bush2 = Model('./obj/bush.obj','./texture/bush_texture.png')
bush2.setPosition(glm.vec3(-40, 0, -15))
bush2.setScale(glm.vec3(10.0, 10.0, 10.0))
bush2.setRotation(rotationAngle=90, vec_rotationAxis=glm.vec3(0,1,0))

bench1 = Model('./obj/bench.obj','./texture/bench_texture.png')
bench1.setPosition(glm.vec3(87.5, 4, 25))
bench1.setRotation(rotationAngle=90, vec_rotationAxis=glm.vec3(0,1,0))

bench2 = Model('./obj/bench.obj','./texture/bench_texture.png')
bench2.setPosition(glm.vec3(87.5, 4, -25))
bench2.setRotation(rotationAngle=-90, vec_rotationAxis=glm.vec3(0,1,0))

bench3 = Model('./obj/bench.obj','./texture/bench_texture.png')
bench3.setPosition(glm.vec3(-88.75, 4, -28))
bench3.setRotation(rotationAngle=90, vec_rotationAxis=glm.vec3(0,1,0))

bench4 = Model('./obj/bench.obj','./texture/bench_texture.png')
bench4.setPosition(glm.vec3(-88.75, 4, 28))
bench4.setRotation(rotationAngle=-90, vec_rotationAxis=glm.vec3(0,1,0))

raioAnimation = 55
delay = -0.1
wagonAnimation = Model('./obj/wagon.obj','./texture/wagon_texture.png')
wagonAnimation.setPosition(glm.vec3(0, 2, raioAnimation))
wagonAnimation.setRotation(90, glm.vec3(0,1,0))
wagonAnimation.setScale(glm.vec3(1.5, 1.5, 1.5))

animationWagon = AnimationInCircles(0,0,wagonAnimation.position,delay)
wagonAnimation.animation = animationWagon

cowAnimation = Model('./obj/cow.obj','./texture/cow_texture.png')
cowAnimation.setPosition(glm.vec3(0, 0, raioAnimation))
cowAnimation.setRotation(180, glm.vec3(0,1,0))
cowAnimation.setScale(glm.vec3(3, 3, 3))

animationCow = AnimationInCircles(0,0,cowAnimation.position,0)
cowAnimation.animation = animationCow

lamp = Model('./obj/lamp.obj','./texture/lamp_texture.png')
lamp.setLight(1,1,0,1000)
lamp.setPosition(glm.vec3(0, 2, raioAnimation))

animationLamp = AnimationInCircles(0,0,lamp.position,delay)
lamp.animation = animationLamp

luz = Light('lightPos1', 'lightColor1')
luz.setPosition(glm.vec3(0, 5, raioAnimation))
luz.setLightColor(12*glm.vec3(1,0.4,0.4))
luz.isVisible = True

animationLight = AnimationInCircles(0,0,luz.position,delay)
luz.animation=animationLight

engine.addModel(night)
engine.addModel(grass)
engine.addModel(soil)
engine.addModel(medievalHouse)
engine.addModel(axe)
engine.addModel(table)
engine.addModel(checkers)
engine.addModel(luz2)
engine.addModel(luz3)
engine.addModel(tree1)
engine.addModel(tree2)
engine.addModel(tree3)
engine.addModel(tree4)
engine.addModel(bush1)
engine.addModel(bush2)
engine.addModel(bench1)
engine.addModel(bench2)
engine.addModel(bench3)
engine.addModel(bench4)
engine.addModel(wagonAnimation)
engine.addModel(cowAnimation)
engine.addModel(lamp)
engine.addModel(luz)

def flora(engine, numOfPlants, angleInicial, angleFinal, radiusInicial, radiusFinal):
    i = 0
    while i < numOfPlants:
        angle = math.radians(uniform(angleInicial, angleFinal))
        radius = uniform(radiusInicial, radiusFinal)

        tree = Model('./obj/tree.obj','./texture/tree_texture.png')
        tree.setPosition(glm.vec3(radius*math.sin(angle), 0, radius*math.cos(angle)))
        tree.setScale(glm.vec3(8.0, 8.0, 8.0))
        tree.setRotation(0.0, vec_rotationAxis=glm.vec3(0,1,0))

        engine.addModel(tree)

        i += 1

flora(engine, 40, -60, 60, 70, 150)
flora(engine, 40, 180-60, 180+60, 70, 150)

engine.initialize()
    