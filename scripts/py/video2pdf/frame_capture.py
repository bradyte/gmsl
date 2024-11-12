import cv2
import os
import img2pdf

class VIDEO2PDF:
    def __init__(self, video_file, timestamp_file) -> None:
        self.video = cv2.VideoCapture(video_file)
        self.timestamp_file = timestamp_file
        self.total_frames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)

    def _get_frame_number(self, hours, minutes, seconds):
        return self.fps * (hours * 3600 + minutes * 60 + seconds)
    
    def _process_timestamp(self, timestamp):  # assumes format 'HH:MM:SS.MSEC'
        ts_list = timestamp.split(':')
        ts_list_floats = [float(i) for i in ts_list]
        hours, minutes, seconds = ts_list_floats
        return self._get_frame_number(hours, minutes, seconds)

    def grab_frame(self, timestamp, frame_name=None):
        self.video.set(1, self._process_timestamp(timestamp))
        success, frame = self.video.read()
        if frame_name == None:
            cv2.imwrite(f'frame.jpeg', frame)
        else:
            cv2.imwrite(f'{frame_name}.jpeg', frame)

    def grab_frames(self, frame_name=None):
        frame_count = 0
        with open(self.timestamp_file, 'r') as file:
            for line in file:
                timestamp = line.rstrip()
                self.grab_frame(timestamp, f'frame_{frame_count}')
                frame_count += 1

    def video_close(self):
        self.video.release()
        cv2.destroyAllWindows

    def create_pdf(self):
        frames_file_loc = './'
        image_files = [i for i in os.listdir(frames_file_loc) if i.endswith(".jpeg")]
        print(image_files)
        pdf_data = img2pdf.convert(image_files)
        with open("output.pdf", "wb") as file:
            file.write(pdf_data)


    




def main():
    video_file = 'SampleVideo_1280x720_1mb.mp4'
    timestamp_file = 'timestamps.txt'
    v2p = VIDEO2PDF(video_file, timestamp_file)
    v2p.grab_frames()
    v2p.create_pdf()
    v2p.video_close()

if __name__ == "__main__":
    main()
