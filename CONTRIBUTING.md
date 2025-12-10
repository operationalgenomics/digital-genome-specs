# Contributing to Operational Genomics

Thank you for your interest in contributing to the Digital Genome Framework. This document provides guidelines for contributing while maintaining alignment with the theoretical foundations that make this project unique.

---

## Philosophy of Contribution

Operational Genomics is not merely a software project — it is a **scientific discipline** with deep philosophical foundations. Contributions must respect and reinforce these foundations rather than dilute them.

Before contributing, please understand:

1. **The genome is not a database — it is the brain itself.** Contributions that treat DNA blocks as mere data storage misunderstand the architecture.

2. **Craft Performance is a PRODUCT, not a weighted sum.** Any contribution that implements weighted averages or allows compensatory logic violates a core principle.

3. **The system distinguishes Foucauldian and Platonic truths.** These are not interchangeable categories; they have fundamentally different mutability and provenance characteristics.

4. **The four motors operate in PARALLEL.** Sequential evaluation defeats the purpose of triangulation.

If these principles are unfamiliar, please read the [Foundational Documents](specs/foundations/) before contributing.

---

## Types of Contributions

### Highly Valued

**Domain-Specific Gene Libraries**
- Industrial gene sets for manufacturing, healthcare, energy, logistics
- Must include preconditions, postconditions, and exception handlers
- Must be evaluable by all four motors

**Motor Implementations**
- Alternative algorithms for Praxeological, Nash, Chaotic, or Meristic evaluation
- Domain-specific calibrations
- Performance optimizations that preserve mathematical properties

**Visualization Tools**
- Genome visualization (neurons, synapses, stems, chromosomes)
- Motor evaluation dashboards
- Craft Performance evolution over time

**Integration Adapters**
- Connectors to industrial systems (SCADA, MES, ERP)
- BIM/IFC integration
- IoT sensor adapters

**Documentation**
- Translations of foundational documents
- Tutorial content
- Case studies

**Empirical Validation**
- Benchmark datasets
- Comparative studies against other frameworks
- Industrial case studies with metrics

### Requires Discussion First

**Theoretical Extensions**
- New motor types
- Alternative truth architectures
- Modifications to Craft Performance calculation

Please open an issue to discuss theoretical changes before implementation. These require careful consideration to avoid undermining the framework's coherence.

### Not Accepted

- Changes that replace product function with weighted sums
- Implementations that treat DNA as static data rather than neurons
- Sequential motor evaluation
- Removal of the Foucauldian/Platonic distinction
- Contributions that cannot explain their alignment with foundational principles

---

## Contribution Process

### 1. Understand the Foundations

Read these documents in order:

1. [Philosophical Foundations](specs/foundations/philosophical-foundations.md)
2. [Truth Architecture](specs/foundations/truth-architecture.md)
3. [Parallel Motors](specs/cognitive-core/parallel-motors.md)
4. [Craft Performance](specs/cognitive-core/craft-performance.md)

### 2. Check Existing Issues

Before starting work, check if:
- An issue already exists for your contribution
- Someone else is working on it
- The contribution aligns with project direction

### 3. Open an Issue (for significant changes)

For anything beyond minor fixes, open an issue describing:
- What you want to contribute
- How it aligns with the theoretical foundations
- Any open questions or design decisions

### 4. Fork and Branch

```bash
git clone https://github.com/YOUR_USERNAME/digital-genome-specs.git
cd digital-genome-specs
git checkout -b feature/your-feature-name
```

### 5. Implement Your Contribution

Follow these guidelines:

**Code Style**
- Python: Follow PEP 8
- Use type hints
- Document functions with docstrings
- Include examples in docstrings where appropriate

