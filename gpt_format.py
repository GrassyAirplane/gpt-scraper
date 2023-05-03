from env_variables import API_KEY, MODEL_VERSION
import openai

openai.api_key = API_KEY

prompt = "Can you please extract the following fields - prices, land area, and address - from the following OCR text I have provided and format the output in CSV, here is the text"
text = "T2-17-8 RIMBA RESIDENCE @ BOR KINRARA 58/5 | RM583,200 | 1422SF | 12-Sep | RHB | SOLD RM 640,000 |\",,| T2-17-8 RIMBA RESIDENCE @ BOR KINRARA 58/5 |,\"RM 583,200 _\",1422 SF,,\u2014 -RHB,\"\u2014 SOLD RM 640,000 _\"\r\n\"28-11 SUASANA BUKIT CEYLON 2 @ RAIACHULAN KL $| RMS511,000 | 743SF | 7:Sep | UOB\u2019 [| SOLDRM 513,000 |\",,28-11 SUASANA BUKIT CEYLON 2 @ RAJACHULANKL sf,\"RM 511,000\",-743SF,7-Sep,UOB,\"~ SOLD RM 511,000 \u2014\"\r\n\"A-9-8 VERVE SUITE @ OKR KL RM 510,300 872 SF 27-Se RHB SOLD RM 555\",,A-9-8 VERVE SUITE @ OKR KL |,\"RM 510,300\",872 SF,,RHB,\"SOLD RM 555,000 |\"\r\n\"A-22-2 PAISLEY @ METROPARK SUBANG | RM567,000 | 969SF | 27-Sep | AMBANK | SOLD RM 582,000 |\",,A-22-2 PAISLEY @ METROPARK SUBANG,\"RM567,000\",\u2014 \u00ab O69SF,27-Sep,~ AMBANK,\"SOLD RM 582,000 _\"\r\n,,,,,,uoB,\r\n\"C-19-7 PACIFIC STAR @ SEKSYEN 13 PJ.  | = RM697,000 | 1242SF | 7-Sep  |  uoB | SOLDRM6E97.000 |\",CASH,C-19-7 PACIFIC STAR @ SEKSYEN 13 PJ.,\"~RM 697,000\",1242 SF,7-Sep,uUoB-,~ SOLD RM 697.000 \u2014\r\n\"fF OG CENDANA@KLCC 3=\u2014\u201cis\u2018CSC~CSYSE#PRM1,131,000 | 2626SF | 14Sep | UOB | SOLD RM 1,131,000 |\",,20-06 CENDANA@KLCC i ests,\"RM 1,131,000\",2626 SF,14-Sep,UuOB,EEE\r\n\"A-23A-05 NIDOZ @ DESA PETALING KL | = RM702,000 | 1399SF | 27-Sep | RHB | SOLD RM 702,000 |\",,A-23A-05 NIDOZ @ DESA PETALING KL,\"RM 702,000\",,,RHB,\r\n\"| | 19-10 ANGGUN JSI @ MEDAN TUANKU KL |} RM641,500 | 732SF | 27-Sep | RHB | SOLDRM 641,500 |\",,19-10 ANGGUN JSI @ MEDAN TUANKU KL,\"RM 641,500\",732 SF,-27-Sep,RHB,\"SOLD RM 641,500 |\"\r\n\"C-13-6 VIVO 9 SEPUTEH @ OKR KL | RMS557,68S | 1248SF | 29-Sep | AMBANK | SOLD RM 635,000 |\",,C-13-6 VIVO 9 SEPUTEH @ OKR KL,\"RM 557,685\",,29-Sep,AMBANK,\"SOLD RM 635,000 \u2014\"\r\n\"BUMI 30 JALAN TROPICANA HEIGHTS 2/6, KAJANG RM 899,100 2314 SF 29-Sep AMBANK | SOLD RM 970,000\",\u2014 BUMI,\"30 JALAN TROPICANA HEIGHTS 2/6, KAJANG |\",\"RM 899,100\",2314 SF,29-Sep,AMBANK,\"SOLD RM 970,000 _\"\r\n\"A-5-1 PUSAT KORPORAT MELAWATI KL  | = RM770,000 | 1442SF | 29-Sen | SME  | SOLD RM 770,000 |\",,A-5-1 PUSAT KORPORAT MELAWATI KL,\"~ RM770,000 \u2014\",1442 SF,29-Sep,SME,\"~ SOLD RM 770,000 \u2014\"\r\n\"A-2-10, NINE RESIDENCE @ CHERAS | = RM382,638 | 1211SF | 29-Sep | AMBANK | SOLO RM 382,638 |\",,\"A-2-10, NINE RESIDENCE @ CHERAS\",\"\u2014 RM 382,638 _\",1211 SF,_ 29-Sep,_ AMBANK |,\"\u2014 SOLD RM 382,638 __\"\r\n\"A-34-7 ASTETICA @ THE MINES SERDANG RI 1154SF | 29-Sep BSN | SOLD RM 405,000\",,A-34-7 ASTETICA @ THE MINES SERDANG,\"RM 405,000\",1154 SF,29Sep,BSN,\"SOLD RM 405,000 \u2014\"\r\n"


completion = openai.ChatCompletion.create(
    model="ada",
    messages=[{
                "role":"user",
                "content": prompt + text
            }]
)

"""
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "The circumference of the moon is approximately 10,921 km.",
        "role": "assistant"
      }
    }
  ],
  "created": 1683087258,
  "id": "chatcmpl-7ByAc8aZcV2XUMGKmU0Lj3B66Ahtp",
  "model": "gpt-3.5-turbo-0301",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 13,
    "prompt_tokens": 18,
    "total_tokens": 31
  }
}

E.G
"""
print(completion)


"""
        "content": "prices,land area,address\n\"RM583,200\",1422SF,\"T2-17-8 RIMBA RESIDENCE @ BOR KINRARA 58/5\"\nRMS511,000,743SF,\"28-11 SUASANA BUKIT CEYLON 2 @ RAIACHULAN KL\"\nRM510,300,872 SF,\"A-9-8 VERVE SUITE @ OKR KL\"\nRM567,000,969SF,\"A-22-2 PAISLEY @ METROPARK SUBANG\"\nRM697,000,1242SF,\"C-19-7 PACIFIC STAR @ SEKSYEN 13 
PJ.\"\nRM1,131,000,2626 SF,\"20-06 CENDANA@KLCC\"\nRM702,000,1399SF,\"A-23A-05 NIDOZ @ DESA PETALING KL\"\nRM641,500,732 SF,\"19-10 ANGGUN JSI @ MEDAN TUANKU KL\"\nRMS557,68S,1248SF,\"C-13-6 VIVO 9 SEPUTEH @ OKR KL\"\nRM 899,100,2314 SF,\"30 JALAN TROPICANA HEIGHTS 2/6, KAJANG\"\nRM770,000,1442SF,\"A-5-1 PUSAT KORPORAT MELAWATI KL\"\nRM382,638,1211SF,\"A-2-10, NINE RESIDENCE @ CHERAS\"\nRM405,000,1154 SF,\"A-34-7 ASTETICA @ THE MINES SERDANG\""

"""

