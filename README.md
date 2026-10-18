# Local Product Listing Writer

A small Streamlit app that writes product listings (title, description, bullet points, hashtags) for sellers on Etsy, eBay, Amazon, Instagram and WhatsApp. It supports English, Hindi and Hinglish.

It runs fully on your own laptop with Gemma, an open-weight model, through Ollama. Product details never leave your computer, it costs nothing to run, and it works offline.

![Example output from gemma3:4b in English](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/ltccxvxsh5vrs9mx5i9r.png)

## Features

- Platform, tone and language options
- Strict prompt that tells the model to use only the seller's facts
- Guard that asks for more details instead of letting the model guess
- Claim checker that warns about risky words the seller never typed
- Model switch between `gemma3:1b` (fast) and `gemma3:4b` (more accurate)

## Setup

1. Install [Ollama](https://ollama.com/download) and pull a model:

```
   ollama pull gemma3:1b
   ollama pull gemma3:4b
```

2. Install the Python packages:

```
   pip install -r requirements.txt
```

3. Run the app:

```
   streamlit run listing_writer.py
```

## Known limits

Small models can still invent claims such as "durable" or "100%", and Hinglish quality is weak, especially on the 1b model. In Hindi mode the model sometimes ignores the "hashtags in English" rule.

The claim checker only knows English words, so claims written in Hindi or Hinglish can slip through. It also can't catch invented measurements or features. Always review the text before publishing.

## License

MIT. See the `LICENSE` file.

Built for the Hacktoberfest Open-Source AI Challenge, Week 2.
