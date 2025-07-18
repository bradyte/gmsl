import csv
import re
import sys
import os
import logging
import webvtt
from textwrap import wrap

logger = logging.getLogger(__name__)

batch_dir = "batch_vtt_files"
webpage_dir = "webpage"
tests_dir = "tests"
sc_dir = "spellchecked"

logging.basicConfig(
    format="[%(asctime)s.%(msecs)03d] %(levelname)s\t- %(message)s",
    datefmt='%H:%M:%S',
    level=logging.INFO
                    )

class Sentence:
    def __init__(self):
        self.identifier = None
        self.lines = None
        self.sentence_string = None
        self.max_caption_length = None
        self.caption_span = None

    def get_max_caption_length(self):
        return len(max(self.lines, key=len))
    
    def lines_to_string(self):
        self.sentence_string = ' '.join(self.lines)


class GMSLSpellCheck:
    """
    The main spellcheck class to read in the file and create a cleaned
        VTT file based off of the caption_library.csv file.

    :param vtt_file: this is the main vtt_file intended for spellchecking
    :returns: creates a new spellchecked file under the same name with a
        spellcheck suffix
    :raises IndexError: when peeking lines at the end of file
    """

    def __init__(self, vtt_file, output_dir, mode) -> None:
        self.mode = mode
        self.vtt = webvtt.read(vtt_file)
        self.vtt_filename = os.path.basename(vtt_file).rsplit('.', 1)[0]  # grab the file name only, remove extension
        self.output_dir = output_dir
        self.custom_library_path = None

        # check if there is a custom library
        if os.path.exists(os.path.join(webpage_dir, 'custom_caption_library.csv')):
            self.custom_library_path = os.path.join(webpage_dir, 'custom_caption_library.csv')

        self.custom_gmsl_dictionary = None
        self.gmsl_dictionary = self._create_gmsl_dictionary('caption_library.csv')
        
        self.parse_sentences()
        self.create_vtt()

    def _create_gmsl_dictionary(self, csv_file):
        if self.mode == 'webpage' and self.custom_library_path is not None:
            with open(self.custom_library_path,'r') as inp:
                csvreader = csv.reader(inp)
                self.custom_gmsl_dictionary = {rows[0]:rows[1] for rows in csvreader}
            
        with open(csv_file,'r') as inp:
                csvreader = csv.reader(inp)
                return {rows[0]:rows[1] for rows in csvreader}

    def parse_sentences(self):
        caption_index = 0
        while caption_index < len(self.vtt.captions):
            sentence = Sentence()
            sentence.lines = self.vtt.captions[caption_index].lines[:]
            sentence.identifier = self.vtt.captions[caption_index].identifier
            sentence.caption_span = int(self.vtt.captions[caption_index].identifier[-1:])
            try:  # handle peeking the end of the file
                # while the next cue id indicates there is more sentence
                while (int(self.vtt.captions[caption_index+1].identifier[-1:]) != 0):
                    caption_index += 1  # update the caption index to next block of text
                    sentence.lines.extend(self.vtt.captions[caption_index].lines[:])
                    sentence.caption_span = int(self.vtt.captions[caption_index].identifier[-1:])
            except IndexError as e:  # end of file
                logger.info(f'"{self.vtt_filename}.vtt" spellcheck complete!\n')
                logger.debug(f'[unzip_sentences] {e}: end of file')
            sentence.lines_to_string()
            self.spellcheck(sentence)
            self.update_vtt(sentence, caption_index)
            caption_index += 1  # update the chunk index to next block of text

    def spellcheck(self, sentence):
        if self.mode == 'webpage' and self.custom_gmsl_dictionary is not None:
            self._search_sentence(sentence, self.custom_gmsl_dictionary)
        self._search_sentence(sentence, self.gmsl_dictionary)

    def _search_sentence(self, sentence, dictionary):
        for key in list(dictionary.keys()):
            # compare the exact spelling of the incorrect word to the sentence 
            if re.search(r'\b' + re.escape(key) + r'\b', sentence.sentence_string):
                logger.info(f"[{sentence.identifier[:8]}]: Replacing {key} => {dictionary[key]}")
                # replace the incorrect word with the dictionary word
                sentence.sentence_string = re.sub(r'\b' + re.escape(key) + r'\b', dictionary[key], sentence.sentence_string)

    def update_vtt(self, sentence, caption_index):
        max_caption_length = int(sentence.get_max_caption_length() * 1.25)  # 25% buffer is arbitrary
        sentence_list = wrap(sentence.sentence_string , width=max_caption_length)
        # keep shortening the caption until it fits the the existing caption span
        while not (len(sentence_list) >= (2 * (sentence.caption_span + 1) - 1)):
            max_caption_length -= 1
            sentence_list = wrap(sentence.sentence_string, width=max_caption_length)

        current_caption_index = caption_index - sentence.caption_span 
        while (sentence_list):
            self.vtt.captions[current_caption_index].lines = [sentence_list.pop(0)]
            if sentence_list:
                self.vtt.captions[current_caption_index].lines.extend([sentence_list.pop(0)])
            current_caption_index += 1  # ensure a maximum of two lines per caption

    def create_vtt(self):
        self.vtt.save(os.path.join(self.output_dir, f'{self.vtt_filename}_spellchecked.vtt'))

def main():
    '''
    All VTT files should be located in the vtt_files folder for batch editting.
    The processed files will end up in the spellchecked folder for batch editting.
    '''
    try:
        # mode = sys.argv[1]
        mode = 'test'

        if mode == 'batch':
            vtt_dir = batch_dir
        elif mode == 'webpage':
            vtt_dir = webpage_dir
        elif mode == 'test':
            vtt_dir = tests_dir
        else:
            print(f'You entered "{mode}". Please enter a valid mode option: "batch" or "webpage"')

        if not os.path.exists(vtt_dir):  # if it can find the vtt folder
            logger.warning("Cannot find batch folder. Exiting program...")
            sys.exit(0)

        if not os.path.exists(os.path.join(vtt_dir, sc_dir)):  # if you don't have a output folder
            os.makedirs(os.path.join(vtt_dir, sc_dir))

        for file in os.listdir(vtt_dir):
            if file.endswith('.vtt'):
                input_file_path = os.path.join(vtt_dir, file)
                GMSLSpellCheck(input_file_path, os.path.join(vtt_dir, sc_dir), mode) 

    except IndexError as e:
        print(f'Please enter a valid mode option: "batch" or "webpage"')

if __name__ == "__main__":
    main()