#
# I M B A L A N C E
#

# 
# Produce a graph that shows the change in F1 
library(dplyr)
library(ggplot2)
library(gghighlight)
library("GGally")

library(lemon)

setwd("c:/uofa/weeds/post")
imbalances <- read.csv("imbalance.csv")

imbalances$classification <- as.factor(imbalances$classification)
imbalances$correction <- as.factor(imbalances$correction)
imbalances$ratio <- as.factor(imbalances$ratio)

#
# This is a version that puts the ratio at tbe base of each bar
# Too busy, perhaps
#
# For the bar chart
#ggplot(imbalances, aes(x = classification,
#                      y = f1.delta,
#                       fill = as.factor(ratio))) +
ggplot(imbalances, aes(x = classification, 
                      y = f1.delta,
                      fill = as.factor(ratio))) +
  geom_segment(aes(x = x, xend = x, y = 0, yend = y)) +
  geom_point() +
  xlab("Classification Method") +
  ylab("Delta on F1") +
  facet_wrap(~correction) +
  geom_col(position = "dodge", show.legend = T) +
    labs(fill="Ratio") +
  geom_text(aes(label = format(round(f1.delta, digits=2), nsmall=2), y = 0),
            position = position_dodge(width=0.9),
            hjust = 1,
            angle = -90,
            size = 2) +
  theme(axis.text.x = element_text(angle = -90, hjust = 0))

#
# This is the version without the ratio at the bottom of the bar
#
ggplot(imbalances, aes(x = classification,
                       y = f1.delta,
                       fill = as.factor(ratio),
                       width=1.0)) +
  xlab("Classification Method") +
  ylab("Delta of F1") +
  facet_wrap(~correction) +
  geom_col(position = position_dodge(0.95), show.legend = T) +
  labs(fill="Ratio") +
  # geom_text(aes(label = ratio, y = -.095),
  #           position = position_dodge(width=0.9),
  #           hjust = 1,
  #           angle = -90,
  #           size = 2) +
  theme(axis.text.x = element_text(angle = -90, hjust = 0.0, vjust = 0.3))


