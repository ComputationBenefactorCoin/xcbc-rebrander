"""
    XCBC Rebrander
"""
import os
from argparse import ArgumentParser
from re import search as re_search, sub as re_sub
from sys import exit as sys_exit

class Rebrander():
    """
        Main XCBC Rebrander class
    """
    directory = ''
    excluded_directories = set(['.git'])
    rebrand_dictionary = {
        'https://bitcoin.org/': 'https://computationbenefactorcoin.com/',
        'https://bitcoincore.org/': 'https://computationbenefactorcoin.com/',
        'https://bitcoincore.org/en/download/': 'https://computationbenefactorcoin.com/',
        'https://bitcointalk.org/': 'https://computationbenefactorcoin.com/',
        'https://doxygen.bitcoincore.org/': 'https://computationbenefactorcoin.com/',
        'https://en.bitcoin.it/wiki/Main_Page': 'https://computationbenefactorcoin.com/',
        'https://github.com/bitcoin/bitcoin': 'https://github.com/ComputationBenefactorCoin/xcbc',
        'https://github.com/bitcoin-core': 'https://github.com/ComputationBenefactorCoin/xcbc',
        'https://github.com/bitcoin': 'https://github.com/ComputationBenefactorCoin',
        'https://web.libera.chat/#bitcoin': 'https://computationbenefactorcoin.com/',
        'bitcoin.org': 'computationbenefactorcoin.com',
        'bitcoincore.org': 'computationbenefactorcoin.com',
        'bitcoin': 'xcbc',
        'Bitcoin': 'XCBC',
        'BITCOIN': 'XCBC',
        'BTC': 'XCBC',
    }

    def __init__(self, directory):
        self.directory = directory

    def check_content(self, name, root):
        """
            Performs content check
        """
        file_name = root + '/' + name
        new_content = []
        overwrite_file = False
        try:
            with open(file_name, encoding='utf8') as file:
                for line in file:
                    new_line = self.check_line(line)
                    new_content.append(new_line)
                    if new_line != line:
                        overwrite_file = True

            if overwrite_file:
                print('Overwriting', file_name)
                file = open(file_name, 'w', encoding='utf8')
                file.writelines(new_content)
                file.close()
        except UnicodeDecodeError:
            print('File content checking error', file_name)

    def check_dir_names(self):
        """
            Loops over dirs and performs name check
        """
        for root, subdir_names, _file_names in os.walk(self.directory, topdown=True):
            subdir_names[:] = [d for d in subdir_names if d not in self.excluded_directories]
            for subdir_name in subdir_names:
                self.check_name(subdir_name, root)

    def check_file_names(self):
        """
            Loops over files and performs name check
        """
        for root, subdir_names, file_names in os.walk(self.directory, topdown=True):
            subdir_names[:] = [d for d in subdir_names if d not in self.excluded_directories]
            for file_name in file_names:
                self.check_name(file_name, root)

    def check_files_content(self):
        """
            Loops over files and performs content check
        """
        for root, subdir_names, file_names in os.walk(self.directory, topdown=True):
            subdir_names[:] = [d for d in subdir_names if d not in self.excluded_directories]
            for file_name in file_names:
                self.check_content(file_name, root)

    def check_line(self, line):
        """
            Performs content rebrand
        """
        new_line = line
        for rebrand_key, rebrand_value in self.rebrand_dictionary.items():
            if re_search(rebrand_key, new_line) and not re_search('Copyright', new_line):
                new_line = re_sub(rebrand_key, rebrand_value, new_line)

        return new_line

    def check_name(self, name, root):
        """
            Performs rebrand for dir or file
        """
        for rebrand_key, rebrand_value in self.rebrand_dictionary.items():
            if re_search(rebrand_key, name):
                new_name = re_sub(rebrand_key, rebrand_value, name)
                old_file = root + '/' + name
                new_file = root + '/' + new_name
                print('Renaming', old_file, new_file)
                os.rename(old_file, new_file)

    def run(self):
        """
            Run method performs all rebrand actions
        """
        print('Rebrander', self.directory, 'dictionary', self.rebrand_dictionary)

        if not os.path.isdir(self.directory):
            print(self.directory, 'is not a directory')
            sys_exit()

        self.check_dir_names()
        self.check_file_names()
        self.check_files_content()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--directory', help='directory to rebrand')
    args = parser.parse_args()

    rebrander = Rebrander(args.directory)
    rebrander.run()
