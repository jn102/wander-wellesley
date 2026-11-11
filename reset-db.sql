use wanderw_db;

drop table if exists hotel, restaurant, activity, visit, itinerary;
drop table if exists review;
drop table if exists establishment, user;


CREATE TABLE `user` (
  `email` char(19) not null,
  `password_hash` varchar(255) not null,
  `name` varchar(50),
  `uid` int PRIMARY KEY AUTO_INCREMENT,
  unique(email)
);

CREATE TABLE `establishment` (
  `eid` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(50),
  `type` enum('Hotel','Restaurant','Activity'),
  `website` varchar(200),
  `country` varchar(50),
  `city` varchar(50),
  `description` varchar(200)
);

CREATE TABLE `restaurant` (
  `eid` int PRIMARY KEY,
  `cuisine` varchar(50),
  `reservations` boolean,
  `outdoor_seating` boolean,
  `credit_card` boolean,
  `hours` varchar(50)
);

CREATE TABLE `hotel` (
  `eid` int PRIMARY KEY,
  `gym` boolean,
  `breakfast` boolean,
  `pool` boolean,
  `laundry` boolean,
  `check_in_time` varchar(50),
  `check_out_time` varchar(50)
);

CREATE TABLE `activity` (
  `eid` int PRIMARY KEY,
  `hours` varchar(50),
  `outdoors` boolean,
  `student_discount` boolean,
  `ticket` enum('Reservation required','Ticket required','None')
);

CREATE TABLE `review` (
  `rid` int PRIMARY KEY AUTO_INCREMENT,
  `eid` int,
  `user` int,
  `stars` tinyint,
  `price` tinyint,
  `review_body` varchar(200),
  `image` varchar(50),
  `date_added` date,
  `date_visited` date
);

CREATE TABLE `itinerary` (
  `user` int,
  `iid` int PRIMARY KEY AUTO_INCREMENT,
  `country` varchar(50),
  `city` varchar(50),
  `season` enum('Winter','Spring','Summer','Fall'),
  `name` varchar(50)
);

CREATE TABLE `visit` (
  `iid` int,
  `eid` int
);

ALTER TABLE `restaurant` ADD FOREIGN KEY (`eid`) REFERENCES `establishment` (`eid`);

ALTER TABLE `hotel` ADD FOREIGN KEY (`eid`) REFERENCES `establishment` (`eid`);

ALTER TABLE `activity` ADD FOREIGN KEY (`eid`) REFERENCES `establishment` (`eid`);

ALTER TABLE `review` ADD FOREIGN KEY (`user`) REFERENCES `user` (`uid`);

ALTER TABLE `visit` ADD FOREIGN KEY (`iid`) REFERENCES `itinerary` (`iid`);

ALTER TABLE `visit` ADD FOREIGN KEY (`eid`) REFERENCES `establishment` (`eid`);

ALTER TABLE `review` ADD FOREIGN KEY (`eid`) REFERENCES `establishment` (`eid`);