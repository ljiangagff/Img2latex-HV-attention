import torch
import os
import argparse
import loader as LD
from val import DecodingVal
from models.model import Model

parser = argparse.ArgumentParser()
parser.add_argument('--device', type=str, default="7")
opt = parser.parse_args()
DEVICE_ID = int(opt.device)

torch.cuda.set_device(DEVICE_ID)
DEVICE = torch.device('cuda')

DATA_DIR = '../im2tex100k/data'
LABEL_DIR = '../im2tex100k/seqs'
MODEL_DIR = '../im2tex100k/test/ckpt/'
RESULT_DIR = "../im2tex100k/test/result/decoded/"
LOG_DIR = '../im2tex100k/test/log'
# LOG_DIR = os.path.normpath(os.path.join(os.getcwd(), '../test_log'))


ld = LD.Loader(data_dir=DATA_DIR, label_dir=LABEL_DIR)
my_test = DecodingVal(ld, DEVICE, LOG_DIR, category='test')
my_test.load_data()

def test_models(ckpt_dir, test):
    logger = test.get_logger()
    files = os.listdir(ckpt_dir)
    for file in files:
        if file[-4:] == '.pth':

            my_model = torch.load(os.path.join(ckpt_dir, file), map_location=DEVICE)
            logger.info(f'Begin to validate the model {file}')
            my_model.eval()
            bleu, blue_no, emr, count = test.greedy_validate(my_model, True, result_dir=os.path.join(RESULT_DIR, file[:-4]+".json"))
            logger.critical(f"Validate {count} items. Bleu score: {bleu/count}. Bleu no blank score: {blue_no/count}. Exact match rate: {emr/count}.")
            free_model(my_model)

def free_model(model):
    del model
    torch.cuda.empty_cache()

test_models(MODEL_DIR, my_test)
