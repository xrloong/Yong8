# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Yong8 constructs Hanzi (Chinese character) glyphs by modeling them as constraint satisfaction problems, inspired by iOS Auto Layout / Android ConstraintLayout. Strokes and components are laid out by declaring geometric constraints, which are solved via the [xrSolver](https://github.com/xrloong/xrSolver) library (installed from GitHub release wheels, see pyproject.toml).

## Commands

Dependencies and the virtualenv are managed with [uv](https://docs.astral.sh/uv/):

```console
uv sync                       # install deps (dev group includes pytest, injector, gekko solver)
uv run pytest                 # run all tests
uv run pytest tests/test/yong8/test_stroke.py            # run one test file
uv run pytest tests/test/yong8/test_stroke.py -k <name>  # run one test
uv run --extra gekko python examples/U5341.py            # run an example (draws 十)
```

Note: pytest is configured with `python_files = "*.py"`, so every `.py` file under `tests/` is collected as a test module.

## Architecture

Source lives in `src/yong8/` (added to pythonpath by pytest config). The core is a hierarchy of "constraint shapes" that each contribute variables, constraints, and objectives to a shared solver `Problem`:

- **shape.py** — `ConstraintShape` (abstract base) defines the problem-building protocol: `appendVariablesTo` / `appendConstraintsTo` / `appendObjectivesTo`, composed by `appendProblemTo` / `generateProblem`. Subclasses `ConstraintRegion` / `ConstraintBoundaryShape` add boundary variables (left/top/right/bottom/width/height/center). Every shape has a UUID and a `resolve(uuid)` lookup that recurses through children.
- **segment.py** → **stroke.py** → **component.py** → **glyph.py** — the composition hierarchy. A stroke is a sequence of beeline/Q-curve segments with direction/weight parameters; components contain strokes; a glyph contains components. Parents implement `appendChildrenProblemTo` to merge child problems.
- **constraint.py** — cross-shape `CompoundConstraint`s, e.g. `SegmentIntersectionConstraint` (parameterized by `IntersectionPos`, exposes `t1`/`t2` intersection variables that callers can further constrain) and `BoundaryConstraint`.
- **factory.py** — `SegmentFactory`, `StrokeFactory`, `ComponentFactory`, `GlyphFactory`. `StrokeFactory` methods are named in Chinese after stroke types (橫, 豎, 橫折鉤, …) and assemble strokes from directed segments.
- **drawing.py** — drawing policies (canvas size / margins).

Variables are created via `generateVariable(prefix, name)` using xrsolver's `V`; naming is `<component-prefix>.<name>`, with prefixes derived from the shape type and UUID.

Typical usage flow (see `examples/`): create strokes via `StrokeFactory`, group them with `ComponentFactory.generateComponent`, add compound constraints (intersections, boundary), call `generateProblem()`, optionally append extra constraints on exposed variables, then solve with an xrsolver solver (e.g. `xrsolver.solver.gekko.Solver`) and `dump()` the result.

Tests (`tests/test/yong8/`) use `injector` for dependency injection: `base.py` provides `BaseTestCase` with an injector wiring factories, drawing policies, and the gekko solver (see `injection.py`).

## Conventions

- Indentation is tabs, and identifiers (factory methods for stroke types) may be Chinese; keep both.
- Comments and docs are bilingual Chinese/English.
