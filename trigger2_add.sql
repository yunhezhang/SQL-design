-- constraint9:  A user may not bid on an item he or she is also selling. 
PRAGMA foreign_keys = ON; 
drop trigger if exists no_bidsof_seller;
create trigger no_bidsof_seller
before insert on Bids
for each row
when exists (
         select *
         from Items
         where new.ItemID = Items.ItemID and new.UserID = Items.UserID
     )
begin
  select raise(rollback, 'A user can not bid on an item he or she is also selling.');
end; 

-- constraint11: No auction may have a bid before its start time or after its end time. 
drop trigger if exists enforce_bidTime;
create trigger enforce_bidTime
  before insert on Bids
  for each row
  when exists (
          select *
          from Items
          where Items.ItemID = new.ItemID and Items.Started > new.Time
          UNION
          select *
          from Items
          where Items.ItemID = new.ItemID and Items.Ends < new.Time
      )
begin
  select raise(rollback, 'No auction may have a bid before its start time or after its end time.');
end;

-- constraint12:No user can make a bid of the same amount to the same item more than once. 
drop trigger if exists no_same_bidAmount;
create trigger no_same_bidAmount
before insert on Bids
  for each row
  when exists (
          select *
          from Bids
          where Bids.ItemID = new.ItemID and Bids.UserID = new.UserID
                and Bids.Amount = new.Amount
       )
begin
  select raise(rollback, 'No user can make a bid of the same amount to the same item more than once.');
end;

-- congstraint14: Any new bid for a particular item must have a higher amount than any of the previous bids for that particular item. 
drop trigger if exists enforce_higherAmount;
create trigger enforce_higherAmount
before insert on Bids
for each row
when exists (
       select *
       from Bids
       where ItemID = new.ItemID and Amount >= new.Amount
     )
begin
  select raise(rollback, 'Any new bid for this item must have a higher amount than any of the previous bids');
end;
