# Constraint-Driven Development: Building Trust in AI-Assisted Code

## The Problem: A Real Scenario

You ask Claude to implement rate limiting for your API. It writes code, runs tests, and reports success. Everything looks good. But weeks later, during load testing, you discover the rate limiter isn't actually persisting state to Redis—it's just tracking requests in memory. When the server restarts, the limits reset.

How did this happen? The specification said "rate state must be persisted in Redis." Claude even wrote a constraint to check for it: `redis-cli keys 'rate:*' | grep -q 'rate:'`. But here's the catch: that constraint was never actually *run* against the empty codebase before implementation started. It would have failed immediately, caught the missing implementation. Instead, it was just words in a document.

This is a fundamental problem with AI-assisted development: **You can't trust that a feature meets requirements unless you've actively proven it does.**

---

## The Core Issue: Specifications Become Fiction

The real problem is deeper than one missed test. When you work with AI agents, several things happen simultaneously:

**Specifications diverge from reality.** You write requirements in a document. Implementation happens in code. Both start coherent, but they evolve independently. Six weeks later, the code does something different than what the spec says. Now you have two sources of truth, and they contradict each other.

**Constraints become decoration.** You write test criteria that look rigorous ("must persist to Redis"), but they're never validated until the end—if at all. By then, fixing a fundamental architecture mistake is expensive.

**No way to know what actually happened.** A task finishes. Did it really meet all requirements? How do you know? What changed between iteration 1 and iteration 5? There's no record.

**Edits can bypass safety.** If a constraint is failing, nothing stops the AI agent (or a developer) from simply rewriting the constraint to make it pass, instead of fixing the implementation. The constraint becomes a target to game, not a rule to follow.

The root cause: **specifications are treated as second-class citizens—documents that sit alongside code but don't control or validate it.**

---

## The Insight: Specifications as First-Class Entities

What if specifications weren't documents that live in parallel with code, but *entities that actively govern what code can be written*?

What if:
- Specifications and implementation *couldn't diverge* because they're synchronized at a fundamental level?
- Constraints *had to fail* before you could write code, proving they test real requirements?
- Every constraint execution was *recorded and immutable*, creating a complete audit trail?
- Specifications *locked themselves* during implementation, preventing mid-course requirement changes?
- You *couldn't exit development* without proving all constraints pass?

This isn't about adding more documentation or better processes. It's about redesigning the system so specifications are enforced by the infrastructure itself.

---

## The Solution: Constraint-Driven Development Framework

**The elevator pitch**: A plugin system that treats specifications as immutable, verified sources of truth. Constraints must be proven to test real code before implementation starts. Every constraint execution is recorded. Specifications lock during execution. Development cannot complete until all constraints pass.

The system has four core mechanisms:

1. **Synchronized Documents** — Specifications exist in two forms (structured data + rendered documentation) that always match. No divergence possible.

2. **Verified Constraints** — Constraints must fail on empty code before you can start implementing. This proves they test real requirements.

3. **Locked Specifications** — Once implementation starts, specifications become read-only. Requirements don't change mid-development.

4. **Complete Audit Trail** — Every constraint execution is recorded. You can see the exact state of every feature at every iteration.

---

## Part I: The Synchronization Problem

### Why Specifications Diverge

Let's start with the simplest problem: keeping specifications and documentation in sync.

Developers write specifications as structured data (JSON—machine-readable) because they need to query it, validate it, apply patches to it. But humans read specifications as documentation (Markdown—human-readable). So you maintain both versions of the same information.

The problem is obvious: they diverge. Someone updates the JSON but forgets to regenerate Markdown. Someone edits the Markdown directly, but the JSON doesn't change. Git shows conflicts. Nothing is the source of truth anymore.

### The Architecture Solution: Canonical Form with Projection

Here's the key insight: **One form is canonical, the other is a projection.**

The JSON is the source of truth. It's the only form that's directly edited. The Markdown is derived from the JSON. Always. Automatically. Every update to JSON immediately regenerates Markdown.

But here's what makes this work: both files are marked read-only. You can't edit either one directly. All changes go through a single API that:
1. Accepts structured update requests
2. Validates them against the semantic model
3. Updates the JSON
4. Regenerates the Markdown
5. Sets both files read-only again

If something tries to directly edit the JSON or Markdown, the system rejects it and says "use the API."

This solves the divergence problem completely. JSON and Markdown never disagree because there's only one way to change either one, and that way keeps them synchronized.

### Why This Matters for AI Agents

When Claude or another AI agent reads the specification and needs to update it, they don't edit files directly. They submit structured update requests. The system validates every request. Invalid changes are rejected with feedback.

More importantly: the specification Claude sees is always consistent with what the code sees. There's no confusion about what the requirement actually is.

---

## Part II: The Verification Problem

