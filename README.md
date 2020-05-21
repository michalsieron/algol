**Algol** is a simulation of [eclipsing binary stars](https://en.wikipedia.org/wiki/Binary_star#Eclipsing_binaries). It is my university project for OOP course.

## ✨ Features of **Algol**

- is written in python3
- uses ray tracing
- utilizes compute shaders

## 🚀 Installation

You will need python3.4+ (tested only on 3.8)
As algol is using OpenGL Compute Shaders you will need GPU with drivers supporting OpenGL 4.3.

- clone this repo `git clone https://github.com/michalsieron/algol.git`
- go to cloned directory `cd algol`
- install required packages `pip install -r requirements.txt --user`
- run simulation `python algol/main.py`

## 💻 Usage

- you can use mouse scroll to change zoom level and space to reset it
- `Y` and `Z` keys change perspective
- use 1-9 keys on numpad to change presets
- press escape button to exit program

## ❗ Notice

**Algol** is not physically correct! Movements of stars and planets are described by sines and cosines. No physical forces are taken into account!

## 📝 TODO

- [x] base app
- [x] compute shader
- [x] ray tracing
- [ ] calculate luminosity of the system and graph it
- [ ] proper abstract classes using `abc` module
- [ ] Planet subclass
- [x] config files