# Craft Performance
### The Mathematics of Cognitive Convergence

---

## 1. What Craft Performance Is Not

Before defining what Craft Performance (CP) is, we must be clear about what it is not.

**CP is not an average.** If you have one million yen and I have zero yen, our "average" is 500,000 yen each. But this is a fiction — you can buy anything while I beg on the streets. Averages homogenize what cannot be homogenized. They create imaginary entities with imaginary properties.

**CP is not a weighted sum.** Traditional scoring systems add components with weights: `Score = w₁×A + w₂×B + w₃×C`. This allows a high score in one dimension to compensate for a low score in another. An action that is extremely efficient but completely unsafe could still achieve a high total score. This is unacceptable.

**CP is not a vote.** Ten thousand people doing something wrong does not make it right. Consensus is not truth. The majority can be — and often is — wrong.

**CP is not binary.** It is not simply "pass/fail" or "good/bad." Between zero and one exist infinite gradations, each representing a different degree of approximation to the ideal.

---

## 2. What Craft Performance Is

Craft Performance is the **measure of convergence** of the four parallel motors toward the Platonic Form of an action.

It answers the question: "Across all perspectives — intention, strategy, robustness, and imagination — how close is this action to the ideal?"

The ideal (CP = 1.0) is the action that:
- Perfectly realizes its intention (Praxeological Motor)
- Produces perfect equilibrium among all agents (Nash Motor)
- Is perfectly robust to any perturbation (Chaotic Motor)
- Cannot be improved by any imaginable alternative (Meristic Meta-Motor)

This ideal may never be achieved. It is the Platonic Form — approached but never reached. But the distance from this Form can be measured.

---

## 3. The Product Function

The Craft Performance is computed as the **product** of the four motor scores:

```ts
CP = Score_P × Score_N × Score_C × Score_M
```

Where each score is in the interval [0, 1].

This mathematical structure has profound and intentional consequences.

### 3.1 The Veto Property

If **any** motor gives a score of zero, the entire CP is zero.

```ts
CP = 0.95 × 0.88 × 0 × 0.92 = 0
```

This is not a bug — it is the core design principle. A zero from any motor is an **absolute veto**. 

An action that perfectly realizes its intention but creates destructive strategic instability (Nash = 0) is not acceptable.

An action that achieves equilibrium but is extremely fragile to perturbations (Chaotic = 0) is not acceptable.

An action that is robust but contradicts its own purpose (Praxeological = 0) is not acceptable.

No amount of excellence in three dimensions can compensate for complete failure in one. This is the mathematical encoding of the principle that **safety and coherence are non-negotiable**.

### 3.2 The Compression Property

The product of numbers less than one is always less than the smallest factor:

```ts
0.9 × 0.9 × 0.9 × 0.9 = 0.6561
```

Even when all motors give relatively high scores (0.9), the CP is significantly lower (0.66). This is intentional. It means that achieving a high CP requires **all motors to give high scores simultaneously**.

A truly excellent action — one that approaches the Platonic Form — must excel in all four dimensions. Mediocrity in any dimension drags down the entire score.

### 3.3 The Sensitivity Property

Near zero, the function is extremely sensitive:

```ts
0.1 × 0.9 × 0.9 × 0.9 = 0.0729
```

A single low score (0.1) collapses the CP dramatically. This ensures that problematic actions cannot be disguised by excellence in other dimensions.

Near one, the function rewards consistent excellence:

```ts
0.95 × 0.95 × 0.95 × 0.95 = 0.8145
```

Only when all motors converge at high values does the CP reflect genuine quality.

---

## 4. The Interval [0, 1]

The domain of Craft Performance is the closed interval from zero to one, but this interval is not what it appears to be in naive mathematics.

### 4.1 Zero: The Void

CP = 0 represents **absolute failure**. Not just "bad" but "unacceptable" — an action that must not be executed because at least one fundamental perspective rejects it entirely.

Zero is the void. It is the action that contradicts itself, destroys equilibrium, collapses under any perturbation, or is so far from the ideal that even imagining improvements cannot save it.

### 4.2 One: The Platonic Form

CP = 1 represents **perfect truth** — the Platonic Form of the action. It is the ideal that exists in the realm of Forms but may never manifest in the material world.

