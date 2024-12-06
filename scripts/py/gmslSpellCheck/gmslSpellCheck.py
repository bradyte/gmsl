import csv
import re
import logging
from textwrap import wrap

logger = logging.getLogger(__name__)

logging.basicConfig(
    format="[%(asctime)s.%(msecs)d] %(levelname)s\t- %(message)s",
    datefmt='%H:%M:%S',
    level=logging.INFO
                    )

class GMSLSpellCheck:
    MAX_VTT_ITEMS = 4
    CUE_ID, TIMESTAMP, TEXT1, TEXT2 = range(MAX_VTT_ITEMS)  # use the newline as 0 offset
    CAPTION_LENGTH = 32

    def __init__(self, vtt_file) -> None:
        self.vtt_file = vtt_file
        self.vtt_lines = None
        self.new_vtt_lines = ['WEBVTT\n', '\n']  # empty vtt file structure
        self.processed_vtt = []  # contains array of vtt chunks in list format
        self.vtt_num_chunks = 0
        self.vtt_sentences = []  # contains concatenated sentences
        self.gmsl_dictionary = self._create_gmsl_dictionary('caption_library.csv')
        self.parse_vtt()
        self.unzip_sentences()
        self.spellcheck()
        self.create_vtt()

    def _create_gmsl_dictionary(self, csv_file):
        with open(csv_file,'r') as inp:
            csvreader = csv.reader(inp)
            return {rows[0]:rows[1] for rows in csvreader}

    def parse_vtt(self):
        with open(self.vtt_file, 'r') as inp:  # read in the VTT file
            self.vtt_lines = inp.readlines()
            for vtt_line_index, line in enumerate(self.vtt_lines):  # grab line number and line string              
                if line == '\n':  # start of text block after \n
                    buf = []
                    idx = vtt_line_index + 1
                    buf.append(self.vtt_lines[idx + self.CUE_ID])  # grab the cue information
                    buf.append(self.vtt_lines[idx + self.TIMESTAMP])  # grab the timestamp
                    buf.append(self.vtt_lines[idx + self.TEXT1].strip())  # at minimum there will be one text line

                    try:  # handle peeking the next line of text
                        if self.vtt_lines[idx + self.TEXT2] != '\n':  # if there is a second line of text
                            buf.append(self.vtt_lines[idx + self.TEXT2].strip())  # append the second line of text
                        else:
                            buf.append('')  # else pad the second caption block
                    except IndexError:  # end of file
                        logger.debug('[parse_vtt]:IndexError: hit the end of the file')

                    self.processed_vtt.append(buf)
        self.vtt_num_chunks = len(self.processed_vtt)
        logger.info(f'{self.vtt_file} parsed.')

    def unzip_sentences(self):
        chunk_index = 0
        while chunk_index < self.vtt_num_chunks:
            sentence = ''
            if self.processed_vtt[chunk_index][self.TEXT2]:  # if there is a second line of text
                sentence = ' '.join((self.processed_vtt[chunk_index][self.TEXT1], self.processed_vtt[chunk_index][self.TEXT2]))   # create a sentence from these two lines
            else:  # if there is only one line of text, that's the full sentence
                sentence = self.processed_vtt[chunk_index][self.TEXT1]
            
            try:  # handle peeking the end of the file
                while(((self.processed_vtt[chunk_index+1][self.CUE_ID]).strip())[-1:] != '0'):  # while the cue id indicates there is more sentence
                    chunk_index += 1  # update the chunk index to next block of text
                    if self.processed_vtt[chunk_index][self.TEXT2]:  # if there is a second line of text
                        sentence = ' '.join((sentence, self.processed_vtt[chunk_index][self.TEXT1], self.processed_vtt[chunk_index][self.TEXT2]))
                    else:
                        sentence = ' '.join((sentence, self.processed_vtt[chunk_index][self.TEXT1]))
            except IndexError:  # end of file
                logger.debug('[unzip_sentences]:IndexError: list index out of range.')

            self.vtt_sentences.append([self.processed_vtt[chunk_index][self.CUE_ID], sentence])
            chunk_index += 1  # update the chunk index to next block of text


    def spellcheck(self):
        keys = list(self.gmsl_dictionary.keys())

        for idx, sentence in enumerate(self.vtt_sentences):
            for key in keys:
                if re.search(r"\b" + re.escape(key) + r"\b", sentence[1]):
                    logger.info(f'{sentence[0].strip()} Replacing {key} => {self.gmsl_dictionary[key]}')
                    self.vtt_sentences[idx][1] = re.sub(r"\b" + re.escape(key) + r"\b", self.gmsl_dictionary[key], self.vtt_sentences[idx][1])


    def create_vtt(self):
        self.zip_sentences()
        for chunk in self.processed_vtt:
            self.new_vtt_lines.extend((chunk[self.CUE_ID], chunk[self.TIMESTAMP], chunk[self.TEXT1], chunk[self.TEXT2]))
            if chunk[self.TEXT2] == '\n':
                pass
            else:
                self.new_vtt_lines.append('\n')

        with open('new_vtt.vtt', 'w') as outp:
            outp.writelines(self.new_vtt_lines)

    def zip_sentences(self):
        chunk_index = 0
        for sentence in self.vtt_sentences:
            max_text_span = (int((sentence[0].strip())[-1:]) + 1) * 2  # max number of text caption slots
            sentence_wrap = wrap(sentence[1], self.CAPTION_LENGTH)  # wrap the sentence into a list

            # check that you will span the same number text caption slots
            new_cap_length = self.CAPTION_LENGTH  # it can fit in the max number of slots or (max - 1)
            while not (len(sentence_wrap) == max_text_span or len(sentence_wrap) == (max_text_span - 1)):
                new_cap_length -= 1
                sentence_wrap = wrap(sentence[1], new_cap_length) 

            while sentence_wrap:
                self.processed_vtt[chunk_index][self.TEXT1] = ''.join([sentence_wrap.pop(0), '\n'])
                if sentence_wrap: # is there more text
                    self.processed_vtt[chunk_index][self.TEXT2] = ''.join([sentence_wrap.pop(0), '\n'])
                else:
                    self.processed_vtt[chunk_index][self.TEXT2] = '\n'
                chunk_index += 1

def main():
    vtt_file = 'GMSL200D - GPIO rev a-en-US.vtt'
    sc = GMSLSpellCheck(vtt_file)
    sc.spellcheck()

if __name__ == "__main__":
    main()