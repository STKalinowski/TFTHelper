import math
import matplotlib 
from plotly.subplots import make_subplots
import plotly.express as px
from plotly import graph_objects as go
import pandas as pd
import numpy as np
     

#Bag gets 1 items for each carosel, minus initial carosel!
def makeItemBag(stage, itemsDropped=None):
  retDic = {'chain':0, 'sword':0, 'rod':0, 'cloak':0, 'belt':0, 'tear':0, 'glove':0, 'bow':0}
  for k in retDic.keys():
    retDic[k] = 2+stage-1

  if itemsDropped != None:
    for k in itemsDropped:
      if k in retDic:
        retDic[k] -= itemsDropped[k]
  return retDic
     

def chanceOfItems(stage, itemsDropped):
  #Setup
  itemBag = makeItemBag(stage, itemsDropped)
  itemsLeft = 8 - sum(itemsDropped.values())
  retVal = {}
  totalInBag = 0
  for k in itemBag.keys():
    totalInBag += itemBag[k]
  #Calculate odds for each item
  for k in itemBag.keys():
    retVal[k] = chanceOfX(itemBag[k], totalInBag, itemsLeft)

  return retVal

#Recursive
def chanceOfX(itemCount, total, dropsLeft):
  #Base case
  if dropsLeft <= 0:
    return [1.0]

  proDrop = float(itemCount/total)
  proNot = 1.0 - proDrop
  #We add on ends for 0 because:
  #a is Drop happened, no item case not represented
  #b is No dropped case, so chance of 1 extra item is 0
  a = [0.0] + [proDrop*i for i in chanceOfX(itemCount-1.0, total-1.0, dropsLeft-1.0)]
  b = [proNot * i for i in chanceOfX(itemCount, total-1.0, dropsLeft-1.0)] + [0.0]
  return [item1+item2 for item1,item2 in zip(a,b)] 
     

#######Item Drop Odds Calculator###################
#Minimum 12 components
#!!!!! ATTENTION !!!!!
#There is a chance of more than 12 components!
#Usually 12->15 range
#Default setting is 12 but you can enter total items as an option
#ALSO
#Calculator does not update between stages
#So if calculation was done for Wolves(3-5)
#The calculator does not take into account
#the extra item added on 4-3 carousel!!!

#Enter Setting:
stage = 4
itemsDropped = makeItemBag(-1)
itemsDropped['chain'] = 0
itemsDropped['sword'] = 0
itemsDropped['rod'] = 0
itemsDropped['cloak'] = 2
itemsDropped['belt'] = 2
itemsDropped['tear'] = 0
itemsDropped['glove'] = 0
itemsDropped['bow'] = 0

results = chanceOfItems(stage, itemsDropped)

#Display Results
#Make dataframe for display
#Apparently all ploting libraries love dataframes not lists.
dfProb = pd.DataFrame.from_dict(results)
dfProb = dfProb.mul(100)
dfProb['Amount Dropped'] = np.arange(len(dfProb))

res = []
for i in results.keys():
  #fig.add_trace(go.Bar( x=dfProb['Amount Dropped'], y=dfProb[i]),1,1)
  res.append(go.Bar( x=dfProb['Amount Dropped'], y=dfProb[i], name=i))
fig = go.Figure(data=res)
fig.update_xaxes(title='Amount Hit')
fig.update_yaxes(title='Probabilities')
fig.update_layout(title='ALL')
fig.show()


for i in results.keys():
  #fig = px.bar(dfProb, x='Amount Dropped', y=i, labels={ i:'Probabilities'}, title=i)
  fig = go.Figure(data=go.Bar(x=dfProb['Amount Dropped'], y=dfProb[i], marker_color='ForestGreen'))
  fig.update_xaxes(title='Amount Hit')
  fig.update_yaxes(title='Probabilities')
  fig.update_layout(title=i.upper())
  fig.show()

#Krugs(2-5), Wolves(3-5), Raptors(4-5)
#5 components from carosel, rest are dropped items
#Between, +1 is added to all items in the bag!
#+1 Addition Source: https://www.youtube.com/watch?v=r4X6HAMNbY8&t=34s
#So this gives a rough porbability
#But this rough guess should be fine for analysis, although off by a couple of percentage points.
     

