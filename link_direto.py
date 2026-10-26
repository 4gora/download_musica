# -*- coding: utf-8 -*-
import glob
import os
import re
import sys
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
from yt_dlp import YoutubeDL


def sanitizar_nome(nome: str) -> str:
    """Remove caracteres proibidos pelo Windows para nomes de arquivos ou pastas."""
    nome_limpo = re.sub(r'[\\/*?:"<>|]', "", nome)
    return nome_limpo.strip(". ")


def sanitizar_url_youtube(url: str) -> str:
    url = url.strip().strip("'\"")

    try:
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)

        params_uteis = {}
        # Se for playlist, preserva o parâmetro 'list'
        if "list" in query_params:
            params_uteis["list"] = query_params["list"][0]
        # Se for vídeo avulso, preserva 'v'
        if "v" in query_params:
            params_uteis["v"] = query_params["v"][0]

        if params_uteis:
            nova_query = urlencode(params_uteis)
            return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", nova_query, ""))

        if "youtu.be" in parsed.netloc:
            return f"https://www.youtube.com/watch?v={parsed.path.strip('/')}"

    except Exception:
        pass

    return url


def limpar_imagens_soltas(pasta_raiz: str):
    """Remove qualquer arquivo de imagem que tenha sobrado na pasta."""
    extensoes = ("*.jpg", "*.jpeg", "*.webp", "*.png")
    for raiz, _, _ in os.walk(pasta_raiz):
        for ext in extensoes:
            for img in glob.glob(os.path.join(raiz, ext)):
                try:
                    os.remove(img)
                except OSError:
                    pass


def pasta_fallback() -> str:
    pasta = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(pasta, exist_ok=True)
    return pasta


def carregar_config(caminho_arquivo: str = "config.yaml") -> dict:
    fallback = pasta_fallback()
    config = {
        "pasta_destino": fallback,
    }

    if not os.path.exists(caminho_arquivo):
        return config

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha_limpa = linha.split("#", 1)[0].strip()
                if not linha_limpa or ":" not in linha_limpa:
                    continue

                chave, valor = [parte.strip() for parte in linha_limpa.split(":", 1)]
                chave = chave.lower()
                valor = valor.strip().strip('"').strip("'")

                if chave in {"pasta_destino", "download_dir", "music_path"} and valor:
                    config["pasta_destino"] = valor
                    break
    except Exception:
        return config

    pasta = config["pasta_destino"]
    if not os.path.isabs(pasta):
        pasta = os.path.abspath(os.path.join(os.path.dirname(__file__), pasta))

    if not os.path.isdir(pasta):
        try:
            os.makedirs(pasta, exist_ok=True)
        except Exception:
            return {"pasta_destino": fallback}

    config["pasta_destino"] = pasta
    return config


def baixar_mp3(url: str, pasta_destino: str = None):
    if pasta_destino is None:
        pasta_destino = carregar_config().get("pasta_destino")

    if not pasta_destino:
        pasta_destino = pasta_fallback()

    pasta_destino = os.path.abspath(pasta_destino)
    os.makedirs(pasta_destino, exist_ok=True)
    url_limpa = sanitizar_url_youtube(url)

    # 1. Inspeciona a URL antes do download para checar se é playlist
    print(f"\nObtendo informações de: {url_limpa}...")
    pasta_final = pasta_destino

    try:
        with YoutubeDL({"quiet": True, "extract_flat": True}) as ydl:
            info = ydl.extract_info(url_limpa, download=False)

            # Se for uma playlist ou tiver lista de faixas
            if info and ("entries" in info or info.get("_type") == "playlist"):
                titulo_playlist = info.get("title") or "Playlist"
                nome_pasta = sanitizar_nome(titulo_playlist)

                # Monta a subpasta específica: <pasta_destino>\<Nome da Playlist>
                pasta_final = os.path.join(pasta_destino, nome_pasta)
                os.makedirs(pasta_final, exist_ok=True)
                print(f"[Playlist Detectada] As músicas serão salvas em: '{pasta_final}'")
    except Exception as e:
        print(f"[Aviso] Não foi possível verificar dados prévios: {e}")
        pasta_final = pasta_destino

    # 2. Configura o download salvando na pasta_final definida pelo Python
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(pasta_final, "%(title)s.%(ext)s"),
        "writethumbnail": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
            {
                "key": "FFmpegThumbnailsConvertor",
                "format": "jpg",
            },
            {
                "key": "FFmpegMetadata",
                "add_metadata": True,
            },
            {
                "key": "EmbedThumbnail",
                "already_have_thumbnail": False,
            },
        ],
        "ignoreerrors": True,
        "quiet": False,
        "no_warnings": False,
    }

    print(f"Baixando e convertendo áudios...\n")
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url_limpa])

    # 3. Limpeza de imagens temporárias que possam ter sobrado
    limpar_imagens_soltas(pasta_final)

    print(f"\nConcluído com sucesso! Pasta de destino: '{pasta_final}'")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        link = sys.argv[1]
    else:
        link = input("Cole o link do YouTube / Playlist: ").strip()

    if link:
        baixar_mp3(link)