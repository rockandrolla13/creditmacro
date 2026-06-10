-- Thesis Tracker — canonical schema. One thesis row per ticker plus a market_data
-- side table; the computed view derives probability check / weighted price / upside.
--
-- The view's arithmetic mirrors ComputedThesisTrackerRecord.from_record exactly
-- (engine/schema/thesis_tracker.py). Tolerance 0.0001 == the Excel ABS(SUM-100%)<0.0001
-- rule. Nothing here infers a price or a probability: missing inputs -> NULL outputs.

PRAGMA foreign_keys = ON;

-- ── market data: ticker -> current price (the only external number) ──────────
CREATE TABLE IF NOT EXISTS market_data (
    ticker        TEXT PRIMARY KEY,
    current_price REAL,
    as_of_date    TEXT,        -- ISO date
    source        TEXT,
    notes         TEXT
);

-- ── thesis rows: one per ticker ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS thesis_tracker (
    thesis_id          TEXT NOT NULL,
    ticker             TEXT NOT NULL UNIQUE,   -- one row per ticker
    weight_placeholder REAL,
    thesis             TEXT,
    bull_case_price    REAL,
    base_case_price    REAL,
    bear_case_price    REAL,
    p_bull             REAL,
    p_base             REAL,
    p_bear             REAL,
    next_catalyst      TEXT,
    catalyst_date      TEXT,    -- ISO date
    kill_criteria      TEXT,
    status             TEXT NOT NULL DEFAULT 'active',
    source_theme_id    TEXT,
    source_run_id      TEXT,
    source_evidence_ids TEXT NOT NULL DEFAULT '[]',  -- JSON array of strings
    notes              TEXT,
    -- bound probabilities to [0,1]; sum is intentionally NOT constrained (off-sum
    -- rows persist and are flagged CHECK by the view).
    CHECK (p_bull IS NULL OR (p_bull >= 0.0 AND p_bull <= 1.0)),
    CHECK (p_base IS NULL OR (p_base >= 0.0 AND p_base <= 1.0)),
    CHECK (p_bear IS NULL OR (p_bear >= 0.0 AND p_bear <= 1.0)),
    CHECK (status IN ('active','watchlist','closed','killed','stale','needs_review'))
);

-- ── computed read model ──────────────────────────────────────────────────────
CREATE VIEW IF NOT EXISTS thesis_tracker_view AS
SELECT
    t.thesis_id,
    t.ticker,
    t.weight_placeholder,
    t.thesis,
    t.bull_case_price,
    t.base_case_price,
    t.bear_case_price,
    t.p_bull,
    t.p_base,
    t.p_bear,
    t.next_catalyst,
    t.catalyst_date,
    t.kill_criteria,
    t.status,
    t.source_theme_id,
    t.source_run_id,
    t.source_evidence_ids,
    t.notes,
    m.current_price AS current_price,
    CASE
        WHEN t.p_bull IS NULL OR t.p_base IS NULL OR t.p_bear IS NULL THEN NULL
        ELSE (t.p_bull + t.p_base + t.p_bear)
    END AS probability_sum,
    CASE
        WHEN t.p_bull IS NULL OR t.p_base IS NULL OR t.p_bear IS NULL THEN 'MISSING'
        WHEN ABS(t.p_bull + t.p_base + t.p_bear - 1.0) < 0.0001 THEN 'OK'
        ELSE 'CHECK'
    END AS probability_check,
    CASE
        WHEN t.p_bull IS NOT NULL AND t.p_base IS NOT NULL AND t.p_bear IS NOT NULL
             AND ABS(t.p_bull + t.p_base + t.p_bear - 1.0) < 0.0001
             AND t.bull_case_price IS NOT NULL
             AND t.base_case_price IS NOT NULL
             AND t.bear_case_price IS NOT NULL
        THEN (t.bull_case_price * t.p_bull
              + t.base_case_price * t.p_base
              + t.bear_case_price * t.p_bear)
        ELSE NULL
    END AS probability_weighted_price,
    CASE
        WHEN t.p_bull IS NOT NULL AND t.p_base IS NOT NULL AND t.p_bear IS NOT NULL
             AND ABS(t.p_bull + t.p_base + t.p_bear - 1.0) < 0.0001
             AND t.bull_case_price IS NOT NULL
             AND t.base_case_price IS NOT NULL
             AND t.bear_case_price IS NOT NULL
             AND m.current_price IS NOT NULL
             AND m.current_price <> 0
        THEN (t.bull_case_price * t.p_bull
              + t.base_case_price * t.p_base
              + t.bear_case_price * t.p_bear) / m.current_price - 1.0
        ELSE NULL
    END AS upside_to_current
FROM thesis_tracker t
LEFT JOIN market_data m ON m.ticker = t.ticker;
