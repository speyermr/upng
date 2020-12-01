#from png_examples import examples
#examples()


import png

def pixel():
    return (0xeb, 0x15, 0xff)

frame = [
    [pixel(), pixel()],
    [pixel(), pixel()]
    ]
png.write(frame, 'lol.png')