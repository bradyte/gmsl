import csv

# modify the following 4 variables as needed
edid_file = 'lilliput_edid.bin' # can be called whatever
outfile = 'output.csv' # can be called whatever
dev_address = 0x80 # 8-bit address of the device you are trying to talk to
starting_index = 0x6500 # starting index of the EDID block for MAX96751

# do not modify below
try:
    with open(edid_file, mode='rb') as file: # read the file as bytes
        with open(outfile, 'w', newline='') as csvfile: # create and output CSV file
            writer = csv.writer(csvfile)
            while(byte := file.read(1)): # keeps reading the file until no more bytes
                data = [f'0x{dev_address:x}', f'0x{starting_index:x}', f'0x{byte.hex()}'] # GMSL script format
                writer.writerow(data)
                starting_index += 1 # increment the EDID index
except FileNotFoundError as e:
    print(f'\n{e.args[1]}!\nEnsure {edid_file} is located in the same directory as this script.\n')
