/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50726
 Source Host           : localhost:3306
 Source Schema         : quqiadminflask

 Target Server Type    : MySQL
 Target Server Version : 50726
 File Encoding         : 65001

 Date: 24/02/2024 21:29:22
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version`  (
  `version_num` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`version_num`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('10db8193d755');

-- ----------------------------
-- Table structure for info_user
-- ----------------------------
DROP TABLE IF EXISTS `info_user`;
CREATE TABLE `info_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '用户昵称',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '头像',
  `mobile` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '用户手机号',
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '加密的密码',
  `role_id` int(11) NULL DEFAULT NULL,
  `create_at` datetime(0) NULL DEFAULT NULL,
  `update_at` datetime(0) NULL DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '用户邮箱',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '用户地址',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uq_info_user_username`(`username`) USING BTREE,
  INDEX `fk_info_user_role_id_rt_role`(`role_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of info_user
-- ----------------------------
INSERT INTO `info_user` VALUES (1, 'quqi', '/static/images/user_pic.png', '18249869955', 'scrypt:32768:8:1$gbCLHH6gUXj3jWjD$a19725d30f603e291b834f88d90fec26bf65aae718c72926a0e3b2aea7dd0e522405f6f1adedb471468319f6358bc1af29e9efe24b3b72f697534e201a3a5739', 2, '2024-02-20 13:34:00', '2024-02-24 21:25:03', 'xiaoquqi54188@163.com', '0|0|0|内网IP|内网IP');

-- ----------------------------
-- Table structure for rt_power
-- ----------------------------
DROP TABLE IF EXISTS `rt_power`;
CREATE TABLE `rt_power`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '权限名字',
  `url` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '权限路径',
  `code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '权限标识',
  `type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '权限类型',
  `pid` int(11) NULL DEFAULT NULL COMMENT '父类编号',
  `sort` int(11) NULL DEFAULT NULL,
  `create_at` datetime(0) NULL DEFAULT NULL,
  `update_at` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uq_rt_power_name`(`name`) USING BTREE,
  INDEX `fk_rt_power_pid_rt_power`(`pid`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 117 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of rt_power
-- ----------------------------
INSERT INTO `rt_power` VALUES (100, '工作台', '/dashboard/console', 'dashboard:console', 'menu', NULL, 1, NULL, NULL);
INSERT INTO `rt_power` VALUES (101, '系统管理', '', 'dashboard:system', 'menu', NULL, 2, NULL, NULL);
INSERT INTO `rt_power` VALUES (102, '角色管理', '/dashboard/role', 'dashboard:system:role', 'path', 101, 1, NULL, NULL);
INSERT INTO `rt_power` VALUES (103, '权限管理', '/dashboard/power', 'dashboard:system:power', 'path', 101, 2, NULL, NULL);
INSERT INTO `rt_power` VALUES (104, '用户管理', '/dashboard/user', 'dashboard:system:user', 'path', 101, 3, NULL, NULL);
INSERT INTO `rt_power` VALUES (105, '新增角色', '', 'dashboard:system:role:add', 'auth', 102, 1, NULL, NULL);
INSERT INTO `rt_power` VALUES (106, '删除角色', NULL, 'dashboard:system:role:del', 'auth', 102, 2, NULL, NULL);
INSERT INTO `rt_power` VALUES (107, '修改角色', NULL, 'dashboard:system:role:edit', 'auth', 102, 3, NULL, NULL);
INSERT INTO `rt_power` VALUES (108, '查看角色', NULL, 'dashboard:system:role:read', 'auth', 102, 4, NULL, NULL);
INSERT INTO `rt_power` VALUES (109, '新增权限', NULL, 'dashboard:system:power:add', 'auth', 103, 1, NULL, NULL);
INSERT INTO `rt_power` VALUES (110, '删除权限', NULL, 'dashboard:system:power:del', 'auth', 103, 2, NULL, NULL);
INSERT INTO `rt_power` VALUES (111, '修改权限\r\n', NULL, 'dashboard:system:power:edit', 'auth', 103, 3, NULL, NULL);
INSERT INTO `rt_power` VALUES (112, '查看权限\r\n', NULL, 'dashboard:system:power:read', 'auth', 103, 4, NULL, NULL);
INSERT INTO `rt_power` VALUES (113, '新增用户', NULL, 'dashboard:system:user:add', 'auth', 104, 1, NULL, NULL);
INSERT INTO `rt_power` VALUES (114, '删除用户', NULL, 'dashboard:system:user:del', 'auth', 104, 2, NULL, NULL);
INSERT INTO `rt_power` VALUES (115, '修改用户', NULL, 'dashboard:system:user:edit', 'auth', 104, 3, NULL, NULL);
INSERT INTO `rt_power` VALUES (116, '查看用户', NULL, 'dashboard:system:user:read', 'auth', 104, 4, NULL, '2024-02-20 14:43:59');

-- ----------------------------
-- Table structure for rt_role
-- ----------------------------
DROP TABLE IF EXISTS `rt_role`;
CREATE TABLE `rt_role`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '角色名称',
  `code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '角色标识',
  `create_at` datetime(0) NULL DEFAULT NULL,
  `update_at` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uq_rt_role_code`(`code`) USING BTREE,
  UNIQUE INDEX `uq_rt_role_name`(`name`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of rt_role
-- ----------------------------
INSERT INTO `rt_role` VALUES (1, '普通用户', 'user', '2024-02-20 13:33:34', '2024-02-20 13:33:34');
INSERT INTO `rt_role` VALUES (2, '管理员', 'admin', '2024-02-20 13:33:34', '2024-02-20 13:33:34');

-- ----------------------------
-- Table structure for rt_role_power
-- ----------------------------
DROP TABLE IF EXISTS `rt_role_power`;
CREATE TABLE `rt_role_power`  (
  `power_id` int(11) NULL DEFAULT NULL COMMENT '用户编号',
  `role_id` int(11) NULL DEFAULT NULL COMMENT '角色编号',
  INDEX `fk_rt_role_power_power_id_rt_power`(`power_id`) USING BTREE,
  INDEX `fk_rt_role_power_role_id_rt_role`(`role_id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Fixed;

-- ----------------------------
-- Records of rt_role_power
-- ----------------------------
INSERT INTO `rt_role_power` VALUES (100, 1);
INSERT INTO `rt_role_power` VALUES (100, 2);
INSERT INTO `rt_role_power` VALUES (101, 2);
INSERT INTO `rt_role_power` VALUES (102, 2);
INSERT INTO `rt_role_power` VALUES (103, 2);
INSERT INTO `rt_role_power` VALUES (105, 2);
INSERT INTO `rt_role_power` VALUES (106, 2);
INSERT INTO `rt_role_power` VALUES (107, 2);
INSERT INTO `rt_role_power` VALUES (108, 2);
INSERT INTO `rt_role_power` VALUES (109, 2);
INSERT INTO `rt_role_power` VALUES (110, 2);
INSERT INTO `rt_role_power` VALUES (111, 2);
INSERT INTO `rt_role_power` VALUES (112, 2);
INSERT INTO `rt_role_power` VALUES (104, 2);
INSERT INTO `rt_role_power` VALUES (113, 2);
INSERT INTO `rt_role_power` VALUES (115, 2);
INSERT INTO `rt_role_power` VALUES (114, 2);
INSERT INTO `rt_role_power` VALUES (116, 2);

SET FOREIGN_KEY_CHECKS = 1;
