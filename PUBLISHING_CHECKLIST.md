# Pre-publication checklist

The staging repository is not ready to publish until the unresolved items
below are reviewed.

## Rights, privacy, and authorship

- [ ] Confirm the source, version, license, redistribution rights, and
  derivative-data terms for WUSTL-EHMS-2020.
- [ ] Confirm who created `wustl-ehms-2020_with_attacks_categories.csv`, how
  `Attack Category` was assigned, and permission to distribute it.
- [ ] Review raw address/MAC-style fields and determine whether the data or
  derived model artifacts could disclose identifying or sensitive information.
- [ ] Choose a project code license only after confirming ownership and
  collaborator approval. No license has been selected or included.
- [ ] Confirm author names, affiliations, paper title, citation, DOI, and
  publication status; none is asserted by this staging snapshot.
- [ ] Obtain permission for any manuscript, figures, or supplementary
  material before adding them. They were not copied into the snapshot.

## Scientific integrity

- [ ] Resolve full-data one-hot encoding before the chronological split.
- [ ] Decide whether the intended estimand is class-held-out detection across
  all periods or future-period detection; the current evaluation pools
  withheld attack examples from earlier periods into test collections.
- [ ] Re-run the corrected protocol and regenerate metrics, tables, logs, and
  figures from source in a clean environment.
- [ ] Reproduce and preserve the statistical-test inputs/output; currently
  cited task logs are absent.
- [ ] Reconcile all manuscript, results, benchmark, and demo metric
  discrepancies before making publication claims.
- [ ] Replace hard-coded/obsolete visualizations with plots generated from
  reproducible result files.
- [ ] Verify the QKD description does not claim complete security or actual
  payload encryption.

## Repository safety and release

- [ ] Review `REPOSITORY_AUDIT.md`, especially all `INVESTIGATE` and `EXCLUDE`
  entries.
- [ ] Run a fresh secret/PII scan on the final snapshot and check Git history
  after initialization. The original folder has no `.git` directory, so no
  local history was available to inspect.
- [ ] Confirm `.gitignore` excludes datasets and locally generated model
  artifacts unless rights/privacy review explicitly permits distribution.
- [ ] Select/complete a citation file only after bibliographic details are
  verified.
- [ ] Review the results and reproduction claims with the research supervisor
  and coauthors.
- [ ] Only after review, initialize Git in this staging directory, inspect
  `git status` and the staged diff, commit locally, create the intended blank
  GitHub repository, add its remote, and push only with explicit approval.

## Manual decisions still needed

1. Project license and owner approval.
2. Dataset source, license, annotation provenance, and publication decision.
3. Authoritative project title and citation metadata.
4. Scientific decision on evaluation protocol and full rerun.
5. Whether the manuscript and demo artifacts may be shared.