### Why Constraints Lie

Now let's talk about constraints—the rules that define what "success" means for a feature.

Suppose you write: "The rate limiter must persist state to Redis." You write a constraint: `redis-cli keys 'rate:*' | grep -q 'rate:'`. It looks solid.

But here's the trap: if the code doesn't implement anything yet, does this constraint fail? Let's see. Redis is empty, so there are no `rate:*` keys. The grep finds nothing. The command exits with failure code 1.

Great! The constraint correctly identifies that the feature isn't implemented. Now you implement rate limiting. The constraint passes. Success.

But what if the constraint was wrong in a subtle way? What if it only passes coincidentally—because you're testing in a specific environment, or because the condition happens to be true for unrelated reasons?

**The problem**: Most constraints pass trivially on incomplete code. They're always true until proven false. They don't actually validate that the feature was implemented correctly; they validate that someone ran the code at all.

### The Zero-State Rule

The architecture enforces a simple rule: **Every constraint must fail on a completely empty codebase.**

If a constraint passes when the feature doesn't exist, it's not testing the feature. It's testing nothing. Delete it.

This means before you write any code, you must:
1. Define the constraint
2. Run it against empty code
3. Watch it fail
4. Mark it as "verified"

Only after verification can you start implementing. This forces you to know *what* you're testing before you write code to pass the test.

### Why This Prevents Bypass

Once a constraint is verified (failed at least once), the system locks critical fields. You can't rewrite the constraint command. You can't change the failure count. You can only update the description.

Why? Because if you allowed edits after verification, an AI agent (or a lazy developer) could rewrite the constraint to make it pass without fixing the code. "The constraint says to check for Redis persistence? Let me change it to just check that Redis exists." Problem bypassed, not solved.

By locking verified constraints, the only way forward is to fix the actual implementation.

### The Execution Model

How does the system actually run constraints? It doesn't care *how*—that's pluggable. Constraints can be:
- Shell commands (exit code 0 = pass, non-zero = fail)
- LLM evaluations ("does the code structure match the design?")
- HTTP assertions (API returns 429 for rate limit)
- Containerized tests (run in isolated Docker)

What matters is the result: did the constraint pass or fail? That result is recorded, timestamped, and never changed.

---

## Part III: The Lifecycle Problem

### Specifications as Moving Targets

Here's a scenario that happens constantly: You specify a feature. Implementation starts. Halfway through, you realize the requirement needs to change. "Actually, we should persist to Memcached instead of Redis." You update the specification. The developer updates the code. Everything works.

Except now you have a problem: which specification was actually implemented? The original one or the updated one? If someone asks "what was intended for this feature?" you don't have a clear answer. The specification that exists now is different from the one that drove implementation.

### Lifecycle States and Locked Specs

The architecture solves this by treating specifications as living documents with an explicit lifecycle.

**Planning State**: Specifications are open for editing. Requirements are being refined. Constraints are being designed and verified. No code implementation happens yet.

**Executing State**: Specifications lock. They become read-only. No changes allowed. Implementation proceeds against a fixed target. Whatever specification exists now is the one being implemented, and it can't change.

**Completion State** (succeed or failed): Specifications remain locked. They preserve what was intended, creating a historical record. If the task failed, the specification shows what was attempted.

This is not about process—it's not "please don't edit specs mid-implementation." It's about architecture: the system physically prevents specification changes once execution starts.

### Iterations as Snapshots

As implementation progresses, the system captures snapshots called iterations. Each iteration records:
- What code changed (files modified, lines added/removed)
- What tests ran (pass rate, coverage)
- Which constraints passed/failed (feature validation results)
- When it happened (timestamp)

Iterations are immutable. Once iteration_1 is recorded, it doesn't change. Iteration_2 is a new snapshot. This creates a timeline:
- At iteration 1, features A and B were passing
- At iteration 3, feature C started passing
- At iteration 5, feature B started failing (regression!)

This history is invaluable. You can see exactly how the code evolved, which features worked when, and where problems appeared.

---

## Part IV: The Control Problem

### Why Sessions End With Broken Code

Developers finish a coding session. They commit their work. Later, QA runs the constraints and discovers three are failing. The code shouldn't have been committed.

Why wasn't this caught? Because the developer finished their work without checking if constraints actually pass. There was nothing preventing them from exiting.

### Enforcement Through Hooks

The system integrates with the development environment through hooks—integration points that observe and control key events.

**Edit/Write Hook**: Before allowing a file to be edited or written, the system checks: are all constraints verified? If unverified constraints exist, editing is blocked. Message: "Fix your constraints first. They must fail on empty code to prove they test real requirements."

The point isn't to be annoying. It's to enforce the zero-state rule. You can't skip constraint verification and jump to coding.

