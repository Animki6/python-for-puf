import os
import sys
import time
import datetime
import serial




class TestParameters:
    results_dir = 'results_RO_new'
    results_filename = 'test_output.csv'
    all_pairs = False
    num_of_iter = None
    results_filepath = None


def parse_arguments(parameters):
    if len(sys.argv) < 2:
        print('Please specify USB port to use, e.g. "/dev/ttyUSB0" as an input argument!')
        sys.exit(1)

    if len(sys.argv) > 2:
        parameters.num_of_iter = int(sys.argv[2])
    else:
        parameters.num_of_iter = 1

    if len(sys.argv) > 3:
        parameters.results_filename = sys.argv[3] + '.csv'

    if len(sys.argv) > 4:
        parameters.all_pairs = True

    parameters.results_filepath = os.path.join(parameters.results_dir, parameters.results_filename)

def open_serial():

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

    print(ser.isOpen())
    return ser

def get_neightbours(max_number):
    pass


def main():

    params = TestParameters()

    parse_arguments(params)

    ser = open_serial()

    pair_counter = 0

    print('Starting getting board characterization. This may take a while.')
    for i_num in range(params.num_of_iter):
        header = []
        output = bytearray()
        print('Iteration number: {}'.format(i_num + 1))
        start = time.time()
        if params.all_pairs:
            i_max = 128
        else:
            i_max = 1
        for i in range(i_max):

            for j in range(128):
                pair_counter += 1
                ser.write(bytes([j+1]))
                ser.write(bytes([j]))
                time.sleep(0.005)

                header.append('{}x{}'.format(i + 1, j + 1))
                if pair_counter % 8 == 0:
                   puf_out = ser.read(1)
                   output += puf_out

                # output.append(0 if puf_out == bytes([0x00]) else 1)

            progress = (i / 128) * 100
            sys.stdout.write(" Progress: {:10.2f}% \r".format(progress, ))
            # sys.stdout.flush()

        # puf_out = ser.read(pair_counter//8)
        # output += puf_out
        pair_counter = 0

        end = time.time()

        print('Total time: {}'.format(datetime.timedelta(seconds=end - start)))

        if not os.path.exists(params.results_dir):
            os.mkdir(params.results_dir)

        if not os.path.exists(params.results_filepath):
            with open(params.results_filepath, 'a') as file:
                file.write(','.join(header))
                file.write('\n')

        with open(params.results_filepath, 'a') as file:
            bits_str = ''.join(format(byte, '08b') for byte in output)
            bits_separated = ','.join(bits_str)
            file.write(bits_separated)
            # file.write(','.join(map(str, output)))
            file.write('\n')

        print('Output saved succesfully!')

    print('Done. Thank you!')


  

if __name__ == '__main__':
    main()