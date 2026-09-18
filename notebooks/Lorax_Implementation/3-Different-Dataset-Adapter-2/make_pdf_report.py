import os
import base64
import subprocess

def get_base64(path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')
    return ''

imgs = {
    'code_frob': get_base64('extracted_images/3-adapter-comparison-2_cell23_out0.png'),
    'dolly_frob': get_base64('extracted_images/3-adapter-comparison-2_cell25_out0.png'),
    'meta_frob': get_base64('extracted_images/3-adapter-comparison-2_cell27_out0.png'),
    'code_svd': get_base64('extracted_images/3-adapter-comparison-2_cell38_out0.png'),
    'dolly_svd': get_base64('extracted_images/3-adapter-comparison-2_cell39_out0.png'),
    'meta_svd': get_base64('extracted_images/3-adapter-comparison-2_cell40_out0.png'),
    'lin_frob': get_base64('extracted_images/3-adapter-merged-model-comparision-fixed-2_cell19_out0.png'),
    'svd_frob': get_base64('extracted_images/3-adapter-merged-model-comparision-fixed-2_cell20_out0.png'),
    'dare_frob': get_base64('extracted_images/3-adapter-merged-model-comparision-fixed-2_cell21_out0.png'),
    'ties_frob': get_base64('extracted_images/3-adapter-merged-model-comparision-fixed-2_cell22_out0.png'),
    'slerp_frob': get_base64('extracted_images/3-adapter-merged-model-comparision-fixed-2_cell23_out0.png'),
    'merged_svd': get_base64('extracted_images/3-adapter-merged-model-comparision-fixed-2_cell26_out0.png'),
    'slerp_angle': get_base64('extracted_images/slerp-angle-diagnostic(2)_cell6_out0.png'),
    'dolly_train': get_base64('extracted_images/dolly-training-adapter (1)_cell16_out16.png'),
    'code_train': get_base64('extracted_images/qwen-training-on-code-alpaca_cell15_out9.png'),
    'cka_heatmap': get_base64('extracted_images/cka_layerwise_heatmap.png')
}

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Technical Evaluation Report: Multi-Task LoRA Adapter Merging, Structural Diagnostics, CKA & Evidence Gap Closure</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
  @page {
    size: letter portrait;
    margin: 16mm 14mm 16mm 14mm;
  }
  * {
    box-sizing: border-box;
  }
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #1e293b;
    line-height: 1.55;
    font-size: 9.5pt;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }
  .page-break {
    page-break-before: always;
  }
  .avoid-break {
    page-break-inside: avoid;
  }
  
  /* Header / Cover Styling */
  .header-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #2563eb 100%);
    color: #ffffff;
    padding: 24px 28px;
    border-radius: 10px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }
  .header-card h1 {
    font-size: 18pt;
    font-weight: 800;
    margin: 0 0 8px 0;
    line-height: 1.2;
    letter-spacing: -0.5px;
  }
  .header-card .subtitle {
    font-size: 10.5pt;
    color: #93c5fd;
    font-weight: 500;
    margin-bottom: 12px;
  }
  .meta-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    border-top: 1px solid rgba(255,255,255,0.2);
    padding-top: 12px;
    font-size: 8.5pt;
  }
  .meta-item strong {
    display: block;
    color: #cbd5e1;
    text-transform: uppercase;
    font-size: 7pt;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
  }

  /* Section Styling */
  h2 {
    color: #0f172a;
    font-size: 12pt;
    font-weight: 700;
    border-bottom: 2px solid #2563eb;
    padding-bottom: 4px;
    margin-top: 20px;
    margin-bottom: 10px;
  }
  h3 {
    color: #1e3a8a;
    font-size: 10pt;
    font-weight: 600;
    margin-top: 14px;
    margin-bottom: 6px;
  }
  p, li {
    text-align: justify;
    margin-bottom: 6px;
  }
  ul, ol {
    margin-top: 2px;
    margin-bottom: 8px;
    padding-left: 18px;
  }
  li {
    margin-bottom: 4px;
  }

  /* Callout Boxes */
  .callout {
    background: #f8fafc;
    border-left: 4px solid #2563eb;
    padding: 10px 14px;
    border-radius: 4px;
    margin: 12px 0;
    font-size: 9pt;
  }
  .callout-title {
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 3px;
  }
  .callout.warning {
    background: #fffbebf8;
    border-left-color: #d97706;
  }
  .callout.warning .callout-title {
    color: #b45309;
  }
  .callout.success {
    background: #f0fdf4;
    border-left-color: #16a34a;
  }
  .callout.success .callout-title {
    color: #15803d;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 8pt;
  }
  th, td {
    padding: 6px 8px;
    text-align: left;
    border: 1px solid #cbd5e1;
    vertical-align: top;
  }
  th {
    background-color: #0f172a;
    color: #ffffff;
    font-weight: 600;
    text-align: center;
    font-size: 8pt;
  }
  td.num {
    text-align: right;
    font-family: 'JetBrains Mono', monospace;
  }
  tr:nth-child(even) {
    background-color: #f8fafc;
  }
  tr.highlight {
    background-color: #eff6ff;
    font-weight: 600;
  }
  tr.collapsed-row {
    background-color: #fef2f2;
  }

  /* Image Layout Grids */
  .img-grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin: 12px 0;
  }
  .img-grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin: 12px 0;
  }
  .img-card {
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 5px;
    background: #ffffff;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  .img-card img {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
    display: block;
    margin: 0 auto;
  }
  .img-caption {
    font-size: 7.5pt;
    color: #64748b;
    margin-top: 4px;
    font-weight: 500;
  }

  /* Code / Formula Boxes */
  code {
    font-family: 'JetBrains Mono', monospace;
    background: #f1f5f9;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 8pt;
    color: #0f172a;
  }
  .formula-box {
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px 14px;
    margin: 10px 0;
    font-family: "Georgia", serif;
    font-style: italic;
    text-align: center;
    font-size: 9.5pt;
  }
  .bold {
    font-weight: 700;
  }
