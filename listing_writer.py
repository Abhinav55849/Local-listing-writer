import re

import streamlit as st
import ollama

st.set_page_config(page_title="Local Listing Writer", page_icon="🛍️")

st.title("🛍️ Local Product Listing Writer")
st.caption(
    "Runs 100% on your own laptop using an open-weight model (Gemma via Ollama). "
    "Your product details never leave your computer, and it costs nothing to run."
)
MODEL = st.sidebar.selectbox("Model (runs locally)", ["gemma3:1b", "gemma3:4b"])
st.sidebar.caption("Bigger model = better quality, slower, needs more RAM.")

product = st.text_input("Product name", placeholder="Handmade jute tote bag")
details = st.text_area(
    "Key details (material, size, colour, price, who it is for)",
    placeholder="Eco-friendly jute, 15x12 inch, cotton lining, Rs 349, good for college and shopping",
)

col1, col2, col3 = st.columns(3)
with col1:
    platform = st.selectbox(
        "Platform", ["Etsy", "eBay", "Amazon", "Instagram shop", "WhatsApp catalogue"]
    )
with col2:
    tone = st.selectbox("Tone", ["Friendly", "Professional", "Fun", "Premium"])
with col3:
    language = st.selectbox("Language", ["English", "Hindi", "Hinglish"])

LANGUAGE_HINTS = {
    "English": "Write in simple English.",
    "Hindi": "Write in Hindi using Devanagari script.",
    "Hinglish": (
        "Write in Hinglish: Hindi words written in English letters, mixed with "
        "common English words, like how people chat on WhatsApp. "
        "Example: 'Ye jute ka bag college aur shopping ke liye perfect hai.'"
    ),
}

SYSTEM_PROMPT = (
    "You are a careful e-commerce copywriter. You only use facts given by the seller. "
    "You never invent materials, colours, sizes, prices, certifications, discounts or "
    "quality claims. You never add words like durable, premium, ethically sourced, "
    "organic or handmade unless the seller wrote them. You output only the listing, "
    "with no introduction and no closing remarks."
)

RISKY_CLAIMS = [
    "handmade", "handcrafted", "durable", "100%", "organic", "certified",
    "premium", "pesticide", "waterproof", "guarantee", "lifetime",
    "breathable", "lightweight", "naturally dyed",
]

if st.button("Write my listing", type="primary"):
    if not product.strip():
        st.warning("Please enter a product name first.")
    elif len(re.findall(r"\w+", details)) < 4:
        st.warning(
            "Please add a few more details (material, size, colour, price, who it is for). "
            "With too little information, small AI models start making things up."
        )
    else:
        user_prompt = f"""Write a product listing for {platform}.

Product: {product}
Seller's details: {details}
Tone: {tone}
Language: {language}. {LANGUAGE_HINTS[language]}

Use exactly this format and start directly with "Title:":
Title: (one catchy title under 80 characters)
Description: (2 to 3 short sentences)
Bullet points: (up to 4 short bullet points, one per fact from the seller's details)
Hashtags: (5 relevant hashtags)

Rules:
- Use ONLY the facts in the seller's details.
- If something is not mentioned, leave it out completely.
- Write the hashtags in English.
- Write the whole listing in {language}."""

        with st.spinner("Writing your listing..."):
            try:
                response = ollama.chat(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    options={"temperature": 0.3},
                )
                text = response["message"]["content"]

                # Remove any chatty intro the model adds before the listing.
                start = text.find("Title:")
                if start > 0:
                    text = text[start:]

                st.subheader("Your listing")
                st.markdown(text)

                # Claim checker: warn about risky words the seller never typed.
                source_text = (product + " " + details).lower()
                flagged = [
                    w for w in RISKY_CLAIMS
                    if w in text.lower() and w not in source_text
                ]
                if flagged:
                    st.warning(
                        "Check these claims, you did not mention them: "
                        + ", ".join(flagged)
                    )

                st.info(
                    "Always review the text before publishing, "
                    "small models can still make mistakes."
                )
            except Exception as e:
                st.error(
                    "Could not reach the local model. Make sure Ollama is running "
                    f"and you have run: ollama pull {MODEL}"
                )
                st.caption(f"Technical details: {e}")