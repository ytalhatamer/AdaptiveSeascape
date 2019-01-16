from CylinderFunctions import *
import numpy as np
import os, povexport
from vpython import vector, canvas, box, ring
from datetime import datetime

class CreatePlatform(CylinderFunctions):
    def __init__(self,data,states):
        CylinderFunctions.__init__(self,data,states)
        self.scene = canvas()
        self.scene.center = vector(0, 120, 1)  # Use this for upside down 2D picture
        self.scene.width = 1920
        self.scene.height = 1080
        self.scene.background = vector(1, 1, 1)
        self.scene.ambient = vector(0.5, 0.5, 0.5)
        self.scene.fov = np.pi / 5.0
        self.scene.range = 180.0
        datenow=str(datetime.now()).replace(' ', '-').replace(':', '-').split('.')[0]
        for Fitnesses in self.FitnessColumns:
            self.plot_scene(Fitnesses)
            self.pov_export('.',datenow+'-'+Fitnesses)

    def plot_scene(self,FitnessColumn):
        cyls = []

        for index,variant in self.data.iterrows():
            self.num_cylinder_in_orbital=len([i for i in self.data['Orbital_Number'] if variant['Orbital_Number']==i])
            poss = self.position_cylinder(self.num_cylinder_in_orbital, variant['Order_in_Orbital'],variant['Orbital_Number'])

            if 'Mutant_Middle' in variant:
                prom=variant['Mutant_Middle']
            else:
                prom=0
            cyls_now = self.create_cylinder(poss.x,poss.y, variant[FitnessColumn]*self.disk_height, variant[self.MutantColumns].values, prom)
            cyls.append(cyls_now)

        for i in range(1,self.data['Orbital_Number'].max()+1):
            ring(pos=vector(0, 0, .1), axis=vector(0, 0, 0.1), radius=self.orbital_diameter * i, thickness=.2, color=vector(0, 0, 0))

        return cyls

    def arrow_between_cylinders(pos1, pos2, color, r):
        def distance(pos1, pos2):
            x = pos2.x - pos1.x
            y = pos2.y - pos1.y
            lenR = np.sqrt(x * x + y * y)
            return (lenR)

        lenArrow = distance(pos1, pos2)
        box(pos=(pos1 + pos2) / 2, axis=pos2 - pos1, length=lenArrow - 10, width=.1, height=.25, color=color)
        #    arrow(pos=pos1,axis=vector(pos2.x-pos1.x,pos2.y-pos1.y,0),length=lenArrow,shaftwidth=.01,color=color)

    def hide_scene(listobjs):
        for curr_object in listobjs:
            for j in curr_object:
                j.visible = False

    def pov_export(self,export_path,export_name):
        if not os.path.exists(export_path):
            os.makedirs(export_path)
        filename = export_name + '.pov'
        fullname = export_path + '/' + filename
        print(self.scene.camera.pos)
        povexport.export(canvas=self.scene, filename=fullname, shadowless=1)

    def take_screenshot(self):
        return None
