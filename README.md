# Testing with mocks — Expense report example

This repo is a teaching scaffold for a lesson on **testing with mocks**, using an **expense report** example and a (mockable) BigQuery client (both functional and class-based via `DatabaseBQ`).

### Setup

1. **Create and activate a virtualenv**
   - On Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - On macOS / Linux:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment (.env)**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env       # or copy .env.example .env on Windows
     ```
   - Fill in:
     - `GOOGLE_CLOUD_PROJECT`
     - `BIGQUERY_DATASET`
     - `BIGQUERY_TABLE`
4. **Set these environment variables in your shell** (Cloud Shell or local):
   ```bash
   export GOOGLE_CLOUD_PROJECT=your-gcp-project-id
   export BIGQUERY_DATASET=321_dataset
   export BIGQUERY_TABLE=slides_example
   ```
5. **Make the script executable** 
   ``` bash
   chmod +x scripts/seed_bq.sh
   ```
6. **Seed the table** using the helper script:
   ```bash
   ./scripts/seed_bq.sh
   ```

### How to run the CLI

From the project root (with your virtualenv activated):

```bash
python -m src.example.cli
```

The CLI will:
- Load configuration from `.env`
- Pretend to fetch expense data (you will later swap this out for a real or mocked BigQuery client)
- Print a tiny summary to the console

### How to run tests (pytest)

From the project root:

```bash
pytest
```

The `pytest.ini` is set up so that:
- `src` is on the Python path
- tests live under the `tests` directory

### When ready: BigQuery setup for integration-ish tests

You **do not** need real BigQuery access for the core unit tests. If you want
the "integration-ish" tests and CLI to talk to a real BigQuery table:

3. **(When Ready) Enable BigQuery integration tests**:
   - Set `RUN_BQ_TESTS=1` before running pytest so tests that touch BigQuery
     are enabled:
     ```bash
     export RUN_BQ_TESTS=1
     pytest
     ```

The `scripts/bq_setup.sql` + `scripts/seed_bq.sh` pair together simulate the
**Database dependency** from Slide 10 in a controlled way for this repo.

### Slide mapping

Use this as a guide to connect the slides to the code:

- **Slide 1–4: Project layout & goals**
  - `requirements.txt`
  - `README.md`
  - Folder structure: `src/example`, `tests`, `scripts`

- **Slide 5–7: Core domain logic (pure functions)**
  - `src/example/expense_report.py`
    - Calculating totals
    - Separating I/O from computation so it is easy to test
  - `src/example/models.py`
    - Shared `ExpenseRow` shape for database rows

- **Slide 8–11: Collaborators and mocks**
  - `src/example/bigquery_client.py`
    - Thin wrapper around BigQuery access (to be mocked in tests)
  - `src/example/database_bq.py`
    - `DatabaseBQ` class to mirror `Database.connect("expenses")` from the slides
    - Example of wrapping network I/O behind a small API surface
  - `tests/test_expense_report.py`
    - Using mocks/fakes/doubles for collaborators

- **Slide 12–15: CLI and integration-style tests**
  - `src/example/cli.py`
    - Wiring everything together
  - `tests/test_cli.py`
    - Example of testing the CLI with mocks

- **Slide 16: Refactoring safely with tests**
  - This README’s **“Warning for refactors”** section

You can adjust file names or add more modules, but keep the same ideas: small, focused functions and clear boundaries between pure logic and I/O.

### Warning for refactors (Slide 16)

To keep the examples consistent with the slides and avoid breaking prepared tests:

- **Keep public function headers stable**
  - Do not rename key functions once they are introduced in the slides.
  - Do not reorder or remove required parameters that the tests depend on.

- **Prefer adding default arguments over changing signatures**
  - If you need extra data, **add new parameters with sensible default values** instead of changing or removing existing parameters.
  - Example pattern:
    - Before: `def generate_report(expenses): ...`
    - After:  `def generate_report(expenses, currency="USD"): ...`

- **Avoid breaking test contracts**
  - If you must change behavior, update or add tests deliberately to reflect the new contract.
  - When in doubt, deprecate old behavior gradually instead of deleting it outright.


