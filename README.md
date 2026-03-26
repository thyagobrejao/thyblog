# Thyago.dev.br 🚀

This is the repository for my personal blog, built with [Hugo](https://gohugo.io/) and the [Hextra](https://github.com/imfing/hextra) theme.

You can visit the live blog at [thyago.dev.br](https://thyago.dev.br/).

## 🌟 Features

- **Static Site Generation:** Lightning fast, built with Hugo.
- **Multilingual Support:** All content is available in both Portuguese (Brazil) and English.
- **Auto-generated Index:** Uses a custom Python script to automatically group and list posts chronologically by year and month.
- **Modern Theme:** Powered by Hextra (a clean, responsive, and documented-oriented theme).

## 🛠️ Tech Stack

- [Hugo](https://gohugo.io/)
- [Hextra Theme](https://hextra.imfing.com/)
- Python (for index generation)

## 📁 Project Structure

```text
thyblog/
├── content/               # Blog content and sections
│   ├── about.md           # About page
│   ├── _index.md          # Auto-generated main index
│   └── YYYY/MM/slug/      # Posts organized by date
├── i18n/                  # Translation files for UI strings
├── scripts/               # Helper scripts
│   └── generate_index.py  # Python script to generate chronological indices
├── static/                # Static assets (images, fonts, etc.)
└── hugo.yaml              # Main Hugo configuration file
```

## 🚀 Getting Started

### Prerequisites

- [Hugo Extended](https://gohugo.io/installation/)
- [Python 3](https://www.python.org/downloads/) (for the index generation script)

### Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/thyagobrejao/thyblog.git
   cd thyblog
   ```

2. Start the Hugo development server (including drafts):
   ```bash
   hugo server -D
   ```
   The site will be available at `http://localhost:1313/`.

### Managing Content

To create a new post or section:
1. Create a bilingual entry in `content/` (e.g., `index.md` for `pt-br` and `index.en.md` for `en`).
2. Include the required frontmatter (`title`, `date`, `tags`, `draft`).
3. Run the index generation script to update the main listing:
   ```bash
   python3 scripts/generate_index.py
   ```

## ⚖️ License

The source code and scripts in this repository are licensed under the **MIT License**.

The written content, articles, and images located in the `content/` directory are licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)**. 

See the [LICENSE](LICENSE) file for more details.
