import os

vtt_dir = ".\\vtt_files"
scripts_dir = ".\\scripts"

def create_script(input_file, output_file):
    with open(input_file, 'r') as inp:
        with open(output_file, 'w') as outp:
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

if not os.path.exists(scripts_dir):  # if you don't have a output folder
    os.makedirs(scripts_dir)

if not os.path.exists(vtt_dir):  # if you don't have a output folder
    print("Cannot find *.vtt folder")

for file in os.listdir(vtt_dir):
    input_file_path = os.path.join(vtt_dir, file)
    output_file_path = os.path.join(scripts_dir, file.replace(".vtt", ".txt"))
    create_script(input_file_path, output_file_path)

