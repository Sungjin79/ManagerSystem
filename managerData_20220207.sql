-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        5.6.24-log - MySQL Community Server (GPL)
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- managerdb 데이터베이스 구조 내보내기
DROP DATABASE IF EXISTS `managerdb`;
CREATE DATABASE IF NOT EXISTS `managerdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `managerdb`;

-- 테이블 managerdb.batch_manager 구조 내보내기
DROP TABLE IF EXISTS `batch_manager`;
CREATE TABLE IF NOT EXISTS `batch_manager` (
  `type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '타입(정규/명품)',
  `hour` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '출고시간',
  `chk` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '체크여부',
  KEY `type_hour` (`type`,`hour`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='명품/정규 출고 시간';

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 managerdb.cello_request_data 구조 내보내기
DROP TABLE IF EXISTS `cello_request_data`;
CREATE TABLE IF NOT EXISTS `cello_request_data` (
  `spr_nm` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `trs_type` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ord_no` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ord_opt_no` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `invoice_no` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `packing_yn` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `total_qty` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `packing_qty` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `qty_yn` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ins_date` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  KEY `ord_no` (`ord_no`,`ord_opt_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 managerdb.cello_request_value 구조 내보내기
DROP TABLE IF EXISTS `cello_request_value`;
CREATE TABLE IF NOT EXISTS `cello_request_value` (
  `ajaxUid` varchar(1500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `browserUid` varchar(1500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cellosessionkey` varchar(1500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ins_date` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `login_yn` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 managerdb.cp_data1 구조 내보내기
DROP TABLE IF EXISTS `cp_data1`;
CREATE TABLE IF NOT EXISTS `cp_data1` (
  `ORD_OPT_NO` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  KEY `ORD_OPT_NO` (`ORD_OPT_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 managerdb.cp_data2 구조 내보내기
DROP TABLE IF EXISTS `cp_data2`;
CREATE TABLE IF NOT EXISTS `cp_data2` (
  `ORD_OPT_NO` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `SEND_CUST_NO` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  KEY `ORD_OPT_NO` (`ORD_OPT_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 managerdb.mmg_auth 구조 내보내기
DROP TABLE IF EXISTS `mmg_auth`;
CREATE TABLE IF NOT EXISTS `mmg_auth` (
  `com_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ip` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT 'N'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 managerdb.moms_excel_log 구조 내보내기
DROP TABLE IF EXISTS `moms_excel_log`;
CREATE TABLE IF NOT EXISTS `moms_excel_log` (
  `BZ_YN` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `MAKE_YN` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TOTAL` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `EMER` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `INV` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `NO_INV` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `CELLO` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `CLS_DATE` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `CUT_OFF_NO` varchar(190) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `CUT_SEQ` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  KEY `CUT_OFF_NO` (`CUT_OFF_NO`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 managerdb.moms_outbound_data 구조 내보내기
DROP TABLE IF EXISTS `moms_outbound_data`;
CREATE TABLE IF NOT EXISTS `moms_outbound_data` (
  `CLS_DATE` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `CUT_OFF_NO` varchar(190) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `CUT_SEQ` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `INS_DATE` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `DOC_QTY` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `BZ_YN` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT 'N',
  KEY `CUT_OFF_NO` (`CUT_OFF_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 managerdb.moms_request_data 구조 내보내기
DROP TABLE IF EXISTS `moms_request_data`;
CREATE TABLE IF NOT EXISTS `moms_request_data` (
  `CUT_OFF_NO` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ORD_NO` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ORD_OPT_NO` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `PROC_NM` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ORD_NM` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TRS_NM` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TRS_ZIP` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TRS_ADDR` varchar(700) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TRS_ADDR2` varchar(700) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TRS_ADDR3` varchar(700) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TRS_PHONE` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TRS_MOBILE` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `GDS_COMBINE` varchar(700) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `GDS_LOCATION` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `GDS_OPT` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ORD_QTY` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `GDS_TYPE` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `BRD_NM` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `GIFT` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TRS_MSG` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `STL_NO` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `BARCODE` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TRS_INVOICE_NO` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `FILE_NAME` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  KEY `ORD_NO` (`ORD_NO`,`ORD_OPT_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 managerdb.moms_request_value 구조 내보내기
DROP TABLE IF EXISTS `moms_request_value`;
CREATE TABLE IF NOT EXISTS `moms_request_value` (
  `authorization` varchar(1500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cookie` varchar(1500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ins_date` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `login_yn` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
