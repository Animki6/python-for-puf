import os
import sys
import time
import datetime
import serial


#results_dir = 'results_simple_NEW'
results_dir = 'results_butterfly_NEW'
results_filename = 'test_output.csv'
all_pairs = False
i_max = 128

if '--help' in sys.argv:
    print('Arguments: port, num_of_iter, output_file_name')
    sys.exit(0)

if len(sys.argv) < 2:
    print('Please specify USB port to use, e.g. "/dev/ttyUSB0" as an input argument!')
    sys.exit(1)

if len(sys.argv) > 2:
    num_of_iter = int(sys.argv[2])
else:
    num_of_iter = 1

if len(sys.argv) > 3:
    results_filename = sys.argv[3]+'.csv'

results_filepath = os.path.join(results_dir, results_filename)

try:
	ser = serial.Serial(
		port=sys.argv[1],
		baudrate=115200,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS
	)
except:
    print('Oops... Port {} could not be opened!'.format(sys.argv[1]))
    print('Check port name and your permissons.')
    sys.exit(1)



ser.isOpen()



print('Starting getting board characterization. This may take a while.')
for i_num in range(num_of_iter):
    header = []
    #output = []
    output = bytearray()
    print('Iteration number: {}'.format(i_num+1))
    start = time.time()
    
    challenge_counter = 0

    for i in range(i_max):
 
        ser.write(bytes([i]))

        header.append('{}'.format(i+1))
        challenge_counter += 1
        if challenge_counter % 8 == 0:
            puf_out = ser.read(1)
            output += puf_out
            #output.append(0 if puf_out == bytes([0x00]) else 1)

        progress = (i / i_max) * 100
        sys.stdout.write(" Progress: {:10.2f}% \r".format(progress, ) )
        #sys.stdout.flush()

    end = time.time()

    print('Total time: {}'.format(datetime.timedelta(seconds=end-start)))

    if not os.path.exists(results_dir):
        os.mkdir(results_dir)

    if not os.path.exists(results_filepath):
        with open(results_filepath, 'a') as file:
            file.write(','.join(header))
            file.write('\n')

    with open(results_filepath, 'a') as file:
        #file.write(','.join(map(str,output)))
        bits_str = ''.join(format(byte, '08b') for byte in output)
        bits_separated = ','.join(bits_str)
        file.write(bits_separated)
        file.write('\n')

    print('Output saved succesfully!')

print('Done. Thank you!')



  

