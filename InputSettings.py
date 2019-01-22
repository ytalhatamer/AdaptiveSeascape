from vpython import vector
import numpy as np
import random
import seaborn as sns
class InputSettings:
    def __init__(self,data,states):
        # self.color_palette = [  vector(1.00, 0.00, 0.00),
        #                         vector(0.00, 0.00, 1.00),
        #                         vector(0.00, 1.00, 1.00),
        #                         vector(0.00, 1.00, 0.00),
        #                         vector(1.00, 0.00, 1.00),
        #                         vector(1.00, 1.00, 0.00),
        #                         vector(0.00, 0.00, 0.00),
        #                         vector(1.00, 0.47, 0.00),
        #                         vector(0.20, 0.47, 0.75),
        #                         vector(0.75, 0.59, 0.27),
        #                         vector(0.50,0.25,0.75)]
        self.circle_color_middle = vector(0.30, 0.30, 0.30)
        self.orbital_diameter = 50
        self.cylinder_diameter = 4
        self.disk_height = 4
        self.view_angle= 2. * np.pi / 3. # Cylinders in one orbital can be put total of 2pi/3 degrees seperated left end to right end
        self.data = data
        self.states = states
        self.MutantColumns= [i for i in self.data.columns if 'Mutant_' in i]

        self.numVariants=len(self.MutantColumns)
        # self.circle_color_periphery=[i/255.0 for i in [vector(117,116,114),
        #                              vector(81,177,107),
        #                              vector(47,161,221),
        #                              vector(95,193,204),
        #                              vector(130,127,186),
        #                              vector(237,136,122)]]
        colorpalette=[sns.color_palette('bright')[i] for i in [0,1,2,3,4,7,8,9,5,6]]
        self.circle_color_periphery=[vector(*i) for i in colorpalette[:self.numVariants]]
        # if len(self.color_palette) < self.numVariants:
        #     self.circle_color_periphery=[vector(random.random(),random.random(),random.random()) for i in range(self.numVariants)]
        # else:
        #     self.circle_color_periphery=self.color_palette[:self.numVariants]
        # self.circle_color_periphery=random.sample(self.color_palette,self.numVariants)
        self.FitnessColumns=[i for i in self.data.columns if 'Fitness' in i]
        self.numFitnessStates = len(self.FitnessColumns)
        self.numStates = len(self.states)
        print('Number of variants on top of cylinders: ', self.numVariants)
        print('Number of fitness states: ', self.numFitnessStates)
        print('Number of states: ', self.numStates)

        if self.numFitnessStates == self.numStates:
            print('Number of states and number of fitness values are matching.')
        else:
            print('Number of states and number of fitness values are not matching.\n')
            print('Please fill fitness values in data sheet or selection states in states sheet')
