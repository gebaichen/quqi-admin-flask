/*
 Navicat Premium Data Transfer

 Source Server         : quqi-admin
 Source Server Type    : SQLite
 Source Server Version : 3021000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3021000
 File Encoding         : 65001

 Date: 20/02/2024 14:55:52
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS "alembic_version";
CREATE TABLE "alembic_version" (
  "version_num" VARCHAR(32) NOT NULL,
  CONSTRAINT "alembic_version_pkc" PRIMARY KEY ("version_num")
);

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO "alembic_version" VALUES ('78fa31f97705');

-- ----------------------------
-- Table structure for info_user
-- ----------------------------
DROP TABLE IF EXISTS "info_user";
CREATE TABLE "info_user" (
  "id" INTEGER NOT NULL,
  "username" VARCHAR(32) NOT NULL,
  "password_hash" VARCHAR(256) NOT NULL,
  "role_id" INTEGER,
  "create_at" DATETIME,
  "update_at" DATETIME,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("role_id") REFERENCES "rt_role" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("username" ASC)
);

-- ----------------------------
-- Records of info_user
-- ----------------------------
INSERT INTO "info_user" VALUES (1, 'quqi', 'scrypt:32768:8:1$gbCLHH6gUXj3jWjD$a19725d30f603e291b834f88d90fec26bf65aae718c72926a0e3b2aea7dd0e522405f6f1adedb471468319f6358bc1af29e9efe24b3b72f697534e201a3a5739', 2, '2024-02-20 13:34:00.296131', '2024-02-20 13:34:00.296131');

-- ----------------------------
-- Table structure for rt_power
-- ----------------------------
DROP TABLE IF EXISTS "rt_power";
CREATE TABLE "rt_power" (
  "id" INTEGER NOT NULL,
  "name" VARCHAR(64) NOT NULL,
  "url" VARCHAR(64),
  "code" VARCHAR(64),
  "type" VARCHAR(30),
  "pid" INTEGER,
  "sort" INTEGER,
  "create_at" DATETIME,
  "update_at" DATETIME,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("pid") REFERENCES "rt_power" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("name" ASC)
);

-- ----------------------------
-- Records of rt_power
-- ----------------------------
INSERT INTO "rt_power" VALUES (100, '工作台', '/dashboard/console', 'dashboard:console', 'menu', 0, 1, NULL, NULL);
INSERT INTO "rt_power" VALUES (101, '系统管理', '', 'dashboard:system', 'menu', 0, 2, NULL, NULL);
INSERT INTO "rt_power" VALUES (102, '角色管理', '/dashboard/role', 'dashboard:system:role', 'path', 101, 1, NULL, NULL);
INSERT INTO "rt_power" VALUES (103, '权限管理', '/dashboard/power', 'dashboard:system:power', 'path', 101, 2, NULL, NULL);
INSERT INTO "rt_power" VALUES (104, '用户管理', '/dashboard/user', 'dashboard:system:user', 'path', 101, 3, NULL, NULL);
INSERT INTO "rt_power" VALUES (105, '新增角色', '', 'dashboard:system:role:add', 'auth', 102, 1, NULL, NULL);
INSERT INTO "rt_power" VALUES (106, '删除角色', NULL, 'dashboard:system:role:del', 'auth', 102, 2, NULL, NULL);
INSERT INTO "rt_power" VALUES (107, '修改角色', NULL, 'dashboard:system:role:edit', 'auth', 102, 3, NULL, NULL);
INSERT INTO "rt_power" VALUES (108, '查看角色', NULL, 'dashboard:system:role:read', 'auth', 102, 4, NULL, NULL);
INSERT INTO "rt_power" VALUES (109, '新增权限', NULL, 'dashboard:system:power:add', 'auth', 103, 1, NULL, NULL);
INSERT INTO "rt_power" VALUES (110, '删除权限', NULL, 'dashboard:system:power:del', 'auth', 103, 2, NULL, NULL);
INSERT INTO "rt_power" VALUES (111, '修改权限
', NULL, 'dashboard:system:power:edit', 'auth', 103, 3, NULL, NULL);
INSERT INTO "rt_power" VALUES (112, '查看权限
', NULL, 'dashboard:system:power:read', 'auth', 103, 4, NULL, NULL);
INSERT INTO "rt_power" VALUES (113, '新增用户', NULL, 'dashboard:system:user:add', 'auth', 104, 1, NULL, NULL);
INSERT INTO "rt_power" VALUES (114, '删除用户', NULL, 'dashboard:system:user:del', 'auth', 104, 2, NULL, NULL);
INSERT INTO "rt_power" VALUES (115, '修改用户', NULL, 'dashboard:system:user:edit', 'auth', 104, 3, NULL, NULL);
INSERT INTO "rt_power" VALUES (116, '查看用户', NULL, 'dashboard:system:user:read', 'auth', 104, 4, NULL, '2024-02-20 14:43:59.386379');

-- ----------------------------
-- Table structure for rt_role
-- ----------------------------
DROP TABLE IF EXISTS "rt_role";
CREATE TABLE "rt_role" (
  "id" INTEGER NOT NULL,
  "name" VARCHAR(64),
  "code" VARCHAR(64),
  "create_at" DATETIME,
  "update_at" DATETIME,
  PRIMARY KEY ("id"),
  UNIQUE ("code" ASC),
  UNIQUE ("name" ASC)
);

-- ----------------------------
-- Records of rt_role
-- ----------------------------
INSERT INTO "rt_role" VALUES (1, '普通用户', 'user', '2024-02-20 13:33:34.076828', '2024-02-20 13:33:34.076828');
INSERT INTO "rt_role" VALUES (2, '管理员', 'admin', '2024-02-20 13:33:34.076828', '2024-02-20 13:33:34.076828');

-- ----------------------------
-- Table structure for rt_role_power
-- ----------------------------
DROP TABLE IF EXISTS "rt_role_power";
CREATE TABLE "rt_role_power" (
  "power_id" INTEGER,
  "role_id" INTEGER,
  FOREIGN KEY ("role_id") REFERENCES "rt_role" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("power_id") REFERENCES "rt_power" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of rt_role_power
-- ----------------------------
INSERT INTO "rt_role_power" VALUES (100, 1);
INSERT INTO "rt_role_power" VALUES (100, 2);
INSERT INTO "rt_role_power" VALUES (101, 2);
INSERT INTO "rt_role_power" VALUES (102, 2);
INSERT INTO "rt_role_power" VALUES (103, 2);
INSERT INTO "rt_role_power" VALUES (105, 2);
INSERT INTO "rt_role_power" VALUES (106, 2);
INSERT INTO "rt_role_power" VALUES (107, 2);
INSERT INTO "rt_role_power" VALUES (108, 2);
INSERT INTO "rt_role_power" VALUES (109, 2);
INSERT INTO "rt_role_power" VALUES (110, 2);
INSERT INTO "rt_role_power" VALUES (111, 2);
INSERT INTO "rt_role_power" VALUES (112, 2);
INSERT INTO "rt_role_power" VALUES (104, 2);
INSERT INTO "rt_role_power" VALUES (113, 2);
INSERT INTO "rt_role_power" VALUES (115, 2);
INSERT INTO "rt_role_power" VALUES (114, 2);
INSERT INTO "rt_role_power" VALUES (116, 2);

PRAGMA foreign_keys = true;
