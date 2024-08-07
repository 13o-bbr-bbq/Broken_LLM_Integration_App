-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- ホスト: db
-- 生成日時: 2024 年 8 月 07 日 22:15
-- サーバのバージョン： 8.0.28
-- PHP のバージョン: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- データベース: `broken_chatbot`
--

-- --------------------------------------------------------

--
-- テーブルの構造 `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `full_name` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `hashed_password` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `is_superuser` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- テーブルのデータのダンプ `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `full_name`, `hashed_password`, `is_active`, `is_superuser`) VALUES
(1, 'Alice', 'alice@brokenchatbot.example.com	', 'Alice', '$2y$10$tLkmwLYnmnC1jSZ9CEA0WusJ3VpVjJnXEO18r/VlkflotV2ewbeUW', 1, 0),
(2, 'Carol', 'carol@brokenchatbot.example.com	', 'Carol', '$2y$10$WT1ivYSqJp30IJvLZD73H.OQlCuJk1g5eg3oPpSVpNgDCS3Lica06', 1, 1),
(3, 'Charlie', 'charlie@brokenchatbot.example.com', 'Charlie', '$2y$10$j0WzjvV1lPFYmRYTcFx.tuMo5J/uFpLoDVQ9k8cz83SYXXldcXOFS', 1, 1),
(4, 'Dave', 'dave@brokenchatbot.example.com', 'Dave', '$2y$10$rVhbhLGhYnOMe.DGy/9S4eCc78Ep10iaxAQFFJfG46P//k3vtndYa', 1, 1),
(5, 'Bob', 'bob@brokenchatbot.example.com', 'Bob', '$2y$10$hA1sLNNiZ92BhVcF4uXgKO7fmCDZyZxqO0r7IXQqXtgTCP1SiFHRa', 1, 0);

--
-- ダンプしたテーブルのインデックス
--

--
-- テーブルのインデックス `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_users_username` (`username`),
  ADD UNIQUE KEY `ix_users_email` (`email`);

--
-- ダンプしたテーブルの AUTO_INCREMENT
--

--
-- テーブルの AUTO_INCREMENT `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