**Stop Hook**: Before a session ends, the system runs all constraints. Are they all passing? If any fail, the session stop is blocked. Message: "These constraints are failing. Fix them before exiting."

Again, the point is infrastructure-level enforcement. You *cannot* end a session with failing constraints. The system won't allow it.

**Specification Lock**: Once a task enters execution, editing the specification is blocked. Not "discouraged"—blocked. The specification is immutable during implementation.

These hooks don't replace process or discipline. They enforce it at the infrastructure level, making violations impossible.

---

## Part V: Putting It Together—The Complete Flow

Here's what a real development session looks like with this architecture:

**Step 1: Planning**
- Define features and their requirements
- Design constraints that test each requirement
- Verify constraints against empty codebase (watch them fail)
- Mark constraints as verified

**Step 2: Implementation Begins**
- Task status transitions to "executing"
- Specifications lock (become read-only)
- Developer writes code

**Step 3: Iterative Development**
- After each significant change, run constraints
- System aggregates results
- Creates iteration snapshot with metrics
- Shows progress: "3/5 features passing, 2 failing"

**Step 4: Completion**
- All constraints passing
- Run stop hook: all constraints pass ✓
- Session can exit cleanly
- Final iteration captures complete metrics
- Task marked "succeed"

**Step 5: Audit Trail**
- Complete history of what was intended (locked spec)
- Iteration-by-iteration progress (code changes, test results, constraint status)
- When problems appeared (which iteration, which constraints)
- How they were resolved

This entire flow is enforced by the system. You can't skip steps or reorder them. You can't ignore failing constraints. You can't change requirements mid-implementation. The system makes all of this impossible.

---

## The Architectural Patterns Underneath

The system achieves this through several architectural patterns:

### Pattern 1: Single Source of Truth with Derived Views

Only the JSON specification is directly editable (through the API). Markdown, git history, and all other views are derived from it. Nothing in the system contradicts the canonical specification.

### Pattern 2: Immutable Results with Audit Trail

Every constraint execution produces a timestamped result record. Results never change. When a constraint passes later, you don't modify the old result—you create a new one. The history is permanent.

### Pattern 3: Explicit State Machines

Task lifecycle is an explicit state machine. Tasks have well-defined states, and transitions between them are controlled. You can't jump from planning to completion; you must go through executing.

### Pattern 4: Asymmetric Permissions Based on State

Constraints have different edit permissions based on their verification state (verified vs. unverified). Specifications have different permissions based on task state (planning vs. executing).

### Pattern 5: Multi-Model Abstraction

The system is abstracted over how constraints are executed. New execution models (bash, LLM, Docker, etc.) can be added without changing the verification or result aggregation logic.

### Pattern 6: Pluggable Extensions

New constraint types, document models, and hook handlers can be added without modifying core code. The system is designed for extension.

---

## Why This Design Matters

Traditional development relies on discipline, process, and review. "Let's all agree to write good tests." "Let's do code review." "Let's document requirements."

This all works until it doesn't—usually under deadline pressure or when working with AI agents that don't understand organizational culture.

The Claude Code Plugin removes discipline from the equation. The system itself enforces:
- **Specifications are trustworthy** — They can't diverge from documentation; they lock during implementation
- **Constraints are real** — They must fail on empty code; they can't be rewritten after verification
- **Progress is measurable** — Every iteration is recorded with objective metrics
- **Incomplete work is blocked** — You can't exit with failing constraints

This works for human developers. It works even better for AI agents, which don't have organizational memory or understand implicit conventions. The system makes everything explicit and enforced.

---

## The Deeper Insight

The real innovation here isn't any single feature—it's the recognition that **specifications must be treated as executable, verifiable entities, not passive documentation.**

In traditional software, specifications are text. "The system must support 10,000 concurrent users." Nice, but unprovable without load testing.

In constraint-driven development, specifications are rules. "The API must return 429 on the 11th request within 60 seconds." Testable. Verifiable. Lockable once requirements are frozen.

The architecture is built around this principle. Every decision—the synchronization layer, the verification barrier, the lifecycle states, the audit trail—flows from the idea that specifications must be first-class, enforced entities that actively govern code quality.

---

## Conclusion

The Claude Code Plugin solves a practical problem: **How do you verify that an AI-generated (or any) implementation actually meets stated requirements?**

The answer is architectural: build a system where specifications are immutable sources of truth, constraints must be verified before implementation, and no development can complete until all requirements are proven.

The result is a framework where:
- ✓ Specifications can't diverge from documentation
- ✓ Constraints can't be bypassed by rewriting them
- ✓ Requirements don't change mid-implementation
- ✓ Progress is objectively measured
- ✓ Incomplete work can't be committed
- ✓ Complete audit trails exist for every decision

This enables developers to confidently delegate complex tasks to AI while maintaining absolute control over quality and requirements.
