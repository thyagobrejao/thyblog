---
title: "Thyago.dev.br — Como eu criei um blog com Hugo, Hextra e zero banco de dados"
date: '2026-03-25T14:00:00-03:00'
slug: thyblog
tags:
  - projeto
  - hugo
  - hextra
  - github-pages
  - python
  - blog
  - ci-cd
draft: false
---

Sempre quis ter um blog pessoal. Daqueles que você abre e pensa: "hm, legal, o cara realmente fez isso". Mas entre querer e fazer existe um abismo chamado **preguiça de configurar WordPress**, lidar com banco de dados, pagar hosting e descobrir que seu blog foi hackeado porque você esqueceu de atualizar um plugin de 2019.

Aí um belo dia eu assisti ao Fábio Akita explicando como ele montou o [The M.Akita Chronicles](https://akitaonrails.com/2026/02/19/frontend-sem-framework-bastidores-do-the-m-akita-chronicles/#hugo--hextra-blog-sem-banco-de-dados) usando **Hugo + Hextra** — sem framework JavaScript, sem banco de dados, sem drama. E pensei: "Se o Akita faz assim, quem sou eu pra discordar?"

Foi a inspiração que eu precisava. Obrigado, Akita. A culpa deste blog existir é sua. 😄

## O que é o Hugo (e por que ele é absurdamente rápido)

**Hugo** é um gerador de sites estáticos escrito em Go. Você escreve seus posts em Markdown, roda um comando, e ele cospe um site HTML completo em milissegundos. Sério. Milissegundos. Enquanto o Next.js ainda está decidindo qual versão do React usar, o Hugo já buildou, deployou e está tomando um café.

Sem banco de dados, sem servidor rodando PHP, sem nada. São arquivos HTML puros servidos diretamente. É a web como ela deveria ser — rápida, simples e sem surpresas no meio da madrugada.

## Hextra — O tema que faz o trabalho pesado

O [Hextra](https://github.com/imfing/hextra) é um tema de documentação para Hugo que funciona surpreendentemente bem como tema de blog. Ele vem com:

- 🔍 **Busca integrada** — sem precisar de Algolia ou ElasticSearch
- 📑 **Sidebar de navegação** — organização automática por seções
- 🌙 **Dark mode** — porque estamos em 2026, não em 2010
- 🌐 **Suporte multilingual** — o blog roda em pt-br e en
- 📋 **Table of Contents** — gerado automaticamente a partir dos headers

Tudo isso sem uma única linha de JavaScript customizado. O Akita estava certo: dá pra ter um frontend moderno sem framework.

## A estrutura do blog

O conteúdo fica organizado de um jeito que faz sentido (pelo menos pra mim):

```
content/
├── _index.md              # Página principal (auto-gerada! 🤖)
├── about.md               # Sobre mim (pt-br)
├── about.en.md            # About me (en)
├── projetos/              # Posts sobre projetos
│   ├── saiu-a-escala/
│   └── thyblog/           # ← Você está aqui!
├── tecnologias/           # Posts sobre tech
├── automacao-residencial/ # Home automation
├── motociclismo/          # Motos 🏍️
└── armas-de-pressao/      # Airsoft e pressão 🎯
```

Cada post vive dentro de sua própria pasta com um `index.md` (pt-br) e um `index.en.md` (en). Sim, **todo post é bilíngue**. Porque se é pra fazer, faz direito.

## O script mágico: `generate_index.py`

Aqui mora uma das partes mais legais do projeto. O Hugo é fantástico, mas ele não gera automaticamente uma página de índice cronológico com todos os posts agrupados por mês e ano. Então eu fiz um script Python que faz isso.

O `generate_index.py` é um script que:

1. **Varre** todo o diretório `content/` procurando arquivos `.md`
2. **Extrai** o frontmatter (título, data, tags) de cada post
3. **Ignora** rascunhos e páginas marcadas como "em breve"
4. **Agrupa** os posts por ano e mês
5. **Gera** os arquivos `_index.md` e `_index.en.md` — tanto o índice raiz quanto os índices de cada seção (projetos, tecnologias, etc.)

O resultado é uma página principal bonita e organizada, com links para todos os posts, datas formatadas e tags. Tudo automático, tudo em dois idiomas.

E a melhor parte? Ele roda no pipeline de CI/CD antes do Hugo buildar. Ou seja, eu nunca preciso me preocupar em atualizar o índice manualmente. Escrevo o post, faço push, e o resto acontece sozinho.

## Deploy no GitHub Pages — CI/CD sem dor

O deploy é feito via **GitHub Actions** e é de uma simplicidade que chega a ser bonita:

1. Faço `git push` na branch `main`
2. O GitHub Actions acorda e começa o workflow:
   - Instala o Hugo (versão extended, porque temos classe)
   - Instala o Go (necessário para os Hugo Modules)
   - Instala o Python
   - **Roda o `generate_index.py`** para gerar os índices atualizados
   - **Builda o site** com `hugo --gc --minify`
   - Faz upload do artefato
3. O job de deploy publica no GitHub Pages
4. O Cloudflare cuida do DNS e do SSL pro domínio `thyago.dev.br`

**Custo total da infraestrutura: R$ 0,00.** 🎉

O repositório é público, inclusive. O código do blog inteiro está no [GitHub](https://github.com/thyagobrejao/thyblog). Transparência total — e se alguém quiser copiar a ideia, fique à vontade.

## Multilingual — Porque a internet é grande

Todo o conteúdo é produzido em **Português do Brasil** (idioma padrão) e **Inglês**. O Hugo gerencia isso de forma nativa através do sufixo do arquivo:

- `index.md` → Português
- `index.en.md` → English

Os menus de navegação, labels e strings da interface também são traduzidos via arquivos `i18n/`. O switcher de idioma fica no topo da página, discreto e funcional.

## O Stack completo

Pra quem gosta de uma lista organizada (eu gosto):

| Tecnologia | Função |
|---|---|
| **Hugo** | Gerador de sites estáticos |
| **Hextra** | Tema (importado via Hugo Modules) |
| **Python** | Script de geração de índices |
| **GitHub Actions** | CI/CD automatizado |
| **GitHub Pages** | Hosting gratuito |
| **Cloudflare** | DNS + SSL |
| **Markdown** | Formato dos posts |
| **Go** | Necessário para Hugo Modules |

## A inspiração — Obrigado, Akita

Como mencionei lá no começo, a maior inspiração pra esse blog veio do post do **Fábio Akita** sobre os bastidores do [The M.Akita Chronicles](https://akitaonrails.com/2026/02/19/frontend-sem-framework-bastidores-do-the-m-akita-chronicles/#hugo--hextra-blog-sem-banco-de-dados). A ideia de que dá pra ter um blog moderno, bonito e funcional sem um único framework JavaScript me convenceu imediatamente.

O Akita levou a coisa a outro nível — com shortcodes customizados, templates de newsletter, transcrição de podcast... Eu sou mais modesto. Meu blog tem posts, tem busca, tem dark mode e tem café. Mas a essência é a mesma: **conteúdo primeiro, framework nunca**.

## O resultado

O que começou como "vou fazer um blogzinho" virou um projeto que eu realmente gosto de manter. Escrever em Markdown é prazeroso, o deploy é instantâneo, e o site carrega mais rápido que eu consigo piscar.

Se você está pensando em criar um blog, considere seriamente essa stack. É grátis, é rápido, é elegante — e você ainda aprende sobre CI/CD, DNS e geração de sites estáticos no processo.

O código está todo no [GitHub](https://github.com/thyagobrejao/thyblog). Bisbilhote à vontade.

---

*Feito com Hugo, Hextra, um script Python e uma dose generosa de "se o Akita faz, eu também faço".* 🚀
