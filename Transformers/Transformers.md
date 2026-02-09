---
tags:
  - umbrella
---
# Architecture

![[Transformer,_full_architecture.jpg]]


Instead of processing words one by one (like older RNNs), the Transformer looks at the entire sentence at once, using "Attention" to figure out which words relate to each other.


---

## 1. The Encoder (Left Side)

The Encoder’s job is to "understand" the input (the Source Sequence).

- **Embeddings & Positional Encoding:** Words are converted into vectors. Since Transformers process everything simultaneously, they don't naturally know the order of words. **Positional Encoding** adds a mathematical "signal" to each word so the model knows its position.
- **Multi-Headed Self-[[Attention]]:** This is the secret sauce. It allows the model to look at a word and focus on other relevant words in the same sentence. For example, in "The animal didn't cross the street because **it** was too tired," attention helps the model link "**it**" to "**animal**."
- **Feed-Forward Network:** A simple neural network applied to each word independently to further process the features extracted by attention.
- **Add & Norm:** The arrows skipping over blocks are **Residual Connections**. They help gradients flow during training, and **Layer Normalization** keeps the math stable.

---

## 2. The Decoder (Right Side)

The Decoder’s job is to "generate" the output (the Target Sequence) one word at a time.

- **Masked Multi-Headed Self-Attention:** Similar to the encoder, but with a twist. It is "masked" so that when the model is predicting a word, it can't "cheat" by looking at future words in the sequence.
- **Multi-Headed Cross-Attention:** This is where the Encoder and Decoder talk. The Decoder takes the information from the Encoder (the $V$ and $K$ arrows coming from the left) to make sure its output matches the context of the input.
- **Linear & Softmax:** At the very top, the model turns its internal math back into probabilities. The **Softmax** layer picks the most likely word for the next part of the sentence.

---

## Why is it a big deal?

1. **Parallelization:** Because it doesn't process word-by-word (linearly), it can be trained much faster on GPUs.
2. **Long-Range Dependencies:** It’s great at remembering context from the beginning of a long paragraph, which older models struggled with.

---

[[Archiectures]] 