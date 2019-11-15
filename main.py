import mido
import psutil
outport = mido.open_output('Launchpad S:Launchpad S MIDI 1 20:0')

core_positions = [
    [70, 60, 50, 40],
    [71, 61, 51, 41],
    [72, 62, 52, 42],
    [73, 63, 53, 43],
    [74, 64, 54, 44],
    [75, 65, 55, 45],
    [76, 66, 56, 46],
    [77, 67, 57, 47]
]

def all_on():
    outport.send(mido.Message.from_hex('B0 00 7F'))
def all_off():
    outport.send(mido.Message.from_hex('B0 00 00'))
def enable_led(position, color):
    outport.send(mido.Message.from_hex('90 {} {}'.format(position, color)))
def print_cores():
    values = psutil.cpu_percent(interval=1, percpu=True)
    print(values)
    for i in range(7):
        # import pdb;pdb.set_trace()
        value = map_to_core(values[i])
        for j in range(value):
            print(i,j)
            enable_led(str(core_positions[i][j]), '0f')
        # core_positions[i]


    # outport.send(mido.Message.from_hex('90 00 0f'))
def map_to_core(value):
    if value < 25:
        return 0
    elif value >= 25 and value < 50:
        return 1
    elif value >= 50 and value < 75:
        return 2
    else:
        return 3

print_cores()