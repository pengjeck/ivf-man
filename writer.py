import io
import sys

# 参考：https://wiki.multimedia.cx/index.php?title=IVF
def write_header(f:io.FileIO, width: int, height: int, fourcc: str):
    # byte 0-3     signature: 'DKIF'
    f.write("DKIF".encode())
    # byte 4-5     version (should be 0)
    f.write(int(0).to_bytes(2, 'little'))
    # byte 6-7     length of header in bytes
    f.write(int(32).to_bytes(2, 'little'))
    # bytes 8-11   codec FourCC (e.g., 'VP80')
    f.write(fourcc.encode())
    # bytes 12-13  width in pixels
    f.write(width.to_bytes(2, 'little'))
    # bytes 14-15  height in pixels
    f.write(height.to_bytes(2, 'little'))
    # bytes 16-23  time base denominator
    # bytes 20-23  time base numerator
    f.write(int(4294968296).to_bytes(8, 'little'))
    # bytes 24-27  number of frames in file
    f.write(int(62866).to_bytes(4, 'little'))
    # bytes 28-31  unused
    f.write(int(0).to_bytes(4, 'little'))

def write_frame(f: io.FileIO, pts: int, packet: bytes):
    # bytes 0-3    size of frame in bytes (not including the 12-byte header)
    f.write(len(packet).to_bytes(4, 'little'))
    # bytes 4-11   64-bit presentation timestamp
    f.write(pts.to_bytes(8, 'little'))
    f.write(packet)

if __name__ == "__main__":
    file_name = "output.ivf"
    with open(file_name, 'wb') as f:
        write_header(f, 800, 800, "VP80")