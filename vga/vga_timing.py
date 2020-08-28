from functools import reduce

from migen import *


class VgaTiming(Module):
    H_SYNC = 96
    H_FRONT_PORCH = 16
    H_BACK_PORCH = 48

    V_SYNC = 2
    V_FRONT_PORCH = 10
    V_BACK_PORCH = 33
    
    def __init__(self, width: int = 640, height: int = 480):
        self.width = width
        self.height = height

        self.hsync = Signal()
        self.vsync = Signal()
        self.active = Signal()

        self.h_overscan = self.H_SYNC + self.H_BACK_PORCH + self.H_FRONT_PORCH
        self.v_overscan = self.V_SYNC + self.V_BACK_PORCH + self.V_FRONT_PORCH
        self.scan_counter = Signal(max=self.width + self.h_overscan)
        self.line_counter = Signal(max=self.height + self.v_overscan)

        self.sync.vga += [
            If(
                self.scan_counter == self.width + self.h_overscan - 1,
                [
                    self.scan_counter.eq(0),
                    If(
                        self.line_counter == self.height + self.v_overscan - 1,
                        self.line_counter.eq(0),
                    ).Else(
                        self.line_counter.eq(self.line_counter + 1),
                    ),
                ],
            ).Else(
                self.scan_counter.eq(self.scan_counter + 1),
            ),
        ]

        self.comb += [
            self.active.eq(reduce(
                lambda x, y: x & y,
                [
                    self.line_counter >= self.V_SYNC + self.V_BACK_PORCH,
                    self.line_counter < self.V_SYNC + self.V_BACK_PORCH + self.height,
                    self.scan_counter >= self.H_SYNC + self.H_BACK_PORCH,
                    self.scan_counter < self.H_SYNC + self.H_BACK_PORCH + self.width,
                ]
            )),
            self.hsync.eq(~(self.scan_counter < self.H_SYNC)),
            self.vsync.eq(~(self.line_counter < self.V_SYNC)),
        ]
