CREATE TABLE `us-border`.cbp_apprehensions_monthly (
  `id` int auto_increment primary key,
  `fiscal_year` VARCHAR(4),
  `year` VARCHAR(4),
  `month` ENUM('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'),
  `sector` VARCHAR(32),
  `region` VARCHAR(32),
  `count` INT UNSIGNED
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin;