[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/F2F01JB1KE)

# Colebrook-Clamond-Python
Efficient Python implementation of Clamond’s quartic algorithm (2008) for solving the Colebrook equation, widely used in fluid mechanics, hydraulics, and district heating/cooling (DH/DC) pipe network calculations.

This repository provides:
* Fast and robust friction factor solver (f_clamond) using Clamond’s algorithm.
* Example scripts for district heating (DH) cases, showing effects of pipe diameter, roughness, velocity, and temperature.
* Clear, compact, and extendable code — ready for engineering simulations and teaching.

The Colebrook equation cannot be solved explicitly with elementary functions. Approximations (like Haaland) are fast but inaccurate; the Lambert W-function gives an exact form but is unstable at high Reynolds numbers.

Clamond (2008) introduced a quartic iteration algorithm that is:
* Accurate to machine precision (≈16 digits with 2 iterations).
* Robust across all relevant Reynolds and K values.
* As fast as explicit approximations (only a few logarithm evaluations).
* Simple to implement and integrate into engineering workflows.

## Table of Contents
- [Structure](README.md#Structure)
- [Installation](README.md#Installation)
- [Applications](README.md#Applications)
- [Reference](README.md#Reference)
- [License](README.md#License)
- [Acknowledgements](README.md#Acknowledgements)

## Structure
`colebrook_clamond.py`: core solver (f_clamond) with user-defined iteration control.

`examplescript.py`: practical district heating examples:
* Full set of DH pipe scenarios (service, feeder, main).
* New vs old steel pipes (different roughness).
* Temperature effects (20 °C, 60 °C, 80 °C water).
* Outputs Reynolds number, relative roughness, friction factor, and pressure gradient.

## Installation
```
git clone https://github.com/YourUserName/Colebrook-Clamond-Python.git
cd Colebrook-Clamond-Python
```

## Applications
* District heating & cooling (DHC) pipe network analysis
* Water distribution systems
* Hydraulic engineering calculations
* Teaching fluid dynamics (Reynolds, roughness, friction)
* Simulation frameworks (CFD, energy systems, network models)

## Reference
Clamond, D. (2008). Efficient resolution of the Colebrook equation. arXiv:0810.5564.

## License
Open-source under MIT License. Please acknowledge authorship if you use or modify.

## Acknowledgements
Above all, I give thanks to **Allah, The Creator (C.C.)**, and honor His name **Al-‘Alīm (The All-Knowing)**.

This repository is lovingly dedicated to my parents who have passed away, in remembrance of their guidance and support.

I would also like to thank **ChatGPT (by OpenAI)** for providing valuable support in updating and improving the Python implementation.
