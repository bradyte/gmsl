import csv
import re
import sys
import os
import logging
from textwrap import wrap

logger = logging.getLogger(__name__)

vtt_dir = "vtt_files"
sc_dir = "spellchecked"

logging.basicConfig(
    format="[%(asctime)s.%(msecs)d] %(levelname)s\t- %(message)s",
    datefmt='%H:%M:%S',
    level=logging.INFO
                    )

class GMSLSpellCheck:
    """
    The main spellcheck class to read in the file and create a cleaned
        VTT file based off of the caption_library.csv file.

    :param vtt_file: this is the main vtt_file intended for spellchecking
    :returns: creates a new spellchecked file under the same name with a
        spellcheck suffix
    :raises IndexError: when peeking lines at the end of file
    """
    MAX_VTT_ITEMS = 4
    CUE_ID, TIMESTAMP, TEXT1, TEXT2 = range(MAX_VTT_ITEMS)  # use the newline as 0 offset
    CAPTION_LENGTH = 33

    def __init__(self, vtt_file) -> None:
        self.vtt_file = vtt_file
        self.vtt_file_name = os.path.basename(vtt_file).rsplit('.', 1)[0]  # grab the file name only, remove extension
        self.vtt_lines = None  # raw text lines of the VTT file
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
        with open(self.vtt_file, 'r', encoding='utf-8',errors='ignore') as inp:  # read in the VTT file
            self.vtt_lines = inp.readlines()
            for vtt_line_index, line in enumerate(self.vtt_lines):  # grab line number and line string   
                # start of text block after \n and check for consecutive \n           
                if line == '\n' and self.vtt_lines[vtt_line_index+1] != '\n':  
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
                        buf.append('')  # else pad the second caption block
                        logger.debug('[parse_vtt]:IndexError: hit the end of the file')

                    self.processed_vtt.append(buf)
        self.vtt_num_chunks = len(self.processed_vtt)
        logger.info(f'"{self.vtt_file_name}" parsed!')

    def unzip_sentences(self):
        chunk_index = 0
        while chunk_index < self.vtt_num_chunks:
            sentence = ''
            if self.processed_vtt[chunk_index][self.TEXT2]:  # if there is a second line of text
                sentence = ' '.join((self.processed_vtt[chunk_index][self.TEXT1], self.processed_vtt[chunk_index][self.TEXT2]))   # create a sentence from these two lines
            else:  # if there is only one line of text, that's the full sentence
                sentence = self.processed_vtt[chunk_index][self.TEXT1]
            
            try:  # handle peeking the end of the file
                # while the cue id indicates there is more sentence
                while(((self.processed_vtt[chunk_index+1][self.CUE_ID]).strip())[-1:] != '0'):
                    chunk_index += 1  # update the chunk index to next block of text
                    # if there is a second line of text
                    if self.processed_vtt[chunk_index][self.TEXT2]:  
                        sentence = ' '.join((sentence, self.processed_vtt[chunk_index][self.TEXT1], self.processed_vtt[chunk_index][self.TEXT2]))
                    else:
                        sentence = ' '.join((sentence, self.processed_vtt[chunk_index][self.TEXT1]))
            except IndexError:  # end of file
                logger.debug('[unzip_sentences]:IndexError: list index out of range.')

            self.vtt_sentences.append([self.processed_vtt[chunk_index][self.CUE_ID], sentence])
            chunk_index += 1  # update the chunk index to next block of text


    def spellcheck(self):
        logger.info(f'Spellchecking "{self.vtt_file_name}"...')
        for idx, sentence in enumerate(self.vtt_sentences):
            # grab all the incorrect words in the dicitionary
            for key in list(self.gmsl_dictionary.keys()):
                # compare the exact spelling of the incorrect word to the sentence
                if re.search(r"\b" + re.escape(key) + r"\b", sentence[1]):  
                    logger.info(f"[{sentence[0].split('-')[0]}]:Replacing {key} => {self.gmsl_dictionary[key]}")
                    # replace the incorrect word with the dictionary word
                    self.vtt_sentences[idx][1] = re.sub(r"\b" + re.escape(key) + r"\b", self.gmsl_dictionary[key], self.vtt_sentences[idx][1])
        logger.info(f'Spellcheck of "{self.vtt_file_name}" complete!\n'
                    '===============================================================================\n')


    def create_vtt(self):
        self.zip_sentences()
        for chunk in self.processed_vtt:
            self.new_vtt_lines.extend((chunk[self.CUE_ID], chunk[self.TIMESTAMP], chunk[self.TEXT1], chunk[self.TEXT2]))
            if chunk[self.TEXT2] == '\n':
                pass
            else:
                self.new_vtt_lines.append('\n')

        with open(os.path.join(sc_dir, f'{self.vtt_file_name}_spellcheck.vtt'), 'w') as outp:
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
    '''
    All VTT files should be located in the vtt_files folder.
    The processed files will end up in the spellchecked folder.
    '''
    if not os.path.exists(vtt_dir):  # if it can find the vtt folder
        logger.warning("Cannot find *.vtt folder. Exiting program...")
        sys.exit(0)

    if not os.path.exists(sc_dir):  # if you don't have a output folder
        os.makedirs(sc_dir)

    for file in os.listdir(vtt_dir):
        input_file_path = os.path.join(vtt_dir, file)
        GMSLSpellCheck(input_file_path) 

if __name__ == "__main__":
    main()