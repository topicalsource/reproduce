CREATE TABLE nationwide_encounters_aor (
  `id` int auto_increment primary key,
  `year` VARCHAR(4),
  `fiscal_year` VARCHAR(4),
  `month` ENUM('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'),
  `month_grouping` ENUM('Remaining', 'FYTD'),
  `component` ENUM('Office of Field Operations', 'U.S. Border Patrol'),
  `region` ENUM('Southwest Land Border', 'Northern Land Border', 'Other'),
  `area_of_responsibility` VARCHAR(32),
  `aor` VARCHAR(16),
  `demographic` ENUM('Single Adults', 'FMUA', 'Accompanied Minors', 'UC / Single Minors'),
  `citizenship` VARCHAR(32),
  `title_of_authority` VARCHAR(16),
  `encounter_type` ENUM( 'Inadmissibles', 'Expulsions', 'Apprehensions'),
  `encounter_count` INT UNSIGNED
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin;