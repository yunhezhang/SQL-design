-- constraint15: All new bids must be placed at the time which matches the current time of your AuctionBase system.
PRAGMA foreign_keys = ON;
drop trigger if exists enforce_timeMatch;
create trigger enforce_timeMatch
before insert on Bids
for each row
when exists (
        select *
        from CurrentTime
        where new.Time <> CurTime
     )
begin
  select raise(rollback, 'All new bids must be placed at the time which matches the current time of the AuctionBase system.');
end;

-- constraint16: The current time of your AuctionBase system can only advance forward in time, not backward in time.
drop trigger if exists enforce_forward_time;
create trigger enforce_forward_time
before update of CurTime on CurrentTime
for each row when (new.CurTime < old.CurTime)
begin
select raise(rollback, 'The current time can only advance forward in time, not backward in time.');
end;
