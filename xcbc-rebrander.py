import argparse, os, re

class Rebrander():
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
        'bitcoin': 'xcbc',
        'Bitcoin': 'XCBC',
        'BITCOIN': 'XCBC',
        'BTC': 'XCBC',
    }

    def __init__(self, directory):
        self.directory = directory

    def check_dir_names(self):
        for root, subdir_names, file_names in os.walk(self.directory, topdown=True):
            subdir_names[:] = [d for d in subdir_names if d not in self.excluded_directories]
            for subdir_name in subdir_names:
                self.check_name(subdir_name, root)

    def check_file_names(self):
        for root, subdir_names, file_names in os.walk(self.directory, topdown=True):
            subdir_names[:] = [d for d in subdir_names if d not in self.excluded_directories]
            for file_name in file_names:
                self.check_name(file_name, root)

    def check_files_content(self):
        for root, subdir_names, file_names in os.walk(self.directory, topdown=True):
            subdir_names[:] = [d for d in subdir_names if d not in self.excluded_directories]
            for file_name in file_names:
                self.check_content(file_name, root)

    def check_content(self, name, root):
        file_name = root + '/' + name
        new_content = []
        overwrite_file = False
        try:
            with open(file_name, encoding='utf8') as f:
                for line in f:
                    new_line = self.check_line(line)
                    new_content.append(new_line)
                    if new_line != line:
                        overwrite_file = True

            if overwrite_file == True:
                print("Overwriting", file_name)
                f = open(file_name, 'w', encoding='utf8')
                f.writelines(new_content)
                f.close()
        except:
            print("File content checking error", file_name)

    def check_line(self, line):
        new_line = line
        for rebrand_key, rebrand_value in self.rebrand_dictionary.items():
            if re.search(rebrand_key, new_line) and not re.search("Copyright", new_line):
                new_line = re.sub(rebrand_key, rebrand_value, new_line)

        return new_line

    def check_name(self, name, root):
        for rebrand_key, rebrand_value in self.rebrand_dictionary.items():
            if re.search(rebrand_key, name):
                new_name = re.sub(rebrand_key, rebrand_value, name)
                old_file = root + '/' + name
                new_file = root + '/' + new_name
                print("Renaming", old_file, new_file)
                os.rename(old_file, new_file)

    def run(self):
        print("Rebrander", self.directory, "dictionary", self.rebrand_dictionary)
        self.check_dir_names()
        self.check_file_names()
        self.check_files_content()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', help='directory to rebrand')
    args = parser.parse_args()

    rebrander = Rebrander(args.directory)
    rebrander.run()
