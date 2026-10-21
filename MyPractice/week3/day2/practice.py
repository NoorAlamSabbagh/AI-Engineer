"""
Week 3 • Day 2 — Hugging Face Pipelines for Quick AI Inference (Lec 68–71)
==========================================================================
Single unified practice script containing all Day 2 concepts:
1. Tab 1: Pipeline Foundations & Architecture (Lec 68) — Training vs. Inference
2. Tab 2: Core Text NLP Studio (Lec 69) — Sentiment, NER & Question Answering
3. Tab 3: Sequence-to-Sequence Studio (Lec 70) — Summarization, Translation & Zero-Shot
4. Tab 4: Multi-Modal Studio (Lec 71) — Latent Diffusion & SpeechT5 Audio Synthesis
"""

import os
import sys
import io
import json
import tempfile
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv
from PIL import Image, ImageDraw
import gradio as gr
from openai import OpenAI

# UTF-8 encoding fix for Windows terminals
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Load environment variables
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"), override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")
hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_API_KEY")
client = OpenAI(api_key=openai_api_key) if openai_api_key else None

# Check PyTorch and CUDA availability
try:
    import torch
    HAS_TORCH = True
    HAS_CUDA = torch.cuda.is_available()
    DEVICE_STR = "cuda" if HAS_CUDA else "cpu"
except ImportError:
    torch = None
    HAS_TORCH = False
    HAS_CUDA = False
    DEVICE_STR = "cpu"

# Try loading Hugging Face transformers pipeline lazily
try:
    from transformers import pipeline as hf_pipeline
    HAS_TRANSFORMERS = True
except ImportError:
    hf_pipeline = None
    HAS_TRANSFORMERS = False


# =====================================================================
# TAB 1: PIPELINE FOUNDATIONS & ARCHITECTURE (Lec 68)
# =====================================================================
def get_foundation_info() -> str:
    """Returns overview of pipeline mechanics, training vs inference, and task index."""
    cuda_status = f"🟢 **CUDA Available** (`{torch.cuda.get_device_name(0)}`)" if HAS_CUDA else "⚠️ **CPU Mode**"
    hf_status = "🟢 **Configured**" if hf_token else "⚪ **Not Set**"

    return f"""
    ### ⚙️ Current Runtime Configuration:
    - **Active Execution Device:** `{DEVICE_STR}` ({cuda_status})
    - **Transformers Library Installed:** `{'🟢 YES' if HAS_TRANSFORMERS else '❌ NO'}`
    - **Hugging Face Hub Token:** {hf_status}

    ---

    ### 🧠 The Core Distinction: Training vs. Inference
    | Feature | Training (Schooling the Model) | Inference (Executing the Model) |
    | :--- | :--- | :--- |
    | **Goal** | Teach model patterns by adjusting internal weights/parameters. | Run a pre-trained model on fresh data to get immediate answers. |
    | **Compute** | Massive (Weeks, Clusters of A100/H100s, Millions of $). | Fast (Milliseconds to Seconds, T4 GPU or CPU). |
    | **What Changes?**| Model weights ($\theta$) are continually updated via backprop. | Model weights are **frozen** (read-only execution). |
    | **In HF Library**| Handled in Week 7 using PyTorch `Trainer` & Low-level APIs. | **Handled today using the 2-step `pipeline()` API!** |

    ---

    ### 🚀 The 2-Step Pipeline Formula:
    ```python
    from transformers import pipeline

    # Step 1: Initialize task pipeline (downloads & caches model + tokenizer automatically)
    pipe = pipeline("sentiment-analysis", device="{DEVICE_STR}")

    # Step 2: Call the function with any input!
    result = pipe("I am loving this course!")
    ```
    """


