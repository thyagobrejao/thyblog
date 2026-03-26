# AGENTS.md — Blog Thyago.dev.br

Este é um blog pessoal construído com [Hugo](https://gohugo.io/) usando o tema [Hextra](https://github.com/imfing/hextra), hospedado em [thyago.dev.br](https://thyago.dev.br/).

## Quick Reference

```bash
# Rodar servidor local
hugo server -D

# Gerar índice principal
python scripts/generate_index.py

# Build de produção
hugo --minify
```

## Project Structure

```
thyblog/
├── AGENTS.md                  # Este arquivo
├── hugo.yaml                  # Configuração principal do Hugo
├── content/                   # Todo o conteúdo do blog
│   ├── _index.md              # Página principal (auto-gerada)
│   ├── about.md               # Página Sobre (pt-br)
│   ├── about.en.md            # Página Sobre (en)
│   └── YYYY/MM/slug/          # Posts organizados por data
│       ├── index.md           # Post em pt-br
│       └── index.en.md        # Post em en
├── i18n/                      # Traduções
│   ├── pt-br.yaml
│   └── en.yaml
├── scripts/
│   └── generate_index.py      # Script para gerar o índice
├── static/                    # Arquivos estáticos (imagens, etc.)
├── layouts/                   # Customizações de layout
└── themes/                    # Tema Hextra (via Hugo modules)
```

## Content Conventions

### Bilingual Content (OBRIGATÓRIO)

**Toda página DEVE ser criada em duas versões:**

1. **Português do Brasil** (idioma padrão): `index.md` ou `nome.md`
2. **Inglês**: `index.en.md` ou `nome.en.md`

O Hugo utiliza o sufixo do idioma no nome do arquivo para identificar a tradução. O idioma padrão (`pt-br`) **não** usa sufixo, enquanto o inglês usa `.en.md`.

### Post Location

Posts seguem o padrão de organização por **ANO/MÊS**:

```
content/YYYY/MM/slug-do-post/index.md      # pt-br
content/YYYY/MM/slug-do-post/index.en.md   # en
```

Exemplo:
```
content/2026/03/meu-homelab/index.md
content/2026/03/meu-homelab/index.en.md
```

### Frontmatter Format

Todo arquivo `.md` de conteúdo **DEVE** conter o seguinte frontmatter:

```yaml
---
title: "Título do Post"
date: '2026-03-26T14:00:00-03:00'
slug: slug-do-post
tags:
  - tag1
  - tag2
  - tag3
draft: false
---
```

#### Campos obrigatórios:

| Campo   | Descrição                                                    |
|---------|--------------------------------------------------------------|
| `title` | Título do post (usado em listagens e SEO)                    |
| `date`  | Data no formato ISO 8601 com timezone (`-03:00` para Brasil) |
| `tags`  | Lista de tags/palavras-chave relevantes ao conteúdo          |
| `draft` | `false` para publicado, `true` para rascunho                 |

#### Campos opcionais:

| Campo         | Descrição                                    |
|---------------|----------------------------------------------|
| `slug`        | Slug da URL (default: nome do diretório)     |
| `description` | Meta description para SEO                    |

### Tags (OBRIGATÓRIO)

Toda página **DEVE** ter tags com palavras-chave relevantes. Use tags que facilitem a categorização e busca do conteúdo.

Exemplos de boas tags:
- Temas: `home-assistant`, `automação`, `motociclismo`, `airsoft`, `programação`
- Tecnologias: `python`, `docker`, `proxmox`, `frigate`, `hugo`
- Tipos: `tutorial`, `review`, `projeto`, `dica`

### Creating New Posts

```bash
# 1. Criar diretório do post
mkdir -p content/YYYY/MM/slug-do-post

# 2. Criar arquivo pt-br (index.md) com frontmatter
# 3. Criar arquivo en (index.en.md) com frontmatter traduzido
# 4. Regenerar o índice
python scripts/generate_index.py
```

### Images in Posts

Imagens devem ser colocadas no mesmo diretório do post e referenciadas com caminho relativo:

```markdown
![Descrição da imagem](imagem.png)
```

Para imagens compartilhadas entre posts, use o diretório `static/images/`.

## Index Generation

A página principal (`content/_index.md`) é **auto-gerada** pelo script `scripts/generate_index.py`.

Este script:
- Percorre todos os arquivos `.md` em `content/`
- Extrai `title`, `date` e `tags` do frontmatter
- Agrupa posts por ano e mês
- Gera uma listagem cronológica (mais recentes primeiro)

**IMPORTANTE**: Execute `python scripts/generate_index.py` após adicionar ou modificar posts.

## Multilingual Configuration

O blog usa o sistema multilingual nativo do Hugo:

- **Idioma padrão**: `pt-br` (Português do Brasil)
- **Segundo idioma**: `en` (English)
- Traduções de strings da UI ficam em `i18n/pt-br.yaml` e `i18n/en.yaml`
- O switcher de idioma está no menu de navegação

### Menus Traduzidos (OBRIGATÓRIO)

O Hextra usa o campo `identifier` nos itens de menu para tradução via arquivos `i18n/`. Os menus são definidos **uma única vez** no nível raiz do `hugo.yaml` com o campo `identifier`, e as traduções ficam em `i18n/pt-br.yaml` e `i18n/en.yaml`.

```yaml
# hugo.yaml — menu com identifier
menu:
  main:
    - identifier: about
      name: Sobre
      pageRef: /about
      weight: 1
```

```yaml
# i18n/en.yaml — tradução para inglês
about: "About"
```

```yaml
# i18n/pt-br.yaml — tradução para português
about: "Sobre"
```

**NUNCA** defina menus dentro de `languages` no `hugo.yaml`, pois isso causa problemas com o sidebar do Hextra. Sempre use o `menu:` no nível raiz com `identifier` e traduza via `i18n/`.

Ao criar novos itens de menu:
1. Adicione o item com `identifier` em `menu:` no `hugo.yaml`
2. Adicione a tradução em `i18n/pt-br.yaml`
3. Adicione a tradução em `i18n/en.yaml`

## Hugo/Hextra Commands

```bash
# Iniciar servidor de desenvolvimento (com rascunhos)
hugo server -D

# Iniciar servidor (apenas publicados)
hugo server

# Gerar site para produção
hugo --minify

# Criar novo conteúdo (scaffold básico)
hugo new content/YYYY/MM/slug/index.md
```

## Gotchas and Notes

1. **Nunca edite `content/_index.md` manualmente** — ele é sobrescrito pelo script
2. **Sempre crie ambas versões** (pt-br e en) de cada post
3. **Tags são obrigatórias** — posts sem tags dificultam a navegação
4. **Use o timezone `-03:00`** nas datas (horário de Brasília)
5. **Imagens locais** devem ficar no mesmo diretório do post
6. O tema Hextra é importado via Hugo modules (`go.mod`/`go.sum`)
7. **Menus devem ser traduzidos** — use `identifier` no `hugo.yaml` e adicione traduções em `i18n/pt-br.yaml` e `i18n/en.yaml`
