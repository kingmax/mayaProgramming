# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 0.2.1 - 2018-02-01
#### Fixed
- *wireMeshFromCurve* command giving an error because Python *cmds* namespace is not visible inside Maya by default.

## 0.2 - 2018-01-22
#### Added
- *RPolygon* wire profile.
- *Pattern*, new option to extend wire profiles. Enabling creation of ropes, parallel cables and more.
- *Distance* interpolation range.
- *Reverse normals*.
- *Smoothing* option to manage wire mesh normals (soft/hard edges).
- *wireMeshFromCurve* command renames newly created transform and mesh nodes to: *wire#* and *wireShape#*.

#### Changed
- Icons. New ones match Maya's orange color scheme for polygonal modeling.

#### Removed
- *Circle 8* wire profile (replaced by more general *RPolygon*).
- *Square* wire profile (replaced by more general *RPolygon*).

#### Fixed
- Unable to load *wireMeshCreator* node attributes values to Attribute Editor when node is created for the first time in Maya session.
- *Wire Mesh from Curve* menu item does not add proper command to a shelf when it is Ctrl+Shift+LMB from menu. 
- Maya crashes on undo/redo of *wireMeshFromCurve* command.
- Inability to properly keyframe and animate on *wireMeshCreator* node.
- Wrong calculations in *wireMeshCreator* node when curve is intersecting with itself.
- Icon for *wireMeshCreator* node not showing in Node Editor.

## 0.1 - 2017-10-01
#### Added
- *wireMeshFromCurve* command.
- *wireMeshCreator* node.
    - *Circle 8* wire profile.
    - *Square* wire profile.
    - *Line* wire profile.
    - *Start to End* interpolation range.
    - *EP to EP* interpolation range.
    - *Interpolation Steps* to adjust wire precision.
    - *Scale Profile* transformation.
    - *Rotate Profile* transformation.
    - *Twist* transformation.
- Icons for *wireMeshFromCurve* command, *wireMeshCreator* node and wire profiles.