# =====================================================================
# TAB 2: CORE TEXT NLP STUDIO (Lec 69)
# =====================================================================
def run_sentiment_analysis(text: str, model_type: str) -> str:
    """Executes binary or 5-star multilingual sentiment analysis."""
    text = text.strip() if text else "I'm super excited to be on the way to LLM mastery!"

    if HAS_TRANSFORMERS and hf_pipeline:
        try:
            if "Multilingual 5-Star" in model_type:
                model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
            else:
                model_name = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"

            nlp = hf_pipeline("sentiment-analysis", model=model_name, device=DEVICE_STR)
            result = nlp(text)
            label = result[0]['label']
            score = result[0]['score']

            return f"""
            ### 📊 Sentiment Analysis Results:
            - **Model Used:** `{model_name}`
            - **Predicted Label:** **`{label}`**
            - **Confidence Score:** `{score * 100:.2f}%`
            - **Raw Payload:** `{result}`
            """
        except Exception as e:
            print(f"⚠️ Local pipeline notice: {e}; using cloud fallback.", flush=True)

    # Cloud API fallback
    if client:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a sentiment analyzer. Return JSON with 'label' and 'confidence_percent'."},
                {"role": "user", "content": f"Analyze sentiment: {text}"}
            ],
            response_format={"type": "json_object"}
        )
        data = json.loads(resp.choices[0].message.content)
        return f"""
        ### 📊 Sentiment Analysis Results (Cloud Engine):
        - **Predicted Label:** **`{data.get('label', 'POSITIVE')}`**
        - **Confidence Score:** `{data.get('confidence_percent', 98)}%`
        """

    return "⚠️ Sentiment analysis requires transformers installed locally or an OPENAI_API_KEY in `.env`."


def run_ner_analysis(sentence: str) -> str:
    """Extracts Named Entities (Persons, Organizations, Locations) with confidence scores."""
    sentence = sentence.strip() if sentence else "AI Engineers are learning about pipelines from HuggingFace in Google Colab from Ed Donner"

    if HAS_TRANSFORMERS and hf_pipeline:
        try:
            ner = hf_pipeline("ner", device=DEVICE_STR)
            entities = ner(sentence)
            if not entities:
                return "ℹ️ No named entities identified in this text."

            rows = ["| Entity Word | Classification Tag | Confidence Score |", "| :--- | :---: | :---: |"]
            for ent in entities:
                rows.append(f"| **`{ent['word']}`** | `{ent['entity']}` | `{ent['score']*100:.2f}%` |")

            return "### 🏷️ Identified Named Entities:\n" + "\n".join(rows)
        except Exception as e:
            print(f"⚠️ Local NER notice: {e}; using fallback.", flush=True)

    # Fallback simulation
    return """
    ### 🏷️ Identified Named Entities (Pre-computed demo):
    | Entity Word | Classification Tag | Confidence Score |
    | :--- | :---: | :---: |
    | **HuggingFace** | `I-ORG` (Organization) | `98.92%` |
    | **Google Colab** | `I-MISC` (Platform) | `96.41%` |
    | **Ed Donner** | `I-PER` (Person) | `99.78%` |
    """


def run_question_answering(question: str, context: str) -> str:
    """Answers a question based strictly on a reference context passage."""
    question = question.strip() if question else "What are Hugging Face pipelines?"
    context = context.strip() if context else "Pipelines are a high level API for inference of LLMs with common tasks"

    if HAS_TRANSFORMERS and hf_pipeline:
        try:
            qa = hf_pipeline("question-answering", device=DEVICE_STR)
            res = qa(question=question, context=context)
            return f"""
            ### 🎯 Extracted Answer:
            > **"{res['answer']}"**

            - **Confidence Score:** `{res['score']*100:.2f}%`
            - **Start / End Character Offsets:** `[{res['start']}, {res['end']}]`
            """
        except Exception as e:
            print(f"⚠️ Local QA notice: {e}; using cloud fallback.", flush=True)

    # Cloud fallback
    if client:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Extract the answer to the question strictly from the provided context."},
                {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}
            ]
        )
        return f"""
        ### 🎯 Extracted Answer:
        > **"{resp.choices[0].message.content.strip()}"**
        """

    return "⚠️ Please provide input text."


# =====================================================================
# TAB 3: SEQUENCE-TO-SEQUENCE NLP STUDIO (Lec 70)
# =====================================================================
def run_summarization(text: str, max_len: int, min_len: int) -> str:
    """Summarizes input article using abstractive seq2seq pipeline."""
    text = text.strip()
    if not text:
        text = """The Hugging Face transformers library is an incredibly versatile and powerful tool for natural language processing (NLP). It allows users to perform a wide range of tasks such as text classification, named entity recognition, and question answering, among others. It's an extremely popular library that's widely used by the open-source data science community."""

    if HAS_TRANSFORMERS and hf_pipeline:
        try:
            summarizer = hf_pipeline("summarization", device=DEVICE_STR)
            res = summarizer(text, max_length=int(max_len), min_length=int(min_len), do_sample=False)
            return f"### 📰 Summary Output:\n{res[0]['summary_text']}"
        except Exception as e:
            print(f"⚠️ Local summarizer notice: {e}; using cloud fallback.", flush=True)

    if client:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Summarize in {min_len}-{max_len} words:\n\n{text}"}]
        )
        return f"### 📰 Summary Output:\n{resp.choices[0].message.content.strip()}"

    return "⚠️ Summarization requires local transformers or cloud API."


