import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.text import Text
import numpy as np
from numpy.random import rand
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
from matplotlib.collections import PathCollection
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# import all classes/methods
# from the tkinter module
from tkinter import *


# Candidate class
class Candidate:
    def __init__(self):
        self.x = np.random.randint(-6, 6)       # candidates are assumed to be more moderate / centric
        self.y = np.random.randint(-6, 6)       # than the general populace
        self.primaryScore = 0
        self.frontRunner = False    # is the candidate a frontrunner / expected to win?
        self.color = Candidate.colors[Candidate.colorIndex]
        Candidate.colorIndex = Candidate.colorIndex + 1 if (Candidate.colorIndex < len(Candidate.colors)-1) else 0
        self.label = chr(Candidate.labelIndex)
        Candidate.labelIndex = Candidate.labelIndex + 1 if (Candidate.labelIndex < 90) else 65
        self.press = None
        self.cidpress = None
        self.cidmotion = None
        self.cidrelease = None
        self.coll = baseAxes.scatter(self.x, self.y, marker='*', c=self.color, picker=True)
        self.coll.set_offset_position('data')
        # self.coll.set_pickradius(100)
        self.anno = baseAxes.annotate(self.label, (self.x, self.y))
        # self.anno.set_picker(100)
        # print(self.anno.xy)
        # print("x: "+str(self.x)+" y: "+str(self.y))
        # print(self.coll.get_offsets())

    labelIndex = 65                     # start with A
    colorIndex = 0
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']        # array of basic colors

    def connect(self):
        self.cidpress = self.anno.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidmotion = self.coll.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.cidrelease = self.coll.figure.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):
        """on button press we will see if the mouse is over us and store some data"""
        # print("on_press")
        if event.inaxes != self.anno.axes:  # checks that the mouse is over the axes of the given object
            return
        contains, attrd = self.anno.contains(event)     # checks that the event is contained within the path
        # print(contains, attrd)
        if not contains:
            return
        # print('event contains', self.anno.xy)
        # this can probably be skipped in favor of using the self.x and self.y
        # in fact this may be necessary, since anno.xy isnt updating properly...
        x0, y0 = self.anno.xy
        self.press = x0, y0, event.xdata, event.ydata
        print(self.press)

    def on_motion(self, event):
        """on motion we will move the coll if the mouse is over us"""
        if self.press is None:  # check that the mouse was pressed and the on_press was handled
            return
        if event.inaxes != self.coll.axes:  # check that the event axes are the same as the object axes
            return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        # print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' % (x0, xpress, event.xdata, dx, x0+dx))
        self.x = x0 + dx
        self.y = y0 + dy
        # self.anno.set_x(self.x)
        # self.anno.set_y(self.y)
        self.anno.set_position((self.x, self.y))
        self.coll.set_offsets([self.x, self.y])
        self.coll.figure.canvas.draw()

    def on_release(self, event):
        # on release we reset the press data
        print("self xy:", self.x, self.y, "anno.xy:", self.anno.xy,
              "coll.offsets:", self.coll.get_offsets())
        # Question: Why is on_relase called 3 times? (once for each candidate, but still)
        # ?: self.coll.offsets is updated properly, but self.anno.xy always shows the original xy pos...
        self.press = None
        # not sure whethere it makes a difference how the canvas is referenced and redrawn:
        # self.coll.figure.canvas.draw()
        canvas.draw()


# Voter class
class Voter:
    def __init__(self):
        self.x = np.random.randint(-10, 10)
        self.y = np.random.randint(-10, 10)


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Helo, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    # for att in dir(name):
    #   if not att.startswith('__'):
    #   print(att)


def clear_plot():
    # for th in baseAxes.collections:
    #    print(th)
    baseAxes.collections.clear()  # this will clear the plotted data from the axes, but not the axes themselves
    baseAxes.texts.clear()
    clear_simulation()


def clear_simulation():
    baseAxes.patches.clear()  # clear any circles from Approval
    baseAxes.lines.clear()
    for candi in candidates:
        candi.primaryScore = 0


# this bit should probably be moved elsewhere or removed
def onpick1(event):
    print("onpick1 called")
    if isinstance(event.artist, Line2D):
        # for att in dir(event.ind):
        #    if not att.startswith('__'):
        #        print(att)
        thisline = event.artist

        thisline.set_markeredgecolor('#ff0000')

        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        ind = event.ind
        print('onpick1 line:', np.column_stack([xdata[ind], ydata[ind]]))
    elif isinstance(event.artist, Rectangle):
        patch = event.artist
        print('onpick1 patch:', patch.get_path())
    elif isinstance(event.artist, Text):
        text = event.artist
        print('onpick1 text:', text.get_text())
    elif isinstance(event.artist, mpatches.Patch):
        print("its a patch")
    elif isinstance(event.artist, PathCollection):
        print("path collection found")
    plt.show()


