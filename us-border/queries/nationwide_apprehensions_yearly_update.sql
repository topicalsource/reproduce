-- SELECT fiscal_year, SUM(encounter_count)
-- FROM nationwide_encounters_aor
--   WHERE encounter_type != "Inadmissibles"
-- GROUP BY fiscal_year
-- ORDER BY fiscal_year;

-- SELECT fiscal_year, SUM(encounter_count)
-- FROM nationwide_encounters_aor
--   WHERE encounter_type != "Inadmissibles"
-- GROUP BY fiscal_year
-- ORDER BY fiscal_year;


-- Ensure we have aligned data
-- SELECT fiscal_year, month, SUM(encounter_count)
-- FROM nationwide_encounters_aor
--   WHERE encounter_type != "Inadmissibles"
--   -- WHERE encounter_type = "Apprehensions"
--     AND fiscal_year = 2020
-- GROUP BY fiscal_year, month
-- ORDER BY fiscal_year, month;

-- SELECT fiscal_year, month, SUM(count)
-- FROM cbp_apprehensions_monthly
--   -- WHERE sector NOT LIKE "%Border%"
--   WHERE fiscal_year = 2020
-- GROUP BY fiscal_year, month
-- ORDER BY fiscal_year, month;

-- SELECT year, month, REPLACE(area_of_responsibility, " Sector", ""), SUM(encounter_count)
-- FROM nationwide_encounters_aor
--   WHERE encounter_type = "Apprehensions"
--     AND year = 2020
-- GROUP BY year, month, area_of_responsibility
-- ORDER BY year, month, area_of_responsibility;

-- SELECT year, month, sector, SUM(count)
-- FROM cbp_apprehensions_monthly
--   WHERE sector NOT LIKE "%Border%"
--     AND year = 2020
-- GROUP BY year, month, sector
-- ORDER BY year, month, sector;

-- Ensure we have aligned data
SELECT fiscal_year, SUM(encounter_count)
FROM nationwide_encounters_aor
  WHERE encounter_type != "Inadmissibles"
GROUP BY fiscal_year
ORDER BY fiscal_year;

SELECT year, count
FROM nationwide_apprehensions_yearly
  -- WHERE sector NOT LIKE "%Border%"
  WHERE year >= 2020;