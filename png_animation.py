from png import _chunk, _word, IHDR_DEFAULTS, _image_data, _short, _wrap


def write_animation(frames, path, framerate_fps=25):
    '''Write a list of frames (2D arrays of 8-bit RGB tuples) to a file.'''
    data = encode_animation(frames, framerate_fps)
    with open(path, 'wb') as f:
        f.write(data)


def encode_animation(frames, framerate_fps=25):
    '''Encode a list of frames as an animation.
    See https://wiki.mozilla.org/APNG_Specification
    '''
    height = len(frames[0])  # number of rows in frame0
    width = len(frames[0][0])  # number or items in row0 in frame0
    buf = bytearray()
    buf += _chunk(b'IHDR', _word(width) + _word(height) + IHDR_DEFAULTS)
    buf += _chunk(b'acTL', _word(len(frames)) + _word(0))
    buf += _chunk(b'IDAT', _image_data(frames[0]))
    for i, frame in enumerate(frames):
        seq0 = (2 * i) + 0
        seq1 = (2 * i) + 1
        fctl = _word(width) + _word(height) + _fctl_defaults(framerate_fps)
        buf += _chunk(b'fcTL', _word(seq0) + fctl)
        buf += _chunk(b'fdAT', _word(seq1) + _image_data(frame))
    return _wrap(buf)


# Animation: frame control (fcTL) defaults
def _fctl_defaults(framerate_fps=25):
    return bytearray([
        *_word(0),  # x offset
        *_word(0),  # y offset
        *_short(1),  # delay numerator
        *_short(framerate_fps),  # delay denominator
        0,  # previous frame left in place
        0,  # do not blend with previous frame
    ])
