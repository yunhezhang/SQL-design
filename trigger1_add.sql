-- constraint8: The Current Price of an item must always match the Amount of the most recent bid for that item. 
PRAGMA fortign_keys = ON;
drop trigger if exists update_currently;
create trigger update_currently
  after insert on Bids
  for each row
  begin
  update Items set Currently = new.Amount
  where ItemID = new.ItemID;
  end;

-- constraint13: In every auction,the Number_of_Bids attribute corresponds to the actual number of bids for that particular item. 
drop trigger if exists update_numberOfBids;
create trigger update_numberOfBids
  after insert on Bids
  for each row
  begin
    update Items set Number_of_Bids = Number_of_Bids + 1
    where ItemID = new.ItemID;
  end;  
