---
title: "Saiu a Escala — Como eu automatizei a maior dor de cabeça das paróquias"
date: '2026-03-26T18:00:00-03:00'
slug: saiu-a-escala
tags:
  - projeto
  - django
  - python
  - flutter
  - celery
  - firebase
  - whatsapp
  - saas
draft: false
---

Se você já foi coordenador de alguma pastoral na igreja, sabe que a parte mais divertida do trabalho é... **montar a escala do mês**. (Isso foi ironia, caso não tenha ficado claro.)

Pois é, **Saiu a Escala** nasceu exatamente dessa dor. É um sistema web + app mobile que cuida de toda a gestão de escalas de igrejas e pastorais — desde a geração automática da escala até a notificação no WhatsApp do servo que insiste em esquecer que é a vez dele no domingo.

## O problema (ou: por que eu perdi cabelos)

Imagine que você coordena um grupo com 30 voluntários. Todo mês precisa montar uma escala justa, respeitando quem viajou, quem tem restrição de data, quem trocou com quem pelo grupo do WhatsApp às 23h da noite... Agora multiplique isso por vários grupos, várias missas e vários horários.

Pronto. É por isso que coordenadores de pastoral envelhecem mais rápido.

O **Saiu a Escala** resolve isso. Com um clique, a escala do mês inteiro é gerada automaticamente. O sistema sabe quem pode, quem não pode, quem já serviu demais e quem está "devendo". Depois, avisa todo mundo — pelo WhatsApp, por e-mail e por push notification no celular. Simples assim.

## A receita do bolo (ou: como tudo se conecta)

### 🐍 Django + Python — O cérebro da operação

O backend roda com **Django** (Python), que cuida de absolutamente tudo: autenticação, cadastro de grupos e membros, geração das escalas, API REST para o mobile, painel administrativo e a landing page do produto. É o clássico "faz tudo e não reclama".

### 📱 Flutter — Apps nativos para Android e iOS

O app mobile foi construído com **Flutter**, o que significa que com uma única base de código eu tenho aplicativo tanto na Google Play quanto na App Store. Os voluntários usam o app para ver suas escalas, marcar datas que não podem servir, pedir trocas com outros membros e receber notificações.

### ⚡ Celery — As tarefas que ninguém quer esperar

Gerar escalas complexas, enviar dezenas de notificações, processar trocas... tudo isso acontece em segundo plano graças ao **Celery** com **Redis** como broker de mensagens. O usuário clica em "Gerar Escala", o sistema responde "Tá, já volto!", e o Celery vai lá nos bastidores fazer o trabalho pesado sem travar a tela de ninguém.

### 📲 WhatsApp Web — O canal que todo mundo lê

Sejamos honestos: ninguém abre e-mail, mas todo mundo vive no WhatsApp. Por isso, as notificações mais importantes — como "sua escala saiu" ou "alguém quer trocar com você" — vão direto pro WhatsApp do servo. A integração usa a API do **WhatsApp Web** para enviar mensagens automáticas e personalizadas.

### 📧 E-mail — O backup confiável

Para quem prefere (ou para requisitos mais formais, como convites e confirmações), o sistema também envia **e-mails transacionais**. É o canal "sério" da comunicação — aquele que vai parar na caixa de entrada quando o WhatsApp não alcança.

### 🔔 Firebase Cloud Messaging — Push notifications no celular

Sabe aquela notificação que aparece na tela do celular mesmo quando o app está fechado? É o **Firebase Cloud Messaging (FCM)** em ação. O backend dispara as notificações via Firebase, que entrega tanto para Android quanto para iOS. "Ei, amanhã é seu dia na liturgia!" — e o servo não tem mais desculpa.

## Como tudo se conecta

Se eu fosse desenhar num guardanapo, seria mais ou menos assim:

1. O **coordenador** acessa o painel web (Django) e gera a escala
2. O Django empurra a tarefa de geração pro **Celery**, que processa em segundo plano
3. Quando a escala fica pronta, o Celery dispara as notificações:
   - **WhatsApp Web** → mensagem direto no zap do servo
   - **E-mail** → para quem prefere (e pra ter registro formal)
   - **Firebase (FCM)** → push notification no celular via app Flutter
4. O **servo** abre o **app Flutter** ou o site, vê sua escala, marca indisponibilidades e pede trocas
5. As trocas geram novas notificações automáticas para os envolvidos

Tudo orquestrado, tudo automático, tudo sem precisar abrir o Excel das 3 da tarde de um sábado.

## O resultado

Hoje o **Saiu a Escala** roda em centenas de paróquias e comunidades. São milhares de escalas de missa geradas, milhares de servos e voluntários organizados, e um monte de coordenadores que agora usam o tempo livre para... bom, tomar um café em paz. ☕

Se ficou curioso, dá uma olhada em [saiuaescala.com.br](https://saiuaescala.com.br).

---

*Feito com muito café, fé e algumas madrugadas questionáveis.* 🙏