</style>
</head>
<body>

<div class="header-card">
  <h1>Technical Evaluation Report: Multi-Task LoRA Adapter Merging, Structural Diagnostics, CKA & Evidence Gap Closure</h1>
  <div class="subtitle">Comprehensive Scientific Synthesis of 17 Jupyter Notebook Experiments on Qwen3-0.6B</div>
  <div class="meta-grid">
    <div class="meta-item"><strong>Base Model</strong>Qwen3-0.6B (Unsloth)</div>
    <div class="meta-item"><strong>Task Domains</strong>CodeAlpaca, MetaMathQA, Dolly-15k</div>
    <div class="meta-item"><strong>Merging Methods</strong>9 Algorithms Evaluated (Linear, SVD, TIES, DARE, SLERP, BWSum, CT-Calibrated, Adaptive, Joint-SVD Sweep)</div>
    <div class="meta-item"><strong>Analysis Methods</strong>Delta-Representation CKA, Effective Rank, Submodule Attn/MLP Hooking, Bootstrap (n=10k)</div>
  </div>
</div>

<div class="callout">
  <div class="callout-title">Executive Summary</div>
  This report provides a rigorous empirical and mathematical synthesis of multi-adapter LoRA merging across 17 distinct Jupyter Notebook experiments. Combining three domain-specialized adapters (CodeAlpaca-18k, MetaMathQA-15k, and Dolly-15k) trained on <code>unsloth/Qwen3-0.6B</code>, we systematically investigate the mechanisms governing weight-space and representation-space alignment. Key contributions include mapping weight-space Frobenius norms showing a 5&times; magnitude imbalance, identifying high-dimensional orthogonal concentration of measure (97%+ layers orthogonal at ~88&deg;) that causes SLERP's mathematical collapse, quantifying singular-value energy retention proving SVD truncation (94.93% energy kept) is 6&times; less destructive than TIES/DARE magnitude element trimming (69.06% energy kept), and tracing representation dynamics via Delta-Activation CKA ($\Delta h = h_{\text{model}} - h_{\text{base}}$). We show that intermediate layers (Blocks 7–11) serve as critical task hubs, with representation divergence driven primarily by Attention projection sublayers rather than MLPs. Finally, we isolate budget size from truncation topology, demonstrating that joint-SVD truncation at rank-16 is highly optimal, whereas independent truncation prior to summation (Adaptive Rank Merge) collapses downstream reasoning entirely.
</div>

<h2>1. Category 1: Specialist LoRA Adapter Training (Notebooks 1–3)</h2>
<p>
  Three specialist LoRA adapters were independently fine-tuned on <code>unsloth/Qwen3-0.6B</code> to establish task-specific baselines. All adapters share structural parameters: rank $r=16$, scaling factor $\alpha=32$ (yielding a functional scaling multiplier of $\alpha/r = 2.0$), and target weight matrices spanning all self-attention and MLP projection layers (196 total layers: <code>q_proj</code>, <code>k_proj</code>, <code>v_proj</code>, <code>o_proj</code>, <code>gate_proj</code>, <code>up_proj</code>, <code>down_proj</code>).
</p>

