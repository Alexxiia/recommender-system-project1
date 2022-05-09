# Report - Project 1: Recommender

### Project description

<h2>Comparing two different data sets:</h2>

 - RandomForestCBUIRecommender:
    - n_neg_per_pos: 9
    - n_estimators: 276
    - max_depth: 7
    - min_samples_split: 19
    <br>
 - XGBoostCBUIRecommender:
    - n_neg_per_pos: 9
    - n_estimators: 276
    - max_depth: 7
    - min_samples_split: 19
    - learning_rate: np.log(2)

<h2>Version1:</h2>
<p>(as it is now)</p>

 - RandomForestCBUIRecommender:
<img src="assets/version1_random-forest_result.png">

 - XGBoostCBUIRecommender:
<img src="assets/version1_xgboost_result.png">

<h2>Version2:</h2>
in 'i_room_space_for_people_feature':
<br>
<img src="assets/version2_changes.png">

in 'i_room_price_expensiveness_feature':
<br>
<img src="assets/version2_changes2.png">

add user feature 'u_average_values_feature':
<br>
<img src="assets/version2_changes3.png">

 - RandomForestCBUIRecommender:
<img src="assets/version2_random-forest_result.png">

 - XGBoostCBUIRecommender:
<img src="assets/version2_xgboost_result.png">


<h3>It was also checked for both versions with LinearRegressionCBUIRecommender, but the results where worse.
<br>
There were more tests while tuning but there is no need for showing them all and comparing.</h3>