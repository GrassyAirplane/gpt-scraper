from transformers import pipeline

classifier = pipeline("sentiment-analysis")

res = classifier("I've been waiting for a HuggingFace course my whole life.")
res_1 = classifier("Im not to sure")

print(res)
print(res_1)

# generator = pipeline("text-generation", model="distilgpt2")
# res = generator(
#     "In this course, we will teach you",
#     max_length = 30,
#     num_return_sequences=2
# )

# print(res)

classifier = pipeline("zero-shot-classification", "malay-huggingface/bert-tiny-bahasa-cased")

res = classifier(
    "This is a course about python, list comprehension",
    candidate_labels = ["education", "politics", "address"]
)

res = classifier(
    "Bukit Bintang",
    candidate_labels = ["address", "alamat"]
)

res1 = classifier(
    "Bapa saya dan ibu",
    candidate_labels = ["address", "alamat"]
)

print(res)
print(res1)