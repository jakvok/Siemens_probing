# Siemens CNC probing cycles

The script generates text representation of Siemens Sinumerik CNC probing cycles.
Script asks user to several questions about what is needed to probe in CNC program and based on the answers choose right cycle parameters and it's values.

## What is CNC probing cycle?
When parts are machined on CNC milling machines or mill-turn centres, in many causes is necessary to use measuring probe to check machined dimmensions or measure and specify position of workpiece zero point and orientation of base coordination system.
Measuring probe is the piece of hardware driven by machine system in order to CNC code in CNC machining programme.

To make job easier, CNC programm do not drive probe directly move-by-move, actio-by-action, but uses the <i> probing cycle </i>. It can be imagined as manufacturer predefined function with several parameters, which can be used everywhere in CNC programme in any count of instances.

Example of cycle. Set Offset G54, zero point in centre of hole dia 32mm:
CYCLE977(1101,10001,,1,32,,,7,5,11,16,5,,,1,"",,0,1.01,1.01,-1.01,0.34,1,0,,1,11,-3,15)

Example of cycle. Measure position of surface in active CS, move in -X axe:
CYCLE978(0,,,1,-55,15,5,1,2,1,"",,0,1.01,1.01,-1.01,,,,,1,1)

[Process Measuring With Sinumerik](https://www.youtube.com/watch?v=DBjlgdmLbrM)


# Using of the script
The script does not create all CNC programme for machining parts as CAM software is used for, it just generates the probing cycle.
After the cycle is created, it is necessary to copy and paste it into appropriate place in CNC programme created by standard way.

## linux
Python 3.8+, only standard modules required on linux.<br>
Make the script executable:<br>
`$ chmod +x ./probing.py`

Run the script without parameter for communication in default english language:<br>
`$ ./probing.py`

Run the script with parameter `cz` for communication in czech language:<br>
`$ ./probing.py cz`

## windows
When python 3.8+ installed, using is the same as on linux system.

Or when python is not available on your win system, use the standalone executable `probingVx.x.x.exe`.<br>
Executable run without parameter starts script communicate in english language.<br>
Executable run with parameter `cz` starts script communicate in czech language.<br>

How to run executable with parameter using shortcut:
[https://www.digitalcitizen.life/shortcut-arguments-parameters-windows/](https://www.digitalcitizen.life/shortcut-arguments-parameters-windows/)


## capabilities
The script can generate cycles for probing the features:<br>
- surface   (CYCLE978)
- hole      (CYCLE977)
- shaft     (CYCLE977)
- groove    (CYCLE977)
- web       (CYCLE977)

The script is debugged on Siemens Sinumerik 840D control system and Grob G350 5axis milling machine.