"""
Example for creating axes, including empty axes with text.
"""

import matplotlib.pyplot as plt

fig = plt.figure()

# normal subplots
ax1 = fig.add_subplot(2, 3, 1)
ax2 = fig.add_subplot(2, 3, 3)
ax3 = fig.add_subplot(2, 3, 4)
ax4 = fig.add_subplot(2, 3, 5)
ax5 = fig.add_subplot(2, 3, 6)

# axes for text
axt = fig.add_axes([0.4, 0.8, 0.2, 0.2])  # llx, lly, w, h
axt.axis('off')  # turn off coordinate system

template = 'Count: {:5}'
txt = axt.text(0.5, 0.5, template.format(0),
               horizontalalignment='center',
               verticalalignment='center',
               transform=axt.transAxes)  # relative coordinates

plt.pause(0.01)  # pause required to make figure visible

input('Press ENTER to begin counting')

for k in range(30):
    txt.set_text(template.format(k))
    plt.pause(0.1)  # pause required to make update visible

plt.show()
