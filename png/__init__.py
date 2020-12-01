from zlib import compress, crc32

# Standard PNG 'magic number', for the start of each file
SIGNATURE = b'\x89PNG\r\n\x1A\n'

# Header (IHDR) defaults: 8bit; RGB; zlib; no-filter; no-interlace.
IHDR_DEFAULTS = bytearray([8, 2, 0, 0, 0])


def write(frame, path):
    '''Write a 2D array of 8-bit RGB tuples to a PNG file.'''
    data = encode(frame)
    with open(path, 'wb') as f:
        f.write(data)


def encode(frame):
    '''Encode a 2D array of 8-bit RGB tuples.'''
    height = len(frame)
    width = len(frame[0])
    return _wrap(
        _chunk(b'IHDR',
               _word(width) + _word(height) + IHDR_DEFAULTS) +
        _chunk(b'IDAT', _image_data(frame)))


def _wrap(chunks):
    return SIGNATURE + bytes(chunks) + _chunk(b'IEND')


def _image_data(frame):
    pixels = bytearray()
    for row in frame:
        pixels.append(0)  # "prepend each scanline with the filter" ...!? ok
        for pixel in row:
            pixel = pixel or (0, 0, 0)
            pixels.extend(pixel)
    return compress(pixels)


def _chunk(chunk_type, chunk_data=b''):
    length = len(chunk_data)
    checksum = crc32(chunk_type + chunk_data)
    return _word(length) + chunk_type + chunk_data + _word(checksum)


def _short(number):
    return number.to_bytes(2, byteorder='big')


def _word(number):
    return number.to_bytes(4, byteorder='big')
