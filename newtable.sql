use pmsdb;
CREATE TABLE `noti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` varchar(4500) NOT NULL,
  `datetime` datetime NOT NULL,
  `type` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `isread` tinyint(4) DEFAULT '0',
  `step` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;