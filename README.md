# Simulador de Circuitos Elétricos – Trabalho 2 EEL710 (2025/02)

Repositório público contendo a implementação do Trabalho 2 da disciplina **EEL710 – Instrumentação e Técnicas de Medidas (2025/02)**, da Universidade Federal do Rio de Janeiro (UFRJ).

**Autores:**
- Fabricio Guimarães de Moura  
- Gabriel Siqueira Peroba  
- Hugo de Barros Araujo  
- André de Farias Pereira

---

## 📘 Visão Geral

O projeto tem como objetivo o desenvolvimento de um **simulador de circuitos elétricos no domínio do tempo**, com suporte a componentes lineares e não lineares, análise transiente e leitura via netlists. O simulador deve ser implementado em Python, utilizando Programação Orientada a Objetos (POO), e deve seguir rigorosos padrões de projeto, versionamento e documentação técnica.

---

## 🔧 Funcionalidades

- Simulação transiente de circuitos elétricos via método Backward de Euler.
- Suporte à leitura de **netlists** em formato SPICE.
- Arquitetura orientada a objetos, com herança, encapsulamento e polimorfismo.
- Implementação de componentes como resistores, capacitores, indutores, fontes, diodos, MOSFETs e amplificadores operacionais.
- Resolução de equações não lineares via **Newton-Raphson**.
- Interface programática via Python e interface via arquivos `.net`.
- Saídas organizadas em dataframes para análise e visualização dos resultados.

---

## 🧪 Testes Automatizados (CI/CD)

O repositório conta com uma pipeline de **Integração e Entrega Contínuas (CI/CD)** utilizando **GitHub Actions**, com testes escritos em **Pytest** que cobrem os casos essenciais do simulador.

---

## 📁 Estrutura do Repositório

```plaintext
├── src/                  # Código-fonte principal
├── tests/                # Casos de teste automatizados
├── docs/                 # Documentação técnica gerada
├── .github/workflows/    # Pipelines de CI/CD
├── README.md             # Este arquivo
```

---

## 📄 Documentação

A documentação técnica é gerada automaticamente com **Sphinx**, e está disponível em: https://hugodba.github.io/ITM_25.2_G3/ ou na pasta `/docs`, incluindo:

- Diagrama de classes e hierarquia de objetos
- Instruções de instalação e uso
- Exemplos de netlists e execução
- Cobertura de testes e uso do Pytest

---

## 📌 Requisitos Técnicos Atendidos

- Versionamento Git em repositório público  
- Simulação transiente (Backward Euler obrigatório; TRAP e FE opcionais)  
- Suporte a elementos não lineares (Diodo, MOSFET etc.)  
- Leitura de netlist com parâmetros SPICE  
- Geração de documentação e CI/CD via GitHub Actions  

---

## 🏫 Instituição

Departamento de Engenharia Eletrônica e de Computação (DEL)  
Escola Politécnica – Universidade Federal do Rio de Janeiro (UFRJ)  
Disciplina: EEL710 – Instrumentação e Técnicas de Medidas (2025/02)  
Professor responsável: João Victor da Fonseca Pinto
