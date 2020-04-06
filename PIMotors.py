# CIS-223 Final
# Motor control module
#
# Author : Colin Roskos
import pigpio

class Motor:


    def __init__(self, i1, i2, i3, i4):
        self.pi = pigpio.pi()
        self._step_order = [(1, 0, 1, 0), (0, 1, 1, 0), (0, 1, 0, 1), (1, 0, 0, 1)]
        self.pins = [i1, i2, i3, i4]
        self.position = 0
        self.set_position(self.position)


    def set_position(self, step):
        self.pi.write(self.pins[0], self._step_order[step][0])
        self.pi.write(self.pins[1], self._step_order[step][1])
        self.pi.write(self.pins[2], self._step_order[step][2])
        self.pi.write(self.pins[3], self._step_order[step][3])

    def change_position(self, direction=0):
        if direction == 0:
            self.position += 1
        else:
            self.position -= 1

        self.position %= 4
        self.set_position(self.position)

    def print_position(self):
        print(self.position)

def main():
    moto = Motor(2, 3, 4, 17)
    moto.print_position()

    moto.change_position()
    moto.print_position()

if __name__=="__main__":
    main()


