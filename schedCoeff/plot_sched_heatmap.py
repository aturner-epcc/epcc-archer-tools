import sys
import re
import numpy as np

csvfile = open(sys.argv[1], "r")

size = ["1", "2", "3-4", "5-8", "9-16", "17-32", "33-64", "65-128", "129-256", "257-512", "513-1024", "1025-2048", "2049-4096", "4097-8192"]
jobtime = []
eff = []
wait = []
jobs = []
usage = []
values = []
jvalues = []
uvalues = []
wvalues = []

intable = False
for line in csvfile:

   print line

   if re.match("Runtime:", line):
      sizeline = line.rstrip()
      tokens = sizeline.split()
      joblen = tokens[1]
      jobtime.append(joblen)
      intable = True
      values = [None] * len(size)
      jvalues = [0] * len(size)
      uvalues = [0.0] * len(size)
      wvalues = ["0:0:0"] * len(size)
      continue
      # End of if start block match

   # If we are in the time range then accumulate data
   if intable:
               
      # Skip the end indicator
      if re.match(",", line):
         eff.append(values)
         jobs.append(jvalues)
         usage.append(uvalues)
         wait.append(wvalues)
         intable = False
         continue
      elif re.match("Nodes", line):
         continue
      dataline = line.rstrip()
      tokens = dataline.split(",")
      ind = size.index(tokens[0])
      jvalues[ind] = int(tokens[1])
      uvalues[ind] = float(tokens[2])
      wvalues[ind] = tokens[4]
      values[ind] = float(tokens[5])

csvfile.close()

sys.stdout.write("{:12s}".format(" "))
for j in range(len(size)):
   sys.stdout.write("{:>12s}".format(size[j]))
sys.stdout.write("\n")
for i in range(len(jobtime)):
   sys.stdout.write("{:>12s}".format(jobtime[i]))
   for j in range(len(size)):
      if eff[i][j] is None:
         eff[i][j] = -1
         usage[i][j] = -1.0
      sys.stdout.write("{:12.3f}".format(eff[i][j]))
   sys.stdout.write("\n")

sys.stdout.write("\n")
sys.stdout.write("{:12s}".format(" "))
for j in range(len(size)):
   sys.stdout.write("{:>12s}".format(size[j]))
sys.stdout.write("\n")
for i in range(len(jobtime)):
   sys.stdout.write("{:>12s}".format(jobtime[i]))
   for j in range(len(size)):
      sys.stdout.write("{:>12s}".format(wait[i][j]))
   sys.stdout.write("\n")

xeff = np.array(eff)
xusage = np.array(usage)


# Plot a heatmap
import matplotlib

# Plot to image file without need for X server
matplotlib.rcParams['font.size'] = 9
matplotlib.rcParams.update({'figure.autolayout': True})
matplotlib.use("Agg")

# Import the required functions
from matplotlib import pyplot as plt
from matplotlib import cm

fig = plt.figure()
ax1 = plt.subplot(1, 1, 1)
masked_array = np.ma.masked_where(xeff==-1, xeff)
cmap = cm.RdYlGn
cmap.set_bad('w', 1.0)
print masked_array
cax1 = ax1.imshow(masked_array, interpolation='nearest', cmap=cmap, vmin=0.0, vmax=1.0)
plt.xticks(np.arange(len(size)), size, rotation='45')
ax1.set_yticks(np.arange(len(jobtime)))
ax1.set_yticklabels(jobtime)
ax1.set_xlabel("Job Size / nodes")
ax1.set_ylabel("Run Time / h")
ax1.set_title("Scheduling Coefficient Matrix (numbers are numbers of jobs)")
cbar1 = plt.colorbar(cax1, orientation='vertical', shrink=0.45, aspect=10)
for i in range(len(jobtime)):
   for j in range(len(size)):
      ax1.text(j, i, str(jobs[i][j]), horizontalalignment='center', verticalalignment='center', fontsize=7)

fig.savefig("sched_coeff_heatmap_jobs.png")

# fig = plt.figure()
fig.clf()
ax2 = plt.subplot(1, 1, 1)
masked_array = np.ma.masked_where(xeff==-1, xeff)
cmap = cm.RdYlGn
cmap.set_bad('w', 1.0)
cax2 = ax2.imshow(masked_array, interpolation='nearest', cmap=cmap, vmin=0.0, vmax=1.0)
plt.xticks(np.arange(len(size)), size, rotation='45')
ax2.set_yticks(np.arange(len(jobtime)))
ax2.set_yticklabels(jobtime)
ax2.set_xlabel("Job Size / nodes")
ax2.set_ylabel("Run Time / h")
ax2.set_title("Scheduling Coefficient Matrix\n(boxes contain mean queue time in hours and number of jobs)")
cbar2 = plt.colorbar(cax2, orientation='vertical', shrink=0.45, aspect=10)
for i in range(len(jobtime)):
   for j in range(len(size)):
      hms = wait[i][j].split(':')
      hrs = float(hms[0]) + float(hms[1])/60.0 + float(hms[2])/3600.0
      shrs = "{0:.2f}\n({1:d})".format(hrs, jobs[i][j])
      ax2.text(j, i, shrs, horizontalalignment='center', verticalalignment='center', fontsize=7)

fig.savefig("sched_coeff_heatmap_wait.png")

fig.clf()
ax3 = plt.subplot(1, 1, 1)
masked_array = np.ma.masked_where(xusage==-1.0, xusage)
maxu = masked_array.max()
cmap = cm.hot_r
cmap.set_bad('w', 1.0)
cax3 = ax3.imshow(masked_array, interpolation='nearest', cmap=cmap)
plt.xticks(np.arange(len(size)), size, rotation='45')
ax3.set_yticks(np.arange(len(jobtime)))
ax3.set_yticklabels(jobtime)
ax3.set_xlabel("Job Size / nodes")
ax3.set_ylabel("Run Time / h")
ax3.set_title("Usage Matrix\n(Colours indicate kAU usage and boxes contain number of jobs)")
cbar3 = plt.colorbar(cax3, orientation='vertical', shrink=0.45, aspect=10)
for i in range(len(jobtime)):
   for j in range(len(size)):
      if xusage[i][j]/maxu > 0.9:
         ax3.text(j, i, str(jobs[i][j]), horizontalalignment='center', verticalalignment='center', fontsize=7, color='white')
      else:
         ax3.text(j, i, str(jobs[i][j]), horizontalalignment='center', verticalalignment='center', fontsize=7)

fig.savefig("usage_heatmap.png")

