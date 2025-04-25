# PyPhysicsv1
A Python-based 2D n-body engine which allows the user to easily customize the bodies that are in the simulation.
Written by Van Nipper for a 2024 independent research study under the guidance of Professor Andy Digh.

OVERVIEW
This program was designed to explore particle simulation as well as computer graphics.

RUNTIME
This engine was designed to have a runtime of O(n^2). This means as the number of bodies increases,
the runtime increases quadratically. There are other algorithms for n-body engines that can optimize
this runtime down to O(n*log n). In a future study (v2), I will implement this algorithm to significantly
increase the number of bodies that can be simulated simultaneously.

HOW TO RUN
1. Ensure the pygame module is installed. Do "pip install pygame"
2. To run the engine directly, do "python3 runengine.py"
3. To customize the bodies, do "python3 start.py"
4. To randomize the bodies, do "python3 createdata.py" then run the engine directly.

HOW TO USE
 - Click and drag to move around
 - Use + / - to zoom in and out
 - Press space to center the cursor on (0,0)
 - Click on a body to center the camera on it.
 - Use < / > to slow down and speed up time.
 - Use Cmd + W to exit the program.

For more information, along with an in-depth analysis of the physics involved in this program, please
read the research paper included in the Git repo.
