# CIS-223 Final
# Motor control module
#
# Author : Colin Roskos
import pigpio


class Motor:

    def __init__(self, i1, i2, i3, i4):
        self.pi = pigpio.pi()
        self.prev_dir = 0
        self._step_order = [(1,0,0,0),
                            (1,1,0,0),
                            (0,1,0,0),
                            (0,1,1,0),
                            (0,0,1,0),
                            (0,0,1,1),
                            (0,0,0,1),
                            (1,0,0,1)]
        self.num_steps = len(self._step_order)
        self.pins = [i1, i2, i3, i4]
        self.cycles = 0 # number of pin cycles from on
        self.position = 0
        self.set_position(self.position)
        self.zero = [self.cycles, self.pins]
        self.backlash_cw = 0
        self.backlash_ccw = 0

    def set_zero(self):
        self.zero = [self.position, self.pins]

    def set_position(self, step):
        self.pi.write(self.pins[0], self._step_order[step][0])
        self.pi.write(self.pins[1], self._step_order[step][1])
        self.pi.write(self.pins[2], self._step_order[step][2])
        self.pi.write(self.pins[3], self._step_order[step][3])

    def change_position(self, steps, direction=0, _backlash_adj=True):
        if direction == 0:
            self.position += 1
            if self.prev_dir == 1 and _backlash_adj:
                self.prev_dir = 0
                self.change_position(direction, self.backlash_cw, False)
        else:
            self.position -= 1
            if self.prev_dir == 0 and _backlash_adj:
                self.prev_dir = 1
                self.change_position(direction, self.backlash_ccw, False)

        for i in range(steps):
            if self.position < 0:
                self.cycles += 1
            if self.position > len(self.step_order):
                self.cycles -= 1
            self.position %= self.num_steps
            self.set_position(self.position)

    def print_position(self):
        print(self.position)


def main():
    import time
    moto = Motor(2, 3, 4, 17)
    moto.print_position()
    for x in 100:
        moto.change_position(8*10)
        time.sleepms(1)

    moto.print_position()


if __name__ == "__main__":
    main()


