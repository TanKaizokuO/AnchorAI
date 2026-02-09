---
tags:
  - extension
---

---

While a single attention head is powerful, it has a limitation: it often focuses on the **strongest** relationship and misses subtler ones.

> [!NOTE] Analogy
> Think of a single attention head as a **single pair of eyes**. If you are reading a sentence, your eyes might lock onto the subject ("animal") and ignore the action ("cross").
>
> **Multi-Head Attention** solves this by giving the model multiple "heads" (sets of $Q, K, V$ matrices) to look at the sentence from different perspectives simultaneously.


---

## 1. Why Multiple Heads?
By having multiple heads, each one can specialize in different types of linguistic relationships.

**Example Sentence**: *"The animal didn't cross the street because it was too tired."*

* **Head 1 (Grammar focus)**: Might link "it" to "animal" (noun-pronoun relationship).
* **Head 2 (Action focus)**: Might link "tired" to "cross" (reason-action relationship).
* **Head 3 (Position focus)**: Might link "The" to "animal" (determiner-noun relationship).

If we only had one head, the model would have to **average** all these relationships together, making the signal muddy.

---

## 2. The Math of Multi-Head Attention
Instead of one large attention calculation, we perform $h$ separate calculations in parallel.

### Step A: Split and Project
We maintain separate learnable weight matrices for each head $i$:
$$W_i^Q, W_i^K, W_i^V$$

For a standard Transformer ($d_{model} = 512, h = 8$):
* Each head projects the input into a smaller dimension:
* $d_k = d_v = 512 / 8 = 64$.

### Step B: Parallel Attention
We run the [[Attention|Scaled Dot-Product Attention]] on each head independently:
$$\text{head}_i = \text{Attention}(Q W_i^Q, K W_i^K, V W_i^V)$$
* **Result**: 8 different output vectors, each capturing different contextual information.

### Step C: Concatenate
The model needs a single unified vector for the next layer. We join the heads end-to-end:
$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h)$$
* **Result**: This restores the original dimension ($64 \times 8 = 512$).

### Step D: Final Linear Projection
We multiply the long concatenated vector by a final weight matrix $W^O$ to mix the information together:
$$\text{Final Output} = \text{Concat}(\text{head}_1, \dots, \text{head}_h) W^O$$

---

## Summary
1.  **Split**: Input is sliced into multiple lower-dimensional subspaces.
2.  **Attend**: Each "head" looks for different relationships (syntax, semantics).
3.  **Merge**: Results are stitched back together.
4.  **Mix**: Final linear layer combines insights into a single rich representation.

**Next Steps**:
* This output goes into the **Add & Norm** layer.
* Next topics: [[Positional Encoding]] or [[Feed-Forward Networks]].
