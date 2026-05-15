import os
import json
from tokenizers import Tokenizer
#from transformers import AutoTokenizer
from modelscope import AutoTokenizer
tokenizer_name ='Qwen/Qwen2.5-7B-Instruct'
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name,trust_remote_code=True)

