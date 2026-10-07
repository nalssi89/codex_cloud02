# Alternative-method actual input applicability audit

Audit date: 2026-10-07. Scope: existing source/data/research read only; only this evidence file written. No model fit, package install, credentials, network request, or baseline rerun. Coverage: all 17 rows and named subtypes of research_bias_correction/20261007-002200/SYNTHESIS.md:48-67.

## Decisive measured gates

- Active observations: observations/active_source.json selects observations/kmahub_refresh. provenance.json gives retrieval 2026-10-06T23:42:09.597Z, source span 19910101-20261005, daily SHA256 30aae6da5e383bfcadf4e8e652e0b58654828fab95333b07c8f0d55052512747. National equal-weight actual contributors, minimum50; no imputation or62/n scaling. RN_DAY=-9 maps to0 under recorded kmahub policy, so 'true zero' below means exact numerical0 in the active derived source, not independent instrument-level certainty.
- outputs/case_audit.csv: 6,432 VERIFIED of6,580;148 TARGET_OBSERVATION_UNAVAILABLE remain outside observed scoring, not method exclusions. outputs/training_ledger.csv.gz:156,408 rows, all STATUS=OK. Independently reaggregated ALL accepted annual windows from the active daily CSV: maximum absolute OBS difference0; no end>=init, source-year==target-year, invalid calendar window, or historical valid-window intersection with its target year.
- Weekly rain:217/45,756 annual training rows exact0 (0.4743%);30/6,100 unique historical windows0 (0.4918%). Positive near-zero (0,0.1]mm:1,045 repeated/142 unique; (0,1]mm:5,276 repeated/717 unique. Current targets:16/1,874 cases0,2/239 unique windows0. All-wet training strata1,681;one-dry169;two-dry24. At least22 distinct positive outcomes per stratum.
- Monthly rain:0/32,448 training rows and0/316 unique historical windows exact0; none<=1mm; minimum3.4725806451612904mm. All1,342 strata all-wet, at least24 distinct positive outcomes. Targets0/1,342 cases and0/54 unique months0;minimum4.274193548387097mm. Product3mon contains six individual monthly leads, not three-month sums. Product1mon contains eight seven-day weekly leads.
- Mean-response BJP/MOS inputs: all6,432 case strata have varying ensemble means and observations and strictly positive untransformed2D covariance determinant. This is input-rank evidence, NOT validation of a transformation/prior/fit or future skill. Historical3/7members are NOT3/7 independent observations.

## Annual and joint alignment

Same SOURCE_YEAR plus explicit HIST_START/HIST_END T/P vectors:45,756weekly annual pairs and32,448monthly annual pairs. Each fixed T/P case has24 or30 paired years (weekly1,744x24+130x30;monthly1,302x24+40x30). Unique observational vector windows:6,100weekly/316monthly. Full T/P+ALL-lead trajectories are16D (8weeks x2variables) and12D (6months x2variables):232complete weekly issuances (218with24years;14with30),213complete monthly issuances (all24years). Remaining end-horizon issuances have5/6/7weekly leads or1-5monthly leads: retain them for scalar or dimension-matched outputs, never silently discard them from a method comparison.

## Original MEMBER contract versus physical identity

Read all eight original fcst_raw/hcst_mapping gzip schemas, DATA_DICTIONARY.csv:1-8, README_KO.md:1-15, METHOD_CONFIG.yaml:1-16, source metadata listing, and tar archive complete listing. Legitimate original join fields EXIST: MEMBER, MEMBER_NUMBER, INIT_DATE, PRODUCT, LEAD, VARIABLE, SOURCE_FILE; hindcast additionally SOURCE_DATE and SOURCE_YEAR. Example forecast MEMBER=20220307_m100, MEMBER_NUMBER=100. Example hindcast MEMBER=19930307_m100, SOURCE_DATE=19930307, SOURCE_YEAR=1993. SOURCE_FILE locates converted GRIB files under KMA/FCST or KMA/HCST, 1MON for weekly and6MON for monthly; hindcast paths include current case init directories as well as historical dates.

All accepted same-window T/P historical MEMBER-label intersections are complete (6,144weekly annual pairs with3labels;39,612with7;4,608monthly with3;27,840with7). Issued common-label counts vary24-70weekly and18-84monthly; exact distributions below. Full-path labels overlap structurally. This supports an explicit SOURCE_DATE/MEMBER_NUMBER or MEMBER join, not array-index joining. It does NOT certify physical perturbation/lag identity across converted files or statistical iid errors. DATA_DICTIONARY contains no MEMBER definition, only8rows for VALUE/SOURCE_YEAR/observation columns; README/config do not describe member-generation identity; sole metadata file is the station list; archive listing exposes no generation lookup or GRIB metadata dump. Thus physical identity semantics and lag/exchangeability provenance remain an exact metadata gap, rather than 'member IDs unavailable'. Production analysis/data_io.py:294-340 discards labels into value arrays; Forecast/Case schemas:32-47 retain no source identity. A future identity-aware adapter must join original labels, not MEMBER_INDEX in outputs/calibrated_members.csv.gz.

## Pooling and model-generation regimes

Actual ledger regimes, BOTH variables/products:

|Case issuance range|Historical years|Members/year|Weekly rain cases|Monthly rain cases|
|---|---|---:|---:|---:|
|2022-03-07..2022-10-10|1993-2016|3|256|192|
|2022-10-17..2026-05-04|1993-2016|7|1488|1110|
|2026-05-11..2026-08-31|1993-2022|7|130|40|

Dedup key (PRODUCT,VARIABLE,SOURCE_DATE,LEAD,MEMBER):1,039,416 unique original historical member rows, ZERO duplicated keys, ZERO conflicting repeated values. This key describes source features, not unique observational outcomes. Repeated valid windows are extensive (monthly32,448annual features vs316unique outcomes). There are no demonstrated future-case identical hindcast copies to license future issuance rows. No statement that archived operational/reforecast data were available in real time is justified by HIST_END alone.

