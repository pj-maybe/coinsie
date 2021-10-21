CREATE TABLE UserDetails (UserId TEXT PRIMARY KEY, FirstName TEXT, EmailAddress TEXT)

CREATE TABLE OwnerDetails (OwnerId TEXT PRIMARY KEY, OwnerType TEXT, ShortText TEXT, LongText TEXT)

CREATE TABLE OfferDetails (OfferId TEXT PRIMARY KEY, OwnerId TEXT, OfferType TEXT, StarsNeeded INT, Direction INT, ShapeId TEXT, ColorId TEXT, CoinSize INT, ShortText TEXT, LongText TEXT)
