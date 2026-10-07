# Existing baseline read-only regression

## Invocation and result

Project-venv Python `-B` imported `analysis.validate_results` and called
`validate(ROOT, Checks())` directly. It did not invoke `main()`, which would
overwrite the protected `outputs/validation.json`.

First monitor: `mon_52DEHC58KMQPXAX8` / `bash_126`, exit **0**.
Bounded-output recovery: `mon_CGFSMYW0VXRB48Y3` / `bash_127`, exit **0**.
Both processes ended normally. No server, browser or temporary resources were
created. No source, observation or baseline output was written by either driver.

The full digest includes nested observation provenance with hundreds of source
receipts; the terminal history dropped its beginning even after the large
top-level difference list was reduced to its length. The complete scientific
counts and numerical deviation fields below were visible in the captured tail.
No further duplicate validation is needed to recover that unrelated provenance.

## Actual recovered evidence

| Quantity | Value |
| --- | ---: |
| Checks passed | 9,163,254 |
| Supplied cases | 6,580 |
| Verified cases | 6,432 |
| Unavailable targets | 148 |
| Baseline prediction rows | 25,728 |
| Accepted annual training rows | 156,408 |
| Observation windows reconstructed | 13,426 |
| Fresh-versus-original observation differences disclosed | 6,870 |
| Identical method masks checked | 4 |
| Held-out refits checked | 8 |
| Held-out prediction invariance checks | 8 |
| Overall groups checked | 16 |

Maximum absolute differences:

- Independent predictive mean: `5.684341886080802e-14`.
- Independent original-unit CRPS: `8.526512829121202e-14`.
- Predictive intervals: `1.1368683772161603e-13`.
- QM algebra: `8.526512829121202e-13`.
- QDM algebra: `3.069544618483633e-12`.
- EMOS CDF-integral oracle: `1.4210854715202004e-14`.
- Held-out training invariance and refit/export matching: exactly `0`.
- Fresh-versus-original source observation difference:
  `2.0632996774193657`, disclosed as a source difference, not a numerical error.

This validates the unchanged existing baseline using its existing tolerances.
It does **not** replace or weaken the separate original strict QDM precision
alert (`1.0345502232667059e-10` against `1e-10`), and it is not evidence of
FULL alternative-method experiment completion.