Conservative observed pool gate: ORIGINAL CASE INIT_DATE<=outer issue; HIST_END<outer issue; retain SOURCE_YEAR exclusion AND exclude historical valid windows intersecting any outer target year; same product/variable; record lead/calendar and regime; do not mix units or conflate unique windows with independent years. Using the UNION of target years for all leads at each outer issuance yields235outer issues per product: weekly192..45,756 eligible annual feature rows and192..6,100unique windows;monthly144..32,448rows and144..316unique windows;24..30source years only. The first issue excludes45,564future weekly and32,304future monthly annual rows. This is an upper-support envelope over all calendars/leads, not evidence of stationarity or permission to indiscriminately pool.

Research wave-2-validation.md:14-16 records KMA operational3 versus trial7 and external APCC descriptions of initialization regimes (1993-2016 versus2017-2022 ocean reanalysis). Source CSV/config contains no exact row-to-ocean-system/model-version map; do not causally label observed changes as those systems. Pooling may use explicit archive-era/member-count strata and common1993-2016 sensitivity on recent targets. Detrending, cyclic smoothing, and hyperparameters must be trained within each outer gate. Do not double-apply nearby-start weighting: no original start-weight coefficient schema is shipped.

## All17 rows and named subtype eligibility

Eligible = actual required inputs present, NOT proven performance or license to omit validation. 'Conditional' denotes a scientific/input contract needing explicit design, not exclusion by difficulty or sample count.

|#|Row/subtypes|Actual eligibility and binding constraint|
|---:|---|---|
|1|Joint Gaussian; univariate BJP|All6,432 mean-observation strata rank2;24/30annual pairs. Temperature mean-based model feasible without IDs/iid. Rain requires zero-aware transform/censoring for weekly217zeros;monthly positive transform has no observed support violation. Bayesian uncertainty/prior and residual checks still needed.|
|2|Climatology CDF mixture; shrinkage|Train-only empirical climatology available for every stratum; preserve weekly atom and equal-year weighting; estimate lambda only inside outer gate. Bayesian shrinkage differs from fixed CDF mixture.|
|3|Limited anomaly MOS; constant variance|Nonconstant predictor/response all strata; train-only anomaly mean and residual scale available. Rain normal support must be censored/transformed/nonnegative; full predictive CDF required.|
|4|Positive Gamma; CSG EMOS|Positive Gamma support valid in ALLmonthly and1,681all-wet weekly training strata; weekly193strata contain zeros, so unconditional positive Gamma invalid there. Positive component Gamma still identifiable from22+distinct positives. CSG accommodates ALLweekly/monthly support; free shift occurrence effect weak/all-wet monthly, regularize/fix parameters rather than claim zero probability proven absent.|
|5|Fixed square-root/cube-root/power censor regression|Nonnegative responses/members support all strata;0maps to boundary, not log(0). Train/evaluate loss in specified units and recompute original-mm CDF/mean; fixed power does not require new physical IDs.|
|6|Hurdle occurrence + Gamma/lognormal amount|Positive intensity support present ALLstrata. Unpenalized zero-occurrence logistic likelihood has no finite intercept in1,681weekly+1,342monthly all-wet strata;169one-dry/24two-dryweekly supports extremely sparse occurrence. Penalized/prior occurrence or gated pooling can produce full predictions; no all-case removal and no daily0.1mm threshold transplant.|
|7|Censored GEV; Tweedie|Both nonnegative/zero-compatible input support present; rare extremes24/30years do not forbid fitting but cannot substantiate free tail/power precision. Constrain/sensitivity-check GEV shape/support and Tweedie p/dispersion; all-wet monthly atom identification weak. Tweedie positive conditional is NOT single Gamma.|
|8|BMA; group BMA; equal-weight Gaussian/rain kernels|Common member values/spread exist, variable M. Equal-weight kernel is permutation-invariant and needs no identity. Temperature Gaussian dressing feasible; rain requires nonnegative and zero-aware kernels. Original labels permit structural joins but persistent physical-group skill semantics unproved; member-specific/group weights conditional on supplied identity provenance, never array index.|
|9|Coefficient partial pooling; cyclic smoothing|Safe support envelope192..45,756weekly/144..32,448monthlyrows present, only24..30sourceyears;316monthly unique outcomes. Train-only calendar/lead/regime conditioning, shared-response dependence accounting, compare pooled baseline to pooled method; no spatial hierarchy inferred from national inputs.|
|10|BJP-ti; detrend-calibrate-retrend; trend-preserving distribution transfer|Source years1993-2016/2022 and observed/source means present allstrata, so trends can be estimated; future trend strength not measured here. Outer-only trend/prior, original-unit backtransform, moving rain censor boundary. Climate-period trend-preservation claim not established by one issued ensemble.|
|11|Ordinal logistic; ELR|24/30varying ordered responses each stratum support train-derived terciles and probabilities. Fit thresholds/categories within train; regularization/separation checks required. Continuous-value/CRPS output not supplied automatically by category-only fits.|
|12|Componentwise distributional boosting; GAMLSS; NGBoost|Mean/spread/date/lead/regime features present allstrata with safe pooled support; same constraints as9, grouped-year validation. Chosen response family must respect rain0/nonnegative support; Normal NGBoost default does not. Componentwise boosting and natural-gradient NGBoost are different subtypes.|
|13|QRF; IDR|Annual outcomes/features available; QRF empirical weights naturally retain zeros, conditional pooled experiment feasible. Distinct-year leaf support required, tails bounded to observed range unless separate tail model. IDR needs declared stochastic order (mean/spread order not established by this audit); dimension/incomparability check, not sample-count blanket exclusion.|
|14|DRN; BQN|Features/pooled rows available; small shared conditional designs permitted, grouped-year nested regularization. DRN response family support and BQN monotonicity/zero atom/bounded tail must be explicit. No automatic iid/spatial replication or 'NN impossible with30' conclusion.|
|15|Schaake; ECC; residual Gaussian copula; dECC|Schaake same-window T/P vectors45,756weekly/32,448monthly plus232/213fullpaths available;no rawIDsneeded. ECC original-label rank template structurally joinable but physical-semantic gate unresolved; don't equate calibrated output index to ECC. Residual copula has aligned annual features; MUST fit out-of-fold conditional PIT residual dependence, weekly atom handled with censor interval/justified randomizedPIT. dECC has actual8week/6month paths, not only scalar; same template provenance plus conditional historical error covariance gate.|
|16|Multivariate BJP; MBCp; MBCr; MBCn; OTC; dOTC|2D T/P paired annual inputs available, rank/parameter covariance diagnostic still needed for chosen predictors/transforms.16D/12Dpath support24/30years not automatically forbidden but requires regularization/rank checks. MBCp/r/n/OTC/dOTC inputs exist for train-only matched vectors; source members not independent observations; climate-period transport versus finite conditional forecast purpose must be specified, scaling/rain support/tail and held-out calibration verified.|
|17|Bayesian finite-member signal-noise|M_historical=3/7 and actual varyingM_issued available; sample noise can be modeled as hypothesis. Neither labels nor exchangeability alone proves iid homogeneous error or sigma_eta^2/M. Correlated/lagged error and regime-sensitive likelihood alternative remains possible. This metadata gap DOES NOT block ordinary mean-based BJP/MOS.|

