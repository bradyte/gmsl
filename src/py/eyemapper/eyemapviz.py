import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

raw_file = "GMSLEyeMapping_Forward.csv"

# ['0', '0', '0', '16048', '0']
# phase, vth, polarity, hits, min errors

MAXVOLTAGE = 64

eye_map = np.zeros((64, 64))

with open(raw_file, mode='r') as csvfile: # read the file 
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        phase = int(row[0])
        vth = int(row[1])
        polarity = int(row[2])
        hits = int(row[3])
        min_errors = int(row[4])

        x = phase // 2
        if polarity == 0:
            y = 31 - vth // 2
        else:
            y = 32 + vth // 2
        eye_map[y, x] = min_errors / hits
        # eye_map[y, x] = min_errors

pdf_eye_map = np.zeros((64, 64))

for i in range(64):
    ph = eye_map[:, i]
    temp = abs(np.diff(ph, append=0))
    pdf_eye_map[:, i] = temp

plt.imshow(pdf_eye_map, cmap='jet', origin='lower') 
plt.show() 