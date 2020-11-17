
README FILE:

This program is a BattleDot SpinOff where Players will enter into the arena and await the game to start.
Players will then take turns attacking at random the oppenent in front of them. When their ship is taken down by an opponent,
they will send the port/IP of the oppenents adjacent to it so they can be connected. The game ends when only one user remains

The program features 2 ways to play. P2P with different IP's under the same network or different Ports using the same machine!

Written in Python 3.7.3


HOW TO USE:

IF ON THE SAME MACHINE:

1. We initialize all the players by: (Assuming they will form a perfect ring and no user has multiple people attacking it)

Run Python BattleDot N/A N/A PortA PortB #OfOtherplayers PortUser

eg. (Python BattleDot.py N/A N/A 8079 8081 2 8080)

    (Python BattleDot.py N/A N/A 8080 8079 2 8081)

2. Initialize the final player with the last arguement being "first"

Run Python BattleDot N/A N/A PortA PortB #OfOtherplayers PortUser first

eg. (Python BattleDot.py N/A N/A 8081 8080 2 8079 first)



3. Wait until the users done battling !!



IF ON SEPERATE MACHINES:

1. We initialize all the players by: (Assuming they will form a perfect ring and no user has multiple people attacking it)

    Here the ports do not really matter.

Run Python BattleDot IP_A IP_B PortA PortB #OfOtherplayers PortUser

eg. (Python BattleDot.py 129.128.41.11 129.128.41.13 8080 8089 2 8080)

    (Python BattleDot.py 129.128.41.12 129.128.41.11 8080 8089 2 8080)


2. Initialize the final player with the last arguement being "first"

Run Python BattleDot N/A N/A PortA PortB #OfOtherplayers PortUser first

eg. (Python BattleDot.py 129.128.41.13 129.128.41.12 8080 8089 2 8080)



3. Wait until the users done battling !!



RESULTS:

Throughout the entire program for each process there will be "Sent attack to ___" and Received from "____"

these help indicate which node its being attacked by or who it is attacking. Upon getting knocked out, it will say

"Hit! Player Lose" and will then update the neighbors with its each other's IP/POrt so they can continue battling.

Upon being the last player remaining, There is a notification saying the user has won!


