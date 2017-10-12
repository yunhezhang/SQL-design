/* SELECT statement verifying Referential Integrity constraint #2 */
SELECT Bids.UserID
FROM Bids
WHERE Bids.UserID not in (SELECT UserID FROM Users)
UNION
SELECT Items.UserID
FROM Items
WHERE Items.UserID not in (SELECT UserID FROM Users)
;


/* SELECT statement verifying Referential Integrity constraint #4 */
SELECT Bids.ItemID
FROM Bids
WHERE Bids.ItemID not in (SELECT ItemID FROM Items);

/* SELECT statement verifying Referential Integrity constraint #5 */
SELECT Categories.ItemID
FROM Categories
WHERE Categories.ItemID not in (SELECT ItemID FROM Items);






