---
title: "VoltWise — Porque carregar carro elétrico não deveria ser um jogo de baixar 15 apps"
date: '2026-03-27T07:00:00-03:00'
slug: voltwise
tags:
  - projeto
  - open-source
  - veiculos-eletricos
  - ocpp
  - golang
  - django
  - flutter
  - vue
  - saas
  - iot
draft: false
---

Se você tem um carro elétrico ou já tentou usar um, provavelmente passou por isso:

👉 chega no carregador  
👉 abre o app errado  
👉 baixa outro app  
👉 cria conta  
👉 confirma email  
👉 tenta de novo  
👉 não funciona  

Parabéns, você acabou de gastar mais bateria do celular do que do carro.

Foi basicamente isso que me fez começar o **VoltWise**.

---

## 💡 A ideia

O VoltWise nasce com uma proposta simples (e ousada):

> Unificar o ecossistema de carregamento de veículos elétricos.

Hoje, cada eletroposto tem seu próprio app, seu próprio sistema, sua própria API… e sua própria dor de cabeça.

A ideia aqui é criar uma plataforma open source que:

- permita que pequenos hotéis, pousadas e estabelecimentos instalem carregadores facilmente  
- ofereça um backend padronizado para gerenciamento  
- disponibilize um app único para usuários  
- integre com outros sistemas no futuro  

Sim, é ambicioso. Mas alguém precisa começar.

---

## 🏗️ Arquitetura (ou: onde eu me compliquei sozinho)

![Arquitetura do VoltWise](/images/voltwise-architecture.png)

> Visão geral da arquitetura do VoltWise, incluindo comunicação OCPP, agent local e cloud.

O projeto foi dividido em vários módulos, porque monolito aqui só se for de café ☕:

- **voltwise-core** → regras de negócio e estruturas comuns  
- **voltwise-ocpp** → comunicação com os carregadores (o coração do negócio)  
- **voltwise-cloud** → backend central e API  
- **voltwise-agent** → software que roda no local (hotel, pousada, etc)  
- **voltwise-portal** → interface web para gerenciamento  
- **voltwise-mobile** → app para usuários  
- **voltwise-docs** → documentação (porque eu finjo que sou organizado)

---

## ⚙️ Tecnologias escolhidas

Aqui foi uma mistura de experiência, curiosidade e um pouco de “quero testar isso aqui”.

### Backend / Core

- **Go (Golang)**  
  - voltwise-core  
  - voltwise-ocpp  

Motivo: performance, concorrência e porque faz sentido para comunicação com dispositivos.

---

### Cloud / API

- **Django + Django REST Framework**

Motivo: produtividade absurda, ecossistema maduro e porque eu já tenho bastante experiência.

---

### Mobile

- **Flutter**

Motivo: um código só pra Android e iOS, e já uso em outros projetos.

---

### Portal Web

- **Vue.js**

Motivo: leve, organizado e sem sofrimento desnecessário.

---

### Agent (local)

Aqui ainda está em aberto 🤔

Possibilidades:

- Go (faz muito sentido)
- Python
- ou até Flutter Desktop

Esse é um dos pontos que ainda vou explorar.

---

## 🔌 OCPP (a parte que realmente importa)

O projeto vai usar o padrão:

- **OCPP 1.6**

Que é basicamente o “idioma” que os carregadores falam.

Sem isso, nada funciona.

Com isso, tudo funciona (ou pelo menos deveria 😅).

---

## 🌍 Visão de futuro

A ideia não é só criar mais um sistema.

É tentar resolver um problema real:

> hoje você precisa de um app diferente para cada rede de carregamento.

No futuro, o VoltWise pode:

- integrar com outras plataformas  
- servir como base para roaming entre redes  
- permitir pagamentos unificados  
- virar um hub de carregamento open source  

E claro…

👉 talvez virar um SaaS também, porque ninguém vive só de open source e café.

---

## 🚀 Por que estou fazendo isso?

- desafio técnico  
- aprender mais sobre IoT e OCPP  
- construir algo útil de verdade  
- melhorar meu portfólio  
- e porque parecia uma boa ideia às 2h da manhã  

---

## 📌 Próximos passos

- [x] estruturar os repositórios  
- [x] iniciar o core em Go  
- [x] implementar OCPP básico (com WebSocket e autenticação basic)  
- [x] subir o backend em Django (e conectar ao Portal Vue.js)  
- [x] começar a documentação  
- [ ] integrar o agente local (Agent) com a Cloud  
- [ ] finalizar e lançar o App Mobile  

---

Se você leu até aqui, já está mais envolvido no projeto do que muita gente 😄

Se quiser acompanhar (ou contribuir no futuro), fica de olho que vou documentar tudo por aqui.