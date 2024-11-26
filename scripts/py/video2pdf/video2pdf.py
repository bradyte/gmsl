import cv2
import os
import re
import img2pdf

# 8e65d397-7e86-4ce1-b7b8-de39150f1957-0
# 00:00:09.080 --> 00:00:12.939
# Today we will discuss the
# benefits and functionality of

class VIDEO2PDF:
    VTT_ITEMS = 4
    CUE_ID, TS_START, TEXT1, TEXT2 = range(VTT_ITEMS)

    def __init__(self, video_file, vtt_file) -> None:
        self.video = cv2.VideoCapture(video_file)
        self.course_name = video_file.rsplit('.', 1)[0]
        self.vtt_file = vtt_file
        self.processed_vtt = []
        self.total_frames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.script_file = None
        self.output_pdf_file = None
        self.frames_folder = None
        self._folder_check()
        self.process_vtt()

    def _folder_check(self):
        output_folder = 'output'
        frames_folder = 'frames'

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if not os.path.exists(frames_folder):
            os.makedirs(frames_folder)

        self.output_pdf_file = os.path.join(output_folder, f'{self.course_name}.pdf')
        self.script_file = os.path.join(output_folder, f'{self.course_name}_script.txt')
        self.frames_folder = frames_folder

    def process_vtt(self):
        with open(self.vtt_file, 'r') as inp:  # read in the VTT file
            with open(self.script_file, 'w') as outp:  # create a script file
                lines = inp.readlines()
                for idx, line in enumerate(lines):  # grab line number and line string  
                    buf = []               
                    if line == '\n':  # end of previous text block
                        idx += 1  # move idx to line beneath '\n'
                        buf.append(lines[idx + self.CUE_ID].strip())
                        timestamp_string = lines[idx + self.TS_START].strip()  # remove \n
                        timestamps = timestamp_string.split(' --> ')  # split by the arrow
                        buf.append(timestamps[0])  # grab the first timestamp of the scene

                        try:
                            i = 0
                            while(lines[idx + self.TEXT1 + i] != '\n'): # keep going until you hit the next \n
                                buf.append(lines[idx + self.TEXT1 + i].strip())  # remove \n
                                i += 1  # continue to see if the next line has text
                        except IndexError:  # if there is not a second line of text
                            pass  

                        if len(buf) == self.VTT_ITEMS:
                            buf[self.TEXT1] = ' '.join(buf[self.TEXT1:])  # join the two strings of text
                            buf.pop()  # remove the redundant line of text after joining
                        self.processed_vtt.append(buf)
                        outp.write(f'{buf[self.TS_START][3:8]}\t{buf[self.TEXT1]}\n')  # write to the script file
        print(f'{self.vtt_file} processed.')
        print(f'{self.script_file} generated.')

    def grab_frame(self, frame_index, frame_name=None):
        frame_number = self._process_timestamp(self.processed_vtt[frame_index][1])
        self.video.set(1, frame_number)
        success, frame = self.video.read()
        if frame_name == None:
            cv2.imwrite(f'frame.jpeg', frame)
            self.add_subtitle('frame.jpeg', frame_index)
        else:
            frame_path = os.path.join(self.frames_folder, f'{frame_name}.jpeg')
            cv2.imwrite(frame_path, frame)
            self.add_subtitle(frame_path, frame_index)

    def add_subtitle(self, frame, frame_index):
            image = cv2.imread(frame)
            bordered_image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(0, 0, 0))
            bordered_image = cv2.copyMakeBorder(bordered_image, 0, 120, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
            height, width, _ = bordered_image.shape
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.5
            color = (0, 0, 0)  # Blue color in BGR
            thickness = 2

            text = self.processed_vtt[frame_index][self.TEXT1]
            position = (int(width * 0.02), int(height * 0.96))
            cv2.putText(bordered_image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)
            position = (int(width * 0.95), int(height * 0.96))
            cv2.putText(bordered_image, str(frame_index), position, font, font_scale, color, thickness, cv2.LINE_AA)
            cv2.imwrite(frame, bordered_image)

    def grab_frames(self, frame_name='frame'):
        for i in range(len(self.processed_vtt)):
            self.grab_frame(i, f'{frame_name}_{i}')

    def video_close(self):
        self.video.release()
        cv2.destroyAllWindows

    def create_pdf(self, clean_frames_folder=False):
        print('Creating jpegs from frames...')
        self.grab_frames()
        with open(self.output_pdf_file, 'wb') as f:
            frame_jpegs = [f"{self.frames_folder}/{x}" for x in os.listdir(f'{self.frames_folder}') if x.endswith('.jpeg')]
            frame_jpegs.sort(key=lambda x: int(re.sub(fr'{self.frames_folder}/frame_(\d+)\.jpeg', r'\1', x)))  # TODO check file path
            print(f'Converting jpegs to {self.output_pdf_file}')
            f.write(img2pdf.convert(frame_jpegs))
            if clean_frames_folder:
                for frame_jpeg in frame_jpegs:
                    os.remove(frame_jpeg)


    def _process_timestamp(self, timestamp):  
        ts_list = timestamp.split(':')  # assumes VTT format 'HH:MM:SS.MSEC'
        ts_list_floats = [float(i) for i in ts_list]  # convert to floating point numbers
        hours, minutes, seconds = ts_list_floats
        frame_number = round(self.fps * (hours * 3600 + minutes * 60 + seconds))
        return frame_number

def main():
    video_file = 'GMSL200D - GPIO rev a.mp4'
    vtt_file = 'GMSL200D - GPIO rev a-en-US.vtt'
    v2p = VIDEO2PDF(video_file, vtt_file)
    # v2p.grab_frame(frame_index=50)
    v2p.create_pdf(clean_frames_folder=True)
    v2p.video_close()

if __name__ == "__main__":
    main()
