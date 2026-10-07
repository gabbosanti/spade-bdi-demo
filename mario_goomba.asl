+perception(Tick) : obstacle_ahead & direction(right)
    <- .turn_around(Tick);
       .move_left(Tick).

+perception(Tick) : obstacle_ahead & direction(left)
    <- .turn_around(Tick);
       .move_right(Tick).

+perception(Tick) : not obstacle_ahead & direction(right)
    <- .move_right(Tick).

+perception(Tick) : not obstacle_ahead & direction(left)
    <- .move_left(Tick).
