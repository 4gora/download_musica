# download_musica

Projeto simples para baixar músicas do YouTube e salvar em uma pasta configurável.

Há duas versões do código neste repositório:

1. `link_direto.py`  
   Versão que baixa diretamente a partir de um link do YouTube ou playlist.

2. `main.py`  
   Versão com busca por música/artista, mostra resultados e permite escolher qual faixa baixar.

## Como usar

1. Ajuste a pasta de destino no arquivo `config.yaml`.
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute a versão desejada:

```bash
python link_direto.py
```

ou

```bash
python main.py
```

## Configuração

O arquivo `config.yaml` deve conter algo como:

```yaml
pasta_destino: "C:/Users/ale/Music"
```

Se quiser, pode copiar o exemplo:

```bash
copy config.example.yaml config.yaml
```

Se o arquivo não existir ou estiver com problema, o programa usa automaticamente a pasta `downloads` dentro da raiz do projeto.