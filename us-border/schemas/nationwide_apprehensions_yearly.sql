CREATE TABLE `us-border`.nationwide_apprehensions_yearly (
  `id` int auto_increment primary key,
  `year` VARCHAR(4),
  `count` BIGINT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin;