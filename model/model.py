from transformers import pipeline

import torch
import torch.nn.functional as F

classifier = pipeline("sentiment-analysis")
res = classifier([
                    "We are very happy",
                    "We are happy",
                    "You are awsome",
                    "Zoe is stinky poo poo"
                ])

classifier = pipeline("ner", grouped_entities=True)
#print(classifier("My name is Sylvain and I work at Hugging Face in Brooklyn. Malaysia, Kuala Lumpur, RIMBA RESIDENCE"))
print(classifier("T2-17-8 RIMBA RESIDENCE @ BOR KINRARA 58/5"))

# print(classifier("T2-17-8 RIMBA RESIDENCE @ BOR KINRARA 58/5"))
# classifier = pipeline("ner", grouped_entities=False, model="malay-huggingface/bert-tiny-bahasa-cased")
# print("New")
# print(classifier("T2-17-8 RIMBA RESIDENCE @ BOR KINRARA 58/5"))