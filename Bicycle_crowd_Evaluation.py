import json
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

data = json.load(open(r'file path of anonymized_project.json'))
output = json.load(open(r'file path of references.json'))


# function to extract the key values.
def json_extract(obj, key):
    arr = []

    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)

    return values


# print the no of annotators in dataset
annotators = json_extract(data, 'vendor_user_id')
print("1. No of annotators are :", len(set(annotators)))
print("2. No of total annotations in dataset:", len(annotators))
print("3. Annotators in the dataset :", set(annotators))

# print  number of annotations per user
annotation_times = Counter(annotators)
print("4. No of annotations per annotator are : ", annotation_times)

# print the no of times where annotators choose corrupt_data and cant_solve
corrupt_data = json_extract(data, 'corrupt_data')
print("5. No of times annotators chose corrupt_data are :", corrupt_data.count(True))
cant_solve = json_extract(data, 'cant_solve')
print("6. No of times annotators chose cant_solve are :", cant_solve.count(True))

# check whether the reference_set is balanced
is_bicycle = json_extract(output, 'is_bicycle')
result = [is_bicycle.count(True), is_bicycle.count(False)]
print("7. No of True and False value in reference set", result)
# Bar diagram to show
y = np.array([is_bicycle.count(True), is_bicycle.count(False)])
x = np.array(["True", "False"])
c = ['green', 'red']


def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i])


plt.bar(x, y, color=c)
addlabels(x, y)
plt.title("Reference dataset values")
plt.show(block=False)
plt.pause(3)
plt.close()

# finding annotation duration
annotation_durations = json_extract(data, 'duration_ms')
# print the minimum annotation time
print("8. Minimum annotation time is: ", min(annotation_durations))
# print the maximum annotation time
print("9. Maximum annotation time is :", max(annotation_durations))
# print the average annotation time
average = sum(annotation_durations) / len(annotation_durations)
print("10. Average annotation time is :", average)

# finding the disagreement about question between annotators
annotator_answers = json_extract(data, 'answer')
input_image = json_extract(data, 'project_node_input_id')

# creating ad dic for images and corresponding annotator's answers
d = defaultdict(list)
for k, v in zip(input_image, annotator_answers):
    d[k].append(v)

print("11. No of images (results) :", len(is_bicycle))
# finding the no of images where annotators agree and produce same results
annotator_agree = (["true" for key, value in d.items() if len(set(value)) == 1])
print("12. No of images where the annotator agree the results: ", len(annotator_agree))

# finding the no of images where annotators don't agree and produce different results
annotator_disagree = ([value for key, value in d.items() if len(set(value)) != 1])
# print(annotator_disagree)

print("13. No of images where the annotator disagree the result: ", len(annotator_disagree))

# finding the images where annotator disagree
key_va = ([key for key, value in d.items() if len(set(value)) != 1])

# creating numberlist(majority answers from annotator
numberlist = []
# creating indexlist to store the index of incorrect answer
indexlist = []
for i in annotator_disagree:
    if i.count('no') > i.count('yes'):
        answer_no = [False]
        indices = [index for index, element in enumerate(i) if element == 'yes']
        indexlist.append(indices)
        numberlist.append(answer_no)

    else:
        answer_yes = [True]
        indices = [index for index, element in enumerate(i) if element == 'no']
        indexlist.append(indices)
        numberlist.append(answer_yes)

# creating a dictionary for input images and annotators
ano_lt = defaultdict(list)
for k, v in zip(input_image, annotators):
    ano_lt[k].append(v)

# finding the annotators from incorrect answer images
badannotlist = ([value for key, value in ano_lt.items() for i in key_va if key == i])

badannotators_list = []
for i, inner_l in enumerate(indexlist):
    for j, item in enumerate(inner_l):

        for index1, value in enumerate(badannotlist):
            for index2, values in enumerate(value):
                if index1 == i and index2 == indexlist[i][j]:
                    badannotators = badannotlist[index1][index2]

                    badannotators_list.append(badannotators)

print("14. No of times where annotators gave wrong answer:", len(badannotators_list))
badannotatorcount = Counter(badannotators_list)
print("15. List of annotator's bad annotation times", badannotatorcount)

# plot pie chart
labels = 'Good', 'Bad'
sizes = [len(annotators), len(badannotators_list)]
colors = ['gold', 'yellowgreen']
explode = (0.1, 0)  # explode 1st slice
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.title("Total percentage of Good and Bad annotations")

plt.show(block=False)
plt.pause(3)
plt.close()

# Bar diagram of bad annotation per annotator .
dict_div = (Counter({key: (badannotatorcount[key] / annotation_times[key]) * 100 for key in badannotatorcount}))
print("16. Percentage of bad annotaion per annotator", dict_div)
c = ['yellowgreen']
plt.bar(dict_div.keys(), dict_div.values(), color=c)
plt.xticks(rotation=90)
plt.title("Percentage of bad annotations per annotator")
plt.show(block=False)
plt.pause(3)
plt.close()