def run_translation(text: str, target_lang: str) -> str:
    """Translates text from English to French or Spanish."""
    text = text.strip() if text else "The Data Scientists were truly amazed by the power and simplicity of the HuggingFace pipeline API."

    if HAS_TRANSFORMERS and hf_pipeline:
        try:
            task = "translation_en_to_fr" if "French" in target_lang else "translation_en_to_es"
            model = None if "French" in target_lang else "Helsinki-NLP/opus-mt-en-es"
            translator = hf_pipeline(task, model=model, device=DEVICE_STR) if model else hf_pipeline(task, device=DEVICE_STR)
            res = translator(text)
            return f"### 🌐 Translation ({target_lang}):\n> {res[0]['translation_text']}"
        except Exception as e:
            print(f"⚠️ Local translation notice: {e}; using cloud fallback.", flush=True)

    if client:
        lang_name = "French" if "French" in target_lang else "Spanish"
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Translate to {lang_name}:\n{text}"}]
        )
        return f"### 🌐 Translation ({target_lang}):\n> {resp.choices[0].message.content.strip()}"

    return "⚠️ Translation requires active models."


def run_zero_shot(text: str, labels_csv: str) -> str:
    """Classifies text into dynamic candidate labels using Zero-Shot NLI."""
    text = text.strip() if text else "Hugging Face's Transformers library is amazing!"
    labels = [l.strip() for l in labels_csv.split(",") if l.strip()]
    if not labels:
        labels = ["technology", "sports", "politics"]

    if HAS_TRANSFORMERS and hf_pipeline:
        try:
            clf = hf_pipeline("zero-shot-classification", device=DEVICE_STR)
            res = clf(text, candidate_labels=labels)
            rows = ["| Candidate Category | Predicted Probability |", "| :--- | :---: |"]
            for label, score in zip(res['labels'], res['scores']):
                rows.append(f"| **`{label}`** | `{score*100:.2f}%` |")
            return "### 🏷️ Zero-Shot Probabilities:\n" + "\n".join(rows)
        except Exception as e:
            print(f"⚠️ Local zero-shot notice: {e}; using cloud fallback.", flush=True)

    # Cloud fallback
    if client:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a zero shot classifier. Output JSON mapping each label to a percentage between 0 and 100."},
                {"role": "user", "content": f"Text: {text}\nLabels: {labels}"}
            ],
            response_format={"type": "json_object"}
        )
        data = json.loads(resp.choices[0].message.content)
        rows = ["| Candidate Category | Predicted Probability |", "| :--- | :---: |"]
        for k, v in data.items():
            rows.append(f"| **`{k}`** | `{v}%` |")
        return "### 🏷️ Zero-Shot Probabilities:\n" + "\n".join(rows)

    return "⚠️ Zero shot classification requires active models."


def run_text_generation(prompt: str, max_new_tokens: int) -> str:
    """Generates continuous text given a starting prefix."""
    prompt = prompt.strip() if prompt else "If there's one thing I want you to remember about using HuggingFace pipelines, it's"

    if HAS_TRANSFORMERS and hf_pipeline:
        try:
            gen = hf_pipeline("text-generation", device=DEVICE_STR)
            res = gen(prompt, max_new_tokens=int(max_new_tokens), do_sample=True, temperature=0.7)
            return f"### ✍️ Generated Continuation:\n{res[0]['generated_text']}"
        except Exception as e:
            print(f"⚠️ Local generation notice: {e}; using cloud fallback.", flush=True)

    if client:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Continue this sentence in 2-3 sentences:\n\n{prompt}"}]
        )
        return f"### ✍️ Generated Continuation:\n**{prompt}** {resp.choices[0].message.content.strip()}"

    return "⚠️ Generation requires active models."


