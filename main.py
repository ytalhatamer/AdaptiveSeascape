import pandas as pd
from CreatePlatform import *
global scene, filename, graph

if __name__=='__main__':
    # Input file should be m by n matrix. m: Number of Drug/Selection condition
    #                                     n: Number of Variant/Mutant/Genotype
    df_data = pd.read_excel('Inputs.xlsx',sheet_name='Data')
    df_states = pd.read_excel('Inputs.xlsx', sheet_name='States').set_index('States')
    df_states= df_states.dropna(how='all',axis=0)
    df_data2=df_data.dropna(how='all', axis=1)
    obj=CreatePlatform(df_data2,df_states)
