# -*- coding: utf-8 -*-
import sys
from yt_dlp import YoutubeDL
from link_direto import baixar_mp3


def formatar_duracao(segundos):
    if not segundos:
        return "--:--"
    minutos = int(segundos) // 60
    segs = int(segundos) % 60
    return f"{minutos:02d}:{segs:02d}"


def formatar_views(views):
    if not views:
        return "N/A"
    if views >= 1_000_000:
        return f"{views / 1_000_000:.1f}M"
    if views >= 1_000:
        return f"{views / 1_000:.1f}K"
    return str(views)


def buscar_musica(termo: str, limite: int = 5):
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
    }

    print(f"\nBuscando por '{termo}' no YouTube...\n")

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch{limite}:{termo}", download=False)

    if not info or "entries" not in info or not info["entries"]:
        print("Nenhum resultado encontrado.")
        return []

    return info["entries"]


def exibir_menu(resultados):
    print("=" * 80)
    print(f"{'#':<3} | {'DURAÇÃO':<8} | {'VIEWS':<7} | {'CANAL':<20} | {'TÍTULO'}")
    print("-" * 80)

    for i, item in enumerate(resultados, 1):
        titulo = item.get("title", "Sem título")
        canal = item.get("uploader", item.get("channel", "Desconhecido"))
        duracao = formatar_duracao(item.get("duration"))
        views = formatar_views(item.get("view_count"))

        canal_curto = (canal[:18] + "..") if len(canal) > 20 else canal

        print(f"[{i}] | {duracao:<8} | {views:<7} | {canal_curto:<20} | {titulo}")

    print("=" * 80)


def main():
    while True:
        try:
            termo = input("\nDigite o nome da música / artista (ou 'sair' para encerrar): ").strip()
            if not termo:
                continue
            if termo.lower() in ("sair", "exit", "q"):
                print("Encerrando CLI.")
                break

            resultados = buscar_musica(termo, limite=5)
            if not resultados:
                continue

            exibir_menu(resultados)

            escolha = input("\nEscolha o número da faixa para baixar (0 para cancelar): ").strip()
            if not escolha.isdigit():
                print("Entrada inválida. Operação cancelada.")
                continue

            indice = int(escolha)
            if indice == 0:
                print("Download cancelado.")
                continue

            if 1 <= indice <= len(resultados):
                item_escolhido = resultados[indice - 1]
                video_url = item_escolhido.get("url") or f"https://www.youtube.com/watch?v={item_escolhido.get('id')}"
                
                print(f"\n-> Baixando: {item_escolhido.get('title')}")
                baixar_mp3(video_url)
            else:
                print("Opção fora do intervalo válido.")

        except KeyboardInterrupt:
            print("\nSaindo...")
            sys.exit(0)


if __name__ == "__main__":
    main()