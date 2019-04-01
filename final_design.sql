/*
 Navicat Premium Data Transfer

 Source Server         : 233
 Source Server Type    : MySQL
 Source Server Version : 50723
 Source Host           : localhost:3306
 Source Schema         : final_design

 Target Server Type    : MySQL
 Target Server Version : 50723
 File Encoding         : 65001

 Date: 01/04/2019 21:33:10
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for activity
-- ----------------------------
DROP TABLE IF EXISTS `activity`;
CREATE TABLE `activity`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(12) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `created` varchar(19) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `endtime` varchar(19) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `cost` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `userId` int(11) NOT NULL,
  `shipId` int(11) NOT NULL,
  `rent` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `userId`(`userId`) USING BTREE,
  INDEX `shipId`(`shipId`) USING BTREE,
  CONSTRAINT `activity_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `member` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `activity_ibfk_2` FOREIGN KEY (`shipId`) REFERENCES `ship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 218 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ad_resource
-- ----------------------------
DROP TABLE IF EXISTS `ad_resource`;
CREATE TABLE `ad_resource`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uri` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `type` varchar(4) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `sponsorId` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `sponsorId`(`sponsorId`) USING BTREE,
  CONSTRAINT `ad_resource_ibfk_1` FOREIGN KEY (`sponsorId`) REFERENCES `ad_sponsor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 55 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ad_sponsor
-- ----------------------------
DROP TABLE IF EXISTS `ad_sponsor`;
CREATE TABLE `ad_sponsor`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `created` varchar(19) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `endtime` varchar(19) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `cost` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `type` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `content` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `reason` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for brokeship
-- ----------------------------
DROP TABLE IF EXISTS `brokeship`;
CREATE TABLE `brokeship`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cost` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `shipId` int(11) NOT NULL,
  `reason` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `created` varchar(19) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `shipId`(`shipId`) USING BTREE,
  CONSTRAINT `shipId` FOREIGN KEY (`shipId`) REFERENCES `ship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for group_building
-- ----------------------------
DROP TABLE IF EXISTS `group_building`;
CREATE TABLE `group_building`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `principalId` int(11) NOT NULL,
  `count` int(2) NOT NULL,
  `gname` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `extra` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `endtime` varchar(19) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `created` varchar(19) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `type` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `cost` varchar(4) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `reason` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `principalId`(`principalId`) USING BTREE,
  CONSTRAINT `group_building_ibfk_1` FOREIGN KEY (`principalId`) REFERENCES `member` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for member
-- ----------------------------
DROP TABLE IF EXISTS `member`;
CREATE TABLE `member`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(24) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `phone` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `reputation` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `created` varchar(19) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `time` int(11) NOT NULL DEFAULT 0,
  `discount` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '1',
  `sex` varchar(5) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 28 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for reservation
-- ----------------------------
DROP TABLE IF EXISTS `reservation`;
CREATE TABLE `reservation`  (
  `id` int(11) NOT NULL,
  `seeingship` int(5) NOT NULL,
  `rowing` int(5) NOT NULL,
  `smallship` int(5) NOT NULL,
  `walkingball` int(5) NOT NULL,
  `interval` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for rootkey
-- ----------------------------
DROP TABLE IF EXISTS `rootkey`;
CREATE TABLE `rootkey`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `_key` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `type` varchar(6) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `account` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ship
-- ----------------------------
DROP TABLE IF EXISTS `ship`;
CREATE TABLE `ship`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shipname` varchar(24) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `color` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `size` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `cost` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `status` varchar(12) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `descroption` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `created` varchar(19) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `typeId` int(11) NOT NULL,
  `spotId` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `typeId`(`typeId`) USING BTREE,
  INDEX `spotId`(`spotId`) USING BTREE,
  CONSTRAINT `ship_ibfk_1` FOREIGN KEY (`typeId`) REFERENCES `ship_type` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ship_ibfk_2` FOREIGN KEY (`spotId`) REFERENCES `spot` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 371 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ship_sponsor
-- ----------------------------
DROP TABLE IF EXISTS `ship_sponsor`;
CREATE TABLE `ship_sponsor`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `address` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ship_type
-- ----------------------------
DROP TABLE IF EXISTS `ship_type`;
CREATE TABLE `ship_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for spot
-- ----------------------------
DROP TABLE IF EXISTS `spot`;
CREATE TABLE `spot`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `address` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `phone` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `charge` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `level` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `discount` varchar(5) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