No exclusions solely for sample size/difficulty. No candidate efficacy ranking or iid claim was measured.

## Machine evidence and exact executed drivers

Paths below are relative to D:/WORK/Projects/omo/Glosea6. Reader driver1 streams the active daily source and alloriginal fcst_raw/hcst_mapping tables; driver2 measures complete paths, regimes, nondegenerate scalar BJP features, and conservative pool support. Exact invocation pattern used through tool.bash: .venv/Scripts/python.exe -c followed by shell-single-quoted driver text (embedded single quotes escaped as '\''), timeout1800seconds. Both invocations completed without error; JSON printed with indent2 to avoid PTY single-line wrapping. No files were written by either driver. The first single-line JSON output was terminal-wrap corrupted; that identical read-only pass was re-executed with indented JSON and parsed successfully. Original code remains below to reproduce calculations. No old validator ran.

A native eval Python kernel importing numpy stalled twice and was killed/restarted; fallback installed .venv Python scientific streaming with standard library completed. No detached shell sessions/resources remain from these passes.

Source/line basis: analysis/data_io.py:145-212 active selection/hash/provenance;214-263 QC aggregation;266-291SOURCE_YEAR/calendar semantics;294-340original label read then discarded; analysis/run_verification.py:80-123cutoff and ledger creation. Existing training ledger CSV contains156,408data rows; exact identifiers/strata/windows are programmatically selected, not guessed from prose. Read research dossiers wave-2-dependence-mixtures.md, wave-2-learning.md, wave-2-validation.md and original SYNTHESIS. DATA_DICTIONARY/README/config are all short source schemas; metadata and tar listing searched as meaningful alternate identity lookup.

Protected baseline check: root .omo/evidence/alternative-baseline-hashes.json ALL60files SHA256 ANDbyte size match;0mismatches. No protected-file edits. Hash-check exact driver below; completed after measurement passes.

### Structured measured evidence

