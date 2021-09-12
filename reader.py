from typing import cast
import sys
import io

file_name = ""
if len(sys.argv) > 1:
    file_name = sys.argv[1]

if len(file_name) == 0:
    file_name = "../res/video/dancer.ivf"
print("unpacket file name=", file_name)


class Packet:
    def __init__(self, content: bytes, pts: int) -> None:
        self.content = content
        self.pts = pts


class IVFHeader:
    def __init__(self, signature: str, version: int, header_len: int,
                 fourcc: str, width: int, height: int,
                 time_base_denominator: int, frame_num: int,
                 unused: int) -> None:
        self.signature = signature
        self.version = version
        self.header_len = header_len
        self.fourcc = fourcc
        self.time_base_denominator = time_base_denominator
        self.width = width
        self.height = height
        self.frame_num = frame_num
        self.unused = unused

    def __str__(self) -> str:
        return "signature=" + self.signature + ", version=" + str(
            self.version) + ", header_len=" + str(
                self.header_len
            ) + ", codec_fourcc=" + self.fourcc + ", width=" + str(
                self.width) + ", height=" + str(
                    self.height) + ", time_base_denomiator=" + str(
                        self.time_base_denominator) + ", frames=" + str(
                            self.frame_num)


def read_header(f: io.FileIO) -> IVFHeader:
    signature = f.read(4).decode()
    version = int.from_bytes(f.read(2), byteorder="little")
    header_len = int.from_bytes(f.read(2), byteorder="little")
    codec_fourcc = f.read(4).decode()
    width = int.from_bytes(f.read(2), byteorder="little")
    height = int.from_bytes(f.read(2), byteorder="little")

    time_base_denominator = int.from_bytes(f.read(8), byteorder="little")
    frame_num = int.from_bytes(f.read(4), byteorder="little")
    unused = int.from_bytes(f.read(4), byteorder='little')
    return IVFHeader(signature,
                     version,
                     header_len,
                     codec_fourcc,
                     width,
                     height,
                     time_base_denominator,
                     frame_num,
                     unused=unused)


def read_next_frame(f: io.FileIO) -> Packet:
    frame_size = int.from_bytes(f.read(4), byteorder='little')
    if frame_size == 0:
        raise Exception("end of file")

    pts = int.from_bytes(f.read(8), byteorder='little')
    frame_content: bytes = f.read(frame_size)

    return Packet(frame_content, pts)


if __name__ == "__main__":
    with open(file_name, 'rb') as f:
        header = read_header(f)
        print("header content[", header, "]")

        frame_list = []
        while True:
            try:
                frame_list.append(read_next_frame(f))
            except Exception as e:
                print('meet error cause=', e)
                break

        print("frame list size=", len(frame_list))
