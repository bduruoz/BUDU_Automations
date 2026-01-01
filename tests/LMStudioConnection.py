import time
import subprocess
import psutil
from openai import OpenAI

# ---------------------------------------------------
# AYARLAR
# ---------------------------------------------------
LM_STUDIO_PATH = r"C:\Users\chron\AppData\Local\Programs\LM Studio\LM Studio.exe"  # LM Studio uygulama yolu
LM_API_URL = "http://localhost:9090/v1"
LM_API_KEY = "lm-studio"  # placeholder
# ---------------------------------------------------

client = OpenAI(base_url=LM_API_URL, api_key=LM_API_KEY)


# ---------------------------
# 0) LM Studio Çalışıyor mu?
# ---------------------------
def ensure_lm_studio_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and "LM Studio" in proc.info['name']:
            print("LM Studio zaten çalışıyor.")
            return

    print("LM Studio çalışmıyor. Açılıyor...")
    subprocess.Popen([LM_STUDIO_PATH])
    time.sleep(5)  # server ayaklansın diye bekleme süresi


# ---------------------------
# 1) Modelleri Listeleme
# ---------------------------
def list_models():
    try:
        models = client.models.list()
        print("\n--- LM Studio'daki Kurulu Modeller ---")
        for m in models.data:
            print("•", m.id)
    except Exception as e:
        print("HATA (model list):", e)


# ---------------------------
# 2) Prompt Gönderme + Token Sayıları
# ---------------------------
def ask_model(model_name, prompt):
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        output_text = response.choices[0].message.content

        # Token bilgileri (LM Studio API destekliyor)
        usage = response.usage
        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens

        return output_text, input_tokens, output_tokens, total_tokens

    except Exception as e:
        print("HATA (ask_model):", e)
        return None, 0, 0, 0


# ---------------------------
# 3) Geri dönüş süresi ölçme
# ---------------------------
def timed_request(model_name, prompt):
    start = time.time()
    answer, in_tok, out_tok, total_tok = ask_model(model_name, prompt)
    end = time.time()
    return answer, round(end - start, 3), in_tok, out_tok, total_tok


# ---------------------------
# ÖRNEK KULLANIM
# ---------------------------
if __name__ == "__main__":

    ensure_lm_studio_running()

    print("\nLM Studio model listesi getiriliyor...\n")
    list_models()

    print("\n------------------------------------")
    print("Test sorgusu gönderiliyor...")
    print("------------------------------------")

    #MODEL = "deepseek/deepseek-r1-0528-qwen3-8b"
    #MODEL = "qwen/qwen3-vl-4b"
    #MODEL = "phi-3.1-mini-128k-instruct"
    #MODEL = "dolphin3.0-llama3.1-8b"
    #MODEL = "gemma-3n-e4b-it-text"
    #MODEL = "deepseek-coder-6.7b-instruct" # ingilzce
    #MODEL = "google/gemma-3-27b"
    #MODEL = "qwen/qwen2.5-vl-7b"
    #MODEL = "mistral-7b-instruct-v0.3"
    #MODEL = "meta-llama-3.1-8b-instruct"
    MODEL = "gpt-oss-20b"
    #MODEL = "text-embedding-nomic-embed-text-v1.5"

    PROMPT = "Merhaba! Bana karanlık bir hikaye anlat."
    #PROMPT = "Hi! Which AI model are you?"

    answer, latency, in_tok, out_tok, total_tok = timed_request(MODEL, PROMPT)

    print("\n--- Yanıt ---")
    print(answer)

    print("\n--- Token Kullanımı ---")
    print("Input tokens :", in_tok)
    print("Output tokens:", out_tok)
    print("Total tokens :", total_tok)

    print("\nSüre:", latency, "saniye")