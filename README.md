<h1 align="center"> Mechanics of Solids</h1>

[![Downloads](https://static.pepy.tech/badge/Lib-mechsolids-abhinav)](https://pepy.tech/project/Lib-mechsolids-abhinav)

<h2 align="center">Mechanical Engineering Department, Indian Institute of Technology Kharagpur</h2>

<h3> parent repository : <a href="https://github.com/jeevanjyoti4/mechsolids">Repo Link</a> </h3>

This is a repository that contains the code to the python package that I have created for the course ME21003 - Mechanics of Solids. The package contains a module called Beam that can be used to create a beam object. The package also contains a class called math_functions that contains functions to solve add loads on the beam and solve for the shear force and bending moment diagrams.

<h2>  Manual to use the Beam class </h2>
<h3> Simply install the package using the following command and use the Beam class as shown below: </h3>

```bash
pip install Lib-mechsolids-abhinav==0.0.1
```
PyPi link: [https://pypi.org/project/Lib-mechsolids-abhinav/](https://pypi.org/project/Lib-mechsolids-abhinav/)

<!-- <h3> OR if you are forking the repository and want to do things manually, then make sure to have the following libraries</h3> -->
We need to have the following libraries installed before using the beam class. To install them(if not already installed), use the following command:

```bash
pip install sympy
pip install numpy
pip install matplotlib
```

* Tested with Sympy version 1.11.1
* Tested with Python version 3.9.13
* Tested with Matplotlib version 3.5.2
* Tested with Numpy version 1.21.5

<h3> Steps to use the Beam class: </h3>
<ol>
<li> Create a new Python file to solve a problem. Import the Beam and math modules as follows:
  
```python
from Lib_mechsolids_abhinav.Beam import *
from Lib_mechsolids_abhinav.math_functions import *
```
</li>

<li> Create either a <b>Simply Supported Beam</b> or a <b>Cantilever Beam</b> object as follows:
  
```python
beam = SimplySupportedBeam(NameOfBeam, LengthOfBeam)
beam = CantileverBeam(NameOfBeam, LengthOfBeam)
```
</li>

<li> If the beam is a <b>Simply Supported Beam</b>, then add the supports as follows:
  
```python
beam.add_supports(Support(PositionOfSupport1, PositionOfSupport2))
```
where *position* is the distance of the support from the left end of the beam.
</li>

<li> Create loads using the load class as follows:
  
```python
load1 = PointLoad(ValueOfLoad, PositionOfLoad)
load2 = DistributedLoad(StartPosition, EndPosition, LoadAtStart, LoadAtEnd)
load3 = EquationLoad(EquationString, StartPosition, EndPosition, startLoad(=0), endLoad(optional))

# add these loads on the beam
beam.add_load(load1)
beam.add_load(load2)
beam.add_load(load3)
```
where *position* is the distance of the load from the left end of the beam.
</li>

<li> To generate the shear force and bending moment diagrams, use the following functions:
  
```python
beam.plot_sfd_and_bmd()
# if you want to plot just the shear force diagram or bending moment diagram, use the following functions:
beam.plot_sfd()
beam.plot_bmd()
```
</li>
</ol>
