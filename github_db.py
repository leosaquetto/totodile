import os
import json
import base64
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "leosaquetto"
REPO_NAME = "totodile"

def carregar_json(caminho_arquivo):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{caminho_arquivo}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3.raw"}
    try:
        req = requests.get(url, headers=headers)
        if req.status_code == 200:
            return json.loads(req.text), req.headers.get('ETag', '').strip('"')
    except:
        pass
    return {}, None

def salvar_json(caminho_arquivo, dados, sha=None):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{caminho_arquivo}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}
    
    # Busca o SHA atual se não for passado
    if not sha:
        req_get = requests.get(url, headers=headers)
        if req_get.status_code == 200:
            sha = req_get.json().get("sha")

    conteudo_base64 = base64.b64encode(json.dumps(dados, indent=4).encode("utf-8")).decode("utf-8")
    payload = {"message": f"Totodile atualizou {caminho_arquivo}", "content": conteudo_base64}
    if sha:
        payload["sha"] = sha
        
    requests.put(url, headers=headers, json=payload)
