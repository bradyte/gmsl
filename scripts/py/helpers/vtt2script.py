file = 'GMSL250A v1.2-en-US.vtt'

with open(file, 'r') as inp:
    with open('script.txt', 'w') as outp:
        lines = inp.readlines()

        buf = []

        for idx, line in enumerate(lines):
            if line == '\n':
                i = 2
                try:
                    while(lines[idx+i] != '\n'): # keep going until you hit the next \n
                        buf.append(lines[idx + i])
                        i += 1

                    if len(buf) == 3:
                        buf[1] = buf[1].strip() + ' ' + buf[2]
                        
                    tt = buf[0].split(' ')[0] 
                    outp.write(f'{tt[3:8]}\t{buf[1]}')
                    buf.clear()
                except IndexError:
                    pass