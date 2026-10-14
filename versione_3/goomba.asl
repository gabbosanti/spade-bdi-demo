//Belief base
alive.
direction(right).

//Initial goal
!start.


//Plans
+!start <-
    .print("Hello! Goomba BDI agent started.");
    .print("AgentSpeak plan executed successfully.");
    !patrol.

/*
+!patrol : mario_near
    <- !kill_mario.
*/

+!patrol : obstacle_ahead
    <- .print("Obstacle ahead !")
       .turn_around;
       !patrol.

+!patrol : direction(right)
    <- .move_right;
       !patrol.

+!patrol : direction(left)
    <- .move_left;
       !patrol.

-alive : 
    <- .kill_agent.

/*
+!kill_mario : 
    <- .print("Mario is dead")
*/