#Was Kobe Bryant a selfish player?


There's no doubt that Kobe Bryant was an amazing offensive player, regarded among the best due to the many ways he was capable to get to the basket. But, unlike many of the greatest, Kobe got the fame of a ball hog, a selfish player. Countless memes were made about his unwillingness to pass the ball to his teammates, but many Kobe apologists (you might even call them stans), myself included, always felt it was unjustified, maybe not completely, but not enough to justify how often it was talked about.

But when all of this began? I think it started in the 2003-2004 season playoffs, especially in the finals when Detroit Pistons prepared a game plan designed to frustrate Kobe baiting him in taking too many shots reducing the possessions Shaq, who was unstoppable at the time, would have. The plan worked, the Pistons won the title. The narrative then gained strength in the following years. After the departure of Shaq from the team, the Lakers were horrible with Kobe, almost alone, having to carry mediocre players, so he took most of the shots.

And what do Kobe defenders have to use in his defense? "Of course he didn't pass the ball, his teammates were the likes of Kwami Brown, they couldn't hit anything" and most important one stat, Kobe is among the top 50 pass leaders, more precisely the 31st, how can a player that is in the 99th percentile of players in assist be a ball hog? People are just hating on a great player.

Let's take a look at Kobe's pass average for each season and compare it with his team's ability to score (Field Goal percentage - FG%).

Kobe had a long career (9th all-time in minutes played) so it is natural that he has a high number of assists. This is the main counterpoint that the ball hog side of the discussion uses and it makes sense, but it's true? For that, we can analyze and compare the all-time assist leaders with Kobe and see if the Mamba fares well. 

First, let's explore the all-time list data, to get a better understanding of it.

With the boxplot, we can see the majority of the variance in the data is contained in the PG and SG. That's because the majority, 93, of players are split among these two positions, with Shooting Guards having a higher variance.

Basketball is a game of many stats and to compare Kobe among the other 99 players in every stat would not only take a long time but would also be a waste of it. As some stats won't help us better understand the relationship between players when it comes to assists or how selfish a player is So for this exploratory analysis we will focus on the stats that have higher absolute correlation values with assists.

Some interesting data points are how AST is not negatively correlated to any other features, but AST% and AST_PerG are negatively correlated with the majority of them. Another data point that initially surprised me was the relationship between AST and TOV, the third strongest assist correlation, but after thinking for a second it makes sense. A player who has a lot of assists is the one that passes the ball a lot and the most common type of turnovers comes from passes (https://squared2020.com/2019/01/27/the-no-turnover-turnover/).  WS is highly correlated with VORP (Pearson correlation of 0.83), for that reason I'll remove WS.

Three other variables that I'd like to add are points (PTS), minutes per game (MP_PerG) and career length (C_LEN) as these represent well some of the arguments against Kobe, prefers shooting over passing and played a lot).


"But Kobe is a shooting guard, not a passing guard." is another phrase that we hear when this is discussed. Well, we have 46 shooting guards out of a hundred, so we can assume that a shooting guard is a position that gets a lot of assists, almost as much as a point guard). But it's Kobe more of a "shooting" guard than other SGs?


The results are almost a mirror from the comparison among all positions, we can also see how little his assists number deviate from the mean when compared to other stats like points, win shares, and field goal attempts.

From the exploratory analysis, the conclusion I've arrived at is that Kobe's high assist numbers are a product of higher minutes per game played than average for a higher number of games started and career length than most players. And that he was a more selfish player than average.


We've looked at the variable isolated and compared to the assist numbers, not evaluating how these variables might interact with each other and give us more information. To take this into account we will build a model that encapsulates the variables and hopefully can give us a better understanding of the data.


Due to the high number of variables and high colinearity among the variable (many of basketball stats are build upon each other) we will use PCA (Principal Components Analysis)

We will be using the variables with an absolute Pearson correlation value above 0.2 showed in the heatmap above. Taking all the 63 stats into the model adds a lot of noise, describing players in many directions by their defense ability or rebound ability among others. Bringing the number of components necessary to have 85% variance explained to 6, which would nullify the biggest advantage of PCA: the ability to better understand the data by reducing the number of variables.

Limiting the number of variables reduces the number of components necessary to 3


Let's take a better look at the components




Taking a look at the loadings of each component we can interpret what information they try to explain. PC1 explains the variance of the data taking into account the offensive prowess of the players indicated by the high loading of free throws statics, points, and win shares (WS and OWS) PC2 gives importance to the number of assists(the three assist stats that have the highest loadings) PC3, on the other hand, tries to explain the variance with the amount of time the player played (G, MP, and C_LEN) and the number of assists

With this in mind, we can expect that scoring-minded players will have a high PC1 score, pass first players will have a high PC2 score, and players with longer careers that played a lot of games and minutes will have a high PC3 score.

With three principal components, we get a good amount of explained variance and each component gives us 3 good directions to evaluate the players, but it would also require a 3D visualization. For visualization purposes, we will use only 2 components (the elbow method also supports this choice). Fortunately, 2 components give us a good amount of explained variance (75%), and the difference in directions of the weights between PC1 and PC2 on G, MP, and C_LEN could overturn the loss of PC3.

Kobe is well above the median in terms of scoring and below the median when it comes to passing. The PCA model also leads us to the same conclusion. Despite Kobe being among the top 100 assist leaders in the NBA, he was not a prolific passer, and most likely his high assists numbers are due to the number of minutes he was on the floor. 

Yes, Kobe was a ball hog.


