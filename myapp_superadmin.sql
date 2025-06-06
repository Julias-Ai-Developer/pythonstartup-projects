-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 06, 2025 at 02:44 AM
-- Server version: 8.0.42
-- PHP Version: 8.4.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `recordlite_app`
--

-- --------------------------------------------------------

--
-- Table structure for table `myapp_superadmin`
--

CREATE TABLE `myapp_superadmin` (
  `id` bigint NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `company` varchar(255) NOT NULL,
  `branch` varchar(50) NOT NULL,
  `role` varchar(50) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `myapp_superadmin`
--

INSERT INTO `myapp_superadmin` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `company`, `branch`, `role`, `phone_number`, `date`) VALUES
(3, 'pbkdf2_sha256$1000000$jYmQ9GTeXpY5CyHtKMZkQ9$xIpzvPcrkMX2l8fJ6zCNmTtyNsqgZ6yMXVdmnjzmoR8=', '2025-06-06 02:01:40.851769', 1, 'admin', 'Julias', 'Admin', 'info@kamatrustai.com', 1, 1, '2025-06-06 01:39:23.509457', 'KAMATRUST AI DEMOS', 'MainBranch', 'SuperSystemAdmin', '+256776828355', '2025-06-05 14:00:00.000000'),
(6, 'pbkdf2_sha256$1000000$wVy1HUZvBHYeHFlui1WI0d$P0rMoWLdhiy2W/j5ydVcrUuXYqNAGZLnQDPH1o8VTZ8=', NULL, 0, 'demo@kabambiro', 'Kachebezi', 'Kapo', 'demo@kabambiro', 1, 1, '2025-06-06 02:26:22.639781', 'KABAMBIRO LTD', 'MainBranch', 'SuperAdmin', '0776828355', '2025-06-06 02:26:23.992809'),
(7, 'pbkdf2_sha256$1000000$0ajkM9S1pqi5DeyZ0kJV6T$U29KxPHo0NxZoT9wunH6RzOHUrwTqrdCwtgsRAq8020=', NULL, 0, 'lc@lucieevents.com', 'Lucie', 'Nyangoma', 'lc@lucieevents.com', 1, 1, '2025-06-06 02:28:27.002889', 'LUCIE EVENTS', 'MainBranch', 'SuperAdmin', '0776828399', '2025-06-06 02:28:28.204430'),
(8, 'pbkdf2_sha256$1000000$o6zcG9y8H0MkO0JngqODBK$GxGKYgGqlRhik2skJuLeGfiscIuqy0oGvjnMxzZ6U0c=', NULL, 0, 'ai@ug.com', 'John ', 'Doe', 'ai@ug.com', 1, 1, '2025-06-06 02:32:09.181554', 'johnUg Supermarket', 'MainBranch', 'SuperAdmin', '0785999523', '2025-06-06 02:32:10.440630'),
(9, 'pbkdf2_sha256$1000000$HA37pks6jIxEBnwJ5VknGp$mn24Z1dzQQ8b61IRXgZszEW65MsCEDvnhpeD9RHOaws=', '2025-06-06 02:42:30.553446', 0, 'cos@f.com', 'JJJ', 'jaajs', 'cos@f.com', 1, 1, '2025-06-06 02:41:17.525562', 'Kos Ltd', 'MainBranch', 'SuperAdmin', '0785740523', '2025-06-06 02:41:18.758991');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `myapp_superadmin`
--
ALTER TABLE `myapp_superadmin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `myapp_superadmin`
--
ALTER TABLE `myapp_superadmin`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
