from migen import *


class TestPattern(Module):
    def __init__(self, vga):
        self.counter = Signal(12)

        self.sync.vga += [
            If(
                vga.hsync == 0,
                self.counter.eq(0),
            ).Else(
                self.counter.eq(self.counter + 1),
            ),
        ]

        self.comb += [
            vga.red.eq(self.counter[4:7]),
            vga.green.eq(self.counter[4:7]),
            vga.blue.eq(self.counter[4:7]),
        ]
