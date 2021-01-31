# Simple-Turing-Machine

This is a command-line Turing machine that can process quadruples and produce an output as described in Martin D. Davis' *Theory of Computation*.

## Usage

This script can be used either by running `turing.py` or by declaring command-line arguments. \
```python turing.py <quadruple_filepath> <steps> <values>```
- `quadruple_filepath`: path to the file containing the quadruples
- `steps`: number of steps the program should run (-1 means the program will run until it halts)
- `values`: the values to be inserted into the tape

The following would add 4 and 8 using the included example of addition.

```python turing.py example/addition.txt -1 4 8```

## Quadruples
The quadruples are stored in a text file, with each quadruple on separate lines. Each quadruple is in one of the following three forms:
- `initial_state,symbol,L,next_state`
- `initial_state,symbol,R,next_state`
- `initial_state,symbol,symbol,next_state`

## Input/Output
For this Turing machine, the tape alphabet consists only of B (blank) and 1, with numbers represented by successive sections of 1. In addition, all inputs are positive integers.

The input is represented by successive strokes of 1, with each input separated by a single B from the next input. The machine begins in state 1, with the tape head scanning a B immediately to the left of the first input. Finally, the output is a sequence of 1's on the tape, with the tape head scanning the B immediately to the left of the output string.