```json
{
  "measurement": {
    "annual_pairs": 156408,
    "cases": {
      "TARGET_OBSERVATION_UNAVAILABLE": 148,
      "VERIFIED": 6432
    },
    "dedup_members": 1039416,
    "duplicate_source_member_different_values": {},
    "duplicate_source_member_rows": {},
    "errors": [],
    "historical_target_year_intersections": {},
    "ledger_rows": 156408,
    "member_numbers": {
      "fcst_raw_1mon": [
        "100",
        "101",
        "102",
        "103",
        "104",
        "105",
        "106",
        "107",
        "108",
        "109",
        "110",
        "111",
        "112",
        "113",
        "114",
        "115",
        "116",
        "117",
        "118",
        "119",
        "120",
        "121",
        "122",
        "123",
        "124",
        "125",
        "126",
        "127",
        "128",
        "129",
        "130",
        "131",
        "132",
        "133",
        "134",
        "135",
        "136",
        "137",
        "138",
        "139",
        "140",
        "141",
        "142",
        "143",
        "144",
        "145",
        "146",
        "147",
        "148",
        "149",
        "150",
        "151",
        "152",
        "153",
        "154",
        "155",
        "156",
        "157",
        "158",
        "159",
        "160",
        "161",
        "162",
        "163",
        "164",
        "165",
        "168",
        "169",
        "170",
        "171",
        "172",
        "173",
        "174",
        "175",
        "176",
        "177",
        "180",
        "181",
        "182",
        "183"
      ],
      "fcst_raw_3mon": [
        "100",
        "101",
        "102",
        "103",
        "104",
        "105",
        "106",
        "107",
        "108",
        "109",
        "110",
        "111",
        "112",
        "113",
        "114",
        "115",
        "116",
        "117",
        "118",
        "119",
        "120",
        "121",
        "122",
        "123",
        "124",
        "125",
        "126",
        "127",
        "128",
        "129",
        "130",
        "131",
        "132",
        "133",
        "134",
        "135",
        "136",
        "137",
        "138",
        "139",
        "140",
        "141",
        "142",
        "143",
        "144",
        "145",
        "146",
        "147",
        "148",
        "149",
        "150",
        "151",
        "152",
        "153",
        "154",
        "155",
        "156",
        "157",
        "158",
        "159",
        "160",
        "161",
        "162",
        "163",
        "164",
        "165",
        "166",
        "167",
        "168",
        "169",
        "170",
        "171",
        "172",
        "173",
        "174",
        "175",
        "176",
        "177",
        "178",
        "179",
        "180",
        "181",
        "182",
        "183"
      ],
      "hcst_mapping_1mon": [
        "100",
        "101",
        "102",
        "103",
        "104",
        "105",
        "106"
      ],
      "hcst_mapping_3mon": [
        "100",
        "101",
        "102",
        "103",
        "104",
        "105",
        "106"
      ]
    },
    "paired": {
      "1mon": {
        "annual_tp_pairs": 45756,
        "common_year_count": {
          "24": 1744,
          "30": 130
        },
        "historical_member_count_errors": 0,
        "historical_tp_common_label_counts": {
          "3": 6144,
          "7": 39612
        },
        "raw_tp_common_member_counts": {
          "24": 8,
          "28": 248,
          "56": 1384,
          "58": 8,
          "70": 226
        },
        "tp_target_pairs": 1874,
        "unique_tp_windows": 6100
      },
      "3mon": {
        "annual_tp_pairs": 32448,
        "common_year_count": {
          "24": 1302,
          "30": 40
        },
        "historical_member_count_errors": 0,
        "historical_tp_common_label_counts": {
          "3": 4608,
          "7": 27840
        },
        "raw_tp_common_member_counts": {
          "18": 1,
          "32": 1,
          "40": 6,
          "42": 184,
          "52": 5,
          "84": 1145
        },
        "tp_target_pairs": 1342,
        "unique_tp_windows": 316
      }
    },
    "rain": {
      "1mon": {
        "annual_repeated": {
          "0_lt_x_le_0.1": 1045,
          "0_lt_x_le_1": 5276,
          "max": 327.5370967741935,
          "min": 0,
          "n": 45756,
          "negative": 0,
          "zero": 217
        },
        "case_dry_count_distribution": {
          "0": 1681,
          "1": 169,
          "2": 24
        },
        "positive_distinct_min": 22,
        "target_cases": {
          "0_lt_x_le_0.1": 48,
          "0_lt_x_le_1": 246,
          "max": 247.89838709677423,
          "min": 0,
          "n": 1874,
          "negative": 0,
          "zero": 16
        },
        "unique_historical_windows": {
          "0_lt_x_le_0.1": 142,
          "0_lt_x_le_1": 717,
          "max": 327.5370967741935,
          "min": 0,
          "n": 6100,
          "negative": 0,
          "zero": 30
        },
        "unique_target_windows": {
          "0_lt_x_le_0.1": 6,
          "0_lt_x_le_1": 32,
          "max": 247.89838709677423,
          "min": 0,
          "n": 239,
          "negative": 0,
          "zero": 2
        }
      },
      "3mon": {
        "annual_repeated": {
          "0_lt_x_le_0.1": 0,
          "0_lt_x_le_1": 0,
          "max": 642.1790322580645,
          "min": 3.4725806451612904,
          "n": 32448,
          "negative": 0,
          "zero": 0
        },
        "case_dry_count_distribution": {
          "0": 1342
        },
        "positive_distinct_min": 24,
        "target_cases": {
          "0_lt_x_le_0.1": 0,
          "0_lt_x_le_1": 0,
          "max": 506.1,
          "min": 4.274193548387097,
          "n": 1342,
          "negative": 0,
          "zero": 0
        },
        "unique_historical_windows": {
          "0_lt_x_le_0.1": 0,
          "0_lt_x_le_1": 0,
          "max": 642.1790322580645,
          "min": 3.4725806451612904,
          "n": 316,
          "negative": 0,
          "zero": 0
        },
        "unique_target_windows": {
          "0_lt_x_le_0.1": 0,
          "0_lt_x_le_1": 0,
          "max": 506.1,
          "min": 4.274193548387097,
          "n": 54,
          "negative": 0,
          "zero": 0
        }
      }
    },
    "reaggregation_max_delta": 0,
    "schemas": {
      "fcst_raw": [
        "CASE_ID",
        "INIT_DATE",
        "PRODUCT",
        "LEAD",
        "VALID_START",
        "VALID_END",
        "AREA",
        "VARIABLE",
        "MEMBER",
        "MEMBER_NUMBER",
        "VALUE",
        "RAW_ANOM",
        "UNIT",
        "SOURCE_FILE"
      ],
      "hcst_mapping": [
        "CASE_ID",
        "INIT_DATE",
        "PRODUCT",
        "LEAD",
        "VALID_START",
        "VALID_END",
        "AREA",
        "VARIABLE",
        "SOURCE_DATE",
        "SOURCE_YEAR",
        "MEMBER",
        "MEMBER_NUMBER",
        "VALUE",
        "RAW_ANOM",
        "UNIT",
        "SOURCE_FILE"
      ]
    },
    "source": {
      "fcst_raw_1mon_prcp": {
        "eligible_historical_rain": null,
        "missing": 0,
        "rain": {
          "0_lt_x_le_0.1": 1052,
          "0_lt_x_le_1": 9067,
          "max": 505.983521,
          "min": 0,
          "n": 101344,
          "negative": 0,
          "zero": 4562
        },
        "rows_nonmissing": 101344,
        "valid_member_counts": {
          "24": 8,
          "28": 248,
          "56": 1384,
          "58": 8,
          "70": 232
        }
      },
      "fcst_raw_1mon_t15m": {
        "eligible_historical_rain": null,
        "missing": 0,
        "rain": null,
        "rows_nonmissing": 101344,
        "valid_member_counts": {
          "24": 8,
          "28": 248,
          "56": 1384,
          "58": 8,
          "70": 232
        }
      },
      "fcst_raw_3mon_prcp": {
        "eligible_historical_rain": null,
        "missing": 34,
        "rain": {
          "0_lt_x_le_0.1": 1,
          "0_lt_x_le_1": 253,
          "max": 856.196167,
          "min": 0,
          "n": 110138,
          "negative": 0,
          "zero": 102
        },
        "rows_nonmissing": 110138,
        "valid_member_counts": {
          "18": 1,
          "32": 1,
          "40": 6,
          "42": 184,
          "52": 6,
          "84": 1212
        }
      },
      "fcst_raw_3mon_t15m": {
        "eligible_historical_rain": null,
        "missing": 34,
        "rain": null,
        "rows_nonmissing": 110138,
        "valid_member_counts": {
          "18": 1,
          "32": 1,
          "40": 6,
          "42": 184,
          "52": 6,
          "84": 1212
        }
      },
      "hcst_mapping_1mon_prcp": {
        "eligible_historical_rain": {
          "0_lt_x_le_0.1": 1207,
          "0_lt_x_le_1": 12194,
          "max": 305.521515,
          "min": 0,
          "n": 295716,
          "negative": 0,
          "zero": 2577
        },
        "missing": 0,
        "rain": {
          "0_lt_x_le_0.1": 1223,
          "0_lt_x_le_1": 12330,
          "max": 305.521515,
          "min": 0,
          "n": 296976,
          "negative": 0,
          "zero": 2607
        },
        "rows_nonmissing": 296976,
        "valid_member_counts": {
          "72": 256,
          "168": 1488,
          "210": 136
        }
      },
      "hcst_mapping_1mon_t15m": {
        "eligible_historical_rain": null,
        "missing": 0,
        "rain": null,
        "rows_nonmissing": 296976,
        "valid_member_counts": {
          "72": 256,
          "168": 1488,
          "210": 136
        }
      },
      "hcst_mapping_3mon_prcp": {
        "eligible_historical_rain": {
          "0_lt_x_le_0.1": 3,
          "0_lt_x_le_1": 5,
          "max": 488.160126,
          "min": 0,
          "n": 208704,
          "negative": 0,
          "zero": 1
        },
        "missing": 0,
        "rain": {
          "0_lt_x_le_0.1": 3,
          "0_lt_x_le_1": 5,
          "max": 488.160126,
          "min": 0,
          "n": 222732,
          "negative": 0,
          "zero": 1
        },
        "rows_nonmissing": 222732,
        "valid_member_counts": {
          "72": 192,
          "168": 1116,
          "210": 102
        }
      },
      "hcst_mapping_3mon_t15m": {
        "eligible_historical_rain": null,
        "missing": 0,
        "rain": null,
        "rows_nonmissing": 222732,
        "valid_member_counts": {
          "72": 192,
          "168": 1116,
          "210": 102
        }
      }
    },
    "strata": {
      "1mon_W01": {
        "cases": 235,
        "rain": {
          "0_lt_x_le_0.1": 132,
          "0_lt_x_le_1": 670,
          "max": 327.5370967741935,
          "min": 0,
          "n": 5742,
          "negative": 0,
          "zero": 28
        },
        "training_n": {
          "24": 218,
          "30": 17
        }
      },
      "1mon_W02": {
        "cases": 235,
        "rain": {
          "0_lt_x_le_0.1": 129,
          "0_lt_x_le_1": 662,
          "max": 327.5370967741935,
          "min": 0,
          "n": 5742,
          "negative": 0,
          "zero": 28
        },
        "training_n": {
          "24": 218,
          "30": 17
        }
      },
      "1mon_W03": {
        "cases": 235,
        "rain": {
          "0_lt_x_le_0.1": 130,
          "0_lt_x_le_1": 664,
          "max": 327.5370967741935,
          "min": 0,
          "n": 5742,
          "negative": 0,
          "zero": 28
        },
        "training_n": {
          "24": 218,
          "30": 17
        }
      },
      "1mon_W04": {
        "cases": 235,
        "rain": {
          "0_lt_x_le_0.1": 132,
          "0_lt_x_le_1": 665,
          "max": 327.5370967741935,
          "min": 0,
          "n": 5742,
          "negative": 0,
          "zero": 27
        },
        "training_n": {
          "24": 218,
          "30": 17
        }
      },
      "1mon_W05": {
        "cases": 235,
        "rain": {
          "0_lt_x_le_0.1": 131,
          "0_lt_x_le_1": 662,
          "max": 327.5370967741935,
          "min": 0,
          "n": 5742,
          "negative": 0,
          "zero": 27
        },
        "training_n": {
          "24": 218,
          "30": 17
        }
      },
      "1mon_W06": {
        "cases": 234,
        "rain": {
          "0_lt_x_le_0.1": 131,
          "0_lt_x_le_1": 654,
          "max": 327.5370967741935,
          "min": 0,
          "n": 5712,
          "negative": 0,
          "zero": 27
        },
        "training_n": {
          "24": 218,
          "30": 16
        }
      },
      "1mon_W07": {
        "cases": 233,
        "rain": {
          "0_lt_x_le_0.1": 131,
          "0_lt_x_le_1": 651,
          "max": 327.5370967741935,
          "min": 0,
          "n": 5682,
          "negative": 0,
          "zero": 26
        },
        "training_n": {
          "24": 218,
          "30": 15
        }
      },
      "1mon_W08": {
        "cases": 232,
        "rain": {
          "0_lt_x_le_0.1": 129,
          "0_lt_x_le_1": 648,
          "max": 327.5370967741935,
          "min": 0,
          "n": 5652,
          "negative": 0,
          "zero": 26
        },
        "training_n": {
          "24": 218,
          "30": 14
        }
      },
      "3mon_M01": {
        "cases": 235,
        "rain": {
          "0_lt_x_le_0.1": 0,
          "0_lt_x_le_1": 0,
          "max": 642.1790322580645,
          "min": 3.4725806451612904,
          "n": 5742,
          "negative": 0,
          "zero": 0
        },
        "training_n": {
          "24": 218,
          "30": 17
        }
      },
      "3mon_M02": {
        "cases": 230,
        "rain": {
          "0_lt_x_le_0.1": 0,
          "0_lt_x_le_1": 0,
          "max": 642.1790322580645,
          "min": 3.4725806451612904,
          "n": 5592,
          "negative": 0,
          "zero": 0
        },
        "training_n": {
          "24": 218,
          "30": 12
        }
      },
      "3mon_M03": {
        "cases": 226,
        "rain": {
          "0_lt_x_le_0.1": 0,
          "0_lt_x_le_1": 0,
          "max": 642.1790322580645,
          "min": 3.4725806451612904,
          "n": 5472,
          "negative": 0,
          "zero": 0
        },
        "training_n": {
          "24": 218,
          "30": 8
        }
      },
      "3mon_M04": {
        "cases": 221,
        "rain": {
          "0_lt_x_le_0.1": 0,
          "0_lt_x_le_1": 0,
          "max": 642.1790322580645,
          "min": 3.4725806451612904,
          "n": 5322,
          "negative": 0,
          "zero": 0
        },
        "training_n": {
          "24": 218,
          "30": 3
        }
      },
      "3mon_M05": {
        "cases": 217,
        "rain": {
          "0_lt_x_le_0.1": 0,
          "0_lt_x_le_1": 0,
          "max": 642.1790322580645,
          "min": 3.4725806451612904,
          "n": 5208,
          "negative": 0,
          "zero": 0
        },
        "training_n": {
          "24": 217
        }
      },
      "3mon_M06": {
        "cases": 213,
        "rain": {
          "0_lt_x_le_0.1": 0,
          "0_lt_x_le_1": 0,
          "max": 642.1790322580645,
          "min": 3.4725806451612904,
          "n": 5112,
          "negative": 0,
          "zero": 0
        },
        "training_n": {
          "24": 213
        }
      }
    }
  },
  "additional": {
    "covariance": {
      "1mon_prcp": {
        "constant_mean_or_response": 0,
        "nonpositive_2d_covariance_determinant": 0,
        "strata": 1874
      },
      "1mon_t15m": {
        "constant_mean_or_response": 0,
        "nonpositive_2d_covariance_determinant": 0,
        "strata": 1874
      },
      "3mon_prcp": {
        "constant_mean_or_response": 0,
        "nonpositive_2d_covariance_determinant": 0,
        "strata": 1342
      },
      "3mon_t15m": {
        "constant_mean_or_response": 0,
        "nonpositive_2d_covariance_determinant": 0,
        "strata": 1342
      }
    },
    "joint_paths": {
      "1mon": {
        "available_lead_counts": {
          "5": 1,
          "6": 1,
          "7": 1,
          "8": 232
        },
        "complete_issuances_common_labels": {
          "24": 1,
          "28": 31,
          "56": 173,
          "58": 1,
          "70": 26
        },
        "complete_issuances_common_years": {
          "24": 218,
          "30": 14
        },
        "leads": [
          "W01",
          "W02",
          "W03",
          "W04",
          "W05",
          "W06",
          "W07",
          "W08"
        ]
      },
      "3mon": {
        "available_lead_counts": {
          "1": 5,
          "2": 4,
          "3": 5,
          "4": 4,
          "5": 4,
          "6": 213
        },
        "complete_issuances_common_labels": {
          "18": 1,
          "32": 1,
          "40": 1,
          "42": 29,
          "84": 181
        },
        "complete_issuances_common_years": {
          "24": 213
        },
        "leads": [
          "M01",
          "M02",
          "M03",
          "M04",
          "M05",
          "M06"
        ]
      }
    },
    "regimes": {
      "1mon": {
        "(24, ('3',), 1993, 2016)": {
          "cases": 256,
          "first_init": "2022-03-07",
          "last_init": "2022-10-10"
        },
        "(24, ('7',), 1993, 2016)": {
          "cases": 1488,
          "first_init": "2022-10-17",
          "last_init": "2026-05-04"
        },
        "(30, ('7',), 1993, 2022)": {
          "cases": 130,
          "first_init": "2026-05-11",
          "last_init": "2026-08-31"
        }
      },
      "3mon": {
        "(24, ('3',), 1993, 2016)": {
          "cases": 192,
          "first_init": "2022-03-07",
          "last_init": "2022-10-10"
        },
        "(24, ('7',), 1993, 2016)": {
          "cases": 1110,
          "first_init": "2022-10-17",
          "last_init": "2026-05-04"
        },
        "(30, ('7',), 1993, 2022)": {
          "cases": 40,
          "first_init": "2026-05-11",
          "last_init": "2026-08-31"
        }
      }
    },
    "safe_pools": {
      "1mon_prcp": {
        "annual_feature_rows_minmax": [
          192,
          45756
        ],
        "future_case_annual_rows_excluded_minmax": [
          0,
          45564
        ],
        "outer_issues": 235,
        "source_years_minmax": [
          24,
          30
        ],
        "unique_observation_windows_minmax": [
          192,
          6100
        ]
      },
      "1mon_t15m": {
        "annual_feature_rows_minmax": [
          192,
          45756
        ],
        "future_case_annual_rows_excluded_minmax": [
          0,
          45564
        ],
        "outer_issues": 235,
        "source_years_minmax": [
          24,
          30
        ],
        "unique_observation_windows_minmax": [
          192,
          6100
        ]
      },
      "3mon_prcp": {
        "annual_feature_rows_minmax": [
          144,
          32448
        ],
        "future_case_annual_rows_excluded_minmax": [
          0,
          32304
        ],
        "outer_issues": 235,
        "source_years_minmax": [
          24,
          30
        ],
        "unique_observation_windows_minmax": [
          144,
          316
        ]
      },
      "3mon_t15m": {
        "annual_feature_rows_minmax": [
          144,
          32448
        ],
        "future_case_annual_rows_excluded_minmax": [
          0,
          32304
        ],
        "outer_issues": 235,
        "source_years_minmax": [
          24,
          30
        ],
        "unique_observation_windows_minmax": [
          144,
          316
        ]
      }
    }
  },
  "protection": {
    "protected_files": 60,
    "mismatches": []
  }
}
```

