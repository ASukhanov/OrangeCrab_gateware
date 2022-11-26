""" Blink the three LEDs in a counting pattern.
Reset the OrangeCrab on button press.
It is amaranth implementation of a verilog project blink_reset at:
https://github.com/orangecrab-fpga/orangecrab-examples/tree/main/verilog
"""
__version__ = 'v0.0.1 2022-11-26'#

from amaranth import Elaboratable, Module, Signal
from amaranth.sim import Simulator, Delay, Settle
import amaranth_boards.orangecrab_r0_2 as amaranth_boards

class Blink(Elaboratable):
    def __init__(self):
        self.count = Signal(5, reset=0)
        self.count_rst = Signal()
        #self.usr_btn = 
        self.platform = amaranth_boards.OrangeCrabR0_2Platform()

    def elaborate(self, platform_):
        m = Module()
        platform = self.platform

        rgb = platform.request('rgb_led', 0)
        red_led = rgb.r
        green_led = rgb.g
        blue_led = rgb.b

        self.pad_button = platform.request('button', 0)
        pad_program = platform.request('program', 0)

        m.d.sync += self.count.eq(self.count + 1)
        #m.d.comb += self.count_rst.eq(self.count == 30)# counts till 1E
        m.d.sync += self.count_rst.eq(self.count == 30)# counts till 1F
        m.d.comb += [
            red_led.o.eq(self.count[3]),
            green_led.o.eq(self.count[2]),
            blue_led.o.eq(self.count[1]),
        ]
        #with m.If(self.count == 30):
        with m.If(self.count_rst == 1):
            m.d.sync += self.count.eq( 0 )
            #m.d.comb += pad_program.o.eq( 1 )
        #DNW#m.d.sync += m.d.sync.rst.eq(self.count[4])
        with m.If(self.pad_button.i == 1):
            m.d.comb += red_led.o.eq(1)
        return m

    '''DNW
    def ports(self):
        _ports = self.count
        print(f'ports: {_ports}')
        return (_ports)
    '''

if __name__ == "__main__":
    import sys, argparse
    parser = argparse.ArgumentParser(description=__doc__,
      epilog=f'blink_reset: {__version__}')
    parser.add_argument('-g', '--gen', action='store_true',
      help='Generate gateware, simulate otherwise')
    pargs = parser.parse_args()

    #m = Blink()# that is OK for single-module design
    m = Module()
    m.submodules.blink = blink = Blink()

    if pargs.gen:
        print('Gateware generation is not yet supported.')
        #platform = amaranth_boards.OrangeCrabR0_2Platform()
        #platform.build(Blink(), do_program=True)
        sys.exit()

    # Simulation
    sim = Simulator(m)
    sim.add_clock(1./48e6)
    
    def process():
        for i in range( 30 ):
            yield
        for i in range( 30 ):
            #DNW#blink.pad_button.i = 1
            yield

    sim.add_sync_process(process)
    with sim.write_vcd("test.vcd", "test.gtkw"):#, traces=m.ports()):
        sim.run()
        #sim.run_until(100e-6, run_passive=True)

