Title: Fix SDK request dispatch, helper calls, and data feed aliases

Explicit POST requests currently fail, several async methods call synchronous helpers, and two synchronous searches return coroutines. Accept explicit POST alongside DELETE, await the corresponding async helpers in the seven affected methods, and use the synchronous search helper for album and collaborator searches. Expose data_feed and datafeed as the same correctly typed instance on each client. Correct the metadata readme path to readme.md.

Validation used Python 3.12.3 on Linux, standard-library unittest, src-path imports, and mocked aiohttp transport only. No live API calls or writes were made. Tests cover POST with/without a body, implicit GET/POST, mixed-case DELETE, unsupported methods, all named methods and mutation callers, returned data and empty results, request paths/parameters, alias identity/types, and readme existence.

Each slice was tested before its production edit, then rerun:

| Slice / unittest target | Observed red | Green |
| --- | --- | --- |
| tests.test_runtime (initial wrapper and caller tests) | 4 tests, 10 subtest errors: unsupported POST | 4 passed |
| tests.test_runtime.AsyncHelperTests | 10 tests, 10 errors: sync API called from async context | 10 passed |
| tests.test_runtime.SearchTests | 2 tests, 6 assertion failures: coroutine results | 2 passed |
| tests.test_runtime.ClientTests | 2 tests, 2 missing-attribute errors | 2 passed |
| tests.test_metadata | 1 test, missing readme path failure | 1 passed |

Commands for the slice runs: `.venv/bin/python -m unittest <target> -v`.
Final full suite: `.venv/bin/python -m unittest discover -v` — 19 tests passed. The metadata test uses standard-library tomllib (Python 3.11+).

Linux wheel build: `.venv/bin/python -m pip wheel . --no-deps --wheel-dir .verification/wheels` — failed while installing build dependencies. The virtual environment lacks setuptools; network DNS failure prevented fetching setuptools>=40.8.0. No wheel was produced. No project dependencies were changed.

Reviewed the production diff against byte-for-byte copies taken before editing: only the scoped changes, no line-ending churn. No documentation, dependency, version, or CI changes. Local verification logs and this description are under .verification and are review artifacts, not intended PR source files.

Publication blocker: the supplied source folder has no usable Git metadata (`git status` reports “not a git repository”). The provided master SHA adc61e300367e35d88ed01102ac6236190eee172 could not be independently verified; no branch, commit, push, or draft PR could be created here.
