# Simple-Psspy
# By: Behdad Dalvandi <b.dalvandi@gmail.com>
# Version: 0.1b

Python 2.7 module to simplify automating PSS/E via psspy module

This python module has been / is being developped to make 'psspy' object-oriented in order to simplify the usage of the module.
As the function names and arguments in 'psspy' module do not seem friendly enought, I decided to develop a simpler and more user-friendly one.
I feel it is a nessesary job because the users of 'PTI PSS/E' are more electrical engineers than skilled programmers.

The benefit of this module is that it is an object-oriented module including a class named 'PssCase' which initializes PSS/E engine regardless of the program path, maximum bus size, alert redirecting,... .
Most of the commonly used argument values are set as default and the programmer would seldom mind them.
Methods and arguments are named meaningfully and user-friendly.
Functions to read/write single values are declared as Properties.
