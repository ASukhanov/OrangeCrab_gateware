""" Access to IO pins of the OrangeCrab board
"""
__version__ = 'v0.0.1 2022-11-26'# io.o5 frequency is 24 MHz
gateware = 'blink_io'

from amaranth import Elaboratable, Module, Signal
from amaranth.sim import Simulator, Delay, Settle
import local_amaranth_boards.orangecrab_r0_2 as orangecrab
#TODO: use official amaranth_boards module and update its .resources

class Blink(Elaboratable):
    def __init__(self):
        self.count = Signal(32, reset=0)
        #self.count_rst = Signal()# reset not used.
        self.platform = orangecrab.OrangeCrabR0_2Platform()
        print(f'platform.resources: {self.platform.resources.keys()}')

    def elaborate(self, platform):
        m = Module()
        if not pargs.gen:# by some reason the platform gets None in simulation mode
            platform = self.platform

        rgb = platform.request('rgb_led', 0)
        red_led = rgb.r
        green_led = rgb.g
        blue_led = rgb.b

        self.pad_button = platform.request('button', 0)
        self.pad_program = platform.request('program', 0)
        io = platform.request('io', 0)

        m.d.sync += self.count.eq(self.count + 1)
        blink_rate = 24 if pargs.gen else 0
        m.d.comb += [
            red_led.o.eq(self.count[blink_rate+3]),
            green_led.o.eq(self.count[blink_rate+2]),
            blue_led.o.eq(self.count[blink_rate+1]),
            io.o5.eq(self.count[0]),
            io.o6.eq(self.count[1]),
        ]
        '''
        with m.If(self.count_rst == 1):
            m.d.sync += self.count.eq( 0 )
        '''
        with m.If(self.pad_button.i == 1):
            m.d.sync += self.pad_program.o.eq(1)
        return m

if __name__ == "__main__":
    import sys, argparse
    global pargs
    parser = argparse.ArgumentParser(description=__doc__,
      epilog=f'{gateware}: {__version__}')
    parser.add_argument('-g', '--gen', action='store_true',
      help='Generate gateware, simulate otherwise')
    pargs = parser.parse_args()

    if pargs.gen:
        platform = orangecrab.OrangeCrabR0_2Platform()
        platform.build(Blink(), do_program=True)
    else:
        # Simulation
        m = Module()
        m.submodules.blink = blink = Blink()
        sim = Simulator(m)
        sim.add_clock(1./48e6)
        
        def process():
            for i in range( 20 ):
                yield
            yield blink.pad_button.i.eq(1)# raise pad button on count = 15
            yield
            yield blink.pad_button.i.eq(0)# drop pad button on count = 16
            for i in range( 44 ):
                yield 

        sim.add_sync_process(process)
        with sim.write_vcd(f'{gateware}.vcd', f'{gateware}.gtkw'):
            sim.run()