No real action achieves CP = 1.0. All real actions are imperfect approximations. The Form is the limit, the asymptote, the target that gives direction to all improvement.

### 4.3 The Infinite Between

Between zero and one exist **uncountably infinite** numbers. This is not merely "a lot" — it is a higher order of infinity than the integers. The cardinality of the continuum means that between any two Craft Performance values, no matter how close, there exist infinitely many intermediate values.

This mathematical property reflects the philosophical reality: improvement is always possible. No matter how good an action is, a better one can be imagined. The space between any achieved CP and the ideal 1.0 contains infinite room for evolution.

### 4.4 Fractal, Not Linear

The interval [0, 1] is not uniform in its meaning. The distance from 0.90 to 0.95 is not equivalent to the distance from 0.50 to 0.55.

As CP approaches 1.0, each increment becomes harder to achieve. Moving from 0.9 to 0.95 requires eliminating half of the remaining imperfection. Moving from 0.99 to 0.995 requires eliminating half again. This is asymptotic approach — ever closer, never arriving.

This creates a fractal structure: zoom in on any portion of the interval, and you find infinite detail, infinite room for improvement, infinite gradations of quality.

---

## 5. Convergence Dynamics

### 5.1 When Motors Agree

When all four motors give similar scores, we say the motors **converge**. High convergence with high scores indicates a robust, well-understood action that satisfies all perspectives.

```ts
Scores: [0.85, 0.87, 0.83, 0.86]
CP = 0.85 × 0.87 × 0.83 × 0.86 = 0.527
Convergence = High
```

### 5.2 When Motors Disagree

When motors give divergent scores, we say the motors **diverge**. This indicates an action that appears good from some perspectives but problematic from others.

```ts
Scores: [0.95, 0.30, 0.88, 0.75]
CP = 0.95 × 0.30 × 0.88 × 0.75 = 0.188
Convergence = Low
```

The low CP despite one very high score (0.95) correctly reflects the problematic nature of the action. The Nash Motor's low score (0.30) indicates strategic instability that the other motors cannot compensate for.

### 5.3 Divergence as Information

Motor divergence is not just a problem — it is **information**. When motors disagree, the Oracle Synthesizer can analyze:

- Which motor is raising concerns?
- What specific aspect is problematic?
- Can the action be modified to address the concern?
- Does the divergence indicate fundamental incompatibility?

Divergence may trigger requests for human decision, additional data collection, or Meta-Motor exploration of alternatives.

---

## 6. Relationship to Truth

### 6.1 CP and Foucauldian Truth

Individual registered truths (Foucauldian truths) in the blockchain do not have Craft Performance scores. They are raw experiences, valid in their context, but not evaluated against the Platonic Form.

Foucauldian truth is contextual: "This action worked for this agent in this situation." It makes no claim to universality.

### 6.2 CP and Platonic Approximation

Craft Performance measures how close an action is to the Platonic Form — the ideal action that would work for all agents in all situations.

The DNA of the Digital Genome contains actions with the highest CP scores: those that the system has determined, through rigorous multi-motor evaluation, to be the closest approximations to the ideal.

### 6.3 The Journey from Foucault to Plato

The system's evolution is a journey from collected Foucauldian truths toward Platonic ideals:

1. Experiences are registered (Foucauldian truths, no CP)
2. Motors evaluate patterns (preliminary CP scores)
3. Meta-Motor imagines improvements (hypothetical CP scores)
4. Validated improvements enter DNA (high CP scores)
5. DNA evolves toward ever-higher CP (approaching the Form)

This is the epistemological architecture: from individual experience, through rigorous evaluation, toward universal truth.

---

## 7. Computational Considerations

### 7.1 Score Normalization

Each motor must produce scores normalized to [0, 1]. The normalization method depends on the motor:

**Praxeological Motor**: Ratio of achieved utility to intended utility
```ts
Score_P = min(1, AchievedUtility / IntendedUtility)
```

**Nash Motor**: Distance from Nash equilibrium, normalized
```ts
Score_N = 1 - (EquilibriumDistance / MaxPossibleDistance)
```

