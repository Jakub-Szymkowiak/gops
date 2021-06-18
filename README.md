# Game of Pure Strategy 

This was created as a solution to a Linear Programming assigment at the University of Warsaw. 
It is an attempt to recreate reasoning used in [Computer Solution to the GOPS](https://www.econstor.eu/obitstream/10419/98554/1/749748680.pdf) in Python.

The script recursively calculates the payoff matrix for [GOPS](https://en.wikipedia.org/wiki/Goofspiel) and then uses linear programming solver provided in `` scipy.optimize`` to find the optimal strategy at the first move.
It was not required, so I did not implement it, but the code can be easily edited so that the strategies for later moves are calculated as well (provided the previous ones and the previous upcards).
It would be enough to update the `` init_state `` every move.
The results are saved to a ``gopsN.csv`` file, where ``N`` is the number of "cards" used in the game.

Obiously this implementation will never be nearly as fast as the C++ one authors provided. 
Nonetheless some optimization was done and the solution to the GOPS with 6 or even 7 cards can be obtained within reasonable amount of time, which otherwise would be impossible.



