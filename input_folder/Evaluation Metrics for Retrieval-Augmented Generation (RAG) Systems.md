---
title: "Evaluation Metrics for Retrieval-Augmented Generation (RAG) Systems"
source: "https://www.geeksforgeeks.org/nlp/evaluation-metrics-for-retrieval-augmented-generation-rag-systems/"
author:
  - "[[GeeksforGeeks]]"
published: 2024-09-13
created: 2026-06-20
description: "Your All-in-One Learning Portal: GeeksforGeeks is a comprehensive educational platform that empowers learners across domains-spanning computer science and programming, school education, upskilling, commerce, software tools, competitive exams, and more."
tags:
  - "clippings"
---
[Retrieval Augmented Generation (RAG)](https://www.geeksforgeeks.org/nlp/what-is-retrieval-augmented-generation-rag/) is LLM framework that combines information retrieval and text generation to produce more accurate, factual and context rich responses. Evaluation metrics help check if the system retrieves relevant information, gives accurate answers and meets performance goals while also guiding improvements and model comparisons.

![[rag_system_evaluation_cycle.webp|rag_system_evaluation_cycle]]

Evaluation Metrics

## Steps to Evaluate RAG System

Evaluating a RAG system means checking how well it retrieves and generates accurate, relevant and grounded responses.

****1\. Set Goals:**** Define what matters most—accuracy, relevance, fluency or groundedness.

****2\. Pick Metrics:****

- ****Retrieval level:**** Precision, Recall, F1, MRR, nDCG.
- ****Generation level:**** BLEU, ROUGE, METEOR, BERTScore, Perplexity.
- ****End-to-end:**** Groundedness, Hallucination Rate, Factual Consistency, Answer Relevance.

****3\. Automate:**** Use tools like NLTK, ROUGE-score, BERTScore or Textstat for quick evaluation.

****4\. Add Human Review:**** Rate responses for clarity, accuracy and informativeness.

****5\. Analyze Results:**** Visualize performance, compare models and find weak spots.

****6\. Iterate:**** Refine retrieval and generation steps to improve factuality and coherence.

## Types of Evaluation Metrics

Some of the types of evaluation metrics are:

![[rag_evaluation_metrics_in_ragas.webp|rag_evaluation_metrics_in_ragas]]

Types of Evaluation Metrics

### 1\. Retrieval Level Metrics

Some of the retrieval level metrices are [****Precision, Recall****](https://www.geeksforgeeks.org/machine-learning/precision-and-recall-in-machine-learning/) ****and**** [****F1-Score****](https://www.geeksforgeeks.org/machine-learning/f1-score-in-machine-learning/)****.****

****1\. Precision****: Portion of retrieved documents that are actually relevant.

$$
\text{Precision} = \frac{TP}{TP + FP}
$$

****2\. Recall****: Portion of relevant documents that were successfully retrieved.

$$
\text{Recall} = \frac{TP}{TP + FN}
$$

****3 F1-Score****: Harmonic mean of precision and recall, balancing both.

$$
\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}
$$

****Output:****

> Precision: 1.0, Recall: 0.6666666666666666, F1-Score: 0.8

****4\. Hit Rate:**** Shows how often retrieved answers exactly match the expected ones, higher is better.

$$
\text{Hit Rate} = \frac{\text{Number of Queries with at least one relevant document retrieved}}{\text{Total Number of Queries}}
$$

****Output:****

> Hit Rate: 0.5

****5\. Mean Reciprocal Rank (MRR):**** Measures how quickly the correct answer appears in the ranked results, higher is better.

$$
\text{MRR} = \frac{1}{N} \sum_{i=1}^{N} \frac{1}{\text{rank}_i}
$$

- ****N:**** total number of queries
- ****rank****: rank position of the first relevant document for the i <sup>th</sup> query

****Output:****

> MRR: 0.5

****6\. Mean Average Precision (MAP):**** Evaluates ranking quality across multiple queries.

$$
\text{MAP} = \frac{1}{N} \sum_{i=1}^{N} \text{AP}_i
$$

$$
\text{AP}_i = \frac{1}{R_i} \sum_{k=1}^{n} P_i(k) \times \text{rel}_i(k)
$$

- ****N:**** total number of queries
- ****AP**** **<sub><strong>I</strong></sub>******:**** average precision for the i <sup>th</sup> query
- ****R**** **<sub><strong>i</strong></sub>******:**** number of relevant documents for query i
- ****P**** **<sub><strong>i</strong></sub>** ****(k):**** precision at cutoff k
- ****rel**** **<sub><strong>i</strong></sub>** ****(k):**** 1 if the document at rank k is relevant, else 0

****Output:****

> MAP: 0.25

****7\. Normalized Discounted Cumulative Gain (nDCG):**** Rewards highly relevant documents appearing earlier in results.

$$
\text{nDCG}_p = \frac{\text{DCG}_p}{\text{IDCG}_p}
$$

$$
\text{DCG}_p = \sum_{i=1}^{p} \frac{2^{\text{rel}_i} - 1}{\log_2(i + 1)}
$$

$$
\text{IDCG}_p = \sum_{i=1}^{p} \frac{2^{\text{rel}_i^\text{ideal}} - 1}{\log_2(i + 1)}
$$

- ****p:**** rank position cutoff
- ****rel**** **<sub><strong>i</strong></sub>******:**** relevance score of the document at rank i
- ****rel**** **<sub><strong>i</strong></sub>** **<sup><strong>ideal</strong></sup>******:**** relevance of document at rank i in ideal ordering

****Output:****

> nDCG@5: 0.3065735963827292

****8\. Recall@k and Precision@k:**** Check relevance within the top k retrieved items.

$$
\text{Recall@k} = \frac{|\{\text{relevant documents in top } k\}|}{|\{\text{total relevant documents}\}|}
$$

$$
\text{Precision@k} = \frac{|\{\text{relevant documents in top } k\}|}{k}
$$

****Output:****

> {'Recall@2': np.float64(0.25), 'Precision@2': np.float64(0.25)}

****9\. Similarity Measures (Cosine, BM25):**** Quantify how closely retrieved documents match the query.

$$
\text{Cosine Similarity} = \cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \, \|\mathbf{B}\|}
$$