# this function is leftover from an example i copied in...
# it is not used, and will be removed later
def gen_vote_space():
    # simple picking lines, rectangles and text
    # fig, (ax1, ax2) = plt.subplots(2, 1)
    voters.clear()
    for i in range(10):
        voters.append(Voter())

    figS, ax1 = plt.subplots(1, 1)
    ax1.set_title('click on points, rectangles or text', picker=True)
    ax1.set_ylabel('ylabel', picker=True, bbox=dict(facecolor='red'))
    # line, = ax1.plot(rand(100), 'o', picker=5)  # 5 points tolerance
    # print(line)
    for voter in voters:
        ax1.plot(voter.x, voter.y, 'o', picker=True)
    # ax2.bar(range(10), rand(10), picker=True)     # pick the rectangle
    # for label in ax2.get_xticklabels():  # make the xtick labels pickable
    #   label.set_picker(True)
    # figS.canvas.mpl_connect('pick_event', onpick1)


# generate the voter and candidate populations
def gen_population():
    clear_plot()  # clear the previous data
    candidates.clear()          # clear the prvious set of candidates
    candCt = int(candCtSpinbox.get())       # retrieve number of candidates from spinbox
    for c in range(candCt):             # for nCand, create and add a candidate to the list
        cand = Candidate()
        cand.connect()
        candidates.append(cand)  # the candidates should be plotted as they are created...
    candidates[0].frontRunner = True
    candidates[1].frontRunner = True

    voters.clear()
    # voterCt = int(voterCtEntry.get())
    for v in range(voterCt.get()):
        voters.append(Voter())

    baseAxes.scatter([v.x for v in voters], [v.y for v in voters], marker='o')
    canvas.draw()


def calc_pref_dists(voter):
    prefDists = []
    for candi in candidates:
        d = ((voter.x - candi.x) ** 2 + (voter.y - candi.y) ** 2) ** 0.5
        prefDists.append(d)
    return prefDists


def plurality():
    print("Plurality method called")
    idealismThreshold = 8   # 5% chance a voter will vote their favorite even when not a frontrunner
    for voter in voters:
        dists = calc_pref_dists(voter)
        chosenCand = candidates[dists.index(min(dists))]
        if not (chosenCand.frontRunner or np.random.randint(0, 100) < idealismThreshold):
            frontDists = [d for (d, c) in zip(dists, candidates) if c.frontRunner]
            chosenCand = candidates[dists.index(min(frontDists))]
        chosenCand.primaryScore += 1
        baseAxes.plot([voter.x, chosenCand.x], [voter.y, chosenCand.y], color='#ccc', linewidth=1, zorder=0)
    canvas.draw()

    # determine the winner of the plurality election
    winner = candidates[0]
    for candi in candidates:
        print(f'Candidate {candi.label}: {candi.primaryScore}')
        if candi.primaryScore > winner.primaryScore:
            winner = candi
    winnerLabel.configure(text="Winner: "+winner.label)


def approval(app_radius):
    print("approval called")
    # this is for the approval rings
    for candi in candidates:
        circle = mpatches.Circle((candi.x, candi.y), app_radius, fill=False)    # ec="#0066ff"
        baseAxes.add_patch(circle)
    for voter in voters:
        dists = calc_pref_dists(voter)
        appList = [c <= app_radius for c in dists]
        if not any(appList):        # if voter approves of no candidate...
            # get index of minvalue in dists, increment score of the candidate of that index
            closestCand = candidates[dists.index(min(dists))]
            closestCand.primaryScore += 1
            baseAxes.plot([voter.x, closestCand.x], [voter.y, closestCand.y], color='#ccc', linewidth=1, zorder=0)
        elif all(appList):          # if candidate approves of all candidates
            dists[dists.index(max(dists))] = 2*app_radius
            for (candi, d) in zip(candidates, dists):
                if d <= app_radius:
                    candi.primaryScore += 1
        else:                       # otherwise...
            for (candi, d) in zip(candidates, dists):
                if d <= app_radius:
                    candi.primaryScore += 1

    winner = candidates[0]
    for candi in candidates:
        print(f'Candidate {candi.label}: {candi.primaryScore}')
        if candi.primaryScore > winner.primaryScore:
            winner = candi
    winnerLabel.configure(text="Winner: "+winner.label)
    canvas.draw()


def sim_election():
    print("sim election called")
    clear_simulation()
    votingMethod = methodSelectLB.get(methodSelectLB.curselection())
    if votingMethod == 'Plurality':
        plurality()
    elif votingMethod == 'Approval':
        approval(7)


# this function is also leftover from an example. This originally was used to integrate a mpl figure with
# a TKinter window.
# plot function is created for plotting the graph in tkinter window
def plot():
    # fig = Figure(figsize=(5, 5), dpi=100) # the figure that will contain the plot
    y = [i ** 2 for i in range(101)]        # list of squares
    baseAxes.plot(y)            # plotting the graph
    # canvas = FigureCanvasTkAgg(fig, master=window)    # creating the Tkinter canvas containing the Matplotlib figure
    canvas.draw()
    # placing the canvas on the Tkinter window
    # canvas.get_tk_widget().pack()
    # toolbar = NavigationToolbar2Tk(canvas, window)    # creating the Matplotlib toolbar
    # toolbar.update()
    # canvas.get_tk_widget().pack()     # placing the toolbar on the Tkinter window


