from migen import *

from vga_timing import VgaTiming
from testpattern import TestPattern


class Testbench(Module):
    def __init__(self, timing, pattern):
        self.submodules.timing = timing
        self.submodules.pattern = pattern

def test_vga():
    for _ in range(800 * 36):
        yield

if __name__ == '__main__':
    vga = Record([
        ('hsync', 1),
        ('vsync', 1),
        ('red', 4),
        ('green', 4),
        ('blue', 4),
    ])

    renamer = ClockDomainsRenamer({'vga': 'sys'})
    dut = Testbench(
        renamer(VgaTiming()),
        renamer(TestPattern(vga)),
    )
    run_simulation(
        dut,
        test_vga(),
        clocks={'sys': 40},
        vcd_name='vga_timings.vcd',
    )
