# Musica Relógio

Projeto simples para baixar músicas do YouTube e salvar em uma pasta configurável.

## Como usar

1. Ajuste a pasta de destino no arquivo `config.yaml`.
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o programa:

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

## Observação

A pasta de destino não fica hardcoded no código. Ela é lida do arquivo `config.yaml`.
