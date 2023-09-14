import json
import matplotlib.pyplot as plt

# List of JSON file names for the main plot
json_files_main = ['./dev/analysis.json',  './dev/upload.json', './dev/initial.json', './dev/write.json']
labels_main = ['Analysis', 'FileUpload', 'InitialUpload', 'Write']

# Dictionary to store the average time for each JSON file in the main plot
average_times_main = {}

# Iterate over each JSON file in the main plot
for file_name, label in zip(json_files_main, labels_main):
    with open(file_name, 'r') as file:
        data = json.load(file)
        
        times = [entry['time'] for entry in data]
        average_time = sum(times) / len(times)
        average_times_main[label] = average_time

# List of JSON file names for the additional plot
json_files_additional = ['./dev/access.json', './dev/read.json']
labels_additional = ['AccReq', 'Read']

# Dictionary to store the average time for each JSON file in the additional plot
average_times_additional = {}

# Iterate over each JSON file in the additional plot
for file_name, label in zip(json_files_additional, labels_additional):
    with open(file_name, 'r') as file:
        data = json.load(file)
        
        times = [entry['time'] for entry in data]
        average_time = sum(times) / len(times)
        average_times_additional[label] = average_time

# Plotting the main plot
x_main = range(len(average_times_main))
y_main = list(average_times_main.values())
labels_main = list(average_times_main.keys())

colors_main = ['#F0AB41', '#D9632D', '#FF8C00', '#FFA500']

plt.bar(x_main, y_main, tick_label=labels_main, color=colors_main)
plt.xlabel('Transaction name')
plt.ylabel('Average Time (Seconds)')
plt.title('Transaction Processing Time for Modification Operations')
plt.savefig('fig1.png')

plt.clf()

# Plotting the additional plot
x_additional = range(len(average_times_additional))
y_additional = list(average_times_additional.values())
labels_additional = list(average_times_additional.keys())

colors_additional = ['#FDE186', '#FFA500']

plt.bar(x_additional, y_additional, tick_label=labels_additional, color=colors_additional)
plt.xlabel('Transaction name')
plt.ylabel('Average Time (Seconds)')
plt.title('Transaction Processing Time for Retrieval Operations')
plt.savefig('fig-mod.png')
