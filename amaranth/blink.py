"""Simplest gateware, adopted from official repo: 
https://github.com/orangecrab-fpga/orangecrab-examples/tree/main/nmigen
Blink the three LEDs in a counting pattern.
"""
from amaranth import *
from amaranth_boards.orangecrab_r0_2 import *


class Blink(Elaboratable):
    def __init__(self):
        self.count = Signal(32, reset=0)

    def elaborate(self, platform):
        m = Module()

        m.d.sync += self.count.eq(self.count + 1)
        rgb = platform.request('rgb_led', 0)
        red_led = rgb.r
        green_led = rgb.g
        blue_led = rgb.b

        blink_rate = 24
        m.d.comb += [
            red_led.o.eq(self.count[blink_rate+3]),
            green_led.o.eq(self.count[blink_rate+2]),
            blue_led.o.eq(self.count[blink_rate+1]),
        ]

        return m


if __name__ == "__main__":
    platform = OrangeCrabR0_2Platform()
    platform.build(Blink(), do_program=True)
