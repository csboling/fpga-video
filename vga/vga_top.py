from litex.soc.cores.clock import iCE40PLL
from migen import *
from migen.build.generic_platform import Pins, Subsignal
from migen.build.platforms import icebreaker

from vga_timing import VgaTiming
from testpattern import TestPattern


vga_pmod = [
    (
        'vga', 0,
        Subsignal('hsync', Pins('PMOD1B:4')),
        Subsignal('vsync', Pins('PMOD1B:5')),
        Subsignal('red',   Pins(' '.join('PMOD1A:{}'.format(x) for x in range(0, 4)))),
        Subsignal('green', Pins(' '.join(f'PMOD1B:{x}' for x in range(0, 4)))),
        Subsignal('blue',  Pins(' '.join(f'PMOD1A:{x}' for x in range(4, 8)))),
    ),
]

class VgaTest(Module):

    def __init__(self, vga, clk12):
        self.clock_domains.sys = ClockDomain()
        self.comb += self.sys.clk.eq(clk12)

        self.clock_domains.vga = ClockDomain()
        self.vga_clk_pll = iCE40PLL(primitive='SB_PLL40_PAD')
        self.submodules.vga_clk_pll = self.vga_clk_pll
        self.vga_clk_pll.register_clkin(self.sys.clk, 12e6)
        self.vga_clk_pll.create_clkout(self.vga, 25.175e6)

        self.vga_timing = VgaTiming()
        self.submodules.vga_timing = self.vga_timing

        self.submodules.test_pattern = TestPattern(vga)
        
        self.comb += [
            vga.hsync.eq(self.vga_timing.hsync),
            vga.vsync.eq(self.vga_timing.vsync),
        ]


if __name__ == '__main__':
    plat = icebreaker.Platform()
    plat.add_extension(vga_pmod)
    vga = plat.request('vga')
    clk12 = plat.request('clk12')
    plat.build(VgaTest(vga, clk12))
    plat.create_programmer().flash(0, 'build/top.bin')
