---
title: "VoltWise — Because charging an EV shouldn’t feel like installing 15 different apps"
date: '2026-03-27T07:00:00-03:00'
slug: voltwise
tags:
  - project
  - open-source
  - electric-vehicles
  - ocpp
  - golang
  - django
  - flutter
  - vue
  - saas
  - iot
draft: false
---

If you own (or have tried to use) an electric vehicle, you’ve probably been through this:

👉 arrive at the charger  
👉 open the wrong app  
👉 download another app  
👉 create an account  
👉 verify email  
👉 try again  
👉 still doesn’t work  

Congrats, you just used more phone battery than your car.

That’s basically what made me start **VoltWise**.

---

## 💡 The idea

VoltWise starts with a simple (and slightly ambitious) goal:

> Unify the EV charging ecosystem.

Today, every charging station has:

- its own app  
- its own backend  
- its own API  
- its own problems  

The idea is to build an open-source platform that:

- helps small hotels and businesses offer charging  
- provides a standardized backend  
- offers a unified mobile app  
- integrates with other systems in the future  

Yes, it’s ambitious. But someone has to start.

---

## 🏗️ Architecture (aka: how I made things more complex on purpose)

![VoltWise Architecture](/images/voltwise-architecture.png)

> Overview of VoltWise architecture, including OCPP communication, local agent, and cloud.

The project is split into multiple modules:

- **voltwise-core** → shared business logic  
- **voltwise-ocpp** → charger communication  
- **voltwise-cloud** → central backend and API  
- **voltwise-agent** → local software (hotel / site)  
- **voltwise-portal** → web dashboard  
- **voltwise-mobile** → user app  
- **voltwise-docs** → documentation (because I try to be organized)

---

## ⚙️ Tech stack

A mix of experience, curiosity, and “I want to try this”.

### Backend / Core

- **Go (Golang)**  
  - voltwise-core  
  - voltwise-ocpp  

Why: performance and great concurrency for device communication.

---

### Cloud / API

- **Django + Django REST Framework**

Why: fast development and a very mature ecosystem.

---

### Mobile

- **Flutter**

Why: single codebase for Android and iOS.

---

### Web Portal

- **Vue.js**

Why: clean, simple, and efficient.

---

### Local Agent

Still undecided 🤔

Options:

- Go (very likely)
- Python
- maybe Flutter Desktop

---

## 🔌 OCPP (the important part)

The project will use:

- **OCPP 1.6**

This is basically the language chargers speak.

Without it → nothing works  
With it → things *should* work 😅

---

## 🌍 Future vision

This is not just another project.

It’s an attempt to solve a real problem:

> today you need a different app for every charging network.

In the future, VoltWise could:

- integrate with other platforms  
- enable roaming between networks  
- unify payments  
- become an open charging hub  

And of course…

👉 maybe turn into a SaaS (because open source doesn’t pay for coffee).

---

## 🚀 Why I’m building this

- technical challenge  
- learning IoT and OCPP  
- building something actually useful  
- improving my portfolio  
- and because it sounded like a great idea at 2AM  

---

## 📌 Next steps

- [x] structure repositories  
- [x] start core in Go  
- [x] implement basic OCPP (with WebSocket and basic auth)  
- [x] build Django backend (and connect to Vue.js Portal)  
- [x] document everything  
- [ ] integrate local Agent with the Cloud  
- [ ] finish and launch the Mobile App  

---

If you made it this far, you’re already more involved than most people 😄

I’ll keep documenting everything here.