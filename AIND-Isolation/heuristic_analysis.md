# Isolation Game Player Agent
_Bertrand Louargant_  
_Udacity AI Nanodegree_

&nbsp;   
&nbsp;    
&nbsp;    


******************

## 1. Introduction   
<p>
The goal of this project is to create an AI agent for the Isolation game.
<p>
In the Isolation game, each player move their pawm in a L-shaped step alternately.
Each box on the grid can be visited only once so that the number of possible moves decrease at each turn.
The player that doesn't have any remaining move available loose the game.

## 2. Heuristics analysis   
In addition to the AlphaBeta Pruning strategy we have been tasked to develop
three different heuristics and compare their ability to win.   
As the game is lost by the player that cannot move anymore, then the overall strategy is to try to restrain the opponent's movements.   
In this context, for each functions we return the score of the player minus three times the score of it's opponent.   
The three heuristics are:  

* __custom_score (Center First)__:   
For this approach we introduce a new function, weighted_move, that return a weight equal to square of the distance from the center of the
board to a given position.    
The function add up all the weighted potentials moves of the player and compare it the sum of the weighted moves of it's opponent.   

* __custom_score_2 (Plan Ahead)__:   
In this function, for each available moves we fetch all possible next moves.   
It allows us to focus on openings offering the most mobility.  
Then again, the score is compared to  
Once again this score is compared to that of the opponent with a weight of three in his favor.

* __custom_score_3 (Plan Ahead + Center First)__:   
With the last function we try to determine if the combination of the two previous features increases our chances of winning the game.

## 3. Results    

|               |   AB_Improved  |   AB_Custom   |   AB_Custom_2 |   AB_Custom_3  |
| ------------- | :------------: | :-----------: | :-----------: | :-----------:  |
| **Opponent**  | **Won / 10**   | **Won / 10**  | **Won / 10**  | **Won / 10**   |
| Random        | `8`  | `10` | `9`  | `10` |
| MM_Open       | `7`  | 5    | `7`  | `7`  |
| MM_Center     | `8`  | `8`  | `10` | `8`  |
| MM_Improved   | `6`  | `8`  | `8`  | `8`  |
| AB_Open       | 5    | 5    | `6`  | 5    |
| AB_Center     | 5    | 5    | `6`  | 5    |
| AB_Improved   | `6`  | 4    | 5    | 5  |
| **Win Rate:** |<font color="Blue">64.3%</font>|<font color="Blue">65.7%</font>|<font color="Blue">70.0%</font>|<font color="Blue">70.0%</font>|


As we can see, both functions, __Center First__ and __Plan Ahead__, give us relevant results.
However, the combination of the two approaches does not increase the chances of winning the game.   
This is probably due to the fact that these two approaches favor the same type of movements. And as each time we subtract the score obtained to three times that of the opponent, the final result remains substantially the same.  


> _It should be noted that these results are to be taken with caution.   
Indeed, the number of matches (10) by assignment is far from sufficient to obtain reliable statistics._


## 4. Evolutions:  
Ifhad to dig deeper into the subject, it would be relevant to compare the execution time of __Plan Ahead__ and __Center First__ and to keep only the fastest.  
Other approaches should also be studied, such as a rule-based inference algorithme or a Deep Neural Network and reinforcement learning.
