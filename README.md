# DCC207 - Trabalho Prático I - Geometria Computacional

## Belo Horizonte Orthogonal Range Search KD-Tree

Código fonte para o primeiro trabalho prático da disciplina DCC207-Algoritmos II da Universidade Federal de Minas Gerais.

## Autores

Augusto Guerra de Lima 
augustoguerra@dcc.ufmg.br

Cauã Magalhaẽs Pereira
caua.magalhaes@dcc.ufmg.br

Heitor Gonçalves Leite
heitorleite@dcc.ufmg.br

## Introdução

Este trabalho objetiva estudar como estruturas de dados associadas a geometria computacional, a saber, árvores k-dimensionais, são empregadas no contexto de georreferenciamento.

## Objetivo principal - estrutura de dados e geometria computacional

A priori, este é um trabalho de Algoritmos para geometria computacional. Árvores k-dimensionais dividem o conjunto de pontos em partições; Seja um ponto p de k coordenadas, a estrutura de dados particiona recursivamente o espaço alternando entre suas dimensões, de forma a comparar apenas uma dimensão específica por nível, resultando em uma árvore binária.
Em particular, nos dados geográficos, as coordenadas x,y implicam em uma árvore bidimensional; De forma que se, no nível l é utilizada a coordenada x para o particionamento, em l+1 tão somente, será utilizada a coordenada y.

## Como executar
Para executar o projeto, siga os passos abaixo:

1. Instale as dependências necessárias:
    ```bash
    pip install -r requirements.txt
    ```

2. Acesse o diretório do aplicativo:
    ```bash
    cd app
    ```

3. Execute a aplicação:
    ```bash
    python index.py
    ```
