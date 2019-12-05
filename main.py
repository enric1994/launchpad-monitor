import mido
import psutil
import time
import subprocess
from gpuinfo import GPUInfo
outport = mido.open_output('Launchpad S:Launchpad S MIDI 1')

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

ram_positions = [0,1,2,3,4,5,6,7]

ssd_positions = [10,11,12,13,14,15,16,17]
hdd_positions = [20,21,22,23,24,25,26,27]
temp_positions = [78, 68, 58, 48, 38, 28, 18, 8]
gpu_positions = [30, 31, 32, 33, 34, 35, 36, 37]

def all_on():
    outport.send(mido.Message.from_hex('B0 00 7F'))
def all_off():
    outport.send(mido.Message.from_hex('B0 00 00'))
def enable_led(position, color):
    outport.send(mido.Message.from_hex('90 {} {}'.format(position, color)))
def print_cores():
    values = psutil.cpu_percent(interval=1, percpu=True)
    for i in range(8):
        value = map_to_core(values[i])
        for j in range(value):
            enable_led(str(core_positions[i][j]), '0f')

def print_ram():
    ram = dict(psutil.virtual_memory()._asdict())['used']/(1024*1024*1024)
    for position in ram_positions:
        if position*4 < ram:
            enable_led(str(position).zfill(2), '3C')

def print_disk():
    ssd, hdd = get_disk_space()
    for ssd_position in ssd_positions:
        if 10*(ssd_position-10) < ssd*0.75:
            enable_led(str(ssd_position).zfill(2), '3E')
    
    for hdd_position in hdd_positions:
        if 10*(hdd_position-20) < hdd*0.75:
            enable_led(str(hdd_position).zfill(2), '3F')

def print_temp():
    temp = int(psutil.sensors_temperatures()['coretemp'][0].current)
    if temp > 80:
        max_temp = temp - 80
    if temp > 88:
        max_temp = 7
    if temp <=80:
        max_temp = 0
    for i in range(max_temp):
        enable_led(str(temp_positions[i]).zfill(2), '3F')
    
def print_gpu():
    gpu = GPUInfo.gpu_usage()[0][0]
    for gpu_position in gpu_positions:
        if 10*(gpu_position-30) + 1 < gpu*0.75:
            enable_led(str(gpu_position).zfill(2), '3C')
        

def get_disk_space():
    diskinfo_raw = subprocess.Popen("df -h", shell=True,stdout=subprocess.PIPE)
    output = diskinfo_raw.communicate()[0]
    output_dict = dict((fields[5], fields[4]) for fields in [line.split() for line in output.strip().split("\n")][1:])
    ssd = output_dict['/'].rstrip('%')
    hdd = output_dict['/media/enric/enric_hdd'].rstrip('%')
    
    return int(ssd), int(hdd)

def map_to_core(value):
    if value < 25:
        return 0
    elif value >= 25 and value < 50:
        return 2
    elif value >= 50 and value < 75:
        return 3
    else:
        return 4

while True:
    print_cores()
    print_ram()
    print_temp()
    print_gpu()
    print_disk()
    time.sleep(3)
    all_off()
