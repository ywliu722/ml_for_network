import pandas as pd
import matplotlib.pyplot as plt

input_adaptation = 'fps.txt'
input_fix = 'fps_no_pre.txt'
adaptation = pd.read_csv(input_adaptation, sep=" ", header=None)
fix = pd.read_csv(input_fix, sep=" ", header=None)

result = pd.concat([adaptation[1:51], fix[1:51]], axis=1, join='inner')
result.columns = ['adaptation', 'no adaptation']

output_fps_statistics = open('fps_statistics.txt', 'a')
output_fps_statistics.write(result.describe().to_string())
output_fps_statistics.close()

plt.boxplot(result)
plt.xticks([1, 2], ['Adaptation', 'No Adaptation'])
plt.savefig('boxplot.png')
