# Final Submission

Status: locally ready and published; TaskLearn evaluation pending

TaskLearn deliverables:

- `tool_contracts.json`
- `repo_url`: `https://github.com/grinegor/hesperia-assist-function-calling`
- `e2e_tests.json`

Validated locally with:

- `python3 -m compileall hesperia_assist scripts tests`
- `python3 -m unittest discover -s tests`
- `python3 scripts/run_e2e.py`
- `python3 -m hesperia_assist.cli --tool order_lookup --arguments '{"order_id":"ord_1001","customer_id":"cus_100"}'`
- `python3 scripts/secret_scan.py`
