#Exercise 0
def github() -> str:
    """
    Some docstrings.
    """

    return "https://github.com/Julienmjohnson/ECON_481_HW_6/blob/main/HW6.py"

#Exercise 1
def std() -> str:
    """
    Some docstrings.
    """

    return "select itemid, (sqrt((sum(bidAmount * bidAmount) -2 * avg(bidAmount) * sum(bidAmount) + count(bidAmount) * avg(bidAmount) * avg(bidAmount)) / (count(*) - 1))) as sd from bids group by itemid having count(*) > 1"

#Exercise 2
def bidder_spend_frac() -> str:
    """
    Some docstrings.
    """

    return """
with buy as(
    with buyingindex as(
        with max as 
            (select itemid, max(bidamount) as max_bid
            from bids
            group by itemid)
        
        select b.biddername, b.itemid, max(b.bidamount) as max_user_bid, max.max_bid,
        case when max(b.bidamount) == max.max_bid then max(b.bidamount) else 0 end as bought_price
        from bids as b
        inner join max
        on b.itemid = max.itemid
        group by b.biddername, b.itemid)
    
    select distinct b.biddername, buyingindex.max_user_bid as user_bids, buyingindex.bought_price as user_spent 
    from bids as b
    inner join buyingindex
    on b.biddername = buyingindex.biddername
    order by b.biddername
    )

select biddername, sum(user_bids) as total_bids, sum(user_spent) as total_spent, sum(user_spent)/sum(user_bids) as spend_frac from buy
group by biddername
"""


#Exercise 3
def min_increment_freq() -> str:
    """
    Some docstrings.
    """

    return """
with t as(
        select b.bidAmount, b.itemid, i.bidIncrement, i.isbuynowused,
        lag(b.bidAmount) over (partition by b.itemid) as lagged_price from bids as b
        inner join items as i
        on b.itemid = i.itemid
        where i.isbuynowused == 0
        order by b.itemid
        )
select sum(case when bidAmount == bidIncrement + lagged_price then 1.00 else 0.00 end) / count(*) as freq from t
"""

#Exercise 4
def win_perc_by_timestamp() -> str:
    """
    Some docstrings.
    """

    return """
with t as(
        with auction_length as 
            (select itemid, starttime, endtime, 
            julianday(endtime) - julianday(starttime) as length from items)
        
        select b.itemid, b.bidamount, max(b.bidamount) over(partition by b.itemid) as winning_bid,
        case when (julianday(endtime)-julianday(bidtime)) / a.length > .9 then 10
        when (julianday(endtime)-julianday(bidtime)) / a.length > .8 then 9
        when (julianday(endtime)-julianday(bidtime)) / a.length > .7 then 8
        when (julianday(endtime)-julianday(bidtime)) / a.length > .6 then 7
        when (julianday(endtime)-julianday(bidtime)) / a.length > .5 then 6
        when (julianday(endtime)-julianday(bidtime)) / a.length > .4 then 5
        when (julianday(endtime)-julianday(bidtime)) / a.length > .3 then 4
        when (julianday(endtime)-julianday(bidtime)) / a.length > .2 then 3
        when (julianday(endtime)-julianday(bidtime)) / a.length > .1 then 2
        else 1 end as timestamp_bin
        from bids as b
        inner join auction_length as a
        on b.itemid=a.itemid)

select timestamp_bin, sum(case when bidamount == winning_bid then 1.00 else 0.00 end) / count(*) as win_perc from t
group by timestamp_bin
"""