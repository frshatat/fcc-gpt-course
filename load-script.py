import os
import lzma
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import concurrent.futures
import json
from datasets import load_dataset
import pandas as pd


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

def loadDataSeIfNotExist(dataset_name):
    # Define the paths to the files
    file_path_train = 'output_file_train.txt'
    file_path_val = 'out_file_val.txt'
    vocab_file = 'vocab.txt'

    # Load the dataset
    dataset = load_dataset(dataset_name)

    # Access the 'train' split of the dataset and select the first 1000 examples
    train_dataset = dataset['train'].select(range(1000))

    # Shuffle the dataset and split it into training and validation sets
    train_dataset = train_dataset.shuffle(seed=42)
    num_rows = len(train_dataset)
    split_point = int(num_rows * 0.8)
    train_data = train_dataset[:split_point]['text']
    val_data = train_dataset[split_point:]['text']

    vocab = set()

    # Process the training data
    with open(file_path_train, 'w', encoding='utf-8') as outfile:
        for record in train_data:
            outfile.write(record + '\n')
            characters = set(record)
            vocab.update(characters)

    # Process the validation data
    with open(file_path_val, 'w', encoding='utf-8') as outfile:
        for record in val_data:
            outfile.write(record + '\n')
            characters = set(record)
            vocab.update(characters)

    # Write the vocabulary to a file
    with open(vocab_file, 'w', encoding='utf-8') as vfile:
        for char in vocab:
            vfile.write(char + '\n')

# Call the function
loadDataSeIfNotExist("Skylion007/openwebtext")

            