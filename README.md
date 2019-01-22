# Adaptive Seascape
This tool plots adaptive landscape through time.

For example, below figure is showing the IC<sub>99.99</sub> values of TEM-1 beta-lactamase synonymous mutants. Each colored circle on top of cylinders show synonymous mutation(see legend on top left).Heigh of each cylinder here is normalized to IC<sub>99.99</sub> values of WT. Thus, WT composed on one gray disk. If a mutant has 2 gray disks meaning it has twice resistant to CTX than WT. Check the paper in the link for more details. [https://www.nature.com/articles/s41437-018-0104-z]


![alt text](2019-01-16-11-56-50-JAGMdeVisser-2018-Heredity.png)


Next example, is from Ravikumar et al.[https://www.sciencedirect.com/science/article/pii/S0092867418313308]. They evolved pfDHFR using their orthoRep system. In the paper (Figure 4) they showed the MIC values of 48 mutants. (Full combination of 6 mutations). This time height of the cylinders show the log<sub>10</sub> MIC (nM) median values. In the paper they mentioned that pyrimethamine resistant quadriple mutant malaria DHFR has resistance around 1.5-2mM range. (6 disk height in the picture)   

![alt text](Figure4-BrightColors.png)


This tool exports a *'*.pov' file as an output also opens up a ghostshell in your default browser. By using mouse, the viewing angle can be changed in the ghostshell. You can zoom in/out. Then you can take a screenshot to save the plot. 

For exporting high resolution publication figures, it is better use POV-Ray software (http://www.povray.org) and the exported pov file. POV-Ray can export pictures with different size and resolutions. 