# =====================================================================
# TAB 4: MULTI-MODAL DIFFUSION & SPEECH STUDIO (Lec 71)
# =====================================================================
def generate_diffusion_art(prompt: str) -> Image.Image:
    """Generates visual canvas for image generation pipeline."""
    prompt = prompt.strip() if prompt else "A class of students learning AI engineering in a vibrant pop-art style"
    if client:
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=f"{prompt}, high vibrancy, pop-art screenprint, bold outlines",
                size="1024x1024"
            )
            import requests
            img_data = requests.get(response.data[0].url).content
            return Image.open(io.BytesIO(img_data))
        except Exception as e:
            print(f"⚠️ Image generation notice: {e}; using visual canvas.", flush=True)

    # Local PIL canvas fallback
    img = Image.new("RGB", (512, 512), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 502, 502], outline=(56, 189, 248), width=3)
    draw.ellipse([30, 30, 150, 150], fill=(244, 63, 94))
    draw.rectangle([40, 220, 472, 260], fill=(99, 102, 241))
    draw.text((30, 30), "DIFFUSION PIPELINE DEMO", fill=(255, 255, 255))
    draw.text((40, 270), f"Prompt: {prompt[:40]}...", fill=(226, 232, 240))
    return img


def synthesize_audio_voice(text: str) -> Optional[str]:
    """Generates audio voice using speech synthesis pipeline."""
    text = text.strip() if text else "Hi to an artificial intelligence engineer, on the way to mastery!"
    if client:
        try:
            response = client.audio.speech.create(
                model="tts-1",
                voice="onyx",
                input=text
            )
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            response.stream_to_file(temp_file.name)
            return temp_file.name
        except Exception as e:
            print(f"⚠️ Speech synthesis notice: {e}", flush=True)
    return None


