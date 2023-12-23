from typing import Type


"""
Gates A1-A23 & Gates B1-B31 are located at the Main Terminal Building.
Gates C15-40 are located at the Satellite Terminal Building.

Hall A is used for flights to Non-Schengen countries and Non-European countries.
Hall B handles flights to Intra-Schengen countries as well as domestic services.
"""

GATE: Type = tuple[int, str]

for number in range(1, 24):
    gate: GATE = (number, "A"); print(gate, end="")
for number in range(1, 32):
    gate: GATE = (number, "B"); print(gate, end="")
for number in range(15, 41):
    gate: GATE = (number, "C"); print(gate, end="")
