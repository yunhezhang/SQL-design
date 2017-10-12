PRAGMA foreign_keys = ON;
-- constraint: A user may not bid on an item that already reaches the buy price
drop trigger if exists buy_price;
create trigger buy_price
before insert on Bids
for each row
when exists (
          select *
          from Items
          where Items.ItemID = new.ItemID and Items.Buy_Price <> NULL and Items.Currently >= Buy_Price
     )
begin
  select raise(rollback, 'This auction has been closed.');
end;