Here we have illustrated [cosine similarity.](https://www.geeksforgeeks.org/dbms/cosine-similarity/)

****Output:****

> Cosine Similarity: 0.24755053441657565

### 2\. Generation Level Metrices

Some of the generation level metrices are:

****1.**** [****BLEU, ROUGE,****](https://www.geeksforgeeks.org/nlp/understanding-bleu-and-rouge-score-for-nlp-evaluation/) ****METEOR, BERTScore:**** Compare generated text with reference answers for similarity.

Here we have illustrated BLEU.

$$
\text{BLEU} = \text{BP} \cdot \exp \Bigg( \sum_{n=1}^{N} w_n \log p_n \Bigg)
$$

- ****p**** **<sub><strong>n</strong></sub>******:**** modified n-gram precision
- ****w**** **<sub><strong>n</strong></sub>******:**** weight for n-gram
- ****BP:**** Brevity Penalty

****Output:****

> {'BLEU': np.float64(0.3939917666748808)}

****2.**** [****Perplexity:****](https://www.geeksforgeeks.org/nlp/perplexity-for-llm-evaluation/) Measures how well the model predicts the next word, lower perplexity is better.

$$
\text{Perplexity}(W) = P(w_1, w_2, \dots, w_N)^{-\frac{1}{N}} = \exp\Bigg(-\frac{1}{N} \sum_{i=1}^{N} \log P(w_i \mid w_1, \dots, w_{i-1})\Bigg)
$$

****Output:****

> Perplexity: 901.9484596252441

****3\. Factual Consistency:**** Checks if generated content aligns with retrieved information.

$$
\text{Factual Consistency} = \frac{|\text{Words in Response} \cap \text{Words in Reference}|}{|\text{Words in Response}|}
$$

****Output:****

> Factual Consistency: 0.5714285714285714

****4\. Fluency and Readability:**** Assesses how natural and easy to understand the text is.

$$
\text{Fluency Score} = \frac{\text{Total Words}}{\text{Total Sentences}}
$$

$$
\text{Flesch Reading Ease} = 206.835 - 1.015 \left(\frac{\text{Total Words}}{\text{Total Sentences}}\right) - 84.6 \left(\frac{\text{Total Syllables}}{\text{Total Words}}\right)
$$

****Output:****

> {'Average Readability (Flesch)': np.float64(55.2089285714286), 'Average Fluency (words/sentence)': np.float64(7.5)}

****5\. Diversity and Novelty:**** Evaluates variety and originality in generated responses.

$$
\text{Distinct-n} = \frac{|\text{Unique n-grams in responses}|}{|\text{Total n-grams in responses}|}
$$

$$
\text{Novelty} = \frac{|\text{Words in current response not seen in previous responses}|}{|\text{Total words in current response}|}
$$

****Output:****

> {'Distinct-Unigram': 0.8666666666666667, 'Distinct-Bigram': 1.0, 'Novelty': np.float64(0.9166666666666667)}

### 3\. End to End RAG System Evaluation

End to end evaluation looks at the overall performance of a RAG system considering both retrieval and generation together.

****1\. Answer Relevance and Context Utilization:**** Checks if the system’s answers address the user’s query and effectively use the retrieved information.

$$
\text{Answer Relevance} = \frac{|\text{Words in Response} \cap \text{Words in Reference}|}{|\text{Words in Reference}|}
$$

$$
\text{Context Utilization} = \frac{|\text{Words in Response} \cap \text{Words in Retrieved Docs}|}{|\text{Words in Response}|}
$$

****Output:****

> {'Answer Relevance': np.float64(0.6458333333333333), 'Context Utilization': np.float64(0.35416666666666663)}

****2\. Groundedness:**** Measures whether the generated text is supported by the retrieved sources reducing the risk of hallucinations.

$$
\text{Groundedness} = \frac{|\text{Words in Response} \cap \text{Words in Retrieved Docs}|}{|\text{Words in Response}|}
$$

****Output:****

> Groundedness: 0.6666666666666667

****3\. Hallucination Rate:**** Tracks how often the system produces information that is incorrect or not backed by sources.

$$
\text{Hallucination Rate} = \frac{|\text{Words in Response} - \text{Words in Retrieved Docs}|}{|\text{Words in Response}|}
$$

****Output:****

> Hallucination Rate: 0.4875

****4\. Response Coherence and Readability:**** Ensures the generated answers are clear, logically structured and easy to understand.

$$
\text{Coherence} = \frac{\text{Total Words in Response}}{\text{Number of Sentences in Response}}
$$

****Output:****

> {'Average Coherence (words/sentence)': np.float64(6.5), 'Average Readability (Flesch)': np.float64(28.20704545454545)}

****5\. Relevancy Score:**** Measures how well the system’s output matches the user’s query intent.

$$
\text{Relevancy Score} = \frac{|\text{Words in Response} \cap \text{Words in Query}|}{|\text{Words in Query}|}
$$

****Output:****

> Relevancy Score: 0.3222222222222222

## Human Evaluation in RAG Systems

Human evaluation assesses the quality and usefulness of a RAG system’s responses from a real user perspective.

### Criteria for Human Evaluation

Criteria for Human Evaluation in RAG Systems:

1. ****Relevance:**** Ensures the answer directly addresses the user’s query.
2. ****Informativeness:**** Measures whether the response is helpful, detailed and meaningful.
3. ****Factual Accuracy:**** Confirms that statements are correct and supported by sources.
4. ****Clarity and Readability:**** Evaluates if the response is easy to understand and well structured.
5. ****Evaluation Methods:**** Includes rating scales, pairwise comparisons and expert reviews.

### Methods of Human Evaluation

Methods of Human Evaluation in RAG Systems:

1. ****Rating Scales:**** Evaluators score responses on criteria like relevance, accuracy and clarity.
2. ****Pairwise Comparison:**** Responses are compared in pairs to determine which is better.
3. ****Expert Review:**** Subject matter experts assess the quality, factual correctness and usefulness of responses.

## Emerging and Hybrid Evaluation Approaches

Advanced and combined evaluation methods to get a more accurate performance are:

1. ****LLM based Evaluators:**** Using large language models to automatically assess relevance, factuality and coherence.
2. ****Task Specific Evaluation Pipelines:**** Custom metrics tailored to the domain or application of the RAG system.
3. ****Automatic Fact Checking and Citation Tracking:**** Tools that verify information against trusted sources.
4. ****Hybrid Approaches:**** Combining automated metrics with human evaluation for a balanced, comprehensive assessment.

## Comparative Analysis of Metrics

Comparison table of different RAG evaluation metrics:

| Metric Type | Examples | Strengths | Weaknesses |
| --- | --- | --- | --- |
| Retrieval Metrics | Hit Rate, MRR, Precision, Recall, nDCG | Simple, interpretable, directly measures relevance and ranking quality | Don’t evaluate answer quality, fluency or coherence |
| Generation Metrics | BLEU, ROUGE, METEOR, BERTScore, Perplexity | Quantitative, widely used, easy to compute | May miss semantic meaning, context or factual correctness |
| End-to-End Metrics | Answer Relevance, Groundedness, Hallucination Rate, Coherence | Holistic evaluation of system, includes factual grounding | Harder to compute automatically, may require human evaluation |
| Human Evaluation | Rating scales, Pairwise comparison, Expert review | Captures nuance, context, readability and factual correctness | Time consuming, subjective, not easily scalable |

## Challenges in Evaluating RAG Systems

Some of the challenges faced during evaluating RAG Systems are:

1. ****Measuring Contextual Understanding:**** Ensuring the system correctly interprets the user’s intent and context.
2. ****Balancing Factuality and Creativity:**** Avoiding hallucinations while allowing flexible, natural responses.
3. ****Dataset Bias and Subjectivity:**** Evaluation may be affected by biased datasets or differing human judgments.
4. ****Limited Automated Metrics:**** Existing metrics may not fully capture relevance, coherence or groundedness.
5. ****Scaling Human Evaluation:**** Conducting thorough human assessments can be time consuming and resource intensive.

## Best Practices for RAG Evaluation

We can follow these best practices to get reliable and meaningful results when evaluating RAG systems:

1. ****Combine Multiple Metrics:**** Use retrieval, generation and end-to-end metrics together for better evaluation.
2. ****Use Domain Specific Metrics:**** Tailor evaluation metrics to the application area like medical, legal, technical.
3. ****Monitor Hallucinations and Groundedness:**** Regularly check for unsupported or fabricated content.
4. ****Track Top-k Performance:**** Evaluate not just the top answer but also top-ranked results to assess retrieval effectiveness.
5. ****Maintain Consistent Evaluation Pipelines:**** Ensure reproducibility by using standardized datasets, metrics and procedures.
6. ****Incorporate User Feedback:**** Real world feedback helps assess usefulness, clarity and relevance.
7. ****Visualize Results:**** Use dashboards or charts to track metrics over time and identify trends.

10 Questions

What is the main goal of a Retrieval-Augmented Generation (RAG) system?

- A
	To increase model parameters
- B
	To combine information retrieval and text generation for accurate, factual responses
- C
	To replace human reasoning with machine logic
- D
	To enhance model compression

In a RAG pipeline, which of the following is typically the first step?

- A
	Answer generation
- B
	Document ranking
- C
	Information retrieval
- D
	Evaluation of responses

Which metric is commonly used to evaluate the retrieval quality of a RAG system?

- A
	BLEU
- B
	Recall@k
- C
	ROUGE-L
- D
	F1-score

What does “Precision@k” measure in the context of RAG retrieval?

- A
	Number of relevant documents in the entire corpus
- B
	Percentage of relevant documents among the top-k retrieved results
- C
	Total number of documents retrieved
- D
	Ratio of generated tokens to retrieved ones

Which metric is most appropriate for assessing semantic similarity between generated and reference answers?

- A
	BLEU
- B
	ROUGE
- C
	BERTScore
- D
	Accuracy

Which metric compares the overlap of n-grams between generated and reference texts?

- A
	METEOR
- B
	BLEU
- C
	BERTScore
- D
	MRR

What does F1-score represent in RAG evaluation?

- A
	Balance between precision and recall
- B
	Number of retrieved documents
- C
	Sentence fluency
- D
	Latency of the model

Which of the following evaluates how consistent and contextually appropriate the generated answers are with retrieved evidence?

Which of the following is an end-to-end evaluation metric for RAG systems?

Why are evaluation metrics essential in RAG systems?

![success](https://media.geeksforgeeks.org/auth-dashboard-uploads/sucess-img.png)

Quiz Completed Successfully

Your Score:0/10

Accuracy:0%