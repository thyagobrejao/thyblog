---
title: "Thyago.dev.br — How I built a blog with Hugo, Hextra, and zero databases"
date: '2026-03-25T14:00:00-03:00'
slug: thyblog
tags:
  - project
  - hugo
  - hextra
  - github-pages
  - python
  - blog
  - ci-cd
draft: false
---

I always wanted to have a personal blog. The kind where you open it and think: "hm, cool, this guy actually did this." But between wanting and doing there's a chasm called **"I don't want to deal with WordPress"**, databases, hosting bills, and finding out your blog got hacked because you forgot to update a plugin from 2019.

Then one fine day I watched Fábio Akita explain how he built [The M.Akita Chronicles](https://akitaonrails.com/2026/02/19/frontend-sem-framework-bastidores-do-the-m-akita-chronicles/#hugo--hextra-blog-sem-banco-de-dados) using **Hugo + Hextra** — no JavaScript framework, no database, no drama. And I thought: "If Akita does it this way, who am I to disagree?"

That was the inspiration I needed. Thanks, Akita. This blog existing is your fault. 😄

## What is Hugo (and why it's absurdly fast)

**Hugo** is a static site generator written in Go. You write your posts in Markdown, run a command, and it spits out a complete HTML site in milliseconds. Seriously. Milliseconds. While Next.js is still deciding which React version to use, Hugo has already built, deployed, and is sipping coffee.

No database, no PHP server running, nothing. Just pure HTML files served directly. It's the web as it should be — fast, simple, and no surprises at 3 AM.

## Hextra — The theme that does the heavy lifting

[Hextra](https://github.com/imfing/hextra) is a documentation theme for Hugo that works surprisingly well as a blog theme. It comes with:

- 🔍 **Built-in search** — no Algolia or ElasticSearch needed
- 📑 **Navigation sidebar** — automatic organization by sections
- 🌙 **Dark mode** — because we're in 2026, not 2010
- 🌐 **Multilingual support** — the blog runs in pt-br and en
- 📋 **Table of Contents** — automatically generated from headers

All of this without a single line of custom JavaScript. Akita was right: you can have a modern frontend without a framework.

## Blog structure

The content is organized in a way that makes sense (at least to me):

```
content/
├── _index.md              # Main page (auto-generated! 🤖)
├── about.md               # About me (pt-br)
├── about.en.md            # About me (en)
├── projetos/              # Project posts
│   ├── saiu-a-escala/
│   └── thyblog/           # ← You are here!
├── tecnologias/           # Tech posts
├── automacao-residencial/ # Home automation
├── motociclismo/          # Motorcycles 🏍️
└── armas-de-pressao/      # Airsoft & air guns 🎯
```

Each post lives inside its own folder with an `index.md` (pt-br) and an `index.en.md` (en). Yes, **every post is bilingual**. Because if you're going to do it, do it right.

## The magic script: `generate_index.py`

This is one of the coolest parts of the project. Hugo is fantastic, but it doesn't automatically generate a chronological index page with all posts grouped by month and year. So I wrote a Python script that does exactly that.

The `generate_index.py` script:

1. **Scans** the entire `content/` directory looking for `.md` files
2. **Extracts** frontmatter (title, date, tags) from each post
3. **Skips** drafts and pages marked as "coming soon"
4. **Groups** posts by year and month
5. **Generates** the `_index.md` and `_index.en.md` files — both the root index and the section-level indices (projects, tech, etc.)

The result is a beautiful, organized main page with links to all posts, formatted dates, and tags. All automated, all in two languages.

And the best part? It runs in the CI/CD pipeline before Hugo builds. That means I never need to worry about manually updating the index. I write the post, push it, and everything else happens on its own.

## GitHub Pages deployment — painless CI/CD

The deployment is handled via **GitHub Actions** and it's beautifully simple:

1. I `git push` to the `main` branch
2. GitHub Actions wakes up and starts the workflow:
   - Installs Hugo (extended version, because we have class)
   - Installs Go (required for Hugo Modules)
   - Installs Python
   - **Runs `generate_index.py`** to generate updated indices
   - **Builds the site** with `hugo --gc --minify`
   - Uploads the artifact
3. The deploy job publishes to GitHub Pages
4. Cloudflare handles DNS and SSL for the `thyago.dev.br` domain

**Total infrastructure cost: $0.00.** 🎉

The repository is public, by the way. The entire blog code is on [GitHub](https://github.com/thyagobrejao/thyblog). Full transparency — and if anyone wants to copy the idea, be my guest.

## Multilingual — Because the internet is big

All content is produced in **Brazilian Portuguese** (default language) and **English**. Hugo manages this natively through file suffixes:

- `index.md` → Portuguese
- `index.en.md` → English

Navigation menus, labels, and UI strings are also translated via `i18n/` files. The language switcher sits at the top of the page, discreet and functional.

## The full stack

For those who like an organized list (I do):

| Technology | Purpose |
|---|---|
| **Hugo** | Static site generator |
| **Hextra** | Theme (imported via Hugo Modules) |
| **Python** | Index generation script |
| **GitHub Actions** | Automated CI/CD |
| **GitHub Pages** | Free hosting |
| **Cloudflare** | DNS + SSL |
| **Markdown** | Post format |
| **Go** | Required for Hugo Modules |

## The inspiration — Thanks, Akita

As I mentioned at the beginning, the biggest inspiration for this blog came from **Fábio Akita's** post about the behind-the-scenes of [The M.Akita Chronicles](https://akitaonrails.com/2026/02/19/frontend-sem-framework-bastidores-do-the-m-akita-chronicles/#hugo--hextra-blog-sem-banco-de-dados). The idea that you can have a modern, beautiful, and functional blog without a single JavaScript framework convinced me immediately.

Akita took things to another level — with custom shortcodes, newsletter templates, podcast transcriptions... I'm more modest. My blog has posts, search, dark mode, and coffee. But the essence is the same: **content first, framework never**.

## The result

What started as "I'll make a little blog" became a project I genuinely enjoy maintaining. Writing in Markdown is a pleasure, deployment is instant, and the site loads faster than I can blink.

If you're thinking about creating a blog, seriously consider this stack. It's free, it's fast, it's elegant — and you'll learn about CI/CD, DNS, and static site generation in the process.

The code is all on [GitHub](https://github.com/thyagobrejao/thyblog). Snoop around at will.

---

*Built with Hugo, Hextra, a Python script, and a generous dose of "if Akita does it, so can I".* 🚀
