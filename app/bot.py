import os
from pipecat.serializers.twilio import TwilioFrameSerializer
from pipecat.audio.vad.silero import SileroVADAnalyzer 
from pipecat.frames.frames import LLMRunFrame
from pipecat.audio.vad.vad_analyzer import VADParams
from pipecat.transcriptions.language import Language

from pipecat.services.groq import GroqLLMService
from pipecat.services.sarvam.stt import SarvamSTTService
from pipecat.services.sarvam.tts import SarvamTTSService

from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair

from pipecat.transports.websocket.fastapi import FastAPIWebsocketParams, FastAPIWebsocketTransport

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

SYSTEM_PROMPT = """You are Dagadya, a voice assistant for farmers in Uttarakhand. You speak on phone calls.

STRICT RULES:
- Maximum 2 sentences. Hard limit.
- Stay ONLY on the topic the farmer asked about. Never change subject.
- Never mention weather unless farmer asks about weather.
- Never mention mandi unless farmer asks about mandi.
- Never offer multiple topics in one response.
- If farmer says something unclear, ask "Kya poochh rahe hain aap?" and nothing else.

LANGUAGE:
- Reply in hindi.
- Simple words only. No technical terms.

GREETING: First message only — "Namaste, main Dagadya hoon. Apka naam kya hai or aap kaha rehte hai?"

YOU ONLY HELP WITH:
- Weather alerts
- Crop disease
- Mandi prices  
- PMFBY insurance
- Disaster warnings

If farmer asks anything outside these topics, say "Yeh mere expertise se bahar hai, lekin kheti ke baare mein poochh sakte hain."
"""

async def run_bot(streamSid : str , callSid : str , websocket):
    logger.info(f"Starting bot for call {callSid}")

    serializer = TwilioFrameSerializer(
        stream_sid=streamSid,
        call_sid=callSid,
        auth_token= os.getenv("TWILIO_AUTH_TOKEN"),
        account_sid= os.getenv("TWILIO_ACCOUNT_SID")
    )

    vad_analyzer = SileroVADAnalyzer(
        params= VADParams(
            start_secs=0.1,
            stop_secs=0.3
        )
    )

    transport = FastAPIWebsocketTransport(
        websocket= websocket,
        params= FastAPIWebsocketParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            add_wav_header=False,
            vad_analyzer=vad_analyzer,
            serializer=serializer,
        )
    )

    stt = SarvamSTTService(
        api_key=os.getenv("SARVAM_API_KEY"),
        model="saaras:v3",
        params=SarvamSTTService.InputParams(
            mode="codemix"
        )
    )

    llm = GroqLLMService(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.1-8b-instant"
    )

    
    tts = SarvamTTSService(
        api_key=os.getenv("SARVAM_API_KEY"),
        voice_id="priya",
        model="bulbul:v3",
        params=SarvamTTSService.InputParams(
            language=Language.HI,
            pace=1.1,
            temperature=0.8
        )
    )

    messages=[
        {
            "role" : "system",
            "content" : SYSTEM_PROMPT
        }
    ]
    context = LLMContext(messages=messages)
    context_aggregator = LLMContextAggregatorPair(context)

    pipeline = Pipeline([
        transport.input(),
        stt,
        context_aggregator.user(),
        llm,
        tts,
        transport.output(),
        context_aggregator.assistant()
    ])

    task = PipelineTask(
        pipeline,
        params = PipelineParams(allow_interruptions=True)
    )

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        logger.info("Farmer connected")
        messages.append({
            "role" : "system",
            "content" : "Greet the farmer warmly in hindi and ask their basic info"
        })

        await task.queue_frames([LLMRunFrame()])


    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info("Farner disconnected")
        await task.cancel()

    
    runner = PipelineRunner(handle_sigint=False)
    await runner.run(task)