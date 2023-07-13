-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema bands
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema bands
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bands` DEFAULT CHARACTER SET utf8 ;
USE `bands` ;

-- -----------------------------------------------------
-- Table `bands`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bands`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bands`.`bands`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bands`.`bands` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `band_name` VARCHAR(255) NOT NULL,
  `music_genre` VARCHAR(255) NOT NULL,
  `home_city` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_bands_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_bands_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `bands`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bands`.`joins`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bands`.`joins` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `band_id` INT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_users_has_bands_bands1_idx` (`band_id` ASC) VISIBLE,
  INDEX `fk_users_has_bands_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_bands_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `bands`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_users_has_bands_bands1`
    FOREIGN KEY (`band_id`)
    REFERENCES `bands`.`bands` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