### Executed driver1

```python
import csv,gzip,json,math,calendar
from pathlib import Path
from collections import Counter,defaultdict
from datetime import date,timedelta
from functools import lru_cache
root=Path.cwd(); src=root/'GLOSEA6_KMA_20220301-20260831_v1'
def rows(p):
 with (gzip.open(p,'rt',encoding='utf-8-sig',newline='') if str(p).endswith('.gz') else open(p,encoding='utf-8-sig',newline='')) as f: yield from csv.DictReader(f)
C={r['CASE_ID']:r for r in rows(root/'outputs/case_audit.csv')}; L=list(rows(root/'outputs/training_ledger.csv.gz')); A=defaultdict(dict)
for r in L:
 if r['STATUS']=='OK': A[r['CASE_ID']][int(r['SOURCE_YEAR'])]=r
D={r['DATE']:r for r in rows(root/'observations/kmahub_refresh/asos_kma_daily.csv.gz')}
@lru_cache(None)
def obs(s,e,v):
 a=date.fromisoformat(s); b=date.fromisoformat(e); z=[]
 for i in range((b-a).days+1):
  r=D.get((a+timedelta(days=i)).strftime('%Y%m%d'))
  if not r or r['QC_'+v.upper()]!='OK' or int(r['N_STATION_'+v.upper()])<50:return None
  z.append(float(r[v.upper()]))
 return math.fsum(z)/(len(z) if v=='t15m' else 1)
def freq(values):
 z=list(values);return {'n':len(z),'zero':sum(x==0 for x in z),'0_lt_x_le_0.1':sum(0<x<=.1 for x in z),'0_lt_x_le_1':sum(0<x<=1 for x in z),'negative':sum(x<0 for x in z),'min':min(z),'max':max(z)}
errors=[]; crossings=Counter(); maxdelta=0
for k,yrs in A.items():
 c=C[k]; ini=date.fromisoformat(c['INIT_DATE']); ty=date.fromisoformat(c['VALID_START']).year
 for y,r in yrs.items():
  s=date.fromisoformat(r['HIST_START']);e=date.fromisoformat(r['HIST_END']); x=obs(r['HIST_START'],r['HIST_END'],c['VARIABLE']);maxdelta=max(maxdelta,abs(x-float(r['OBS'])) if x is not None else math.inf)
  if e>=ini or y==ty: errors.append([k,y,'baseline cutoff'])
  if s.year<=ty<=e.year: crossings[c['PRODUCT']+'_'+c['VARIABLE']]+=1
  hi=date(y,ini.month,ini.day);lead=int(c['LEAD'][1:])
  if c['PRODUCT']=='1mon':es=hi+timedelta(days=7*(lead-1));ee=es+timedelta(days=6)
  else:
   m=hi.year*12+hi.month-1+lead; yy,mm=divmod(m,12);es=date(yy,mm+1,1);ee=date(yy,mm+1,calendar.monthrange(yy,mm+1)[1])
  if (s,e)!=(es,ee):errors.append([k,y,'window'])
report={'cases':dict(Counter(r['STATUS'] for r in C.values())),'ledger_rows':len(L),'annual_pairs':sum(map(len,A.values())),'reaggregation_max_delta':maxdelta,'errors':errors,'historical_target_year_intersections':dict(crossings),'rain':{},'strata':{},'paired':{},'source':{}}
for p in ['1mon','3mon']:
 ks=[k for k in A if C[k]['PRODUCT']==p and C[k]['VARIABLE']=='prcp']; vals=[float(r['OBS']) for k in ks for r in A[k].values()]; unique={(r['HIST_START'],r['HIST_END']):float(r['OBS']) for k in ks for r in A[k].values()}
 target=[r for r in C.values() if r['PRODUCT']==p and r['VARIABLE']=='prcp' and r['STATUS']=='VERIFIED']
 report['rain'][p]={'annual_repeated':freq(vals),'unique_historical_windows':freq(unique.values()),'target_cases':freq(float(r['OBS']) for r in target),'unique_target_windows':freq({(r['VALID_START'],r['VALID_END']):float(r['OBS']) for r in target}.values()),'case_dry_count_distribution':dict(Counter(sum(float(r['OBS'])==0 for r in A[k].values()) for k in ks)),'positive_distinct_min':min(len(set(float(r['OBS']) for r in A[k].values() if float(r['OBS'])>0)) for k in ks)}
 for lead in sorted(set(C[k]['LEAD'] for k in ks)):
  subset=[k for k in ks if C[k]['LEAD']==lead]; report['strata'][p+'_'+lead]={'cases':len(subset),'training_n':dict(Counter(len(A[k]) for k in subset)),'rain':freq(float(r['OBS']) for k in subset for r in A[k].values())}
 pairs=[]; targetpairs=0
 for k in ks:
  t=k[:-4]+'t15m'
  if t not in A:continue
  common=[y for y in A[k] if y in A[t] and (A[k][y]['HIST_START'],A[k][y]['HIST_END'])==(A[t][y]['HIST_START'],A[t][y]['HIST_END'])];pairs.append(len(common));targetpairs+= C[t]['STATUS']=='VERIFIED'
 report['paired'][p]={'tp_target_pairs':targetpairs,'annual_tp_pairs':sum(pairs),'common_year_count':dict(Counter(pairs)),'unique_tp_windows':len(unique)}
F={};H={}; dedup={}; dup=Counter();disagree=Counter(); regime=Counter();labels=Counter();schemas={}
for kind in ['fcst_raw','hcst_mapping']:
 for p in ['1mon','3mon']:
  for v in ['t15m','prcp']:
   path=src/f'data/model/{kind}/{p}_{v}.csv.gz'; allvals=[]; kept=[]; counts=Counter(); missing=0
   for r in rows(path):
    schemas.setdefault(kind,list(r)); key=r['CASE_ID']; member=r['MEMBER']; year=int(r['SOURCE_YEAR']) if kind=='hcst_mapping' else None
    if not r['VALUE']:missing+=1;continue
    x=float(r['VALUE']);allvals.append(x);counts[key]+=1
    if kind=='fcst_raw':F.setdefault(key,{})[member]=x
    else:
     dk=(p,v,r['SOURCE_DATE'],r['LEAD'],member); prior=dedup.get(dk)
     if prior is not None:
      dup[p+'_'+v]+=1
      if prior!=r['VALUE']:disagree[p+'_'+v]+=1
     else:dedup[dk]=r['VALUE']
     if year in A.get(key,{}):H.setdefault((key,year),{})[member]=x;kept.append(x)
    if v=='prcp':labels[(kind,p,r['MEMBER_NUMBER'])]+=1
   report['source'][kind+'_'+p+'_'+v]={'rows_nonmissing':len(allvals),'missing':missing,'rain':freq(allvals) if v=='prcp' else None,'eligible_historical_rain':freq(kept) if kept and v=='prcp' else None,'valid_member_counts':dict(Counter(counts.values()))}
report['schemas']=schemas;report['duplicate_source_member_rows']=dict(dup);report['duplicate_source_member_different_values']=dict(disagree);report['dedup_members']=len(dedup)
report['member_numbers']={kind+'_'+p:sorted({m for (kk,pp,m) in labels if kk==kind and pp==p},key=int) for kind in ['fcst_raw','hcst_mapping'] for p in ['1mon','3mon']}
for p in ['1mon','3mon']:
 sizes=Counter();hs=Counter();bad=0;full=Counter();hfull=Counter()
 for k in A:
  if C[k]['PRODUCT']!=p or C[k]['VARIABLE']!='prcp':continue
  t=k[:-4]+'t15m';sizes[len(set(F.get(k,{}))&set(F.get(t,{})))]+=1
  for y in A[k]:
   q=set(H.get((k,y),{}))&set(H.get((t,y),{}));hs[len(q)]+=1
   if len(H.get((k,y),{}))!=int(A[k][y]['MEMBERS']):bad+=1
  sib=[kk for kk in A if C[kk]['INIT_DATE']==C[k]['INIT_DATE'] and C[kk]['PRODUCT']==p and C[kk]['VARIABLE'] in ['prcp','t15m']]
  if C[k]['LEAD']==('W01' if p=='1mon' else 'M01'):
   if len(sib)==(8 if p=='1mon' else 6):
    full[len(set.intersection(*(set(F[kk]) for kk in sib)))]+=1
    ys=set.intersection(*(set(A[kk]) for kk in sib));hfull[len(ys)]+=1
 report['paired'][p].update({'raw_tp_common_member_counts':dict(sizes),'historical_tp_common_label_counts':dict(hs),'historical_member_count_errors':bad,'full_tp_alllead_issuance_common_labels':dict(full),'full_tp_alllead_training_years':dict(hfull)})
print(json.dumps(report,sort_keys=True,indent=2))

```

