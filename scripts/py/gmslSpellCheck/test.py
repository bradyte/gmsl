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
sc_dir = "spellchecked"

logging.basicConfig(
    format="[%(asctime)s.%(msecs)03d] %(levelname)s\t- %(message)s",
    datefmt='%H:%M:%S',
    level=logging.DEBUG
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

    def __init__(self, vtt_file, output_dir, mode) -> None:
        self.mode = mode
        self.vtt = webvtt.read(vtt_file)
        self.vtt_filename = os.path.basename(vtt_file).rsplit('.', 1)[0]  # grab the file name only, remove extension
        self.output_dir = output_dir
        self.vtt_lines = None  # raw text lines of the VTT file
        self.new_vtt_file = ['WEBVTT\n', '\n']  # empty vtt file structure
        self.processed_vtt = []  # contains array of vtt chunks in list format
        self.vtt_num_chunks = 0
        self.vtt_sentences = []  # contains concatenated sentences
        self.custom_library_path = None

        # # check if there is a custom library
        # if os.path.exists(os.path.join(webpage_dir, 'custom_caption_library.csv')):
        #     self.custom_library_path = os.path.join(webpage_dir, 'custom_caption_library.csv')

        # self.custom_gmsl_dictionary = None
        # self.gmsl_dictionary = self._create_gmsl_dictionary('caption_library.csv')
        
        self.parse_sentences()
        # self.spellcheck()
        # self.create_vtt()

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
            # sentence = ' '.join(self.vtt.captions[caption_index].lines)
            sentence = self.vtt.captions[caption_index].lines
            max_caption_length = len(max(self.vtt.captions[caption_index].lines, key=len))
            try:  # handle peeking the end of the file
                # while the cue id indicates there is more sentence
                while(self.vtt.captions[caption_index+1].identifier[-1:] != '0'):
                    caption_index += 1  # update the caption index to next block of text
                    # compare the max of the max of the next caption to the current caption and update
                    max_caption_length = max(max_caption_length, len(max(self.vtt.captions[caption_index].lines, key=len)))
                    sentence.extend(self.vtt.captions[caption_index].lines)
            except IndexError as e:  # end of file
                logger.debug(f'[unzip_sentences] {e}: list index out of range.')
            sentence = ' '.join(sentence)
            self.spellcheck(sentence)
            caption_index += 1  # update the chunk index to next block of text

    def spellcheck(self, sentence):
        logger.info(f'Spellchecking "{self.vtt_file_name}"...')
        if self.mode == 'webpage' and self.custom_gmsl_dictionary is not None:
            logger.info(f'Using custom library.')
            self._search_sentence(sentence, self.custom_gmsl_dictionary)

        logger.info(f'Using main library.')
        self._search_sentence(sentence, self.gmsl_dictionary)
        logger.info(f'Spellcheck of "{self.vtt_file_name}" complete!\n'
                    '===============================================================================\n')

    def _search_sentence(self, sentence, dictionary):
        for key in list(dictionary.keys()):
            # compare the exact spelling of the incorrect word to the sentence 
            # left word boundary for "Serializer" vs "Deserializer"
            if re.search(r'\b' + re.escape(key) + r'\b', sentence[1]):
                logger.info(f"[{sentence[0].split('-')[0]}]:Replacing {key} => {dictionary[key]}")
                # replace the incorrect word with the dictionary word
                self.vtt_sentences[idx][1] = re.sub(r'\b' + re.escape(key) + r'\b', dictionary[key], self.vtt_sentences[idx][1])


    def create_vtt(self):
        self.zip_sentences()
        for chunk in self.processed_vtt:
            self.new_vtt_file.extend((chunk[self.CUE_ID], chunk[self.TIMESTAMP], chunk[self.TEXT1], chunk[self.TEXT2]))
            if chunk[self.TEXT2] == '\n':
                pass
            else:
                self.new_vtt_file.append('\n')

        with open(os.path.join(self.output_dir, f'{self.vtt_file_name}_spellcheck.vtt'), 'w') as outp:
            outp.writelines(self.new_vtt_file)

    def zip_sentences(self):
        chunk_index = 0
        for idx, sentence in enumerate(self.vtt_sentences):
            # max number of text caption slots by looking at ID suffix
            max_caption_span = (int((sentence[0].strip())[-1:]) + 1) * 2
            sentence_wrap = wrap(sentence[1], sentence[2])  # wrap the sentence into a list using the current max length

            # check that you will span the same number text caption slots
            new_caption_length =  sentence[2]  # it can fit in the max number of slots or (max - 1)
            try:
                while not (len(sentence_wrap) == max_caption_span or len(sentence_wrap) == (max_caption_span - 1)):
                    new_caption_length -= 1
                    sentence_wrap = wrap(sentence[1], new_caption_length) 
            except ValueError as e:
                logger.error(f'[zip_sentences] {e}: at sentence {idx}')


            while sentence_wrap:
                self.processed_vtt[chunk_index][self.TEXT1] = ''.join([sentence_wrap.pop(0), '\n'])
                if not sentence_wrap:  # always make it two lines
                    self.processed_vtt[chunk_index][self.TEXT2] = '\n' 
                else:  # is there more text?
                    self.processed_vtt[chunk_index][self.TEXT2] = ''.join([sentence_wrap.pop(0), '\n'])
                chunk_index += 1

def main():
    '''
    All VTT files should be located in the vtt_files folder for batch editting.
    The processed files will end up in the spellchecked folder for batch editting.
    '''
    try:
        # mode = sys.argv[1]
        mode = 'webpage'

        if mode == 'batch':
            vtt_dir = batch_dir
        elif mode == 'webpage':
            vtt_dir = webpage_dir
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