from infer import infill_with_ilm
import torch
from transformers import GPT2LMHeadModel

import os
import pickle

import tokenize_util


MASK_CLS = 'custom.MaskKeyword'
MODEL_DIR = "../Salesgen-App"

tokenizer = tokenize_util.Tokenizer.GPT2
with open(os.path.join(MODEL_DIR, 'additional_ids_to_tokens.pkl'), 'rb') as f:
    additional_ids_to_tokens = pickle.load(f)
additional_tokens_to_ids = {v:k for k, v in additional_ids_to_tokens.items()}
try:
    tokenize_util.update_tokenizer(additional_ids_to_tokens, tokenizer)
except ValueError:
    print('Already updated')
print(additional_tokens_to_ids)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = GPT2LMHeadModel.from_pretrained(MODEL_DIR)
model.eval()
_ = model.to(device)

# keywords = "Red Cotton Hooded Warm"
# keywords_lst = keywords.split()
# keywords_lst[0] = keywords_lst[0] + " _"
# keywords_lst[-1] = "_ " + keywords_lst[-1] 

# cont = " _ ".join(keywords_lst)



# context = cont.strip()
# print(context)
# context_ids = tokenize_util.encode(context, tokenizer)
# _blank_id = tokenize_util.encode(' _', tokenizer)[0]
# context_ids[context_ids.index(_blank_id)] = additional_tokens_to_ids['<|startofinfill|>']

# for i in range(len(keywords_lst) - 1):
#     context_ids[context_ids.index(_blank_id)] = additional_tokens_to_ids['<|infill_not_keyword|>']

# context_ids[context_ids.index(_blank_id)] = additional_tokens_to_ids['<|endofinfill|>']
# print(tokenize_util.decode(context_ids, tokenizer))


# generated = infill_with_ilm(
#     model,
#     additional_tokens_to_ids,
#     context_ids,
#     num_infills=1)

# for g in generated:
#     print('-' * 80)
#     print(tokenize_util.decode(g, tokenizer))



def generate(keywords):
    keywords_lst = keywords.split()
    keywords_lst[0] = keywords_lst[0] + " _"
    keywords_lst[-1] = "_ " + keywords_lst[-1] 

    cont = " _ ".join(keywords_lst)



    context = cont.strip()
    print(context)
    context_ids = tokenize_util.encode(context, tokenizer)
    _blank_id = tokenize_util.encode(' _', tokenizer)[0]
    context_ids[context_ids.index(_blank_id)] = additional_tokens_to_ids['<|startofinfill|>']

    for i in range(len(keywords_lst) - 1):
        context_ids[context_ids.index(_blank_id)] = additional_tokens_to_ids['<|infill_not_keyword|>']

    context_ids[context_ids.index(_blank_id)] = additional_tokens_to_ids['<|endofinfill|>']
    print(tokenize_util.decode(context_ids, tokenizer))


    generated = infill_with_ilm(
        model,
        additional_tokens_to_ids,
        context_ids,
        num_infills=1)

    return (tokenize_util.decode(generated[0], tokenizer))