### Executed driver2

```python
import csv,gzip,json,math
from pathlib import Path
from collections import Counter,defaultdict
from datetime import date
R=Path.cwd();S=R/'GLOSEA6_KMA_20220301-20260831_v1'
def rows(p):
 with (gzip.open(p,'rt',encoding='utf-8-sig',newline='') if str(p).endswith('.gz') else open(p,encoding='utf-8-sig',newline='')) as f:yield from csv.DictReader(f)
C={r['CASE_ID']:r for r in rows(R/'outputs/case_audit.csv')};A=defaultdict(dict)
for r in rows(R/'outputs/training_ledger.csv.gz'):
 if r['STATUS']=='OK':A[r['CASE_ID']][int(r['SOURCE_YEAR'])]=r
F=defaultdict(set);H=defaultdict(set);means=defaultdict(list)
for p in ['1mon','3mon']:
 for v in ['t15m','prcp']:
  for r in rows(S/f'data/model/fcst_raw/{p}_{v}.csv.gz'):
   if r['VALUE']:F[r['CASE_ID']].add(r['MEMBER'])
  for r in rows(S/f'data/model/hcst_mapping/{p}_{v}.csv.gz'):
   k=r['CASE_ID'];y=int(r['SOURCE_YEAR'])
   if y in A.get(k,{}):H[k,y].add(r['MEMBER']);means[k,y].append(float(r['VALUE']))
out={'joint_paths':{},'regimes':{},'safe_pools':{},'covariance':{}}
for p in ['1mon','3mon']:
 leads=sorted({C[k]['LEAD'] for k in A if C[k]['PRODUCT']==p});out['joint_paths'][p]={'leads':leads};gs=defaultdict(list)
 for k in A:
  if C[k]['PRODUCT']==p:gs[C[k]['INIT_DATE']].append(k)
 full=Counter();years=Counter();common=Counter()
 for ini,ks in gs.items():
  common[len(ks)//2]+=1
  if len(ks)==2*len(leads):
   full[len(set.intersection(*(F[k] for k in ks)))]+=1;ys=set.intersection(*(set(A[k]) for k in ks));years[len(ys)]+=1
 out['joint_paths'][p].update({'complete_issuances_common_labels':dict(full),'complete_issuances_common_years':dict(years),'available_lead_counts':dict(common)})
 regimes=defaultdict(list)
 for k in A:
  if C[k]['PRODUCT']!=p or C[k]['VARIABLE']!='prcp':continue
  tag=(len(A[k]),tuple(sorted(set(r['MEMBERS'] for r in A[k].values()))),min(A[k]),max(A[k]));regimes[str(tag)].append(C[k]['INIT_DATE'])
 out['regimes'][p]={t:{'cases':len(ds),'first_init':min(ds),'last_init':max(ds)} for t,ds in regimes.items()}
 for v in ['prcp','t15m']:
  ks=[k for k in A if C[k]['PRODUCT']==p and C[k]['VARIABLE']==v];entries=[];unique=[];yr=[];drop=[];monthlead=[]
  for outer in sorted(set(C[k]['INIT_DATE'] for k in ks)):
   targetyears={date.fromisoformat(C[k]['VALID_START']).year for k in ks if C[k]['INIT_DATE']==outer};z=[];future=0
   for k in ks:
    if C[k]['INIT_DATE']>outer:future+=len(A[k]);continue
    for y,r in A[k].items():
     hs=int(r['HIST_START'][:4]);he=int(r['HIST_END'][:4])
     if r['HIST_END']<outer and y not in targetyears and not any(hs<=ty<=he for ty in targetyears):z.append((k,y,r))
   entries.append(len(z));unique.append(len({(r['HIST_START'],r['HIST_END']) for k,y,r in z}));yr.append(len({y for k,y,r in z}));drop.append(future)
  out['safe_pools'][p+'_'+v]={'outer_issues':len(entries),'annual_feature_rows_minmax':[min(entries),max(entries)],'unique_observation_windows_minmax':[min(unique),max(unique)],'source_years_minmax':[min(yr),max(yr)],'future_case_annual_rows_excluded_minmax':[min(drop),max(drop)]}
  variancebad=0;residualzero=0
  for k in ks:
   x=[sum(means[k,y])/len(means[k,y]) for y in A[k]];z=[float(A[k][y]['OBS']) for y in A[k]];mx=sum(x)/len(x);mz=sum(z)/len(z);vx=sum((a-mx)**2 for a in x);vz=sum((b-mz)**2 for b in z);cov=sum((a-mx)*(b-mz) for a,b in zip(x,z));variancebad+=vx<=0 or vz<=0;residualzero+=vx*vz-cov*cov<=0
  out['covariance'][p+'_'+v]={'strata':len(ks),'constant_mean_or_response':variancebad,'nonpositive_2d_covariance_determinant':residualzero}
print(json.dumps(out,indent=2,sort_keys=True))

```

### Executed protection driver

```python
import hashlib,json
from pathlib import Path
r=Path.cwd();manifest=json.load(open(r/'.omo/evidence/alternative-baseline-hashes.json'));bad=[]
for name,want in manifest['files'].items():
 p=r/name
 with p.open('rb') as f:got=hashlib.file_digest(f,'sha256').hexdigest()
 if got!=want['sha256'] or p.stat().st_size!=want['bytes']:bad.append(name)
print(json.dumps({'protected_files':len(manifest['files']),'mismatches':bad},indent=2))

```

