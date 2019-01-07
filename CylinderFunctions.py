from InputSettings import *
import numpy as np
from vpython import vector, cylinder, color


class CylinderFunctions(InputSettings):
    def __init__(self,data,states):
        InputSettings.__init__(self, data,states)



    def opaque_cylinder(listobjs):
        for i in listobjs:
            i.opacity = .1

    def position_cylinder(self,num_cylinder,order,orbitalnumber):
        if num_cylinder == 1:
            cylpos = vector(0, self.orbital_diameter*orbitalnumber, 0)
            return cylpos
        else:
            alpha_btw_cyl = self.view_angle / (num_cylinder + 1)
            alpha_now = (-self.view_angle / 2.) + alpha_btw_cyl * (order + 1)
            cylpos=vector(self.orbital_diameter*orbitalnumber * np.sin(alpha_now), self.orbital_diameter*orbitalnumber * np.cos(alpha_now), 0)
            return cylpos

    def create_cylinder(self,x, y, MIC, mut_list, prom):

        disks = []
        a = []
        disks=[self.disk_height for i in range(int(MIC//self.disk_height))]+[MIC % self.disk_height
                                                                        for i in range(1) if MIC % self.disk_height!=0]
        # while MIC != 0:
        #     if MIC > self.disk_height:
        #         disks.append(self.disk_height)
        #         MIC -= self.disk_height
        #     else:
        #         disks.append(MIC)
        #         MIC -= MIC
        j = .15
        for i in range(len(disks)):
            a.append(cylinder(pos=vector(x, y, sum(disks[:i])), axis=vector(0, 0, disks[i]),
                              radius=self.cylinder_diameter, color=color.gray(j)))  # ,material=materials.unshaded
            j += .1
        kk = vector(255.0/255.0, 248.0/255.0, 220.0/255.0)
        a.append(cylinder(pos=vector(x, y, MIC + .1), axis=vector(0, 0, .1),
                          radius=self.cylinder_diameter - .5, color=kk))
        posn = vector(x, y, MIC)

        b = self.variants_on_top(posn, mut_list)
        if prom == 1:
            c = self.middle_variant_on_top(posn)

            return a + b + c
        else:
            return a + b

    def variants_on_top(self,position,variants):
        b = []
        rr = (self.cylinder_diameter / 5.)

        for l in range(len(variants)):
            if variants[l] == 1:
                posnew = vector(position.x + (2 * self.cylinder_diameter / 3) *
                                                            np.cos(l * (np.pi / ((len(variants)) / 2.0))),
                                position.y + (2 * self.cylinder_diameter / 3) *
                                                            (np.sin(l * (np.pi / ((len(variants)) / 2.0)))), position.z)
                b.append(cylinder(pos=posnew, axis=vector(0, 0, rr - rr / 5.), color=self.circle_color_periphery[l],
                                  radius=rr + rr / 10, opacity=.7))

            elif variants[l] == 2:
                posnew = vector(position[0] + (2 * self.cylinder_diameter / 3) * np.cos(l * (np.pi / ((len(variants)) / 2.0))),
                                position[1] + (2 * self.cylinder_diameter / 3) * (np.sin(l * (np.pi / ((len(variants)) / 2.0)))), position[2])
                b.append(cylinder(pos=posnew, axis=vector(0, 0, rr - rr / 5.), color=vector(0, .2, 0),
                                  radius=rr + rr / 10, opacity=.7))  # ,height=rr-.5)
        return b

    def middle_variant_on_top(self,position):
        c = []
        rr = self.cylinder_diameter / 5.
        c.append(cylinder(pos=position, axis=vector(0, 0, rr - .1), color=self.circle_color_middle,
                          radius=rr + rr / 10, opacity=.7))
        return c
