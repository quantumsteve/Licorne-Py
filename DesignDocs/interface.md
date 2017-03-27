The main window
===============

- Layer selection widget
- Layer property widget
- Properties profile widget

The program will act on a list of `Layer` objects
=================================================

- thickness float>0
- nsld (nuclear scattering length density) float, complex
- msld (magnetic scattering length density) named tuple of floats length 3 (polar coordinates)
- roughness: contains type and sublayers
- each of them has potential fitting properties

Special behavior for `Substrate` layer.


Layer selection widget
======================

- emit signal with selected layers when selection changes
- emit signal when layers are added or deleted
- slot for selection on plotting window
- slot for new list of layers from script

Layer property widget
=====================

- list of properties
- modify property subwidget (includes fitting properties)
- emit changes for fitting properties
- fitting ties: options are mixed, fixed, together, and separately

Properties profile widget
=========================

Plot of selected property for all layers

- emit signal for selected layers on the plot
- function to update plot on property or property selection change

Main window
===========

Menu for file loading, saving
Menu for model change (script)
