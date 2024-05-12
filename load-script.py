import os
import lzma
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import concurrent.futures
from datasets import load_dataset


def xz_files_in_dir(directory):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".xz") and os.path.isfile(os.path.join(directory, filename)):
    
            files.append(os.path.join(directory, filename))
        return files;

## write method to check if dataset is already downloaded
## if not download it
## if it is downloaded, load it
## save it to disk

def loadDataSetIfNotExists(dataset_name):
    if not os.path.exists('./data'):
        dataset = load_dataset(dataset_name)
        dataset["train"].save_to_disk("./data")
    else:
        _N_DATA_FILES = 21
        _DATA_FILES = ["subsets/urlsf_subset{:02d}.tar".format(i) for i in range(_N_DATA_FILES)]

        dataset = load_dataset(dataset_name, data_files = _DATA_FILES)
    return dataset

dataset = loadDataSetIfNotExists("Skylion007/openwebtext")
dataset = dataset["train"]

# dataset = load_dataset("Skylion007/openwebtext")
# dataset.save_to_disk("./data")

folder_path = "./data"
output_file_train = "output_train.txt"
out_file_val = "output_val.txt"
vocab_file = "vocab.txt"

files = xz_files_in_dir(folder_path)

total_files = len(files)

#Calculate the split index
split_index = int(total_files * 0.9) # 90% train, 10% val
files_train = files[:split_index]
files_val = files[split_index:]

# Proces the files for training and validation seperatly
vocab = set()

# Process the training files
with open(output_file_train, "w", encoding = "utf-8") as outfile:
    for count, filename in tqdm(files_train, total = len(files_train)):
        file_path = os.path.join(folder_path, filename)
        with lzma.open(file_path, "rt", encoding = "utf-8") as infile:
            text = infile.read()
            outfile.write(text)
            characters = set(text)
            vocab.update(characters)

# Process the validation files
with open(out_file_val, "w", encoding = "utf-8") as outfile:
    for filename in tqdm(files_val, total = len(files_val)):
        file_path = os.path.join(folder_path, filename)
        with lzma.open(file_path, "rt", encoding = "utf-8") as infile:
            text = infile.read()
            outfile.write(text)
            characters = set(text)
            vocab.update(characters)

# Write the vocabulatory to a vocab.txt
with open(vocab_file, "w", encoding = "utf-8") as vfile:
        for char in vocab:
            vfile.write(char + "\n")

            