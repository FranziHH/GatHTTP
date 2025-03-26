-----------------------------------
-- comment out, if needed
DROP TABLE IF EXISTS `sc_entry`;
-----------------------------------

CREATE TABLE `sc_entry` (
  `id` int(11) UNSIGNED NOT NULL,
  `current_ts` datetime DEFAULT current_timestamp(),
  `created_ts` datetime DEFAULT NULL,
  `store_id` int(11) UNSIGNED DEFAULT NULL,
  `pos_id` int(11) UNSIGNED DEFAULT NULL,
  `barcode` varchar(255) DEFAULT NULL,
  `entry` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE `sc_entry`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `sc_entry`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