champPoolTotal = [29, 22, 28, 12, 10]
uniqChamps = [13, 13, 13, 12, 8]
lvlOdds =[
          [100, 0,0,0,0],
          [100, 0, 0,0,0],
          [75,25,0,0,0],
          [55, 30, 15, 0,0],
          [45, 33, 20, 2, 0],
          [25, 40, 30, 5, 0],
          [19, 30, 35, 15, 1],
          [16, 20, 35, 25, 4],
          [9, 15, 30, 30, 16],
          [5, 10, 20, 40, 25]
]

def markovTransitions(rollOdds, totalAmount, amountLeft, desiredAmount):
  retVal = []
  
  for i in range(desiredAmount+1):
    if amountLeft > 0:
      PHit = float(rollOdds)* (float(amountLeft)/float(totalAmount))
      PNHit = 1.0-PHit
      retVal.append( (PNHit, PHit))
      totalAmount -= 1
      amountLeft -= 1
    else:
      PHit = 0.0
      PNHit = 1.0
      retVal.append((PNHit, PHit))

  return retVal

def rollDownCalculator(lvl, desiredCost, desiredAmount, amtOwned, otherOwned, otherCostsOut, gold):
  #CONST
  champPoolTotal = [29, 22, 28, 12, 10]
  uniqChamps = [13, 13, 13, 12, 8]
  lvlOdds =[
          [100, 0,0,0,0],
          [100, 0, 0,0,0],
          [75,25,0,0,0],
          [55, 30, 15, 0,0],
          [45, 33, 20, 2, 0],
          [25, 40, 30, 5, 0],
          [19, 30, 35, 15, 1],
          [16, 20, 35, 25, 4],
          [9, 15, 30, 30, 16],
          [5, 10, 20, 40, 25]
  ]
  rollOdds = float(lvlOdds[lvl-1][desiredCost-1]) / 100.0
  totalAmount = champPoolTotal[desiredCost-1]*uniqChamps[desiredCost-1] -amtOwned -otherOwned -otherCostsOut
  amountLeft = champPoolTotal[desiredCost-1] -amtOwned -otherOwned

  trans = markovTransitions(rollOdds, totalAmount, amountLeft, desiredAmount)
  retVal = [0.0]*(desiredAmount+1)
  retVal[0] = 1.0
  for i in range(math.floor(gold/2)*5):
    holdLast = [0]*len(retVal)
    for j in range(len(retVal)):
      holdLast[j] += retVal[j]*trans[j][0]
      if j+1 < len(retVal):
        holdLast[j+1] += retVal[j]*trans[j][1]
      else:
        holdLast[j] += retVal[j]*trans[j][1]
    retVal = list(holdLast)
  return retVal

     

########ROLL DOWN CALCULATOR############
#Level to roll down at:
rollLvl = 8
#Cost of the unit you are looking for:
desiredUnitCost = 4
#Amount you want to hit(from this roll down):
#So if you want 3 total, have 1 already, you want to get 2
desiredAmount = 9
#Amounts currently out of the pool:
#You own:
currentlyOwned = 0
#Others own:
othersOwned = 2
#Amount of other champs in the smae cost others own
#Percision not required, estimate should be good enough:
otherCostsOut = 2
#Gold rolling down:
gold=100

res = rollDownCalculator(rollLvl, desiredUnitCost, desiredAmount,currentlyOwned,othersOwned,otherCostsOut,gold)
#Display Results:
res = [100*i for i in res]
order = np.arange(0,len(res),1,dtype=int)
fig = go.Figure(go.Bar(x=order, y=res, marker_color='ForestGreen'))
fig = fig.update_xaxes(dtick=1, title='Amount Hit')
fig = fig.update_yaxes(title='Probabilities(%)')
fig.update_layout(title='Roll Down Odds', title_x=0.5)
fig.show()

cumulative = [sum(res[i:]) for i in range(1,len(res))]
fig = go.Figure(go.Bar(x=order[1:], y=cumulative, marker_color='ForestGreen'))
fig = fig.update_xaxes(dtick=1, title='Amount Hit Cumulative(X+)')
fig = fig.update_yaxes(title='Probabilities(%)')
fig.show()

     