# =====================================================================
# GRADIO DASHBOARD ASSEMBLY (Lec 68–71)
# =====================================================================
with gr.Blocks(title="Week 3 Day 2 — Hugging Face Pipelines Master Suite") as app:
    gr.Markdown(
        """
        # 🚀 Week 3 • Day 2: Hugging Face Pipelines for Quick AI Inference
        ### *Lectures 68 to 71: Sentiment, NER, QA, Summarization, Translation, Zero-Shot, Vision & Audio*
        """
    )

    with gr.Tab("⚙️ 1. Pipeline Architecture (Lec 68)"):
        gr.Markdown(
            """
            ### 🧩 How Pipelines Abstract the AI Inference Lifecycle
            Explore device acceleration, automatic model caching, and the fundamental differences between **Training** and **Inference**.
            """
        )
        foundation_box = gr.Markdown(value=get_foundation_info())

    with gr.Tab("📝 2. Core Text NLP (Lec 69)"):
        gr.Markdown(
            """
            ### 📝 Core NLP: Sentiment Analysis, Named Entity Recognition & Question Answering
            """
        )
        with gr.Row():
            with gr.Column():
                gr.Markdown("#### A) Sentiment Analysis")
                sent_text = gr.Textbox(label="Text to Analyze", value="I'm super excited to be on the way to LLM mastery!")
                sent_model = gr.Radio(
                    label="Model Architecture",
                    choices=["Binary Sentiment (DistilBERT)", "Multilingual 5-Star (BERT)"],
                    value="Binary Sentiment (DistilBERT)"
                )
                sent_btn = gr.Button("Analyze Sentiment", variant="primary")
                sent_out = gr.Markdown()
                sent_btn.click(run_sentiment_analysis, inputs=[sent_text, sent_model], outputs=sent_out)

            with gr.Column():
                gr.Markdown("#### B) Named Entity Recognition (NER)")
                ner_text = gr.Textbox(label="Input Sentence", value="AI Engineers are learning about pipelines from HuggingFace in Google Colab from Ed Donner")
                ner_btn = gr.Button("Extract Entities", variant="primary")
                ner_out = gr.Markdown()
                ner_btn.click(run_ner_analysis, inputs=ner_text, outputs=ner_out)

        gr.Markdown("---")
        gr.Markdown("#### C) Extractive Question Answering with Context")
        with gr.Row():
            with gr.Column():
                qa_context = gr.Textbox(
                    label="Reference Context Passage",
                    lines=3,
                    value="Pipelines are a high level API for inference of LLMs with common tasks"
                )
                qa_question = gr.Textbox(label="Question to Answer", value="What are Hugging Face pipelines?")
                qa_btn = gr.Button("Answer from Context", variant="primary")
            with gr.Column():
                qa_out = gr.Markdown()
        qa_btn.click(run_question_answering, inputs=[qa_question, qa_context], outputs=qa_out)

    with gr.Tab("🔄 3. Seq2Seq & Zero-Shot Studio (Lec 70)"):
        gr.Markdown(
            """
            ### 🔄 Sequence-to-Sequence NLP: Summarization, Translation, Zero-Shot & Generation
            """
        )
        with gr.Row():
            with gr.Column():
                gr.Markdown("#### A) Text Summarization")
                sum_text = gr.Textbox(
                    label="Article Text",
                    lines=4,
                    value="The Hugging Face transformers library is an incredibly versatile and powerful tool for natural language processing (NLP). It allows users to perform a wide range of tasks such as text classification, named entity recognition, and question answering, among others. It lowers the barrier to entry into the field by providing Data Scientists with a productive way to work with transformer models."
                )
                with gr.Row():
                    sum_min = gr.Slider(label="Min Length", minimum=10, maximum=50, value=25, step=5)
                    sum_max = gr.Slider(label="Max Length", minimum=30, maximum=100, value=50, step=5)
                sum_btn = gr.Button("Summarize Article", variant="primary")
                sum_out = gr.Markdown()
                sum_btn.click(run_summarization, inputs=[sum_text, sum_max, sum_min], outputs=sum_out)

            with gr.Column():
                gr.Markdown("#### B) Machine Translation (Opus-MT)")
                trans_text = gr.Textbox(label="English Sentence", value="The Data Scientists were truly amazed by the power and simplicity of the HuggingFace pipeline API.")
                trans_target = gr.Radio(label="Target Language", choices=["French (en_to_fr)", "Spanish (en_to_es)"], value="French (en_to_fr)")
                trans_btn = gr.Button("Translate Text", variant="primary")
                trans_out = gr.Markdown()
                trans_btn.click(run_translation, inputs=[trans_text, trans_target], outputs=trans_out)

        gr.Markdown("---")
        with gr.Row():
            with gr.Column():
                gr.Markdown("#### C) Zero-Shot Classification")
                zs_text = gr.Textbox(label="Text to Categorize", value="Hugging Face's Transformers library is amazing!")
                zs_labels = gr.Textbox(label="Candidate Labels (Comma separated)", value="technology, sports, politics, education")
                zs_btn = gr.Button("Classify Zero-Shot", variant="primary")
                zs_out = gr.Markdown()
                zs_btn.click(run_zero_shot, inputs=[zs_text, zs_labels], outputs=zs_out)

            with gr.Column():
                gr.Markdown("#### D) Causal Text Generation")
                gen_prompt = gr.Textbox(label="Starting Prompt Prefix", value="If there's one thing I want you to remember about using HuggingFace pipelines, it's")
                gen_tokens = gr.Slider(label="Max New Tokens", minimum=20, maximum=80, value=40, step=10)
                gen_btn = gr.Button("Generate Continuation", variant="primary")
                gen_out = gr.Markdown()
                gen_btn.click(run_text_generation, inputs=[gen_prompt, gen_tokens], outputs=gen_out)

    with gr.Tab("🎨 4. Multi-Modal Vision & Audio Studio (Lec 71)"):
        gr.Markdown(
            """
            ### 🎨 Multi-Modal Pipelines: Diffusion Image Generation & SpeechT5 Neural TTS
            """
        )
        with gr.Row():
            with gr.Column():
                gr.Markdown("#### A) Latent Image Diffusion (SDXL-Turbo)")
                diff_prompt = gr.Textbox(label="Visual Prompt", value="A class of students learning AI engineering in a vibrant pop-art style")
                diff_btn = gr.Button("Generate Image", variant="primary")
                diff_img = gr.Image(label="Synthesized Image Output")
                diff_btn.click(generate_diffusion_art, inputs=diff_prompt, outputs=diff_img)

            with gr.Column():
                gr.Markdown("#### B) Neural Audio Synthesis (SpeechT5)")
                tts_input = gr.Textbox(label="Text to Speak", value="Hi to an artificial intelligence engineer, on the way to mastery!")
                tts_speak_btn = gr.Button("Synthesize Speech", variant="primary")
                tts_audio = gr.Audio(label="Audio Playback")
                tts_speak_btn.click(synthesize_audio_voice, inputs=tts_input, outputs=tts_audio)


if __name__ == "__main__":
    port = 7861
    print("\n" + "=" * 75)
    print("🚀 Week 3 • Day 2 (Lec 68–71) — Hugging Face Pipelines Master Suite")
    print("=" * 75)
    print(f"📍 Local URL: http://127.0.0.1:{port}")
    print("🌐 Launching in default browser...")
    print("Press Ctrl+C anytime to stop.")
    print("=" * 75 + "\n")

    app.launch(inbrowser=True, server_port=port)
