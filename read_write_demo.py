# read packet by reader.py and write to output file by writer.py
import traceback
import sys
sys.path.append(".")
import writer
import reader

input_file = "dancer.ivf"
output_file = "output.ivf"
with open(output_file, 'wb') as output, open(input_file, 'rb') as input:
    input_header = reader.read_header(input)
    print("input header=", input_header)

    writer.write_header(output, input_header.width, input_header.height, input_header.fourcc)

    while True:
        try:
            packet: reader.Packet = reader.read_next_frame(input)
            writer.write_frame(output, packet.pts, packet=packet.content)
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print('err message=', e)
            break
