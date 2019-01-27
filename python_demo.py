import os
import sys
import time
import datetime
import serial


results_dir = 'results'
results_filename = 'test_output.csv'


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
    print('Check port name and your permissons are correct.')
    sys.exit(1)



ser.isOpen()




print('Starting getting board characterization. This may take a while.')
for i_num in range(num_of_iter):
    header = []
    output = []
    print('Iteration number: {}'.format(i_num+1))
    start = time.time()
    for i in range(128):

        for j in range(i+1, 128):
 
            ser.write(bytes([i+1]))
            ser.write(bytes([(j+1)]))

            header.append('{}x{}'.format(i+1, j+1))
            puf_out = ser.read(1)
            output.append(0 if puf_out == bytes([0x00]) else 1)

        progress = (i / 128)* 100
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
        file.write(','.join(map(str,output)))
        file.write('\n')

    print('Output saved succesfully!')


  

