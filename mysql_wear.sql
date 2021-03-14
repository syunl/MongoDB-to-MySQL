CREATE DATABASE IF NOT EXISTS wear;

USE wear;

CREATE TABLE UserInfo 
(
  Uid            VARCHAR(20),
  Gender         VARCHAR(10),
  Height          VARCHAR(10),
  UserURL        VARCHAR(100),
  UserRanking     VARCHAR(10),
  CONSTRAINT UserInfo PRIMARY KEY (Uid)
) ENGINE = INNODB;

CREATE TABLE OftenUseBrand
(
  Uid            VARCHAR(100),
  Brands         VARCHAR(80),
  CONSTRAINT OftenUseBrand_Uid_FK FOREIGN KEY (Uid) REFERENCES UserInfo (Uid)
) ENGINE = INNODB;

CREATE TABLE Outfit
(
  OutfitId         VARCHAR(100),
  Uid              VARCHAR(100),
  PicUploadTime    date,
  Season           VARCHAR(10),
  LikesAdj         float,
  Likes            int,
  PicUrl           VARCHAR(200),

  CONSTRAINT Outfit_Uid_FK FOREIGN KEY (Uid) REFERENCES UserInfo (Uid),
  CONSTRAINT Outfit_OutfitId_PK PRIMARY KEY (OutfitId)
)ENGINE = INNODB;

CREATE TABLE Style
(
  OutfitId            VARCHAR(150),
  Style               VARCHAR(150),

  CONSTRAINT Style_OutfitId_FK FOREIGN KEY (OutfitId) REFERENCES Outfit (OutfitId)
)ENGINE = INNODB;


CREATE TABLE ItemInfo
(
  ItemId             VARCHAR(150),
  purchaseUrl        VARCHAR(500),
  ItemType           VARCHAR(300),
  color				VARCHAR(120),
  brand              VARCHAR(130),
  CONSTRAINT ItemInfo_ItemId_PK PRIMARY KEY (ItemId)
)ENGINE = INNODB;

CREATE TABLE Item
(
  OutfitId            VARCHAR(130),
  ItemId              VARCHAR(130),

  CONSTRAINT Item_OutfitId_FK FOREIGN KEY (OutfitId) REFERENCES Outfit (OutfitId),
  CONSTRAINT ItemInfo_ItemId_FK FOREIGN KEY (ItemId) REFERENCES ItemInfo (ItemId),
  CONSTRAINT Item_OutfitId_ItemId_PK PRIMARY KEY (OutfitId,ItemId)
)ENGINE = INNODB;