**Naming Conventions**
- Use terminology from the specification (codon, gene, genome, motor, etc.)
- Avoid synonyms that create confusion (e.g., don't call genes "procedures" or "workflows")

**Testing**
- Include tests for new functionality
- Ensure existing tests pass
- Test motor evaluation produces products, not sums

**Documentation**
- Update relevant specification documents
- Add docstrings to new code
- Include usage examples

### 6. Submit Pull Request

Your PR description should include:

- **What**: Clear description of the change
- **Why**: Motivation and use cases
- **How**: Brief technical explanation
- **Alignment**: How this respects foundational principles
- **Testing**: How you verified correctness

### 7. Review Process

PRs are reviewed for:

1. **Theoretical alignment** — Does it respect the foundations?
2. **Code quality** — Is it well-written and maintainable?
3. **Testing** — Is it adequately tested?
4. **Documentation** — Is it documented?

---

## Code Standards

### Python Implementation

```python
# Good: Uses framework terminology, type hints, clear docstring
def evaluate_gene(
    gene: OperationalGene,
    context: ContextSnapshot,
    intent: Intent
) -> EvaluationResult:
    """
    Evaluate a gene through all four motors in parallel.
    
    Craft Performance is calculated as the PRODUCT of motor scores.
    Any motor returning 0 results in absolute veto.
    
    Args:
        gene: The operational gene to evaluate
        context: Current operational context
        intent: The intended purpose of activation
        
    Returns:
        EvaluationResult with CP and individual motor scores
        
    Example:
        >>> result = evaluate_gene(shutdown_gene, context, intent)
        >>> print(f"CP: {result.craft_performance}")
        CP: 0.2476
    """
    # Implementation...
```

```python
# Bad: Generic terminology, no types, unclear purpose
def process(g, c, i):
    # evaluate the thing
    score = (prax + nash + chaos + meris) / 4  # WRONG: uses average
    return score
```

### Specification Documents

Specification documents should:

- Use precise terminology from the glossary
- Include diagrams where helpful (Mermaid format)
- Reference related specifications
- Explain the "why" not just the "what"

---

## Testing Guidelines

### Unit Tests

Test individual components in isolation:

```python
def test_craft_performance_is_product():
    """CP must be product of motors, not sum or average."""
    scores = {"praxeological": 0.8, "nash": 0.9, "chaotic": 0.7, "meristic": 0.6}
    cp = calculate_craft_performance(scores)
    expected = 0.8 * 0.9 * 0.7 * 0.6  # Product
    assert cp == pytest.approx(expected)
    assert cp != pytest.approx(sum(scores.values()) / 4)  # Not average

def test_zero_motor_causes_veto():
    """Any motor at 0 must result in CP = 0."""
    scores = {"praxeological": 1.0, "nash": 0.9, "chaotic": 0.0, "meristic": 0.8}
    cp = calculate_craft_performance(scores)
    assert cp == 0.0
```

### Integration Tests

Test component interactions:

```python
def test_gene_evaluation_uses_parallel_motors():
    """All four motors must evaluate simultaneously."""
    # Setup...
    result = system.evaluate_gene(gene, context, intent)
    
    assert "praxeological" in result.individual_scores
    assert "nash" in result.individual_scores
    assert "chaotic" in result.individual_scores
    assert "meristic" in result.individual_scores
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_cognitive_core.py -v
```

---

## Questions?

If you have questions about:

- **Theoretical alignment**: Open an issue with the `question` label
- **Implementation details**: Check existing code and specifications first
- **Project direction**: Review the foundational documents

---

## Recognition

Contributors who make significant contributions will be:

- Listed in the repository's contributors
- Acknowledged in relevant publications (with permission)
- Invited to collaborate on research papers (for major theoretical contributions)

---

## Code of Conduct

Be respectful, constructive, and focused on the work. Technical disagreements should be resolved through reasoned argument grounded in the foundational principles, not through personal attacks or appeals to authority.

Remember: **a single verified truth can replace millions of perceived truths.** In this project, we value correctness over consensus.

---

*"The Digital Genome provides the grammar that makes understanding — and therefore true integration — possible."*
