import logging
import sys

logger = logging.getLogger()
console = logging.StreamHandler()
logger.addHandler(console)

class Tape:
    def __init__(self):
        self.tape = ['B','B']
        self.head_index = 0
    
    def read(self):
        '''
        Returns the symbol at the location of the tape head.
        '''
        return self.tape[self.head_index]

    def move_left(self):
        '''
        Moves the head of the tape to the left by one space.
        '''
        if self.head_index == 0:
            self.tape.insert(0, 'B')
        else:
            self.head_index -= 1
        return self.tape[self.head_index]

    def move_right(self):
        '''
        Moves the head of the tape to the right by one place.
        '''
        self.head_index += 1
        if self.head_index >= len(self.tape):
            self.tape.append('B')
        return self.tape[self.head_index]

    def write_symbol(self, symbol_to_write):
        '''
        Writes over the current space with a symbol.
        If the head is at the leftmost space, a blank symbol will be added at the start of the tape.
        If the head is at the rightmost space, a blank symbol will be added at the end of the tape.
        '''
        self.tape[self.head_index] = symbol_to_write
        if self.head_index == 0:
            self.tape.insert(0, 'B')
            self.head_index = 1
        elif self.head_index == len(self.tape)-1:
            self.tape.append('B')

    def fill_tape(self, values):
        '''
        Fills the tape with values represented by a list. Resets the head_index to 0.
        '''
        for value in values:
            while value > 0:
                self.move_right()
                self.write_symbol('1')
                value -= 1
            self.move_right()
        self.head_index = 0
    
    def get_number(self):
        '''
        Counts the number of 1 symbols starting from the next space leading up to the next blank and returns that count.
        '''
        i = self.head_index + 1
        result = 0
        while i < len(self.tape):
            if self.tape[i] == '1':
                result += 1
            i += 1
        return result

    def __str__(self):
        tape_text = list.copy(self.tape)
        tape_text.insert(self.head_index,'{')
        tape_text.insert(self.head_index+2,'}')
        return ''.join(tape_text)
    
    def __repr__(self):
        tape_text = list.copy(self.tape)
        tape_text.insert(self.head_index,'{')
        tape_text.insert(self.head_index+2,'}')
        return ''.join(tape_text)

class Quadruple:
    def __init__(self, current_state, symbol, action, next_state):
        self.current_state = current_state
        self.scanning_symbol = symbol
        self.action = action
        self.next_state = next_state

    def __str__(self):
        return '{},{},{},{}'.format(self.current_state, self.scanning_symbol, self.action, self.next_state)

    def __repr__(self):
        return '{},{},{},{}'.format(self.current_state, self.scanning_symbol, self.action, self.next_state)

class TuringProgram:
    def __init__(self):
        self.quadruple_list = []
        self.program_tape = Tape()
        self.state = 1
        self.current_quadruple = None
        self.next_quadruple = None
        self.halt = False
        self.step = 0
        self.output = 0

    def load_quadruples_from_file(self, filename):
        '''
        Loads quadruples from a file into the program.
        '''
        # check if file quads are valid
        with open(filename) as quadruples:
            for quadruple in quadruples:
                quadruple = quadruple.rstrip()
                quadruple_items = quadruple.split(',')
                self.quadruple_list.append(Quadruple(int(quadruple_items[0]), quadruple_items[1], quadruple_items[2], int(quadruple_items[3])))
        self.get_next_quadruple()

    def load_values(self, values):
        '''
        Loads a list of values into the program's tape.
        '''
        self.program_tape.fill_tape(values)

    def get_next_quadruple(self):
        '''
        Changes the current quadruple and searches the quadruple list for the next quadruple that can be executed.
        '''
        self.current_quadruple = self.next_quadruple
        for quadruple in self.quadruple_list:
            if (self.state == quadruple.current_state) and (self.program_tape.read() == quadruple.scanning_symbol):             
                self.next_quadruple = quadruple
                break
            else:
                self.next_quadruple = None

    def execute_step(self):
        '''
        Executes the next quadruple (if possible) and returns the current output.
        '''
        self.step += 1
        if self.next_quadruple != None: 
            action = self.next_quadruple.action.lower()
            if action == 'l':
                self.program_tape.move_left()
            elif action == 'r':
                self.program_tape.move_right()
            elif action == '1':
                self.program_tape.write_symbol('1')
            else:
                self.program_tape.write_symbol('B')
            self.state = self.next_quadruple.next_state
            self.get_next_quadruple()
        else:
            self.halt = True
        self.output = self.program_tape.get_number()

    def run_program(self, steps):
        '''
        Runs the program for as many steps as specified. To run the program until it finishes executing, use -1 for the number of steps.
        '''
        count = 0
        while count != steps:
            count += 1
            if self.halt:
                return self.output
            else:
                self.execute_step()
                

    def __str__(self):
        return '{}\n{} (step {})'.format(self.program_tape, self.output, self.step)

    def __repl__(self):
        return '{}\n{} (step {})'.format(self.program_tape, self.output, self.step)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        values = [int(x) for x in sys.argv[3:]]
        steps = int(sys.argv[2])
    else:
        filename = input('Path to file containing quadruples: ')
        values = int(input("Integer values: "))
        steps = int(input("Number of steps to complete (-1 for no step limit): "))

    turing = TuringProgram()
    turing.load_quadruples_from_file(filename)
    turing.load_values(values)
    turing.run_program(steps)

    while not turing.halt:
        print(turing)
        steps = input("Number of steps to complete (-1 for no step limit): ")
        turing.run_program(steps)
    print(turing)

