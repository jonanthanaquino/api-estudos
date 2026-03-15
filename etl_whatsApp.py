import re

with (
    open("notas-teste.txt", "r", encoding="utf-8") as entrada,
    open("links.txt", "w", encoding="utf-8") as saida,
):
    for linha in entrada:
        match = re.search(r"https?://\S+", linha)
        if match:
            saida.write(match.group(0) + "\n")
