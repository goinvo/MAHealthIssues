import csv
from types import *
from collections import Counter
import pprint


class CHARecord:
    municipality_issue_map = dict()
    def __init__(self):
        self.organization = ''
        self.municipalities = set()
        self.issues = set()
        self.interviews = 0
        self.focusGroups = 0

    def make_from_csv_row(self, rownames, row):
        assert type(rownames) is ListType, "use a list of strings for rownames"
        orgstring = row[rownames[0]]
        munsstring = row[rownames[1]]
        healthstring = row[rownames[2]]
        barriersstring = row[rownames[3]]
        commengagestring = row[rownames[4]]

        self.organization = orgstring
        for m in munsstring.split(","):
            if len(m.strip())>0:
                self.municipalities.add(m.strip())
        for i in healthstring.split(","): self.issues.add(i.strip())
        for i in barriersstring.split(","): self.issues.add(i.strip())
        commengagearray = commengagestring.split(' \n')
        for i in range(0, len(commengagearray), 2):
            if commengagearray[i] == 'Key Informant Interviews:':
                self.interviews = int(commengagearray[i+1])
            if commengagearray[i] == 'Focus Groups:':
                self.focusGroups = int(commengagearray[i+1])

        # add municipalities if they are missing. and assign them each the sets of issues
        for m in self.municipalities:
            if m not in CHARecord.municipality_issue_map:
                CHARecord.municipality_issue_map[m] = set()
            CHARecord.municipality_issue_map[m].update(self.issues)


class Issue:
    issue_map = dict() #class level map of names to issues
    def __init__(self, name):
        self.name = name
        self.records = []
        self.connected_issue_names = Counter()  #these are name strings, not other issue objects
        self.rank = 0 #max ranking of connected issues
        Issue.issue_map[name] = self

    def add_record(self, record):
        assert isinstance(record, CHARecord)
        self.records.append(record)
        for issuestr in record.issues:
            if issuestr == self.name: continue  #this is me
            self.connected_issue_names[issuestr] += 1
        if len(self.connected_issue_names)>0:
            self.rank = self.connected_issue_names.most_common(1)[0][1]


class IssueGroup:
    group_list = []
    municipality_group_scores = dict() # each municipality has a dictionary of group to score
    group_municipality_scores = dict()
    def __init__(self, issuelist):
        self.issues = issuelist
        self.issue_names = set([issue.name for issue in issuelist])
        IssueGroup.group_list.append(self)
        IssueGroup.group_municipality_scores[self] = dict()
        municipalities = set()
        for i in issuelist:
            for r in i.records:
                municipalities.update(r.municipalities)
        for m in municipalities: # each municipality gets a group score as percent of issues covered by this group
            mun_issues = CHARecord.municipality_issue_map[m]
            common_issues = mun_issues.intersection(self.issue_names)
            score = len(common_issues)/float(len(mun_issues))
            if m not in IssueGroup.municipality_group_scores: IssueGroup.municipality_group_scores[m] = dict()
            IssueGroup.municipality_group_scores[m][self] = score
            IssueGroup.group_municipality_scores[self][m] = score

#iterative method to grow a group from top rank down to minrank
def extend_group(group, issue_dict, current_rank, min_rank, upper_culling_rank):
    assert isinstance(group, set)
    # issue_dict is {rank, issue}
    issuelist = issue_dict.get(current_rank, [])
    if len(issuelist)==0: # there are no more at this rank
        current_rank = current_rank - 1
        if current_rank<min_rank:
            return group
        return extend_group(group, issue_dict, current_rank, min_rank, upper_culling_rank)
    issue = issuelist.pop() # grab the next at this rank
    group.add(issue) # add it to the group
    for pair in issue.connected_issue_names.most_common():
        pairedrank = pair[1]
        try:
            pairedissue = Issue.issue_map[pair[0]]
        except:
            print('Your issue name isn not an issue...')
        if pairedrank < min_rank:
            break
        if pairedrank >= current_rank:
            continue  # only descend in ranking
        if pairedissue.rank > upper_culling_rank:
            continue  # ignore everything that is too high
        if pairedissue in group:
            continue
        if pairedissue in issue_dict.get(pairedrank,[]):
            continue
        issue_dict.setdefault(pairedrank, []).append(pairedissue)
    return extend_group(group, issue_dict, current_rank, min_rank, upper_culling_rank)




def make_groups(issues, start_limit_rank, min_rank, upper_culling_rank, ):
    # find the issues with the highest ranks
    rankedissues = []
    for string, object in issues.items():
        rankedissues.append(object)
    rankedissues = sorted(rankedissues, key=lambda x: x.rank, reverse=True)
    groups = []

    for iss in (topissue for topissue in rankedissues if (topissue.rank>=start_limit_rank and topissue.rank<upper_culling_rank)):
        issue_dict = {
            iss.rank : [iss]
        }
        group = set()
        print('starting at rank ' + str(iss.rank) + ' with issue: ' + iss.name)
        group = extend_group(group, issue_dict, iss.rank, min_rank, upper_culling_rank)
        if group: groups.append(group)

    # get the unique groups from this collection
    for i in range(0, len(groups)):
        g = groups[i]
        match = False
        for j in range(i+1, len(groups)):
            if g == groups[j]: match = True
        if not match:
            issuegroup = IssueGroup(g)



def load_records(filename):
    csvfile = open(filename, 'rb')
    dictreader = csv.DictReader(csvfile)
    rownames = dictreader.fieldnames
    records = []
    for row in dictreader:
        record = CHARecord()
        record.make_from_csv_row(rownames, row)
        if record.organization: records.append(record)
    return records


def make_issues(records):
    issues = {}
    for r in records:
        for issuestr in r.issues:
            if issuestr not in issues:
                newissue = Issue(issuestr)
                issues[issuestr] = newissue
            issues[issuestr].add_record(r)
    return issues




if __name__ == '__main__':
    filename = '../raw_data/cha_data.csv'
    records = load_records(filename)
    print("Number Records: " + str(len(records)))
    issues = make_issues(records)
    toprank = 2
    minrank = 1
    cullingrank = 35
    make_groups(issues, toprank, minrank, cullingrank)
