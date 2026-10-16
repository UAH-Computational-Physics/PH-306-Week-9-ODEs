---
applyTo: "**/*.py,**/*.ipynb,**/*.txt,**/*.yml,**/*.ini,**/README.md"
---

# Reusable CodeGrade Rubric and Autotest Conventions

The following is provided as background information regarding how these python files will be used. In general, you can expect two different types of prompts from the user:

1. Prompts on setting up the assignment template (*e.g.*, setting up the framework for students).
2. Prompts regarding the implementation of the solution.

Students (not the generated template) must complete the rubric-scored elements.

## CodeGrade Rubric

The instructor's auto-graded CodeGrade rubric for students is divided into the following parts.

| Category | Description | Points |
| -------- | ----------- | -----: |
| Syntax   | Checks the code using the Python [ast](https://docs.python.org/3/library/ast.html) library for [syntax errors](https://docs.python.org/3/tutorial/errors.html#syntax-errors). | 5 |
| Structure | Ensures that the proper structure exists in your code before running it by using [semgrep](https://docs.semgrep.dev/). | 10 |
| Quality | Runs [flake8](https://flake8.pycqa.org/en/latest/#) and [mypy](https://mypy.readthedocs.io/en/stable/getting_started.html) to ensure Python styling best practices. | 15 |
| Documentation | Checks your code to ensure that it follows [numpy's documentation standards](https://numpydoc.readthedocs.io/en/latest/format.html) using [numpydoc](https://numpydoc.readthedocs.io/en/latest/install.html). | 10 |
| Functionality | Uses [pytest](https://pytest.org/) (with public and private tests) to ensure code is behaving as intended. | 60 |

### What to leave for students in a starter template

When creating a student-facing starter template, do not provide completed solutions to the assignment problems. Leave the problem-solving implementation for students (for example, use `raise NotImplementedError`), while keeping the starter code syntactically valid and including the required function names, signatures, and prompts.

The rubric describes how student submissions are graded; it does not by itself specify which checks a starter template must pass. For this course, the starter is only required to pass the syntax check; don’t add rubric-scored features solely to make it pass the other checks.

Type hints, complete NumPy-style docstrings, and other rubric-checked features must be omitted from the starter as they should be implemented by the students. Follow the assignment-specific instructions for these features; if they do not say, ask the instructor whether students are expected to add them.

### Assignment-specific tests and private grading materials

Use the assignment-specific instructions and supplied tests as the source of truth for required behavior, function contracts, and test thresholds. The rubric summary above does not define those details. Do not infer private-test cases, expected values, or thresholds from the rubric; if a requirement is missing or ambiguous, ask the instructor.

Keep private tests and answer-revealing grading details out of student-facing files. Treat public (student-facing) and private (instructor-only) test updates as separate requests, and only create or modify private tests when explicitly asked.

### Example Template

If the user asks for a new version of the assignment template (in this example, the user asked for a template to check function roots), this is an example of what should be generated:

```python
"""Student assignment implementation file.

Complete the TODOs in this file.
"""

# --- Imports --- #


# --- Problem 1: Quadratic (Projectile Fall Time) --- #
def root_quadratic_projectile_time(h0, v0, g):
    """Find the positive time at which a vertically launched projectile returns to height 0."""
    raise NotImplementedError


# --- Problem 2: Transcendental (Wien's Displacement Law) --- #
def root_wien_displacement_x(coef):
    """Find the positive root x of x * exp(x) = coef * (exp(x) - 1)."""
    raise NotImplementedError


# --- Problem 3: Transcendental (Radioactive Decay) --- #
def root_radioactive_decay_time(N0, N_target, half_life):
    """Find the elapsed time at which a sample of N0 nuclei decays to N_target nuclei."""
    raise NotImplementedError
```

Note that the actual number of problems may vary from assignment to assignment. Also note that this example is incomplete and that instructor generally has anywhere from 5-15 problems for the students to solve on an assignment.

Likewise, the README should be updated when new problem templates are added. Here is an example of the matching README items for the problems above:

```markdown
## Problems

### Projectile Flight Time

A ball is launched straight up from height `h0` with initial velocity `v0`
under gravitational acceleration `g`. Its height is

$$y(t) = h_0 + v_0 t - \tfrac{1}{2} g t^2.$$

Return the positive time `t > 0` at which `y(t) = 0` (the ball lands).
Assume parameters are such that exactly one positive root exists.

### Wien's Displacement Law

Wien's displacement law constant comes from the root of

$$x e^{x} = c\left(e^{x} - 1\right)$$

where $c$ is a coefficient from the blackbody radiation equation (in reality $c=5$). Return the positive root `x`.

### Radioactive Decay

A radioactive sample starts with `N0` nuclei and decays as

$$N(t) = N_0 \left(\tfrac{1}{2}\right)^{t / \tau}$$

where $\tau$ is the half life.

Return the time `t > 0` at which `N(t) = N_target`.
```

The user should request updates to the public (student-facing) and private (instructor-only) tests separately.
