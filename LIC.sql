-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Czas generowania: 27 Lut 2022, 19:16
-- Wersja serwera: 5.7.34
-- Wersja PHP: 8.1.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `19_mazur`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `LIC`
--

CREATE TABLE `LIC` (
  `ID` int(5) NOT NULL,
  `Dzialanie` varchar(50) NOT NULL,
  `Dobry` int(5) NOT NULL,
  `Zly` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Zrzut danych tabeli `LIC`
--

INSERT INTO `LIC` (`ID`, `Dzialanie`, `Dobry`, `Zly`) VALUES
(1, '(1*2) + 1', 3, 2),
(2, '(1/1) - 1', 0, 2),
(3, '(7*3) - 3', 18, 17),
(4, '(4*3) + 4', 16, 18),
(5, '(3/3) + 2', 3, 1),
(6, '(2*6) - 4', 8, 6),
(7, '(8*9) - 8', 64, 62),
(8, '(4*5) - 5', 15, 20),
(9, '(4*2) + 6', 14, 18),
(10, '(4/4) + 7', 8, 7),
(11, '(8*2) - 8', 8, 12),
(12, '(2*9) - 9', 9, 11),
(13, '(8/2) + 9', 13, 14),
(14, '(3*8) - 1', 23, 22),
(15, '(6/3) + 1', 3, 2),
(16, '(7/7) + 6', 7, 6),
(17, '(3/3) - 0', 1, 0),
(18, '(9/9) - 1', 0, 1),
(19, '(5/5) + 8', 9, 8),
(20, '(7/7) + 3', 4, 3),
(21, '(3*3) - 7', 2, 3);

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `LIC`
--
ALTER TABLE `LIC`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT dla zrzuconych tabel
--

--
-- AUTO_INCREMENT dla tabeli `LIC`
--
ALTER TABLE `LIC`
  MODIFY `ID` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
