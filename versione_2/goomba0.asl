direction(right).

!patrol.

+!patrol : direction(left)
    <- .move_left;
       !patrol.

+!patrol : obstacle_ahead 
    <- .turn_around;
       !patrol.

+!patrol : direction(right)
    <- .move_right;
       !patrol.

