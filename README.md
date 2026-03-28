# Dagadya

Dagadya is a voice-first AI platform built for farmers in Uttarakhand, India, especially for people who do not have smartphones or reliable internet access.

The name **Dagadya** comes from a Garhwali/Pahadi word meaning friend or companion.

## Why Dagadya Exists

Uttarakhand loses roughly **44,882 hectares of crops annually** due to climate events. At the same time, most digital agriculture tools fail to reach the people who need them most:

- Around **62% of rural Uttarakhand** does not have reliable internet access.
- Existing advisory platforms are mostly app-based and smartphone-dependent.
- Insurance support is broken: about **59% of PMFBY-enrolled farmers** reportedly never received claims.

Dagadya is built to remove these barriers by working over normal phone calls.

## What It Does

A farmer dials a number and speaks in Hindi or Hinglish.

Dagadya responds through natural voice conversation and provides:

- Hyper-local crop advisories
- Real-time weather alerts
- Mandi price information
- Guided crop insurance claim assistance

No smartphone. No app installation. No internet required for the farmer.

## Standout Capability: Proactive Outbound Calling

Dagadya does not only wait for farmers to call.

It can proactively call farmers to warn them about incoming weather risks before crop damage happens. This flips the default advisory model: the system reaches the farmer first.

Compared with platforms like Bharat-VISTAAR, Kisan e-Mitra, and DeHaat, this proactive calling flow is a key differentiator.

## Demo Flow

The demo includes two modes:

1. **Inbound call flow**
	- A farmer dials the Dagadya number.
	- The AI agent handles conversation end-to-end in voice and answers all the queries.

2. **Outbound "Call Me" flow**
	- Dagadya calls farmer before frost or hail hit your field.

During the call, a live transcript UI (plain HTML + Tailwind CSS) displays the conversation in real time.

## Architecture and Tech Stack

- **Telephony (PSTN calls):** Twilio
- **Voice pipeline orchestration:** Pipecat
- **Speech-to-Text (Hindi):** Sarvam AI Saarika
- **LLM reasoning:** Gemini 2.0 Flash
- **Text-to-Speech (Hindi):** Sarvam AI Bulbul
- **WebSocket backend:** FastAPI
- **Deployment:** Railway
- **Weather data:** Open-Meteo API
- **Mandi price data:** Agmarknet API


## Hackathon Context

Building in under 24 hours at **BUILD4Bharat Hackathon 9.0** at **UPES Dehradun** (March 28-29, 2026).

## Vision

Dagadya aims to be a reliable AI companion for small and marginal farmers by making climate intelligence, market information, and insurance guidance accessible through the most universal interface in rural India: a basic phone call.
