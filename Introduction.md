# (UN)HEALTHY MASSACHUSETTS
***Identifying a Focus***

## Goal

What does it mean to be a “big problem” in healthcare? What does it mean to be a “biggest problem” in health in the state of Massachusetts? Naively chasing data to construct a top ten list is fraught with problems. Issues are connected, messy, and don’t always lend themselves to being quantitatively measured. If the issue can be measured quantitatively, the measures of different issues don’t have the same units. It feels like comparing, not oranges to apples, but navel oranges to empire apples.

## Progress

We have identified a catalogue of issues that are cited as problems in MA in documents such as the State Health Assessment produced by the state Department of Public Health Commissioner's Office. The State Assessment relies heavily on Community Health Assessments (CHAs) from around the state. These are self-reported documents prepared by hospitals and medical centers using interviews and focus groups. The reports are not standardized and non-quantitative. The Health Assessment augments those findings with statistics which compare the state values to national values, show worsening trends, and compare values for minority groups. Some examples of the type of data available in the Assessment:

* Infant mortality rate for non-hispanic blacks is 2.1x that for whites
* Cost of of infant child care is highest in country
* Infant mortality rate is up over several years
* Death rate due to opioid use is up 5x since 2000
* Death rate due to opioid use is ~3x US average.

The Department of Public Health also issued an analysis, or scan, of the body of Community Health Assessments. They identified statewide trends and concerns by counting assessments containing key terms across four categories:

1. Health Issues (e.g. mental health, substance abuse, cancer)
2. Barriers to Health (e.g. transportation, lack of affordable housing)
3. Barriers to Health Care (e.g. cost of care, health literacy)
4. Priority Populations (e.g. elderly, youth, latino)

The paper then presents four lists of issues ranked by incidence count. This gives a feel for what issues are prevalent across the state. Indeed, it presents a simple, pan-state, method to rank issues in health. It relies on regional experts and content experts interviews. However, there are several downsides to this method:

* Although each assessment probably covers roughly similar sized communities, this method may bias for or against urban regions.
* Some assessments base these priorities on quantitative data, some do not. There is no standard to these data, and we do not know what biases go into claiming priorities.
* Politics are mixed in as these assessments are used for federal funding.
* Unclear what makes something a “priority”. Is it a priority because it is a problem (data) or because they decide this is the time to act (policy)?
* The method implicitly values universality of a problem over severity. If two towns, and only two town, in Massachusetts sank into the ocean, it wouldn’t make the top ten list.

## Now Where?

Equipped with the statewide Assessment, the community based priority lists, and assorted other national rankings of health issues, we make a plan. I’ve dreamed up a few possibly interesting/useful ways to think of big problems in Massachusetts:

### Comparisons against US averages

We rank the issues/problems by how Massachusetts fairs relative the country at large. In this case we’re focussing on Massachusetts in the context of the country. The issues we fair worst at are most likely those we can solve at the state level. Each issue would have a different metric, and the comparison against the US would be a “n-fold-worse” statement, like “Death rate due to opioid use is ~3x US average.” We would need to find quantitative data at the state level for all the issues we’re interested in, which is probably doable but time consuming.

### Correlations and relationships

One challenge of identifying an issue as “bigger” than another is that issues are related, linked, and causal. For example, the rate of preterm births in MA among black women is very high compared to US mean rate. Preterm birth rate is influenced by inadequate prenatal care, which in turn can be due to difficulty in transportation, and poverty, and systemic inequalities and high costs of living. Which of these issues do we identify as the “problem”?

Rather than trying to unravel these correlations and evaluate the impact of individual problems versus their antecedents or effects, we analyze the correlations themselves. The analysis of the Community Health Assessments has captured a town-by-town distribution of health issues, health barriers, and focus populations, across the state. We also have access to demographic, economic, and other census data for each town. It may be illuminating to find and develop visualizations for the correlations and relationships between these various issues and metrics.

## Issue-Statistics Relationships

I've decided to pursue the second option. Each Community Health Assessment (CHA) is associated with a set of issues, and also with a set of municipalities. Each municipality has, in turn, many varieties of statistics availalbe via census data. We can therefore see how the different issues are related to each other and to demographic, economic, and health statistics recorded in the census data.

The file "issue data map.svg" gives a graphical representation of these relationships. The first frame shows how the issues, documents, municiaplities, and statistics are related, as well as a rough indication of the multiplicity of the connections. The second frame shows how the full interconnected map can be simplified to focus on smaller sets of connected entities. The third frame shows how we expect to group issues based on co-occurence. We can then see how these groups correlate to census data.

I have scrubbed the Scan of CHAs document and the data is now available in CHA_data.csv. The census data will be downloaded from https://censusreporter.org/ as geojson files. I expect to do the data analysis and first pass at visualizations in python. I have some ideas for interactive visualizations and processing somewhere down the road, if results turn out to be interesting.