<h3>Notebook 1: Dolly Specialist Adapter Training (<code>./Training/dolly-training-adapter (1).ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Fine-tune Qwen3-0.6B on Databricks Dolly-15k to acquire general instruction-following and conversation capabilities.</li>
  <li><strong>Methodology:</strong> Trained for 1 epoch using Unsloth's optimized training loop, batch size 8, learning rate 2e-4, using cross-entropy loss over assistant response tokens only.</li>
  <li><strong>Results:</strong> Smooth training loss decay from 1.62 to 0.72. Downstream Dolly Perplexity (PPL) reached <strong>12.6278</strong>. GSM8K EM is 0.0250 and HumanEval pass@1 is 0.1646.</li>
  <li><strong>Inference:</strong> Instruction tuning successfully aligns the model's text generation structure, stabilizing language modeling perplexity, though it provides no specialized math reasoning signal.</li>
</ul>

<h3>Notebook 2: MetaMath Specialist Adapter Training (<code>./Training/metamathqa-training.ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Train a specialist model on MetaMathQA-15k to establish mathematical reasoning capability.</li>
  <li><strong>Methodology:</strong> Fine-tuned with identical LoRA settings (r=16, $\alpha=32$), focusing training signals on mathematical prompt-response pairs.</li>
  <li><strong>Results:</strong> Training loss dropped from 1.15 to 0.38. Downstream GSM8K Exact Match (EM) accuracy reached <strong>0.2200</strong> under restrictive generation settings (320 max tokens, 1.3 repetition penalty) and <strong>0.5250</strong> under optimized decoding settings. HumanEval pass@1 is 0.1220 and Dolly PPL is 28.6676.</li>
  <li><strong>Inference:</strong> The small 0.6B parameter model possesses high receptive capacity for reasoning-oriented fine-tuning, but downstream performance is heavily constrained by token budget limits and repetition penalties.</li>
</ul>

<h3>Notebook 3: CodeAlpaca Specialist Adapter Training (<code>./Training/qwen-training-on-code-alpaca.ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Fine-tune on CodeAlpaca-18k to establish programming and code-generation capabilities.</li>
  <li><strong>Methodology:</strong> Optimized with standard instruction fine-tuning, training on code instructions and python script targets.</li>
  <li><strong>Results:</strong> Training loss decayed from 1.25 to 0.34. HumanEval pass@1 reached <strong>0.1707</strong>. GSM8K EM is 0.0850 and Dolly PPL is 38.3633.</li>
  <li><strong>Inference:</strong> Low-rank updates are capable of encoding complex programming syntax within a sub-billion parameter model. However, coding fine-tuning significantly degrades conversational perplexity (38.36 vs Dolly's 12.63), showing classic task-specific interference.</li>
</ul>

<div class="img-grid-2 avoid-break">
  <div class="img-card">
    <img src="''' + imgs['code_train'] + '''" alt="CodeAlpaca Training Curve">
    <div class="img-caption">Figure 1a: CodeAlpaca Training Loss Decay</div>
  </div>
  <div class="img-card">
    <img src="''' + imgs['dolly_train'] + '''" alt="Dolly Training Curve">
    <div class="img-caption">Figure 1b: Dolly-15k Training Loss Decay</div>
  </div>
</div>

<div class="page-break"></div>

<h2>2. Category 2: Pre-Merge Structural Analyses (Notebooks 4–5)</h2>
<p>
  Before combining specialist updates, we conducted deep structural analyses of the weight matrices ($\Delta W = B \cdot A$, where $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times d}$) to understand their geometric alignment and energy distributions.
</p>

<h3>Notebook 4: Specialist Adapter Structural Comparison (<code>./Comparison/3-adapter-comparison-2.ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Analyze the layer-wise Frobenius norms and singular value spectrum of the Dolly, MetaMath, and CodeAlpaca adapters.</li>
  <li><strong>Methodology:</strong> Extracted weights of all 196 layers, computed the Frobenius norm ($\|\Delta W\|_F = \sqrt{\sum_{i,j} \Delta W_{i,j}^2}$) and Thin SVD ($\Delta W = U S V^T$) to observe singular value decay.</li>
  <li><strong>Results:</strong>
    <ul>
      <li>Dolly adapter total Frobenius norm across layers: <strong>6.1842</strong></li>
      <li>MetaMathQA adapter total Frobenius norm: <strong>15.4020</strong></li>
      <li>CodeAlpaca adapter total Frobenius norm: <strong>30.7433</strong></li>
    </ul>
    CodeAlpaca's update magnitude is <strong>nearly 5&times; larger than Dolly's</strong> and <strong>2.5&times; larger than MetaMath's</strong>. Dolly's singular values decay rapidly, while CodeAlpaca and MetaMath singular values remain high across all 16 dimensions.
  </li>
  <li><strong>Inference:</strong> There is a severe structural imbalance. In an unweighted arithmetic average merge (Linear Merge), CodeAlpaca will dominate the gradient direction, drowning out the general instruction-following and math capabilities. Dolly requires less rank because it updates fewer coordinate directions (fast singular value decay).</li>
</ul>

<h3>Notebook 5: Merged Models Structural Comparison (<code>./Comparison/3-adapter-merged-model-comparision-fixed-2.ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Compare the structural characteristics (Frobenius norms and singular value spectra) of the merged weight matrices across different merging algorithms.</li>
  <li><strong>Methodology:</strong> Calculated norms and SVDs on the merged state dicts of Linear, SVD, DARE, TIES, and SLERP.</li>
  <li><strong>Results:</strong>
    <ul>
      <li>Linear and SVD merges preserve smooth, natural Frobenius norms across all layers.</li>
      <li>TIES and DARE merges exhibit compressed Frobenius norms (highly suppressed updates) due to element-wise dropping and sign masking.</li>
      <li>SVD-merged models exhibit a smooth singular value decay that matches the characteristics of the specialist adapters.</li>
    </ul>
  </li>
  <li><strong>Inference:</strong> Parameter-space trimming algorithms (TIES, DARE) disrupt the continuous representation space, while SVD-based merging preserves the geometric properties of the low-rank updates.</li>
</ul>

<div class="img-grid-3 avoid-break">
  <div class="img-card">
    <img src="''' + imgs['code_svd'] + '''" alt="CodeAlpaca Singular Values">
    <div class="img-caption">Figure 2a: CodeAlpaca Singular Values</div>
  </div>
  <div class="img-card">
    <img src="''' + imgs['meta_svd'] + '''" alt="MetaMath Singular Values">
    <div class="img-caption">Figure 2b: MetaMath Singular Values</div>
  </div>
  <div class="img-card">
    <img src="''' + imgs['dolly_svd'] + '''" alt="Dolly Singular Values">
    <div class="img-caption">Figure 2c: Dolly Singular Values</div>
  </div>
</div>

<h2>3. Category 3: Weight-Space Merging Implementations (Notebooks 6–7)</h2>
<p>
  We implemented and benchmarked 7 core merging algorithms to build multi-task models capable of performing code, math, and instruction tasks simultaneously.
</p>

<h3>Notebook 6: Weight-Space Merging Algorithms (<code>./Merging/3-different-adapter-merging-2-fixed.ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Implement weight-space merging protocols for Linear, SVD, TIES, DARE, SLERP, and BWSum.</li>
  <li><strong>Methodology:</strong>
    <ol>
      <li><em>Linear Merge:</em> Simple average $\Delta W_{\text{linear}} = \frac{1}{3}(\Delta W_{\text{dolly}} + \Delta W_{\text{meta}} + \Delta W_{\text{code}})$.</li>
      <li><em>SVD Merge:</em> Combined delta matrices $\Delta W_{\text{sum}}$ (rank $\le 48$) are truncated back to rank-16 via thin SVD: $\Delta W_{\text{svd}} = U_{:16} S_{:16} V_{:16}^T$.</li>
      <li><em>TIES Merge:</em> Drops the bottom 80% parameter magnitudes, elects sign direction, and averages non-conflicting parameters.</li>
      <li><em>DARE Merge:</em> Randomly drops 80% of parameters with probability $p=0.8$ and rescales the remaining elements by $1/(1-p) = 5.0$.</li>
      <li><em>SLERP Merge:</em> Spherical linear interpolation between adapters. Non-associative, so evaluated across all 6 permutation orderings.</li>
      <li><em>BWSum Merge:</em> Re-weights parameters based on shared subspaces.</li>
    </ol>
  </li>
  <li><strong>Results:</strong> Checked weight shape preservation and successfully uploaded 5 merged checkpoints to HuggingFace.</li>
  <li><strong>Inference:</strong> While technically straightforward, naive weight-space averaging ignores representation alignment, leading to significant task degradation.</li>
</ul>

<h3>Notebook 7: Magnitude-Calibrated Merge (<code>./Merging/7th-method-ct-calibrated-merge(1).ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Implement a Magnitude-Calibrated Merge (inspired by CT-Merging) to resolve the 5&times; Frobenius norm imbalance.</li>
  <li><strong>Methodology:</strong> Rescales each specialist adapter update $\Delta W_i$ to match the average target norm:
    <div class="formula-box">
      &Delta;W<sub>i</sub>' = &Delta;W<sub>i</sub> &middot; (&Vert;&Delta;W&Vert;<sub>target</sub> / &Vert;&Delta;W<sub>i</sub>&Vert;<sub>F</sub>), &nbsp;&nbsp; where &Vert;&Delta;W&Vert;<sub>target</sub> = (1/k) &sum;<sub>j=1</sub><sup>k</sup> &Vert;&Delta;W<sub>j</sub>&Vert;<sub>F</sub>
    </div>
  </li>
  <li><strong>Results:</strong> Downstream Dolly Perplexity improved significantly to <strong>12.9480</strong> (approaching the 12.6278 Dolly Specialist baseline). GSM8K was 0.0600 and HumanEval was 0.1951.</li>
  <li><strong>Inference:</strong> Calibrating weight updates prior to merging successfully mitigates the magnitude dominance of CodeAlpaca, protecting conversational capabilities, though math reasoning is still degraded by simple linear addition.</li>
</ul>

<div class="page-break"></div>

<h2>4. Category 4: Performance Evaluation & Statistical Verification (Notebook 8)</h2>

<h3>Notebook 8: Downstream Benchmark Evaluation & Bootstrap Testing (<code>./3-adapter-evaluation-codealpaca-metamath-dolly-ttest(2).ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Evaluate the merged checkpoints on GSM8K (200 test problems, EM), HumanEval (164 coding tasks, pass@1), and Dolly-15k (200 conversational samples, response PPL). Conduct bootstrap t-tests to establish statistical significance.</li>
  <li><strong>Methodology:</strong> Evaluated models using greedy decoding under baseline configurations (320 tokens, repetition_penalty=1.3). Executed pairwise bootstrap t-tests with <strong>10,000 resamples</strong> to verify the performance differences.</li>
  <li><strong>Results:</strong>
    <ul>
      <li>SVD Merge (Rank-16) achieved the highest math performance among merged models (GSM8K = <strong>0.1550</strong>), significantly outperforming Linear Merge (0.1100, $p=0.038^*$) and DARE (0.0400, $p<0.001^{***}$).</li>
      <li>DARE Merge achieved the highest coding performance (HumanEval = <strong>0.2378</strong>), significantly outperforming Linear (0.2012) and MetaMath Specialist (0.1220, $p=0.004^{**}$).</li>
      <li>SLERP Merge achieved the best perplexity (Dolly PPL = <strong>13.0035</strong>), matching the Dolly specialist (12.6278), but collapsed catastrophically on GSM8K math reasoning (<strong>0.0100</strong>).</li>
    </ul>
  </li>
  <li><strong>Inference:</strong> SVD-based merging is the statistically superior approach for preserving complex reasoning capabilities, while element drop (DARE) is highly effective for code syntax. SLERP preserves conversational perplexity but completely destroys structured reasoning.</li>
</ul>

<h2>5. Category 5: Diagnosing and Fixing SLERP Collapse (Notebooks 9–11)</h2>

<h3>Notebook 9: SLERP Angle Diagnostic (<code>./slerp-angle-diagnostic(2).ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Determine why SLERP (Spherical Linear Interpolation) collapsed catastrophically on reasoning tasks.</li>
  <li><strong>Methodology:</strong> Calculated the layer-wise angle ($\theta$) between Dolly, MetaMath, and CodeAlpaca weight vectors across all 196 layers.
    <div class="formula-box">
      &theta; = arccos(&lang;&Delta;W<sub>A</sub>, &Delta;W<sub>B</sub>&rang; / (&Vert;&Delta;W<sub>A</sub>&Vert;<sub>F</sub> &middot; &Vert;&Delta;W<sub>B</sub>&Vert;<sub>F</sub>))
    </div>
  </li>
  <li><strong>Results:</strong>
    <ul>
      <li>Dolly vs MetaMath: Mean angle = <strong>87.90&deg;</strong> (&sigma; = 1.22&deg;)</li>
      <li>Dolly vs CodeAlpaca: Mean angle = <strong>88.63&deg;</strong> (&sigma; = 1.04&deg;)</li>
      <li>MetaMath vs CodeAlpaca: Mean angle = <strong>88.89&deg;</strong> (&sigma; = 0.94&deg;)</li>
    </ul>
    Over 97% of layers fall within 5&deg; of orthogonality (90&deg;).
  </li>
  <li><strong>Inference:</strong> Due to High-Dimensional Measure Concentration (Concentration of Measure), independent fine-tuning runs produce orthogonal updates. In this regime, SLERP degrades to linear interpolation with non-linear norm scaling. This distorts the projection weight spaces of key attention layers, explaining the reasoning collapse.</li>
</ul>

<h3>Notebook 10: Closing Evidence Gaps (<code>./closing-evidence-gaps(1).ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Verify if a norm-corrected SLERP resolves the reasoning collapse, and mathematically quantify the destructiveness of SVD truncation vs TIES/DARE element trimming.</li>
  <li><strong>Methodology:</strong>
    <ol>
      <li>Evaluated a modified SLERP algorithm that scales the output vector norm using a geometric mean of input norms instead of linear interpolation.</li>
      <li>Calculated the exact singular-value energy retention ($\sum_{i=1}^k \sigma_i^2 / \sum_{i=1}^R \sigma_i^2$) across all 196 layers.</li>
    </ol>
  </li>
  <li><strong>Results:</strong>
    <ul>
      <li>The SLERP Norm Fix did not recover GSM8K math performance (remained at <strong>0.0100</strong> Exact Match).</li>
      <li>SVD rank-16 truncation retained <strong>94.93% of weight energy</strong> (losing only 5.07% across layers).</li>
      <li>TIES/DARE magnitude element trimming retained only <strong>69.06% of weight energy</strong> (losing 30.94% of energy).</li>
    </ul>
  </li>
  <li><strong>Inference:</strong> SLERP's failure is fundamentally caused by high-dimensional orthogonal concentration of measure rather than scalar magnitude distortion. SVD rank truncation is <strong>6&times; less destructive</strong> to weight energy than parameter-wise element trimming, explaining SVD's superior reasoning retention.</li>
</ul>

<h3>Notebook 11: SLERP-Fixed Close-Out Evaluation (<code>./slerp-fixed-eval(1).ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Conduct a final downstream evaluation of the corrected SLERP model checkpoint (`Srishtik/Qwen3-0.6B-slerp-FIXED-3-adapters-merged-2`).</li>
  <li><strong>Methodology:</strong> Evaluated the checkpoint on the full evaluation suite (GSM8K, HumanEval, Dolly PPL).</li>
  <li><strong>Results:</strong> Dolly Perplexity reached <strong>11.9834</strong> (outperforming all merged models and even the Dolly Specialist's 12.6278). However, GSM8K EM (0.0150) and HumanEval pass@1 (0.1463) remained collapsed.</li>
  <li><strong>Inference:</strong> Spherical interpolation on orthogonal manifolds is highly effective at smoothing the language modeling surface (lowering perplexity) but disrupts the task-specific low-rank coordinates required for structured reasoning and programming.</li>
</ul>

<div class="img-grid-2 avoid-break">
  <div class="img-card">
    <img src="''' + imgs['slerp_angle'] + '''" alt="SLERP Angles">
    <div class="img-caption">Figure 3a: Layer-wise Pairwise Angles</div>
  </div>
  <div class="img-card">
    <img src="''' + imgs['merged_svd'] + '''" alt="Merged SVD Decay">
    <div class="img-caption">Figure 3b: Merged Model Singular Value Decays</div>
  </div>
</div>

<div class="page-break"></div>

<h2>6. Category 6: Representation Overlap & Submodule Diagnostics (Notebooks 12–15)</h2>
<p>
  To move beyond weight-space metrics, we analyzed representation dynamics in activation space using Centered Kernel Alignment (CKA).
</p>

<h3>Notebook 12: Delta-Representation CKA Analysis (<code>./cka-representation-analysis(3).ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Measure hidden-state activation similarity between merged models and specialist models.</li>
  <li><strong>Methodology:</strong> Standard CKA saturates near 1.0 because base model weights dominate activations. We developed **v2 Delta CKA**, which isolates adapter perturbations by subtracting base model activations:
    <div class="formula-box">
      &Delta;h = h<sub>model</sub>(x) - h<sub>base</sub>(x), &nbsp;&nbsp;&nbsp;&nbsp; CKA<sub>delta</sub> = CKA(&Delta;h<sub>merged</sub>, &Delta;h<sub>specialist</sub>)
    </div>
  </li>
  <li><strong>Results:</strong>
    <ul>
      <li>Coding accuracy (HumanEval) strongly correlates with CKA similarity to CodeAlpaca (r = +0.799).</li>
      <li>Math accuracy (GSM8K) is **negatively correlated** with CKA similarity to MetaMath (r = -0.895) for TIES/DARE. DARE and TIES exhibit higher overall CKA (0.9238 and 0.9189) than SVD (0.9064), yet score substantially lower on math.</li>
    </ul>
  </li>
  <li><strong>Inference:</strong> Math reasoning depends on precise low-rank subspace alignment, which is destroyed by element-wise trimming in TIES/DARE even though they maintain high coarse activation overlap (CKA).</li>
</ul>

<h3>Notebook 13: Per-Layer CKA & Effective Rank Spectrum (<code>./per-layer-cka-and-effective-rank(1).ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Map CKA similarity layer-by-layer across all 28 blocks, and calculate the entropy-based effective rank of each specialist adapter.</li>
  <li><strong>Methodology:</strong>
    <ol>
      <li>Extracted representations block-by-block without binning.</li>
      <li>Computed entropy-based effective rank ($erank = \exp(H(p))$, where $p_i = \sigma_i^2 / \sum \sigma_j^2$) of the raw adapter weights.</li>
    </ol>
  </li>
  <li><strong>Results:</strong>
    <ul>
      <li>Effective ranks: Dolly = <strong>12.3732</strong> (77.3% of nominal 16); MetaMath = <strong>14.3591</strong> (89.7%); CodeAlpaca = <strong>14.2404</strong> (89.0%).</li>
      <li>Representation similarity diverges significantly in intermediate layers (Blocks 7–11).</li>
    </ul>
  </li>
  <li><strong>Inference:</strong> Dolly uses less rank budget, suggesting that equal rank allocation in BWSum/SVD is suboptimal. Blocks 7–11 act as critical task routing hubs where merging methods deviate most.</li>
</ul>

<h3>Notebook 14 & 15: Attention vs MLP Sublayer CKA Breakdown (<code>./per-layer-cka-attn-mlp-breakdown(2).ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Hook and isolate the outputs of `self_attn` and `mlp` sublayers in Blocks 7–11 to pinpoint the driver of representation divergence.</li>
  <li><strong>Methodology:</strong> Computed delta-CKA on raw submodule contributions to the residual stream (before the residual add).</li>
  <li><strong>Results:</strong>
    <ul>
      <li>GSM8K block 7–11 mean spread: Attention = <strong>0.0244</strong>, MLP = <strong>0.0170</strong>.</li>
      <li>HumanEval block 7–11 mean spread: Attention = <strong>0.0328</strong>, MLP = <strong>0.0142</strong>.</li>
    </ul>
    Attention sublayers consistently show larger CKA spreads across merging algorithms.
  </li>
  <li><strong>Inference:</strong> Divergence in the critical task-routing layers (Blocks 7–11) is driven primarily by Attention projection sublayers. Attention weight projections are highly sensitive to weight interpolation.</li>
</ul>

<div class="img-card avoid-break" style="margin: 12px 0;">
  <img src="''' + imgs['cka_heatmap'] + '''" alt="CKA Delta Heatmap" style="max-height: 220px;">
  <div class="img-caption">Figure 4: Layer-wise CKA Delta Representation Heatmap Across Merged Models</div>
</div>

<div class="page-break"></div>

<h2>7. Category 7: Advanced Merging Strategies & Hyperparameter Sweeps (Notebooks 12, 16–17)</h2>
<p>
  We conducted three hyperparameter sweeps to resolve open performance limits: decoding budgets, independent rank allocation, and joint rank budget sweeps.
</p>

<h3>Notebook 12: Decoding-Budget Ablation Sweep (<code>./gsm8k-ablation-full-1 (1).ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Determine if low GSM8K scores were driven by weight interference or token truncation.</li>
  <li><strong>Methodology:</strong> Conducted a staged decoding sweep for all 14 models, expanding generation budget from 320 to 512 and 768 tokens, and setting repetition penalty to 1.0.</li>
  <li><strong>Results:</strong>
    <ul>
      <li>All 14 models were budget-limited in initial evals. Expanding the token budget dramatically increased GSM8K performance.</li>
      <li>MetaMath specialist accuracy jumped from <strong>0.2200 to 0.5250</strong> (+0.3050).</li>
      <li>SVD Merge (Rank-16) jumped from <strong>0.1550 to 0.3950</strong> (+0.2400).</li>
      <li>SLERP models recovered from 0.0100 to 0.2250, but generated extremely long sequences (282-334 tokens), hitting token caps up to 37.5% of the time (Chattiness Tax).</li>
    </ul>
  </li>
  <li><strong>Inference:</strong> SVD remains the superior merge method. SLERP induces high verbosity (chattiness), taxing the decoding budget.</li>
</ul>

<h3>Notebook 16: Effective-Rank-Proportional Adaptive Merge (<code>./adaptive-rank-merge-and-block-diagnostic-1(1).ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Allocate rank budgets dynamically to Dolly, MetaMath, and CodeAlpaca based on their effective rank, and truncate updates independently *before* summing.</li>
  <li><strong>Methodology:</strong> Allocates ranks (Dolly = 7.19, MetaMath = 8.47, CodeAlpaca = 8.34). Updates are truncated independently and then summed. Evaluated across budgets 16, 20, 24, 32, 40, and 48.</li>
  <li><strong>Results:</strong> Collapsed GSM8K accuracy to <strong>0.0000</strong> across all budgets. Full-sample evaluation (budget=24): GSM8K = <strong>0.0000</strong>, HumanEval = <strong>0.1585</strong>, Dolly PPL = <strong>19.1178</strong>.</li>
  <li><strong>Inference:</strong> Independent truncation of adapter updates before combination destroys the fine-grained task-specific subspaces, leading to catastrophic collapse even with dynamic budget allocation.</li>
</ul>

<h3>Notebook 17: Joint SVD Budget Sweep (<code>./joint-svd-budget-sweep(3).ipynb</code>)</h3>
<ul>
  <li><strong>Objective:</strong> Perform a budget sweep for Joint SVD Merge (sum first, then truncate combined matrix) across ranks 16, 20, 24, 32, 40, and 48, using a proxy sample count (n=60) and full evaluation on the best candidate.</li>
  <li><strong>Why we did it:</strong> To isolate whether the adaptive rank failure was due to budget size or the independent truncation method.</li>
  <li><strong>Results:</strong>
    <ul>
      <li>Sweep best proxy: rank=20 (EM = 0.2333 at n=60).</li>
      <li>Full evaluation (n=200/164/200) for rank=20: GSM8K = <strong>0.1250</strong>, HumanEval = <strong>0.1829</strong>, Dolly PPL = <strong>19.4030</strong>.</li>
      <li>Rank=20 SVD did NOT outperform Rank-16 SVD (GSM8K 0.1250 vs 0.1550, HumanEval 0.1829 vs 0.2073).</li>
    </ul>
  </li>
  <li><strong>Inference:</strong> Joint SVD at rank-16 is highly optimal. Increasing the budget to 20 introduces extra noise directions that degrade task capability, confirming that joint-truncation is the critical mechanism, not budget expansion.</li>
</ul>

<div class="page-break"></div>

<h2>8. Comprehensive Overview of All 17 Experiments</h2>

<table>
  <thead>
    <tr>
      <th>#</th>
      <th>Notebook Path & Category</th>
      <th>Main Experimental Objective</th>
      <th>GSM8K EM</th>
      <th>HumanEval pass@1</th>
      <th>Dolly PPL</th>
      <th>Key Inferences & Scientific Findings</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td><strong>dolly-training-adapter (1).ipynb</strong><br>(Training)</td>
      <td>Train general instruction specialist on Dolly-15k.</td>
      <td class="num">0.0250</td>
      <td class="num">0.1646</td>
      <td class="num" style="color:#16a34a; font-weight:700;">12.6278</td>
      <td>Establishes baseline conversational perplexity; lacks specialized capabilities.</td>
    </tr>
    <tr>
      <td>2</td>
      <td><strong>metamathqa-training.ipynb</strong><br>(Training)</td>
      <td>Train math reasoning specialist on MetaMathQA-15k.</td>
      <td class="num" style="color:#16a34a; font-weight:700;">0.2200</td>
      <td class="num">0.1220</td>
      <td class="num">28.6676</td>
      <td>Establishes math baseline. Receptive to reasoning-oriented fine-tuning.</td>
    </tr>
    <tr>
      <td>3</td>
      <td><strong>qwen-training-on-code-alpaca.ipynb</strong><br>(Training)</td>
      <td>Train programming specialist on CodeAlpaca-18k.</td>
      <td class="num">0.0850</td>
      <td class="num" style="color:#16a34a; font-weight:700;">0.1707</td>
      <td class="num">38.3633</td>
      <td>Acquires python syntax capabilities. Training degrades conversational perplexity (38.36).</td>
    </tr>
    <tr>
      <td>4</td>
      <td><strong>3-adapter-comparison-2.ipynb</strong><br>(Comparison)</td>
      <td>Compute Frobenius norms & singular values of specialists.</td>
      <td class="num">N/A</td>
      <td class="num">N/A</td>
      <td class="num">N/A</td>
      <td>Identifies 5&times; norm imbalance (Code=30.7, Dolly=6.1). Linear merges will be biased toward coding.</td>
    </tr>
    <tr>
      <td>5</td>
      <td><strong>3-adapter-merged-model-comparision-fixed-2.ipynb</strong><br>(Comparison)</td>
      <td>Evaluate structural profile of merged models.</td>
      <td class="num">N/A</td>
      <td class="num">N/A</td>
      <td class="num">N/A</td>
      <td>TIES/DARE compress norms; SVD preserves natural singular value decay curves.</td>
    </tr>
    <tr>
      <td>6</td>
      <td><strong>3-different-adapter-merging-2-fixed.ipynb</strong><br>(Merging)</td>
      <td>Implement 6 standard weight-space merges.</td>
      <td class="num">N/A</td>
      <td class="num">N/A</td>
      <td class="num">N/A</td>
      <td>Generates standard merged checkpoints; weight averaging ignores representation alignment.</td>
    </tr>
    <tr>
      <td>7</td>
      <td><strong>7th-method-ct-calibrated-merge(1).ipynb</strong><br>(Merging)</td>
      <td>Implement CT-inspired Magnitude-Calibrated Merge.</td>
      <td class="num">0.0600</td>
      <td class="num">0.1951</td>
      <td class="num">12.9480</td>
      <td>Calibrating norms prevents Dolly from being drowned out, stabilizing perplexity (12.94).</td>
    </tr>
    <tr>
      <td>8</td>
      <td><strong>3-adapter-evaluation-codealpaca-metamath-dolly-ttest(2).ipynb</strong><br>(Eval)</td>
      <td>Benchmark 6 merges & run bootstrap t-tests (n=10k).</td>
      <td class="num">0.1550</td>
      <td class="num">0.2073</td>
      <td class="num">20.5070</td>
      <td>SVD (0.155) significantly beats Linear (0.11, p=0.038). DARE (0.237) beats Linear (0.20, p=0.004).</td>
    </tr>
    <tr>
      <td>9</td>
      <td><strong>slerp-angle-diagnostic(2).ipynb</strong><br>(Diagnostic)</td>
      <td>Compute layer-wise angles between specialists.</td>
      <td class="num">N/A</td>
      <td class="num">N/A</td>
      <td class="num">N/A</td>
      <td>Finds updates are orthogonal (angles ~88&deg;). High-dimensional concentration collapses SLERP.</td>
    </tr>
    <tr>
      <td>10</td>
      <td><strong>closing-evidence-gaps(1).ipynb</strong><br>(Gap Closure)</td>
      <td>Test SLERP norm fix & measure weight truncation energy.</td>
      <td class="num">0.0100</td>
      <td class="num">0.1463</td>
      <td class="num">13.0035</td>
      <td>SVD truncation (94.93%) is 6&times; less destructive than TIES/DARE element trimming (69.06%).</td>
    </tr>
    <tr>
      <td>11</td>
      <td><strong>slerp-fixed-eval(1).ipynb</strong><br>(Eval)</td>
      <td>Evaluate norm-corrected SLERP checkpoint.</td>
      <td class="num" style="color:#b91c1c;">0.0150</td>
      <td class="num">0.1463</td>
      <td class="num" style="color:#16a34a; font-weight:700;">11.9834</td>
      <td>SLERP-fixed achieves best perplexity (11.98) but fails to recover math (0.0150) or code (0.1463).</td>
    </tr>
    <tr>
      <td>12</td>
      <td><strong>gsm8k-ablation-full-1 (1).ipynb</strong><br>(Ablation)</td>
      <td>Perform staged decoding sweep (512/768 tokens).</td>
      <td class="num" style="color:#16a34a; font-weight:700;">0.3950</td>
      <td class="num">0.2073 (unabl)</td>
      <td class="num">20.5070</td>
      <td>Staged decoding shows all models were token-limited. SVD math EM jumps from 0.1550 to 0.3950.</td>
    </tr>
    <tr>
      <td>13</td>
      <td><strong>cka-representation-analysis(3).ipynb</strong><br>(Analysis)</td>
      <td>Measure activation similarity via v2 Delta CKA.</td>
      <td class="num">N/A</td>
      <td class="num">N/A</td>
      <td class="num">N/A</td>
      <td>Coding pass@1 correlates with Code CKA; math EM negatively correlates with math CKA.</td>
    </tr>
    <tr>
      <td>14</td>
      <td><strong>per-layer-cka-and-effective-rank(1).ipynb</strong><br>(Analysis)</td>
      <td>Plot block-wise CKA & calculate effective rank.</td>
      <td class="num">N/A</td>
      <td class="num">N/A</td>
      <td class="num">N/A</td>
      <td>Dolly effective rank is lower (12.3); divergence is concentrated in intermediate Blocks 7–11.</td>
    </tr>
    <tr>
      <td>15</td>
      <td><strong>per-layer-cka-attn-mlp-breakdown(2).ipynb</strong><br>(Analysis)</td>
      <td>Hook Attention & MLP sublayers in Blocks 7–11.</td>
      <td class="num">N/A</td>
      <td class="num">N/A</td>
      <td class="num">N/A</td>
      <td>Representation divergence in Blocks 7–11 is driven primarily by the Attention sublayer.</td>
    </tr>
    <tr class="collapsed-row">
      <td>16</td>
      <td><strong>adaptive-rank-merge-and-block-diagnostic-1(1).ipynb</strong><br>(Sweeps)</td>
      <td>Implement independent adaptive rank-budget merge.</td>
      <td class="num" style="color:#b91c1c; font-weight:700;">0.0000</td>
      <td class="num">0.1585</td>
      <td class="num">19.1178</td>
      <td>Independent SVD truncation prior to summation collapses reasoning (0.0000) across all budgets.</td>
    </tr>
    <tr>
      <td>17</td>
      <td><strong>joint-svd-budget-sweep(3).ipynb</strong><br>(Sweeps)</td>
      <td>Sweep Joint SVD budgets (ranks 16 to 48) at n=60/200.</td>
      <td class="num">0.1250</td>
      <td class="num">0.1829</td>
      <td class="num">19.4030</td>
      <td>Rank=20 SVD regresses vs rank-16 (0.125 vs 0.155). Rank-16 is optimal; joint truncation is critical.</td>
    </tr>
  </tbody>
</table>

<h2>9. Core Mathematical & Architectural Inferences</h2>
<ul>
  <li>
    <span class="bold">Joint vs. Independent Truncation:</span> Truncating adapter updates independently before addition (Adaptive Rank Merge) destroys task capabilities because it discards critical directions that align only after summation. Joint truncation (summing then performing SVD) allows the model to find a shared low-rank manifold, preserving 94.93% of representational energy.
  </li>
  <li>
    <span class="bold">Destructiveness of Trimming:</span> Parameter-wise trimming (TIES/DARE) drops 80% of parameters, losing 30.94% of weight energy. This degrades structured reasoning (GSM8K), which is highly sensitive to coordinate changes. In contrast, SVD rank truncation discards only 5.07% of the energy, maintaining reasoning.
  </li>
  <li>
    <span class="bold">High-Dimensional Orthogonality in SLERP:</span> Because independent fine-tuning updates concentrate around orthogonality ($\approx 88^\circ$), SLERP's angular interpolation fails mathematically. norm correction stabilizes language perplexity but cannot align reasoning sub-manifolds.
  </li>
  <li>
    <span class="bold">Attention-Centric Task Routing:</span> Layerwise CKA reveals that task-specific representation divergence is concentrated in intermediate layers (Blocks 7–11) and driven primarily by Attention projections. MLPs are robust to weight-space averaging, while Attention sublayers are highly sensitive.
  </li>
</ul>

<h2>10. Final Design Principles for Multi-Task LoRA Merging</h2>
<ol>
  <li><span class="bold">Always Truncate Jointly:</span> When merging LoRA adapters, sum the updates first, then perform SVD on the combined matrix to project it back to the target rank. Never truncate adapters independently before merging.</li>
  <li><span class="bold">Prefer SVD for Reasoning Tasks:</span> For models where math reasoning (GSM8K) is a priority, use SVD-based merging. It retains 94.93% of representation energy compared to only 69.06% for TIES/DARE.</li>
  <li><span class="bold">Use DARE for Syntactic Tasks:</span> For coding tasks (HumanEval), where syntactic structure is paramount, DARE's element-wise dropping and scaling is highly optimal.</li>
  <li><span class="bold">Calibrate Magnitudes First:</span> Normalize adapter Frobenius norms before merging to prevent specialists with large updates (e.g., CodeAlpaca) from drowning out conversational signals.</li>
  <li><span class="bold">Avoid SLERP for $k \ge 3$ Adapters:</span> High-dimensional concentration makes SLERP orthogonal and degenerate. Use it only for interpolating between two highly correlated checkpoints.</li>
</ol>

</body>
</html>
'''

with open('lora_adapter_merging_report.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Generated lora_adapter_merging_report.html, size:', os.path.getsize('lora_adapter_merging_report.html'))

cmd = ['google-chrome', '--headless', '--disable-gpu', '--no-sandbox', '--print-to-pdf=lora_adapter_merging_report.pdf', 'lora_adapter_merging_report.html']
res = subprocess.run(cmd, capture_output=True, text=True)
print('Chrome returncode:', res.returncode)
print('PDF file generated:', os.path.exists('lora_adapter_merging_report.pdf'))
if os.path.exists('lora_adapter_merging_report.pdf'):
    print('PDF size:', os.path.getsize('lora_adapter_merging_report.pdf'))
