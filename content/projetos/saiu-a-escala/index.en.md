---
title: "Saiu a Escala — How I Automated the Biggest Headache in Church Ministry"
date: '2026-03-26T18:00:00-03:00'
slug: saiu-a-escala
tags:
  - project
  - django
  - python
  - flutter
  - celery
  - firebase
  - whatsapp
  - saas
draft: false
---

If you've ever been a ministry coordinator at a church, you know the most fun part of the job is... **building the monthly schedule**. (That was sarcasm, in case it wasn't obvious.)

Yep, **Saiu a Escala** (roughly "The Schedule is Out") was born from that exact pain. It's a web + mobile app system that handles all the scheduling management for churches and ministries — from auto-generating fair schedules to sending WhatsApp notifications to that one volunteer who always "forgets" it's their turn on Sunday.

## The problem (or: why I lost some hair)

Imagine you coordinate a group of 30 volunteers. Every month you need to build a fair schedule while respecting who's traveling, who has date restrictions, who swapped with whom via WhatsApp at 11 PM... Now multiply that by several groups, multiple masses, and various time slots.

There you go. That's why ministry coordinators age faster.

**Saiu a Escala** solves this. With one click, the entire month's schedule is automatically generated. The system knows who can serve, who can't, who's been on too often, and who "owes" a turn. Then it notifies everyone — via WhatsApp, email, and push notifications on their phones. Simple as that.

## The recipe (or: how everything connects)

### 🐍 Django + Python — The brains of the operation

The backend runs on **Django** (Python), which handles absolutely everything: authentication, group and member management, schedule generation, REST API for the mobile app, admin panel, and the product's landing page. It's the classic "does everything and never complains" framework.

### 📱 Flutter — Native apps for Android and iOS

The mobile app was built with **Flutter**, which means a single codebase delivers apps for both Google Play and the App Store. Volunteers use the app to view their schedules, mark dates when they can't serve, request swaps with other members, and receive notifications.

### ⚡ Celery — The tasks nobody wants to wait for

Generating complex schedules, sending dozens of notifications, processing swaps... all of this happens in the background thanks to **Celery** with **Redis** as the message broker. The user clicks "Generate Schedule", the system responds "On it, be right back!", and Celery goes behind the scenes doing the heavy lifting without freezing anyone's screen.

### 📲 WhatsApp Web — The channel everyone actually reads

Let's be honest: nobody checks email, but everyone lives on WhatsApp. That's why the most important notifications — like "your schedule is out" or "someone wants to swap with you" — go straight to the volunteer's WhatsApp. The integration uses the **WhatsApp Web** API to send automatic, personalized messages.

### 📧 Email — The reliable backup

For those who prefer it (or for more formal requirements like invitations and confirmations), the system also sends **transactional emails**. It's the "serious" communication channel — the one that lands in your inbox when WhatsApp can't reach you.

### 🔔 Firebase Cloud Messaging — Push notifications on mobile

You know that notification that pops up on your phone screen even when the app is closed? That's **Firebase Cloud Messaging (FCM)** at work. The backend fires notifications through Firebase, delivering them to both Android and iOS. "Hey, tomorrow is your day at the liturgy!" — and the volunteer has no more excuses.

## How everything connects

If I were to sketch this on a napkin, it would look something like this:

1. The **coordinator** accesses the web dashboard (Django) and generates the schedule
2. Django pushes the generation task to **Celery**, which processes it in the background
3. When the schedule is ready, Celery fires the notifications:
   - **WhatsApp Web** → message straight to the volunteer's WhatsApp
   - **Email** → for those who prefer it (and for formal records)
   - **Firebase (FCM)** → push notification on mobile via the Flutter app
4. The **volunteer** opens the **Flutter app** or the website, views their schedule, marks unavailable dates, and requests swaps
5. Swaps trigger new automatic notifications for everyone involved

All orchestrated, all automatic, all without needing to open that Saturday afternoon Excel spreadsheet.

## The result

Today, **Saiu a Escala** runs in hundreds of parishes and communities. Thousands of mass schedules generated, thousands of volunteers and servants organized, and a bunch of coordinators who now use their free time to... well, enjoy a peaceful cup of coffee. ☕

If you're curious, check it out at [saiuaescala.com.br](https://saiuaescala.com.br).

---

*Made with lots of coffee, faith, and a few questionable late nights.* 🙏
