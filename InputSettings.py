from vpython import vector
import numpy as np
import random
class InputSettings:
    def __init__(self,data,states):
        self.color_palette = [vector(0.20, 0.47, 0.75),
                                        vector(0.75, 0.59, 0.27),
                                        vector(1.00, 0.00, 0.00),
                                        vector(0.00, 1.00, 1.00),
                                        vector(0.00, 0.00, 0.00),
                                        vector(1.00, 0.00, 1.00),
                                        vector(0.00, 1.00, 0.00),
                                        vector(0.00, 0.00, 1.00),
                                        vector(1.00, 1.00, 0.00),
                                        vector(1.00, 0.47, 0.00)]
        self.circle_color_middle = vector(0.30, 0.30, 0.30)
        self.orbital_diameter = 50
        self.cylinder_diameter = 4
        self.disk_height = 4
        self.view_angle= 2. * np.pi / 3. # Cylinders in one orbital can be put total of 2pi/3 degrees seperated left end to right end
        self.data = data
        self.states = states
        self.MutantColumns= [i for i in self.data.columns if 'Mutant_Periphery' in i]

        self.numVariants=len(self.MutantColumns)
        self.circle_color_periphery=random.sample(self.color_palette,self.numVariants)
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