# will need this later for updating the scores/tally table
def update_scores():
    for ro in range(len(candidates)):
        cell = Entry(scoreTable)
        cell.grid(row=ro, column=0)
        cell.insert(END, candidates[r-1].label)
        cell = Entry(scoreTable)
        cell.grid(row=ro, column=1)
        cell.insert(END, candidates[r-1].primaryScore)


def only_nums(char):
    return char.isdigit()


candidates = []     # blank list of candidates
voters = []         # blank list of voters
methods = ['Plurality', 'Approval']     # the voting methods to choose from
# The main tkinter window
root = Tk()
# setting the title and
root.title('Voting Methods: Plurality vs Approval')
# setting the dimensions of
# the main window
# root.geometry("500x500")

# the figure that will contain the plot
prefFigure = Figure(figsize=(5, 5), dpi=100)
#           **********      Create and setup the preference space plot      **********
baseAxes = prefFigure.add_subplot(1, 1, 1)
# plt.ylabel('test plot')
baseAxes.axis([-11, 11, -11, 11])
baseAxes.set_ylabel('Scale 1')
baseAxes.set_xlabel('Scale 2')
baseAxes.grid(True)
baseAxes.axes.xaxis.set_ticklabels([])      # remove x tick labels
baseAxes.axes.yaxis.set_ticklabels([])      # remove y tick labels
baseAxes.set_title('Voter Space')           # sample plot title
# ax.spines['left'].set_position('center')      # this could be done to center axes. No longer desired
# ax.spines['bottom'].set_position('center')

# Voting method label
methodLabel = Label(root, text="Voting Method:", fg="#3333ff", font=30)  # dark blue
# voting method selection listbox
methodSelectLB = Listbox(root, height=2, width=10, name='methodLB', exportselection=False)
# exportselection=False leaves the selection selected when tabbing or switching windows
for method in methods:
    methodSelectLB.insert(END, method)
methodSelectLB.selection_set(0)     # set the default selection to the first in the list
# candidate count label
candCtLabel = Label(root, text="Candidate count:", font=30)
# candidate count spinbox
candCtSpinbox = Spinbox(root, width=2, wrap=True, values=[3, 4, 5, 6, 7, 2])    # from_=2, to=7
# voter count label
voterCtLabel = Label(root, text="Voter Count:", font=30)
# voter count spinbox       ** no longer used. switched to Entry()
# voterCtSpinbox = Spinbox(root, from_=10, to=1000000)
validation = root.register(only_nums)
voterCt = IntVar()      # create a tk variable to store the number of voters
voterCt.set(100)
voterCtEntry = Entry(root, width=7, validate="key", validatecommand=(validation, '%S'), textvariable=voterCt)
# generate / plot button
genButton = Button(root, text="Gen / Plot", height=2, width=10, command=gen_population)
# Simulate button
simButton = Button(root, text="Sim / Vote", command=sim_election)
# winner display label
winnerLabel = Label(root, text="Winner: -", font=30)
# candidate score / tally counts
scoreTable = Frame(root)    # is a table necessary? or just a list?
header = Entry(scoreTable, width=10, justify='center')
header.grid(row=0, column=0)
header.insert(END, "Candidate")
header = Entry(scoreTable, width=10, justify='center')      # reuse header variable
header.grid(row=0, column=1)
header.insert(END, "Vote")
for r in range(1, int(candCtSpinbox.get())):
    for c in range(2):
        cell = Entry(scoreTable, width=10)
        cell.grid(row=r, column=c)
        cell.insert(END, "-")

# frame to hold the canvas and toolbar
plotFrame = Frame(root, height=700, width=700)
# creating the Tkinter canvas containing the Matplotlib figure
canvas = FigureCanvasTkAgg(prefFigure, master=plotFrame)
# canvas.mpl_connect('pick_event', onpick1)
canvas.draw()
# creating the Matplotlib toolbar
toolbar = NavigationToolbar2Tk(canvas, plotFrame)
toolbar.update()
canvas.get_tk_widget().pack()

#           *********     GUI Organization        **********
plotFrame.grid(row=0, column=0, rowspan=10, columnspan=2)
methodLabel.grid(row=0, column=2, columnspan=2)
methodSelectLB.grid(row=1, column=2, columnspan=2)
candCtLabel.grid(row=2, column=2)
candCtSpinbox.grid(row=2, column=3)
voterCtLabel.grid(row=4, column=2)
# voterCtSpinbox.grid(row=5, column=2, columnspan=2)
voterCtEntry.grid(row=4, column=3)
genButton.grid(row=6, column=2, columnspan=2)
simButton.grid(row=7, column=2, columnspan=2)
winnerLabel.grid(row=8, column=2, columnspan=2)
scoreTable.grid(row=9, column=2, columnspan=2)
# placing the toolbar on the Tkinter window
# canvas.get_tk_widget().pack()

# run the gui
root.mainloop()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # gen_vote_space()
    # plt.show()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
