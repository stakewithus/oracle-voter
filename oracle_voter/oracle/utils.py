def get_vote_period(raw_vote_period, raw_height):
    height = int(raw_height)
    vote_period = int(raw_vote_period)
    vote_left = height % vote_period
    vote_height = 0
    if vote_left != 0:
        vote_height = height - vote_left
    else:
        vote_height = height
    vote_period = vote_height / vote_period
    return vote_period
