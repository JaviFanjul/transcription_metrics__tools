import os
import re
import csv
from jiwer import wer, mer, cer

# === CONFIGURACIÓN ===
base_path = "./"
folders = {
    "groundtruth": os.path.join(base_path, "groundtruth"),
    "whisper_large": os.path.join(base_path, "model_large"),
    "whisper_medium": os.path.join(base_path, "model_medium"),
}

file_names = sorted(os.listdir(folders["groundtruth"]))

# === FUNCIONES ===

def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_by_speaker(text):
    agent_lines = []
    client_lines = []

    for line in text.strip().splitlines():
        line = line.strip()
        line = re.sub(r"^\(\d+(\.\d+)?-\d+(\.\d+)?\)\s*", "", line)
        if line.lower().startswith("agente:"):
            agent_lines.append(line[len("agente:"):].strip())
        elif line.lower().startswith("cliente:"):
            client_lines.append(line[len("cliente:"):].strip())

    agent_text = " ".join(agent_lines).lower()
    client_text = " ".join(client_lines).lower()
    full_text = f"{agent_text} {client_text}".strip()
    return full_text, agent_text, client_text

def get_metrics(ref, hyp):
    return {
        "wer": round(wer(ref, hyp), 3),
        "mer": round(mer(ref, hyp), 3),
        "cer": round(cer(ref, hyp), 3),
    }

# === PROCESAMIENTO ===

results = []

for model in ["whisper_large", "whisper_medium"]:
    for file_name in file_names:
        gt_path = os.path.join(folders["groundtruth"], file_name)
        hyp_path = os.path.join(folders[model], file_name)

        if not os.path.exists(hyp_path):
            continue

        ref_text = read_text(gt_path)
        hyp_text = read_text(hyp_path)

        ref_full, ref_agent, ref_client = extract_by_speaker(ref_text)
        hyp_full, hyp_agent, hyp_client = extract_by_speaker(hyp_text)

        global_metrics = get_metrics(ref_full, hyp_full)
        agent_metrics = get_metrics(ref_agent, hyp_agent)
        client_metrics = get_metrics(ref_client, hyp_client)

        results.append({
            "file": file_name,
            "model": model,
            "wer_global": global_metrics["wer"],
            "mer_global": global_metrics["mer"],
            "cer_global": global_metrics["cer"],
            "wer_agente": agent_metrics["wer"],
            "mer_agente": agent_metrics["mer"],
            "cer_agente": agent_metrics["cer"],
            "wer_cliente": client_metrics["wer"],
            "mer_cliente": client_metrics["mer"],
            "cer_cliente": client_metrics["cer"],
        })

# === GUARDAR CSV ===

csv_path = os.path.join(base_path, "results.csv")
with open(csv_path, mode="w", newline="", encoding="utf-8") as csvfile:
    fieldnames = list(results[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    writer.writerows(results)

print(f"\n✅ Resultados guardados en: {csv_path}")