**Chaotic Motor**: Inverse of normalized Lyapunov exponent
```ts
Score_C = 1 / (1 + NormalizedLyapunov)
```

**Meristic Meta-Motor**: Comparison to best imagined alternative
```ts
Score_M = CurrentQuality / BestImaginedQuality
```

### 7.2 Handling Uncertainty

When motors cannot compute precise scores due to uncertainty, they output confidence intervals:

```ts
Score_P = 0.85 ± 0.05 (confidence: 0.9)
```

The CP calculation then uses the expected value, but reports the uncertainty range:

```ts
CP = 0.72 ± 0.08
```

High uncertainty in CP may trigger additional data collection or simulation.

### 7.3 Temporal Dynamics

CP is not static. As context changes, as new evidence arrives, as the genome evolves, the CP of any action may change.

The system maintains CP history for analysis:

```typescript
interface CPHistory {
  actionId: string;
  evaluations: {
    timestamp: number;
    cp: number;
    motorScores: MotorScores;
    context: ContextSnapshot;
  }[];
}
```

Declining CP over time may indicate that an action is becoming obsolete. Increasing CP may indicate that conditions are becoming more favorable.

---

## 8. Data Structures

```typescript
interface MotorScore {
  motor: 'praxeological' | 'nash' | 'chaotic' | 'meta';
  value: number;  // [0, 1]
  confidence: number;  // [0, 1]
  uncertainty: number;  // standard deviation
  vetoActive: boolean;
}

interface CraftPerformance {
  value: number;  // [0, 1]
  motorScores: {
    praxeological: MotorScore;
    nash: MotorScore;
    chaotic: MotorScore;
    meta: MotorScore;
  };
  convergenceLevel: number;  // [0, 1]
  confidenceInterval: {
    lower: number;
    upper: number;
    confidence: number;
  };
  computedAt: number;
  contextHash: string;
}

interface CPEvaluationRequest {
  action: CodonSequence | GeneId;
  context: ContextSnapshot;
  evaluationMode: 'standard' | 'deep' | 'simulation';
  uncertaintyTolerance: number;
}

interface CPEvaluationResult {
  request: CPEvaluationRequest;
  craftPerformance: CraftPerformance;
  explanation: CPExplanation;
  recommendations: Recommendation[];
}
```

---

## 9. Interpretive Guidelines

### 9.1 CP Ranges

| CP Range | Interpretation | Recommended Action |
|----------|---------------|-------------------|
| 0.00 | Absolute veto — at least one motor completely rejects | Do not execute; investigate cause |
| 0.01 - 0.20 | Severely problematic | Require major redesign |
| 0.21 - 0.40 | Significant concerns | Require substantial improvement |
| 0.41 - 0.60 | Moderate quality | Acceptable with monitoring |
| 0.61 - 0.80 | Good quality | Approved for standard execution |
| 0.81 - 0.95 | Excellent quality | Candidate for genome inclusion |
| 0.96 - 0.99 | Near-ideal | Rare; candidate for core DNA |
| 1.00 | Platonic Form | Theoretical limit; never achieved |

### 9.2 Warning Signs

**Single Low Motor**: One motor significantly lower than others indicates a specific problem area that may be addressable.

**All Motors Medium**: All motors around 0.5-0.6 indicates a mediocre action that satisfies nothing well.

**High Variance**: Large spread between motor scores indicates an action that is controversial across perspectives.

**Declining Trend**: CP falling over time indicates changing conditions or degrading relevance.

---

## 10. Philosophical Summary

The Craft Performance is not merely a score. It is the **quantified distance from the Platonic Form**.

By using the product function, the system ensures that excellence requires convergence across all four fundamental perspectives. No single virtue can compensate for a fatal flaw. No amount of efficiency justifies danger. No strategic brilliance excuses purposelessness.

The interval [0, 1] contains infinite room for improvement, reflecting the philosophical truth that the ideal is approached but never reached. Evolution is always possible. Perfection is the direction, not the destination.

And through this mathematics, the Digital Genome encodes the deepest principle of operational wisdom: that true quality is not the absence of flaws, but the **convergence of all virtues** — intention, strategy, robustness, and imagination — toward a single, unified excellence.
