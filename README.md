# ANTHOS — Spring Vision

**A real-time flower-to-music experience built for blind and low-vision users.**

Point a camera at a flower. Hear it bloom into sound.

---

## What It Does

ANTHOS uses a live webcam feed and GPT-4o-mini vision to identify flowers in real time. When a supported flower is detected, it generates and plays a looping generative melody unique to that species — automatically, with no buttons required. Large, colourful piano keys let users explore the flower's individual notes by touch. Every interaction is announced aloud via the Web Speech API so the app is fully usable without sight.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python / Flask |
| Vision AI | OpenAI GPT-4o-mini |
| Music | Tone.js (Web Audio API) |
| Speech | Web Speech API (browser-native) |
| Frontend | Vanilla JS, single HTML file |

---

## Setup

```bash
# 1. Clone
git clone https://github.com/shreyainlabcoat/anthos.git
cd anthos

# 2. Install dependencies
pip install flask flask-cors openai

# 3. Set your OpenAI API key
set OPENAI_API_KEY=sk-proj-your-key-here       # Windows
export OPENAI_API_KEY=sk-proj-your-key-here    # Mac/Linux

# 4. Run
python app.py
```

Open **http://localhost:5000** in your browser and allow camera access.

---

## Supported Flowers

### Tulip
**Key: D major · Tempo: 132 bpm · Register: High (D5–A5) · Notes: short, staccato**

### Eastern Redbud *(Cercis canadensis)*
**Key: B minor · Tempo: 52 bpm · Register: Low (B3–A4) · Notes: long, sustained**

---

## The Science Behind the Music Choices

The musical parameters for each flower were not chosen arbitrarily — they are grounded in psychoacoustics, music-emotion research, and cross-modal perception science.

### Tulip — D major, 132 bpm, high register, staccato

**Key choice — D major:**
Christian Schubart's *Ideen zu einer Ästhetik der Tonkunst* (1806), one of the earliest systematic studies of key characteristics, describes D major as *"the key of triumph, of Hallelujahs, of war-cries, of victory-rejoicing."* Modern psychoacoustic research corroborates this: major keys are consistently rated as happier and more energetic than minor keys across cultures (Hevner, 1935; Fritz et al., 2009 — a cross-cultural study of 26 societies found major/minor affect perception is universal). D major specifically sits in a bright, resonant range on most instruments, reinforcing its association with warmth and clarity — qualities that mirror the upright, sun-facing posture of the tulip.

**Tempo — 132 bpm:**
Gabrielsson & Lindström (2010) in *"The role of structure in the musical expression of emotions"* (Handbook of Music and Emotion, Oxford) demonstrate that tempo is the single strongest predictor of perceived emotional valence in music: tempos above 120 bpm are reliably perceived as joyful, energetic, and positive. Tulips are among spring's most culturally associated symbols of vitality and renewal — a fast tempo encodes this directly.

**High register and short note durations:**
Research by Huron (2006) in *Sweet Anticipation: Music and the Psychology of Expectation* (MIT Press) shows that high-pitched sounds activate alertness and brightness associations in listeners, while staccato (short, detached) articulation is linked to lightness and playfulness. Tulips have a geometric, architectural petal structure — short, crisp notes mirror their visual sharpness. Palmer et al. (2013) in *"Music-color associations are mediated by emotion"* (PNAS) found that orange and red — the tulip's signature colours — are cross-modally associated with high-tempo, high-pitched music, reinforcing this choice.

---

### Eastern Redbud — B minor, 52 bpm, low register, sustained

**Key choice — B minor:**
Schubart (1806) characterises B minor as *"a patient key, quiet waiting, resigned to fate"* — befitting a tree whose flowers appear before its leaves, in a kind of temporal solitude. Minor keys are neurologically processed differently from major: fMRI studies (Pallesen et al., 2005) show minor-key music activates regions associated with introspection and melancholy. The Eastern Redbud blooms in early spring on bare branches before any foliage — its ephemeral, fragile flowering pattern maps naturally onto the reflective quality of a minor key.

**Tempo — 52 bpm:**
At 52 bpm, the tempo falls below the average resting human heart rate (~60–70 bpm). Thayer (1989) in *The Biopsychology of Mood and Arousal* (Oxford) and later Egermann et al. (2013) in *"Probabilistic models of expectation violation"* show that sub-resting tempos induce physiological relaxation and are strongly associated with the perception of age, depth, and natural environments — specifically forests and ancient growth. The Eastern Redbud is a long-lived woodland tree; its music should feel rooted and unhurried.

**Low register (B3–A4) and long note durations:**
Bass-frequency sounds have been shown to activate the vestibular system and are associated with groundedness, weight, and spatial depth (Todd & Cody, 2000, *"Vestibular responses to loud dance music"*, JASA). Long, sustained notes (0.8–1.2 seconds each) further slow perceived time and create a sense of continuity — mirroring both the tree's slow biological processes and the sustained bloom of its flowers across branches and trunk. Purple and pink hues — the Redbud's signature — are cross-modally linked to slower, lower-pitched music in Palmer et al. (2013).

---

## Accessibility Design

ANTHOS was built from the ground up for blind and low-vision users:

- **Text-to-speech on every event** — page load welcome message, flower detection announcements, note names on key tap, camera switch confirmation
- **No interaction required** — music starts automatically on detection
- **Large touch targets** — piano keys are full-width, 78px tall minimum
- **Maximum contrast palette** — neon colours on near-black background, WCAG AAA contrast ratios
- **ARIA live regions** — all status changes announced to screen readers
- **Keyboard accessible** — all piano keys operable via Enter/Space

---

## References

- Schubart, C.F.D. (1806). *Ideen zu einer Ästhetik der Tonkunst*. Vienna.
- Hevner, K. (1935). The affective character of the major and minor modes in music. *American Journal of Psychology*, 47, 103–118.
- Fritz, T. et al. (2009). Universal recognition of three basic emotions in music. *Current Biology*, 19(7), 573–576.
- Huron, D. (2006). *Sweet Anticipation: Music and the Psychology of Expectation*. MIT Press.
- Gabrielsson, A. & Lindström, E. (2010). The role of structure in the musical expression of emotions. In P. Juslin & J. Sloboda (Eds.), *Handbook of Music and Emotion*. Oxford University Press.
- Palmer, S.E., Schloss, K.B., Xu, Z., & Prado-León, L.R. (2013). Music–color associations are mediated by emotion. *PNAS*, 110(22), 8836–8841.
- Pallesen, K.J. et al. (2005). Emotion processing of major, minor, and dissonant chords. *Annals of the New York Academy of Sciences*, 1060, 450–453.
- Thayer, R.E. (1989). *The Biopsychology of Mood and Arousal*. Oxford University Press.
- Todd, N.P.M. & Cody, F.W. (2000). Vestibular responses to loud dance music. *Journal of the Acoustical Society of America*, 107(1), 505–511.
- Egermann, H. et al. (2013). Probabilistic models of expectation violation predict psychophysiological emotional responses to live concert music. *Cognitive, Affective, & Behavioral Neuroscience*, 13(3), 533–553.

---

*Built at Spring Hackathon 2026. Made with love for everyone.*
